"""KURDISH DENT info-image renderer (1080x1350, 4:5) with rotating modern styles.
usage: python3 render_post.py spec.json out.jpg
Spec: {"style":"poster"|"cards"|"myth"|"bignum",
       "badge":"ڕێنمایی ڕۆژانە", "title":"٤ هەڵە کە ڕۆژانە لە فڵچەکردندا دەیکەیت",
       "items":["فڵچەکردن بە **هێز**", ...],      (3-5 items; **word** = highlight)
       "num":"4"                                    (bignum only, Latin digit)
       "footer":"پاشەکەوتی بکە و بۆ هاوڕێکانت بنێرە"}
myth style: items alternate is not needed; use {"myth":"...","fact":"..."} pairs in "pairs" (2-3 pairs).
"""
import sys, os, json, html, re, shutil
from playwright.sync_api import sync_playwright
KIT = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1])); OUT = os.path.abspath(sys.argv[2])
E = html.escape
def fmt(s): return re.sub(r'\*\*(.+?)\*\*', lambda m: f'<b>{m.group(1)}</b>', E(s))
TOOTH = "M50 21.5 A21 21 0 0 1 84 38 C84 54 76 62 73 84 A5 5 0 0 1 63 84 A13 13 0 0 0 37 84 A5 5 0 0 1 27 84 C24 62 16 54 16 38 A21 21 0 0 1 50 21.5 Z"
def logo(size, fill, smile, spark='#2EE6B6'):
    return f'<svg width="{size}" height="{size}" viewBox="10 12 80 80"><path d="{TOOTH}" fill="{fill}"/><path d="M37 47 A13 13 0 0 0 63 47" fill="none" stroke="{smile}" stroke-width="5" stroke-linecap="round"/><path d="M74 14 Q75.2 20.8 82 22 Q75.2 23.2 74 30 Q72.8 23.2 66 22 Q72.8 20.8 74 14 Z" fill="{spark}"/></svg>'
def tooth3d(size):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 100 100"><defs>
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#F3ECFF"/><stop offset="1" stop-color="#CDBEF0"/></linearGradient>
<radialGradient id="hl" cx="0.35" cy="0.3" r="0.35"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>
<g transform="translate(0,4)"><path d="{TOOTH}" fill="url(#tg)"/><path d="{TOOTH}" fill="url(#hl)"/>
<path d="M37 47 A13 13 0 0 0 63 47" fill="none" stroke="#1E1236" stroke-width="4.5" stroke-linecap="round"/>
<circle cx="40" cy="39" r="2.6" fill="#1E1236"/><circle cx="60" cy="39" r="2.6" fill="#1E1236"/></g>
<path d="M80 10 Q81.5 18.5 90 20 Q81.5 21.5 80 30 Q78.5 21.5 70 20 Q78.5 18.5 80 10 Z" fill="#2EE6B6"/>
<path d="M16 66 Q16.8 70.2 21 71 Q16.8 71.8 16 76 Q15.2 71.8 11 71 Q15.2 70.2 16 66 Z" fill="#FFC233"/></svg>'''
HEAD = '''<!doctype html><html lang="ckb"><head><meta charset="utf-8"><style>
@font-face{font-family:Rabar;src:url(Rabar_021.ttf)}@font-face{font-family:Unb;src:url(unb800.woff2);font-weight:800}
*{box-sizing:border-box}body{margin:0;width:1080px;height:1350px;font-family:Rabar;direction:rtl;overflow:hidden}
.brand{display:flex;align-items:center;gap:16px;direction:ltr;font-family:Unb;font-weight:800;font-size:28px}
b{font-weight:normal}
.bgc{position:absolute;inset:0;overflow:hidden}.wrap{position:relative;width:1080px}
</style>'''
style = spec.get('style', 'cards')
items = spec.get('items', []); footer = E(spec.get('footer', 'پاشەکەوتی بکە و بۆ هاوڕێکانت بنێرە')); badge = E(spec.get('badge', 'ڕێنمایی ڕۆژانە'))
title = E(spec['title'])

if style == 'poster':
    rows = ''.join(f'<div class="it"><span class="dot"></span><p>{fmt(t)}</p></div>' for t in items)
    body = f'''<style>
