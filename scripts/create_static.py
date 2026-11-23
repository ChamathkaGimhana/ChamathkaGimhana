#!/usr/bin/env python3
"""Regenerate the editable, custom-designed static brand panels (standard library only)."""
from pathlib import Path
from html import escape
import argparse

HERO = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="405" viewBox="0 0 1280 405" role="img" aria-labelledby="heroTitle">
<title id="heroTitle">Chamathka Gimhana — creative developer and indie creator</title>
<defs>
  <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#091122"/><stop offset=".53" stop-color="#11152A"/><stop offset="1" stop-color="#0B0F22"/></linearGradient>
  <linearGradient id="line" x1="0" x2="1"><stop stop-color="#42F5D1"/><stop offset=".56" stop-color="#A278FF"/><stop offset="1" stop-color="#DB72FF"/></linearGradient>
  <linearGradient id="metal" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#F7FEFF"/><stop offset="1" stop-color="#ABCCDF"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#5C45E3" stop-opacity=".32"/><stop offset="1" stop-color="#5C45E3" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#526686" stroke-opacity=".12" fill="none"/></pattern>
  <filter id="light"><feGaussianBlur stdDeviation="7"/></filter>
  <clipPath id="clip"><rect x="1" y="1" width="1278" height="403" rx="24"/></clipPath>
</defs>
<g clip-path="url(#clip)">
 <rect width="1280" height="405" rx="24" fill="url(#bg)"/>
 <rect width="1280" height="405" fill="url(#grid)"/>
 <circle cx="1010" cy="180" r="250" fill="url(#glow)"/>
 <path d="M0 0H1280" stroke="url(#line)" stroke-width="7"/>
 <path d="M0 364H1280" stroke="#2B3D57" stroke-width="1"/>
 <g font-family="'Segoe UI',Arial,sans-serif">
   <rect x="52" y="35" width="46" height="46" rx="12" fill="#42F5D1"/>
   <text x="75" y="64" font-family="Arial,sans-serif" text-anchor="middle" fill="#071626" font-size="22" font-weight="900">CG</text>
   <text x="115" y="54" fill="#D8E5F8" font-size="13" font-weight="800" letter-spacing="3">CREATOR OS</text>
   <text x="115" y="76" fill="#718CA5" font-size="11" font-weight="700" letter-spacing="1.9">IDENTITY SYSTEM / 001</text>

   <rect x="54" y="118" width="235" height="28" rx="14" fill="#142C3C" stroke="#34736F"/>
   <circle cx="69" cy="132" r="4.5" fill="#42F5D1"/>
   <text x="85" y="136" fill="#8AEFDE" font-size="11.5" font-weight="800" letter-spacing="1.3">CODE  ·  DESIGN  ·  SHIP</text>

   <text x="48" y="226" font-size="78" font-weight="900" fill="url(#metal)" letter-spacing="-2.5">CHAMATHKA</text>
   <text x="52" y="303" font-size="76" font-weight="900" fill="url(#line)" letter-spacing="-1.5">GIMHANA</text>
   <text x="54" y="340" fill="#B9CAE0" font-size="16" font-weight="600" letter-spacing="1.8">CREATIVE DEVELOPER  /  INDIE CREATOR</text>

   <text x="55" y="387" fill="#A0B3CC" font-size="12" font-weight="700" letter-spacing="1.6">SRI LANKA  •  THINK → MAKE → IMPROVE</text>
   <text x="1225" y="387" fill="#7F96B4" font-size="11" font-weight="700" text-anchor="end" letter-spacing="1.3">GAME  /  APP  /  WEB  /  DESIGN  /  MOTION</text>
 </g>
 <!-- Custom system radar with original CG monogram; all shapes are editable. -->
 <g transform="translate(1012 198)">
   <circle r="166" fill="none" stroke="#304466" stroke-width="2"/>
   <circle r="144" fill="none" stroke="#5C77A7" stroke-width="1" stroke-dasharray="3 14" opacity=".8"/>
   <circle r="116" fill="none" stroke="#A278FF" stroke-width="3" stroke-dasharray="75 40 15 80 80 50" opacity=".65">
     <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="56s" repeatCount="indefinite"/>
   </circle>
   <circle r="91" fill="#151A34" stroke="#46658B" stroke-width="2"/>
   <circle r="76" fill="#0B1C33" stroke="#42F5D1" stroke-opacity=".5" stroke-width="2"/>
   <circle r="68" fill="none" stroke="#35B0B7" stroke-opacity=".4" stroke-width="1" stroke-dasharray="1 8"/>
   <path d="M-177 0H177M0-177V177" stroke="#6385AF" stroke-opacity=".24" stroke-width="1"/>
   <path d="M-27-16C-27-50 12-50 36-35" stroke="#42F5D1" stroke-width="9" stroke-linecap="round" fill="none"/>
   <path d="M36 28C8 58-39 42-36 0" stroke="#42F5D1" stroke-width="9" stroke-linecap="round" fill="none"/>
   <path d="M46-26H15V29H46V11H34" stroke="#B289FF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
   <g fill="#42F5D1">
    <circle cx="0" cy="-166" r="5"/><circle cx="166" cy="0" r="4"/><circle cx="-166" cy="0" r="4"/>
   </g>
   <path d="M-152-62L-185-80h-27M121 109l36 24h45" stroke="#A278FF" stroke-width="2" fill="none"/>
   <circle cx="-213" cy="-80" r="4" fill="#A278FF"/><circle cx="202" cy="133" r="4" fill="#A278FF"/>
 </g>
 <rect x="1.5" y="1.5" width="1277" height="402" rx="23" fill="none" stroke="#32425E" stroke-width="3"/>
