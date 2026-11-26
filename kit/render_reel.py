"""KURDISH DENT Reel renderer.
usage: python3 render_reel.py spec.json out.mp4
Spec: {"dur": 20.5, "seed": 0, "scenes": [{"start": 0, "bg": "#1E1236", "gap": 44, "els": [EL, ...]}, ...]}
EL types (each has "in": seconds, "fx": "pop" | "up"):
  {"t":"logo","size":240,"fill":"#FFF7EC","smile":"#1E1236","spark":"#2EE6B6"}
  {"t":"text","lines":["..."],"size":108,"color":"#FFF7EC","bg":"#2EE6B6","pad":[44,14],"r":30}   (Kurdish, Rabar)
  {"t":"latin","lines":["kurdish dent"],"size":76,"color":"#1E1236"}                               (Unbounded)
  {"t":"icon","kind":"x"|"check","size":260,"bg":"#1E1236","fg":"#FFC233"}
  {"t":"drop","size":150,"fill":"#2EE6B6","fg":"#1E1236"}
  {"t":"num","text":"2","size":200,"bg":"#2EE6B6","fg":"#1E1236"}   (big circled number, Latin digits)
Brand: plum #1E1236, enamel #FFF7EC, mint #2EE6B6, gold #FFC233. Flat only: no shadows, gradients or fades.
"""
import sys, os, json, html, subprocess, shutil, wave
import numpy as np
from playwright.sync_api import sync_playwright

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
import music

FPS = 30
spec = json.load(open(sys.argv[1])); OUT = sys.argv[2]
VOICE = spec.get('voice')  # optional path to a voiceover mp3; the timeline stretches to fit it
VD = 0.0
if VOICE:
    VD = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VOICE], capture_output=True, text=True).stdout.strip())
    T_last = spec['scenes'][-1]['start']; k = (VD + 0.9) / T_last
    for sc in spec['scenes']:
        sc['start'] = round(sc['start'] * k, 3)
        for e in sc['els']: e['in'] = round(e['in'] * k, 3)
    spec['dur'] = round(spec['scenes'][-1]['start'] + 3.6, 2)
work = os.path.join(os.path.dirname(os.path.abspath(OUT)), '_reelwork'); shutil.rmtree(work, ignore_errors=True); os.makedirs(work + '/frames')
for f in ('Rabar_021.ttf', 'unb800.woff2'): shutil.copy(os.path.join(KIT, f), work)

TOOTH = "M50 21.5 A21 21 0 0 1 84 38 C84 54 76 62 73 84 A5 5 0 0 1 63 84 A13 13 0 0 0 37 84 A5 5 0 0 1 27 84 C24 62 16 54 16 38 A21 21 0 0 1 50 21.5 Z"
SMILE = "M37 47 A13 13 0 0 0 63 47"
SPARK = "M74 14 Q75.2 20.8 82 22 Q75.2 23.2 74 30 Q72.8 23.2 66 22 Q72.8 20.8 74 14 Z"

def el_html(e):
    a = f'class="el" data-in="{e["in"]}" data-fx="{e["fx"]}"'
    t = e['t']
    if t == 'logo':
        sp = f'<path class="spark" d="{SPARK}" fill="{e["spark"]}" style="transform-origin:74px 22px"/>' if e.get('spark') else ''
        return f'<div {a}><svg width="{e["size"]}" height="{e["size"]}" viewBox="10 12 80 80"><path d="{TOOTH}" fill="{e["fill"]}"/><path d="{SMILE}" fill="none" stroke="{e["smile"]}" stroke-width="5" stroke-linecap="round"/>{sp}</svg></div>'
    if t in ('text', 'latin'):
        body = '<br>'.join(html.escape(l) for l in e['lines'])
        fam = 'Rabar' if t == 'text' else 'Unb'; d = 'rtl' if t == 'text' else 'ltr'
        st = f'font-family:{fam};font-size:{e["size"]}px;line-height:1.38;color:{e["color"]};direction:{d};margin:0'
        if e.get('bg'):
            p = e.get('pad', [36, 10]); st += f';background:{e["bg"]};padding:{p[1]}px {p[0]}px;border-radius:{e.get("r", 24)}px'
        return f'<p {a} style="{st}">{body}</p>'
    if t == 'icon':
        s = e['size']
        g = '<path d="M5 5 L19 19 M19 5 L5 19" stroke="{fg}" stroke-width="3.4" stroke-linecap="round"/>' if e['kind'] == 'x' else '<path d="M4.5 12.5 L10 18 L19.5 6.5" fill="none" stroke="{fg}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        return f'<div {a} style="width:{s}px;height:{s}px;border-radius:{s//2}px;background:{e["bg"]};display:flex;align-items:center;justify-content:center"><svg width="{s//2}" height="{s//2}" viewBox="0 0 24 24">{g.format(fg=e["fg"])}</svg></div>'
    if t == 'drop':
        s = e['size']
        return f'<div {a}><svg width="{s}" height="{int(s*1.27)}" viewBox="0 0 30 38"><path d="M15 2 C15 2 3 16 3 24 A12 12 0 0 0 27 24 C27 16 15 2 15 2 Z" fill="{e["fill"]}"/><path d="M9 25 A6 6 0 0 0 14 30" fill="none" stroke="{e["fg"]}" stroke-width="2.2" stroke-linecap="round"/></svg></div>'
    if t == 'num':
        s = e['size']
        return f'<div {a} style="width:{s}px;height:{s}px;border-radius:{s//2}px;background:{e["bg"]};color:{e["fg"]};font-family:Unb;font-size:{int(s*0.5/max(1,len(e['text'])*0.5))}px;display:flex;align-items:center;justify-content:center">{html.escape(e["text"])}</div>'
    raise ValueError(t)

