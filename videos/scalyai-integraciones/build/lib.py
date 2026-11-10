# Base común para videos de Scaly AI en 16:9 (FMT=h) y 9:16 (FMT=v). Identidad: brand/scalyai/frame.md.
# Uso desde build/html.py:  from lib import *  → definir escenas (SCN) y línea de tiempo → render(SCN, titulo)
import json, os, re, math, itertools
FMT = os.environ.get("FMT", "h")
VERT = FMT == "v"
WW, HH = (1080, 1920) if VERT else (1920, 1080)
def P(h, v): """Devuelve el valor para el formato actual."""; return v if VERT else h
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HL_EXTRA = set()
IMG = os.path.join(ROOT, "assets", "img")
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
SEG = {s["id"]: s for s in segs}
S, T = plan["S"], plan["T"]
NAVY, NAVY7, TEAL, CYAN, SLATE = "#041B3D", "#0D2F5C", "#007B83", "#47D4D4", "#2F4560"
CREAM, CREAM2, CREAM3, WHITE = "#F0F1E8", "#E3E5D9", "#D6D9CB", "#FFFFFF"

EV = []
def ev(kind, t): EV.append([kind, round(t, 3)])
def icon(name, size, color=TEAL, sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>')
def wa(size, color=WHITE):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, "logo-whatsapp.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-label="WhatsApp"><path d="{d}" fill="{color}"/></svg>'
def bars(u, sid, dark=False):
    """Símbolo de Scaly AI con las medidas de la guía (rejilla 64): barras de 14, separación 7, radio completo."""
    k = u / 64
    low = CREAM if dark else NAVY
    spec = [(16, 0, 44, CYAN), (0, 21, 60, TEAL), (0, 42, 44, low)]
    inner = "".join(f'<i id="{sid}{j}" style="left:{x * k:.1f}px;top:{y * k:.1f}px;width:{w * k:.1f}px;height:{14 * k:.1f}px;background:{c}"></i>'
                    for j, (x, y, w, c) in enumerate(spec))
    return f'<div class="bars" style="width:{60 * k:.1f}px;height:{56 * k:.1f}px">{inner}</div>'
def BG(gx, gy, gs=1100): return f'<div class="grid"></div><div class="glow" style="left:{gx}px;top:{gy}px;width:{gs}px;height:{gs}px"></div>'

# ---------------------------------------------------------------- captions (alineadas a los tramos de voz)
HL = {"scaly", "ia", "whatsapp", "crm", "erp", "excel", "piloto", "dos", "seis", "catorce", "conversemos", "treinta", "minutos", "semanas", "proceso", "vender", "error", "flujo"}
def phrases(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[,.:;?!]$", w): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def chars(ws): return sum(len(w) + 1 for w in ws)
def align(s):
    ph, iv = phrases(s["text"]), [list(x) for x in s["speech"]]
    while len(ph) > len(iv):
        k = min(range(len(ph) - 1), key=lambda i: chars(ph[i]) + chars(ph[i + 1])); ph[k:k + 2] = [ph[k] + ph[k + 1]]
    while len(iv) > len(ph):
        k = min(range(len(iv) - 1), key=lambda i: iv[i + 1][0] - iv[i][1]); iv[k:k + 2] = [[iv[k][0], iv[k + 1][1]]]
    return ph, iv
caps, WT = [], {}
for s in segs:
    ph, iv = align(s); lst = []
    for words, (a, b) in zip(ph, iv):
        tot, acc = chars(words), 0
        for w_ in words: lst.append((w_.lower().strip("¿¡,.:;?!"), s["start"] + a + (b - a) * acc / tot)); acc += len(w_) + 1
        n = min(len(words), max(1, math.ceil(chars(words) / (30 if VERT else 46))))
        best = None
        for cut in itertools.combinations(range(1, len(words)), n - 1):
            gs = [words[i:j] for i, j in zip((0,) + cut, cut + (len(words),))]
            sc = max(chars(x) for x in gs) + (10 if any(len(x) == 1 for x in gs) else 0)
            if best is None or sc < best[0]: best = (sc, gs)
        t0 = a
        for x in best[1]:
            d = (b - a) * chars(x) / tot; caps.append([s["start"] + t0, s["start"] + t0 + d, x]); t0 += d
    WT[s["id"]] = lst
def W(i, word, off=0.0, nth=0):
    hits = [t for w_, t in WT[i] if w_.startswith(word)]
    if not hits: raise SystemExit(f"palabra no encontrada: {i} {word}")
    return round(hits[min(nth, len(hits) - 1)] + off, 3)
def END(i, off=0.0): s = SEG[i]; return round(s["start"] + s["dur"] + off, 3)
for i in range(len(caps)):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else caps[i][1] + 0.4
    caps[i][1] = min(nxt, caps[i][1] + 0.35) if nxt - caps[i][1] > 0.7 else nxt
def cw(w):
    k = re.sub(r"[^\wáéíóúñ]", "", w.lower())
    return f"<b>{w}</b>" if k in HL else w
CAPS = "\n".join(f'      <div class="cap" id="cap{i}" data-layout-allow-overlap="true"><span>{" ".join(cw(w) for w in c[2])}</span></div>' for i, c in enumerate(caps))
CAPJS = "\n".join(f'      capShow("#cap{i}", {c[0]:.3f}, {c[1]:.3f});' for i, c in enumerate(caps))

def html_escape(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------------------------------------------------------- línea de tiempo
J = []
def js(s): J.append("      " + s)
EASE = '"power3.out"'
def show(sel, t, d=0.55, y=24, x=0):
    js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y}, x: {x} }}, {{ autoAlpha: 1, y: 0, x: 0, duration: {d}, ease: {EASE} }}, {t:.3f});')