</g>
</svg>'''

SYSTEMS = '''<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="350" viewBox="0 0 1220 350" role="img" aria-labelledby="systemTitle">
<title id="systemTitle">Five creative disciplines: games, mobile apps, web, user interface design, and video production</title>
<defs>
<linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#0B1223"/><stop offset="1" stop-color="#0B1120"/></linearGradient>
<linearGradient id="accent" x1="0" x2="1"><stop stop-color="#42F5D1"/><stop offset="1" stop-color="#A278FF"/></linearGradient>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" stroke="#334766" stroke-opacity=".18" fill="none"/></pattern>
</defs>
<rect width="1220" height="350" rx="24" fill="url(#bg)"/>
<rect width="1220" height="350" rx="24" fill="url(#grid)"/>
<rect x="1" y="1" width="1218" height="348" rx="23" fill="none" stroke="#293F56" stroke-width="2"/>
<g font-family="'Segoe UI',Arial,sans-serif">
<text x="32" y="44" font-size="17" fill="#42F5D1" font-weight="800" letter-spacing="2.4">THE CAPABILITY MATRIX</text>
<text x="1185" y="44" font-size="12" fill="#8395B7" font-weight="700" text-anchor="end" letter-spacing="1.7">05 DISCIPLINES  •  ONE CREATIVE WORKFLOW</text>
'''
CARDS = [
 ('01', 'GAME SYSTEMS', 'Unity  /  C#', '#42F5D1', 'Interactive worlds'),
 ('02', 'MOBILE PRODUCTS', 'Flutter  /  Android  /  Firebase', '#9B83FF', 'Ideas in your pocket'),
 ('03', 'WEB EXPERIENCES', 'HTML  /  CSS  /  JavaScript', '#5FC1FF', 'Design meets function'),
 ('04', 'UI & VISUALS', 'Figma  /  Illustrator', '#FFBE76', 'Interfaces with intent'),
 ('05', 'MOTION & EDITING', 'Premiere  /  After Effects', '#EA8FEF', 'Stories in motion'),
]
for i, (number, title, tech, color, desc) in enumerate(CARDS):
    x = 30 + i*239
    SYSTEMS += f'''<g>
    <rect x="{x}" y="72" width="226" height="238" rx="16" fill="#121D31" stroke="#2B4059" stroke-width="2"/>
    <path d="M{x+20} 95H{x+69}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
    <text x="{x+20}" y="136" font-size="34" font-weight="900" fill="{color}">{number}</text>
    <text x="{x+20}" y="175" font-size="16" font-weight="800" fill="#EFF7FF" letter-spacing=".7">{escape(title)}</text>
    <text x="{x+20}" y="210" font-size="12.4" font-weight="600" fill="#C0D1E3">{escape(tech)}</text>
    <path d="M{x+20} 234H{x+205}" stroke="#31415A" stroke-width="1"/>
    <text x="{x+20}" y="265" font-size="12.5" fill="#90A6C1">{escape(desc)}</text>
    <circle cx="{x+197}" cy="286" r="4" fill="{color}"/>
    </g>'''
SYSTEMS += '''<rect x="30" y="326" width="1160" height="3" rx="1.5" fill="url(#accent)"/>
</g></svg>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='assets')
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out/'hero.svg').write_text(HERO, encoding='utf-8')
    (out/'capabilities.svg').write_text(SYSTEMS, encoding='utf-8')
    print('Created hero.svg and capabilities.svg')

if __name__ == '__main__':
    main()