scenes_html = ''.join(
    f'<div class="scene" id="s{i}" style="background:{sc["bg"]};gap:{sc.get("gap", 44)}px">' + ''.join(el_html(e) for e in sc['els']) + '</div>'
    for i, sc in enumerate(spec['scenes']))
starts = [sc['start'] for sc in spec['scenes']]; bgs = [sc['bg'] for sc in spec['scenes']]
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Rabar;src:url(Rabar_021.ttf)}}@font-face{{font-family:Unb;src:url(unb800.woff2);font-weight:800}}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1920px;overflow:hidden}}
.scene{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 110px;text-align:center}}
#w{{position:absolute;top:0;bottom:0;width:1080px;left:1080px}}
</style></head><body>{scenes_html}<div id="w"></div><script>
const ST={json.dumps(starts)},BG={json.dumps(bgs)};
const cl=x=>Math.max(0,Math.min(1,x)),eOut=x=>1-Math.pow(1-x,3),eBack=x=>{{const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
window.render=function(t){{
 let vis=0;ST.forEach((s,i)=>{{if(t>=s)vis=i}});let wx=1080,wc='#000';
 for(let i=1;i<ST.length;i++){{const p=(t-(ST[i]-0.25))/0.5;if(p>=0&&p<=1){{wc=BG[i];wx=p<0.5?1080*(1-eOut(p*2)):-1080*eOut((p-0.5)*2);vis=p<0.5?i-1:i}}}}
 ST.forEach((s,i)=>document.getElementById('s'+i).style.display=i==vis?'flex':'none');
 const w=document.getElementById('w');w.style.left=wx+'px';w.style.background=wc;
 document.querySelectorAll('.el').forEach(e=>{{const t0=+e.dataset.in;
  if(e.dataset.fx=='pop'){{const p=cl((t-t0)/0.45);e.style.transform=`scale(${{p<=0?0:eBack(p)}})`}}
  else{{const p=cl((t-t0)/0.5);e.style.transform=`translateY(${{(1-eOut(p))*160}}px) scale(${{p<=0?0:1}})`;e.style.clipPath=`inset(0 0 ${{(1-eOut(p))*100}}% 0)`}}}});
 document.querySelectorAll('.spark').forEach(sp=>{{const q=t-(+sp.closest('.el').dataset.in+0.9);sp.style.transform=q>0?`scale(${{1+0.35*Math.sin(q*7)*Math.exp(-q*1.5)}}) rotate(${{q*40}}deg)`:'none'}});
}};render(0);</script></body></html>'''
open(work + '/reel.html', 'w').write(page)

DUR = spec['dur']; NF = int(DUR * FPS)
with sync_playwright() as p:
    exe = shutil.which('google-chrome') or shutil.which('chromium')
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + work + '/reel.html'); pg.wait_for_timeout(900)
    for i in range(NF):
        pg.evaluate(f'render({i/FPS})'); pg.screenshot(path=f'{work}/frames/f{i:04d}.jpg', type='jpeg', quality=93)
    b.close()

# ---- audio: original music + CC0 SFX auto-cued to the animation ----
SR = 48000
music.make(DUR, spec.get('seed', 0), work + '/music.wav')
def load(pth):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', pth, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype='<f4').reshape(-1, 2)
mus = load(work + '/music.wav')[:int(DUR * SR)]
mix = mus * 0.42
if VOICE:
    v = load(VOICE); off = int(0.3 * SR); env_ = np.full(len(mix), 0.42)
    a0, a1 = max(0, off - int(0.3*SR)), min(len(mix), off + len(v) + int(0.3*SR))
    env_[a0:a1] = 0.14
    ker = np.ones(int(0.25*SR)) / int(0.25*SR); env_ = np.convolve(env_, ker, mode='same')
    mix = mus * env_[:, None]
    j = min(len(mix), off + len(v)); mix[off:j] += v[:j - off] * 1.0
S = os.path.join(KIT, 'sfx') + '/'
cues = []
for k, sc in enumerate(spec['scenes']):
    if k: cues.append((sc['start'] - 0.2, 'swish-medium.wav', 0.8))
    last = k == len(spec['scenes']) - 1
    for e in sc['els']:
        if last and e['t'] in ('logo', 'latin') and not any(c[0] == e['in'] and 'sting' in c[1] for c in cues):
            cues.append((e['in'], 'sting-bright-short.wav', 1.0)); continue
        if e['fx'] == 'pop':
            f = {'icon': 'impact-light-firm.wav' if e.get('kind') == 'x' else 'pop-medium-in.wav', 'drop': 'pop-small-bubble.wav'}.get(e['t'], 'pop-small-in.wav' if e['t'] == 'text' else 'pop-medium-in.wav')
            cues.append((e['in'], f, 0.85))
        else:
            cues.append((e['in'], 'whoosh-fast-soft.wav', 0.6))
    if k == len(spec['scenes']) - 2: cues.append((sc['els'][-1]['in'] + 0.3, 'shimmer-medium-sparkle.wav', 0.7))
for t, f, g in cues:
    s = load(S + f); i = max(0, int(t * SR)); j = min(len(mix), i + len(s)); mix[i:j] += s[:j - i] * g * (0.55 if VOICE else 1.0)
mix = mix / np.max(np.abs(mix)) * 0.95
w = wave.open(work + '/mix.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', work + '/frames/f%04d.jpg', '-i', work + '/mix.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', OUT], check=True)
shutil.rmtree(work, ignore_errors=True)
print('ok', OUT)