def hide(sel, t, d=0.4, y=-16): js(f'tl.to("{sel}", {{ autoAlpha: 0, y: {y}, duration: {d}, ease: "power2.in" }}, {t:.3f});')
def tick(sel, t, snd="tick"): show(sel, t, 0.45, 16); ev(snd, t)
def count(sel, t, a, b, d=1.0, suffix=""):
    js(f'(() => {{ const o = {{ v: {a} }}; const el = document.querySelector("{sel}"); tl.to(o, {{ v: {b}, duration: {d}, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v) + "{suffix}"; }} }}, {t:.3f}); }})();')
def heading(sid, t): show(f"#{sid}ey", t + 0.15, 0.5, 16); show(f"#{sid}t", t + 0.28, 0.6, 30)
def grow(sid, t, gap=0.12, d=0.5):  # barras del logo: superior → media → inferior
    for j in range(3):
        js(f'tl.fromTo("#{sid}{j}", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: {d}, ease: {EASE} }}, {t + j * gap:.3f});')
def cam(sid, a, b):
    js(f'tl.fromTo("#s{sid} > .cam", {{ scale: 1 }}, {{ scale: 1.035, duration: {b - a:.2f}, ease: "none" }}, {a:.3f});')
    js(f'tl.fromTo("#s{sid} .glow", {{ x: 0, y: 0 }}, {{ x: -60, y: 40, duration: {b - a:.2f}, ease: "sine.inOut" }}, {a:.3f});')

# transiciones
def t_bars(prev, nxt, t):
    """Las tres barras del logo cruzan la pantalla, tapan y destapan (sin rebote)."""
    js(f'tl.set(".tbar", {{ visibility: "visible" }}, {t:.3f});')
    js(f'tl.fromTo(".tbar", {{ x: {P(-2420, -1900)} }}, {{ x: {P(-220, -340)}, duration: 0.5, ease: "power3.inOut", stagger: 0.07 }}, {t:.3f});')
    js(f'tl.set("{prev}", {{ autoAlpha: 0 }}, {t + 0.66:.3f});')
    js(f'tl.set("{nxt}", {{ autoAlpha: 1 }}, {t + 0.66:.3f});')
    js(f'tl.to(".tbar", {{ x: {P(2000, 1100)}, duration: 0.55, ease: "power3.inOut", stagger: 0.07 }}, {t + 0.7:.3f});')
    js(f'tl.set(".tbar", {{ visibility: "hidden" }}, {t + 1.45:.3f});')
    ev("whoosh", t)