body{{background:radial-gradient(120% 90% at 85% 0%,#4B2A8A 0%,#2A1650 45%,#160C2B 100%)}}
.glow{{position:absolute;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,#2EE6B655 0%,#2EE6B600 70%);left:-160px;top:120px}}
.wrap{{position:relative;height:1350px;padding:80px 84px;display:flex;flex-direction:column;gap:34px;color:#FFF7EC}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.pill{{font-size:30px;color:#1E1236;background:#2EE6B6;padding:8px 28px;border-radius:40px;box-shadow:0 10px 30px #2EE6B655}}
.hero{{display:flex;align-items:center;gap:10px}}
h1{{margin:0;font-weight:normal;font-size:92px;line-height:1.25;text-shadow:0 8px 30px #0008}}
.list{{display:flex;flex-direction:column;gap:20px;margin-top:6px}}
.it{{display:flex;align-items:center;gap:22px;background:#FFFFFF14;border:1.5px solid #FFFFFF26;border-radius:28px;padding:26px 30px;backdrop-filter:blur(6px);box-shadow:0 18px 40px #0005}}
.it p{{margin:0;font-size:44px;line-height:1.4}}.it b{{color:#2EE6B6}}
.dot{{width:22px;height:22px;flex-shrink:0;border-radius:50%;background:#FFC233;box-shadow:0 0 18px #FFC233}}
.ft{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#CFC6DE}}
</style></head><body><div class="bgc"><div class="glow"></div></div><div class="wrap">
<div class="top"><div class="brand" style="color:#FFF7EC">{logo(60,'#FFF7EC','#2A1650')}kurdish dent</div><span class="pill">{badge}</span></div>
<div class="hero"><h1>{title}</h1><div style="flex-shrink:0;filter:drop-shadow(0 30px 40px #0009)">{tooth3d(250)}</div></div>
<div class="list">{rows}</div>
<div class="ft"><span>{footer}</span><span style="font-family:Unb;font-size:22px;direction:ltr">@kurdishdent</span></div></div></body></html>'''
elif style == 'myth':
    pairs = spec['pairs']
    rows = ''.join(f'''<div class="pair"><div class="m"><span class="tag t1">ئەفسانە</span><p>{E(p["myth"])}</p></div><div class="f"><span class="tag t2">ڕاستی</span><p>{E(p["fact"])}</p></div></div>''' for p in pairs)
    body = f'''<style>
body{{background:linear-gradient(160deg,#FFF7EC 0%,#F4EEFF 100%)}}
.wrap{{height:1350px;padding:76px 80px;display:flex;flex-direction:column;gap:40px;color:#1E1236}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.pill{{font-size:30px;color:#FFF7EC;background:#1E1236;padding:8px 28px;border-radius:40px}}
h1{{margin:0;font-weight:normal;font-size:84px;line-height:1.25}}h1 span{{background:linear-gradient(90deg,#2EE6B6,#7CF5D6);padding:0 22px;border-radius:22px}}
.pair{{display:flex;flex-direction:column;border-radius:34px;overflow:hidden;box-shadow:0 24px 50px #1E123622}}
.m,.f{{padding:30px 34px;display:flex;align-items:center;gap:22px}}.m{{background:#FFFFFF}}.f{{background:#1E1236;color:#FFF7EC}}
.m p,.f p{{margin:0;font-size:42px;line-height:1.4}}.m p{{text-decoration:line-through;text-decoration-color:#FF6B6B;text-decoration-thickness:3px;color:#5E5470}}
.tag{{flex-shrink:0;font-size:26px;padding:6px 18px;border-radius:20px}}.t1{{background:#FFE1E1;color:#C0392B}}.t2{{background:#2EE6B6;color:#1E1236}}
.ft{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#5E5470}}
</style></head><body><div class="wrap">
<div class="top"><div class="brand" style="color:#1E1236">{logo(60,'#1E1236','#FFF7EC')}kurdish dent</div><span class="pill">{badge}</span></div>
<h1>{title}</h1>{rows}
<div class="ft"><span>{footer}</span><span style="font-family:Unb;font-size:22px;direction:ltr">@kurdishdent</span></div></div></body></html>'''
elif style == 'bignum':
    rows = ''.join(f'<div class="it"><span class="n">{i+1}</span><p>{fmt(t)}</p></div>' for i, t in enumerate(items))
    body = f'''<style>
body{{background:linear-gradient(180deg,#2EE6B6 0%,#22CFA2 100%)}}
.wrap{{position:relative;height:1350px;padding:76px 80px;display:flex;flex-direction:column;gap:26px;color:#1E1236}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.pill{{font-size:30px;color:#2EE6B6;background:#1E1236;padding:8px 28px;border-radius:40px}}
.head{{display:flex;align-items:center;gap:26px}}
.big{{font-family:Unb;font-weight:800;font-size:300px;line-height:0.9;color:#1E1236;direction:ltr;text-shadow:12px 14px 0 #FFFFFF66}}
h1{{margin:0;font-weight:normal;font-size:76px;line-height:1.28}}
.card{{background:#FFF7EC;border-radius:40px;padding:44px 40px;display:flex;flex-direction:column;gap:30px;box-shadow:0 30px 60px #1E123633}}
.it{{display:flex;align-items:center;gap:22px}}.it p{{margin:0;font-size:46px;line-height:1.4}}.it b{{color:#0E8F70}}
.n{{width:64px;height:64px;flex-shrink:0;border-radius:20px;background:#1E1236;color:#2EE6B6;font-family:Unb;font-size:30px;display:flex;align-items:center;justify-content:center;transform:rotate(-6deg)}}
.ft{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:28px}}
</style></head><body><div class="wrap">
<div class="top"><div class="brand">{logo(60,'#1E1236','#2EE6B6','#FFF7EC')}kurdish dent</div><span class="pill">{badge}</span></div>
<div class="head"><div class="big">{E(spec.get("num", str(len(items))))}</div><h1>{title}</h1></div>
<div class="card">{rows}</div>
<div class="ft"><span>{footer}</span><span style="font-family:Unb;font-size:22px;direction:ltr">@kurdishdent</span></div></div></body></html>'''
else:  # cards
    icons = ['#2EE6B6', '#FFC233', '#B79CFF', '#FF8FA3', '#7CC7FF']
    rows = ''.join(f'<div class="it"><span class="ic" style="background:{icons[i%5]}">{logo(46,"#1E1236","#FFF7EC","#FFF7EC")}</span><p>{fmt(t)}</p></div>' for i, t in enumerate(items))
    body = f'''<style>
body{{background:#F6F1E9}}
.blob1{{position:absolute;width:520px;height:520px;border-radius:50%;background:#2EE6B6;filter:blur(90px);opacity:.45;right:-140px;top:-120px}}
.blob2{{position:absolute;width:460px;height:460px;border-radius:50%;background:#B79CFF;filter:blur(90px);opacity:.4;left:-160px;bottom:-60px}}
.wrap{{position:relative;height:1350px;padding:80px 84px;display:flex;flex-direction:column;gap:32px;color:#1E1236}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.pill{{font-size:30px;background:#FFFFFF;padding:8px 28px;border-radius:40px;box-shadow:0 10px 30px #1E123618}}
h1{{margin:0;font-weight:normal;font-size:88px;line-height:1.25}}
.grid{{display:flex;flex-direction:column;gap:18px}}
.it{{display:flex;align-items:center;gap:24px;background:#FFFFFFD9;border-radius:30px;padding:24px 28px;box-shadow:0 16px 40px #1E12361A}}
.it p{{margin:0;font-size:43px;line-height:1.4}}.it b{{color:#0E8F70}}
.ic{{width:76px;height:76px;flex-shrink:0;border-radius:24px;display:flex;align-items:center;justify-content:center}}
.ft{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#5E5470}}
</style></head><body><div class="bgc"><div class="blob1"></div><div class="blob2"></div></div><div class="wrap">
<div class="top"><div class="brand">{logo(60,'#1E1236','#F6F1E9')}kurdish dent</div><span class="pill">{badge}</span></div>
<h1>{title}</h1><div class="grid">{rows}</div>
<div class="ft"><span>{footer}</span><span style="font-family:Unb;font-size:22px;direction:ltr">@kurdishdent</span></div></div></body></html>'''

work = os.path.dirname(OUT) + '/_postwork'; shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
for f in ('Rabar_021.ttf', 'unb800.woff2'): shutil.copy(os.path.join(KIT, f), work)
open(work + '/post.html', 'w').write(HEAD + body)
with sync_playwright() as p:
    exe = shutil.which('google-chrome') or shutil.which('chromium')
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}); pg.goto('file://' + work + '/post.html'); pg.wait_for_timeout(800)
    pg.screenshot(path=work + '/p.png'); b.close()
from PIL import Image
Image.open(work + '/p.png').convert('RGB').save(OUT, quality=95)
shutil.rmtree(work, ignore_errors=True); print('ok', OUT)
