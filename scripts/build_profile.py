#!/usr/bin/env python3
"""Render first-party, self-hosted GitHub profile graphics.

No third-party stats services, no pip dependencies, and no credentials written to output.
Usage: GITHUB_TOKEN=... GITHUB_USERNAME=ChamathkaGimhana python scripts/build_profile.py --out dist
For local layout review: python scripts/build_profile.py --out preview --preview
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API = 'https://api.github.com'
BG = '#080E1D'
PANEL = '#101B2F'
BORDER = '#24344C'
WHITE = '#EAF4FF'
MUTED = '#8EA3BC'
CYAN = '#42F5D1'
PURPLE = '#A278FF'
ORANGE = '#FFBE76'


def api_request(path: str, token: str, payload: dict | None = None):
    headers = {'Accept': 'application/vnd.github+json',
               'User-Agent': 'Chamathka-Creator-OS-Profile',
               'X-GitHub-Api-Version': '2022-11-28'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    if data is not None:
        headers['Content-Type'] = 'application/json'
    request = Request(f'{API}{path}', data=data, headers=headers, method='POST' if data is not None else 'GET')
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def gather_public_stats(username: str, token: str):
    profile = api_request('/users/' + username, token)
    if profile.get('login', '').casefold() != username.casefold():
        raise ValueError('GitHub username and returned profile did not match')
    pages, stars, page = 0, 0, 1
    while True:
        repos = api_request(f'/users/{username}/repos?type=owner&per_page=100&page={page}', token)
        if not isinstance(repos, list):
            raise RuntimeError('GitHub repository API response is not a list')
        stars += sum(int(repo.get('stargazers_count') or 0) for repo in repos if not repo.get('fork'))
        pages += len(repos)
        if len(repos) < 100:
            break
        page += 1
        if page > 30:
            raise RuntimeError('Excessive GitHub repository pages; refusing to use incomplete totals')
    return {'repos': int(profile.get('public_repos', pages)),
            'followers': int(profile.get('followers', 0)), 'stars': stars}


def fetch_calendar(username: str, token: str):
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=365)
    query = '''query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }'''
    vals = {'login': username,
            'from': start.isoformat(timespec='seconds').replace('+00:00', 'Z'),
            'to': now.isoformat(timespec='seconds').replace('+00:00', 'Z')}
    result = api_request('/graphql', token, {'query': query, 'variables': vals})
    if result.get('errors'):
        raise RuntimeError('GitHub GraphQL: ' + str(result['errors'][0].get('message')))
    cal = result.get('data', {}).get('user', {}).get('contributionsCollection', {}).get('contributionCalendar')
    if not cal:
        raise RuntimeError('No contribution calendar returned by GitHub')
    return cal


def t(x, y, content, *, size=20, color=WHITE, weight=500, anchor=None, extra=''):
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}"{attrs} {extra}>{escape(str(content))}</text>'


def base_start(width, height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <defs>
      <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
      <linearGradient id="background" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#10192E"/><stop offset="1" stop-color="{BG}"/></linearGradient>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#28405E" stroke-opacity=".19" stroke-width="1"/></pattern>
    </defs>
    <rect width="{width}" height="{height}" rx="22" fill="url(#background)"/>
    <rect width="{width}" height="{height}" rx="22" fill="url(#grid)"/>
    <rect x="1.5" y="1.5" width="{width-3}" height="{height-3}" rx="21" fill="none" stroke="{BORDER}" stroke-width="3"/>
    <g font-family="'Segoe UI', Inter, Arial, sans-serif">'''


def render_telemetry(stats: dict, calendar: dict | None, stamp: str, preview=False):
    labels = [
        ('CONTRIBUTIONS / 365D', f"{int(calendar['totalContributions']):,}" if calendar else '—', CYAN),
        ('PUBLIC REPOSITORIES', f"{stats['repos']:,}" if stats else '—', PURPLE),
        ('REPOSITORY STARS', f"{stats['stars']:,}" if stats else '—', ORANGE),
        ('FOLLOWERS', f"{stats['followers']:,}" if stats else '—', WHITE),
    ]
    out = [base_start(1200, 254)]
    out.append('<rect x="32" y="30" width="40" height="3" rx="2" fill="url(#accent)"/>')
    out.append(t(85, 38, 'TELEMETRY / GITHUB', size=16, color=CYAN, weight=800, extra='letter-spacing="2"'))
    out.append(t(1165, 38, 'AUTOMATED • PUBLIC DATA', size=13, color=MUTED, anchor='end', extra='letter-spacing="1.6"'))
    for i, (label, value, hue) in enumerate(labels):
        x = 28 + i * 294
        out.append(f'<rect x="{x}" y="58" width="280" height="154" rx="14" fill="{PANEL}" stroke="{BORDER}"/>')
        out.append(f'<rect x="{x+20}" y="82" width="29" height="3" rx="2" fill="{hue}"/>')
        out.append(t(x+20, 112, label, size=13, color=MUTED, weight=700, extra='letter-spacing="1.4"'))
        out.append(t(x+20, 178, value, size=55, color=hue, weight=800, extra='letter-spacing="-2"'))
    state = 'PREVIEW • RUN THE WORKFLOW TO LOAD REAL NUMBERS' if preview else f'SYNCED {stamp} UTC  •  GitHub API'
    if calendar is None and not preview:
        state += '  •  CONTRIBUTION API TEMPORARILY UNAVAILABLE'
    out.append(t(33, 238, state, size=12, color=MUTED, weight=600, extra='letter-spacing="1.2"'))
    return ''.join(out) + '</g></svg>'


def render_calendar(calendar: dict | None, stamp: str, preview=False):
    out = [base_start(1200, 298)]
    out.append('<rect x="32" y="30" width="40" height="3" rx="2" fill="url(#accent)"/>')
    out.append(t(85, 38, 'ACTIVITY SIGNAL / LAST 365 DAYS', size=16, color=CYAN, weight=800, extra='letter-spacing="1.8"'))
    out.append(t(1165, 38, 'SUN → SAT  •  AUTO-REFRESH', size=13, color=MUTED, anchor='end', extra='letter-spacing="1.2"'))
    out.append('<rect x="30" y="56" width="1140" height="202" rx="14" fill="#0B1526" stroke="#22354A"/>')
    if calendar is None:
        out.append(t(600, 145, 'YOUR CONTRIBUTION GRID WILL APPEAR AFTER THE FIRST SYNC', size=20, color=WHITE, weight=700, anchor='middle'))
        out.append(t(600, 181, 'No contributions or numbers are invented for the preview.', size=15, color=MUTED, anchor='middle'))
    else:
        weeks = calendar.get('weeks', [])[-53:]
        # Limit to 53 weeks so every column is visible at mobile sizes.
        cell, gap, x0, y0 = 12, 5, 132, 95
        # Choose ranges based on real per-day counts, not the calendar's opaque level.
        def color_for(n):
            if n == 0: return '#1B2940'
            if n == 1: return '#284B64'
            if n <= 3: return '#367B92'
            if n <= 6: return '#567BD5'
            return CYAN
        # Week contributionDays are sorted Sun..Sat and at edges may be incomplete.
        for ix, week in enumerate(weeks):
            days = week.get('contributionDays', [])
            for day in days:
                day_date = datetime.strptime(day['date'], '%Y-%m-%d').date()
                # Python weekday is Mon=0, Sunday should be row 0.
                iy = (day_date.weekday() + 1) % 7
                x, y = x0 + ix * (cell + gap), y0 + iy * (cell + gap)
                v = int(day.get('contributionCount', 0))
                out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color_for(v)}"/>')
        for k, day in [(0,'SUN'),(2,'TUE'),(4,'THU'),(6,'SAT')]:
            out.append(t(60, y0 + k*17 + 10, day, size=12, color=MUTED, weight=600))
        if not weeks:
            out.append(t(600, 165, 'NO CONTRIBUTION HISTORY RETURNED', size=17, anchor='middle'))
    out.append(t(32, 281, 'SOURCE: GITHUB CONTRIBUTION CALENDAR', size=12, color=MUTED, weight=600, extra='letter-spacing="1.1"'))
    out.append(t(1024, 281, 'LOW', size=12, color=MUTED, anchor='end'))
    for i, color in enumerate(['#1B2940','#284B64','#367B92','#567BD5',CYAN]):
        out.append(f'<rect x="{1042+i*17}" y="270" width="11" height="11" rx="2" fill="{color}"/>')
    out.append(t(1168, 281, 'HIGH', size=12, color=MUTED, anchor='end'))
    return ''.join(out) + '</g></svg>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='dist')
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%d %b %Y %H:%M')
    username = os.environ.get('GITHUB_USERNAME', 'ChamathkaGimhana')
    token = os.environ.get('GITHUB_TOKEN', '')
    stats, calendar = {}, None
    if not args.preview:
        if not token:
            raise RuntimeError('GITHUB_TOKEN must be set for real GitHub data (use --preview for local layouts)')
        stats = gather_public_stats(username, token)
        try:
            calendar = fetch_calendar(username, token)
        except (HTTPError, URLError, ValueError, KeyError, RuntimeError) as exc:
            # Repo and follower figures stay real; report the unavailable calendar honestly.
            print(f'Warning: contribution calendar unavailable: {exc}', file=sys.stderr)
    (out / 'telemetry.svg').write_text(render_telemetry(stats, calendar, stamp, args.preview), encoding='utf-8')
    (out / 'activity.svg').write_text(render_calendar(calendar, stamp, args.preview), encoding='utf-8')
    print('Created:', out / 'telemetry.svg', 'and', out / 'activity.svg')


if __name__ == '__main__':
    main()