def t_fade(prev, nxt, t):
    js(f'tl.to("{prev}", {{ autoAlpha: 0, duration: 0.45, ease: "power2.in" }}, {t:.3f});')
    js(f'tl.fromTo("{nxt}", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.6, ease: {EASE} }}, {t + 0.25:.3f});')
    ev("swish", t)
def t_wipe(prev, nxt, t):
    js(f'tl.set("{nxt}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{nxt}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power3.inOut" }}, {t:.3f});')
    js(f'tl.set("{prev}", {{ autoAlpha: 0 }}, {t + 0.72:.3f});')
    ev("swish", t)


VCSS_REP = [("html, body { width: 1920px; height: 1080px;", "html, body { width: 1080px; height: 1920px;"),
    ("#root { position: relative; width: 1920px; height: 1080px;", "#root { position: relative; width: 1080px; height: 1920px;"),
    (".sc { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;", ".sc { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;"),
    (".cam { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;", ".cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;"),
    (".grid { position: absolute; left: -64px; top: -64px; width: 2048px; height: 1208px;", ".grid { position: absolute; left: -64px; top: -64px; width: 1208px; height: 2048px;"),
    (".tbar { position: absolute; left: 0; width: 2320px; height: 360px; border-radius: 180px;", ".tbar { position: absolute; left: 0; width: 1800px; height: 640px; border-radius: 320px;"),
    ("#prog { position: absolute; left: 0; bottom: 0; width: 1920px;", "#prog { position: absolute; left: 0; bottom: 0; width: 1080px;"),
    (".cap { position: absolute; left: 0; top: 958px; width: 1920px;", ".cap { position: absolute; left: 0; top: 1490px; width: 1080px;")]
def css():
    s = open(os.path.join(ROOT, "build", "style.css")).read()
    extra = os.path.join(ROOT, "build", "style-extra.css")
    if os.path.exists(extra): s += open(extra).read()
    if VERT:
        for a, b in VCSS_REP:
            assert a in s, a
            s = s.replace(a, b)
        s += "\n      .cap span { font-size: 38px; padding: 14px 32px; }\n"
        vx = os.path.join(ROOT, "build", "style-vertical.css")
        if os.path.exists(vx): s += open(vx).read()
    return s

def render(SCN, title):
    json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))
    
    CSS = css()
    TB = "".join(f'<div class="tbar" style="top:{i * P(360, 640)}px;background:{c}"></div>' for i, c in enumerate([CYAN, TEAL, NAVY]))
    html = f'''<!doctype html>
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width={WW}, height={HH}" />
        <title>{title}</title>
        <script src="assets/vendor/gsap.min.js"></script>
        <style>
    {CSS}
        </style>
      </head>
      <body>
        <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="{WW}" data-height="{HH}">
    {SCN}
          <div class="abs" id="tbars" style="left:0;top:0;width:{WW}px;height:{HH}px" data-layout-allow-overlap="true">{TB}</div>
          <div id="prog"></div>
    {CAPS}
    {"".join(f'      <audio id="v_{s["id"]}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for s in segs)}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.8"></audio>
          <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.5"></audio>
        </div>
        <script>
          window.__timelines = window.__timelines || {{}};
          const tl = gsap.timeline({{ paused: true }});
          const fmt = (v) => String(Math.round(v)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".");
          const capShow = (sel, a, b) => {{
            tl.fromTo(sel, {{ autoAlpha: 0, y: 10 }}, {{ autoAlpha: 1, y: 0, duration: 0.18, ease: "power2.out" }}, a - 0.04);
            tl.set(sel, {{ autoAlpha: 0 }}, b);
          }};
    {chr(10).join(J)}
    {CAPJS}
          window.__timelines["main"] = tl;
          tl.seek(0);
        </script>
      </body>
    </html>
    '''
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    print("captions", len(caps), "events", len(EV), "T", T)
    
