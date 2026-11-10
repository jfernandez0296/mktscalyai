# Scaly AI — "¿Qué pasa en las primeras 2 semanas de un piloto?" (~50 s). FMT=h → 1920×1080 · FMT=v → 1080×1920.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

def pos(x, y, w=None, h=None):
    s = f"left:{x}px;top:{y}px"
    if w: s += f";width:{w}px"
    if h: s += f";height:{h}px"
    return s
M = P(160, 70)
L = lambda *parts: "".join(f'<span class="l">{p}</span>' for p in parts)

def cal(sid, x, y, cell, gap, cols, dark=False):
    out = []
    for d in range(1, 15):
        r, c = divmod(d - 1, cols)
        out.append(f'<div class="abs day{" dk" if dark else ""}" id="{sid}d{d}" style="{pos(x + c * (cell + gap), y + r * (cell + gap), cell, cell)}"><b>{d}</b></div>')
    return "".join(out)

# A · gancho
A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(P(900, 100), -300, 1200)}
        <div class="abs eyebrow" id="Aey" style="{pos(M, P(150, 300))}">Cómo trabajamos</div>
        <div class="abs h1 big" id="At" style="{pos(M - 4, P(200, 350))}">{L("¿Qué pasa en las", "primeras <em>2 semanas</em>", "de un piloto?")}</div>
        {cal("A", *P((M, 640, 100, 14, 14), (M, 900, 120, 15, 7)), dark=True)}
      </div></div>'''

PH = [("Días 1–2", "Elegimos un proceso", [("message-circle", "Conversamos 30 minutos sobre tu operación"), ("target", "Elegimos el proceso que más tiempo le cuesta a tu equipo")], [1, 2]),
      ("Días 3–5", "Mapeamos y conectamos", [("layers", "Vemos cómo funciona hoy, paso a paso"), ("link", "Conectamos tus herramientas: WhatsApp, CRM, hojas de cálculo o ERP")], [3, 4, 5]),
      ("Semana 2", "Lo ponemos a funcionar", [("zap", "Funciona con casos reales de tu negocio"), ("users", "Lo ajustamos con tu equipo")], [8, 9, 10, 11, 12, 13]),
      ("Día 14", "El proceso trabaja solo", [("chart-column", "Empezamos a medir el retorno"), ("target", "ROI medible en 6 semanas")], [14])]
cx, cy, cw, ch = P((M, 560, 1600, 300), (M, 900, 940, 400))
def phase(i, tag, title, bullets):
    bl = "".join(f'<div class="bl" id="Bb{i}{j}"><div class="ni">{icon(ic, 30)}</div><span>{t}</span></div>' for j, (ic, t) in enumerate(bullets))
    return (f'<div class="abs card phase" id="Bp{i}" style="{pos(cx, cy, cw, ch)}"><div class="pl"><span class="tag teal">{tag}</span><h3>{title}</h3></div>'
            f'<div class="pr">{bl}</div></div>')
B = f'''      <div class="sc" id="sB"><div class="cam">{BG(P(1100, -200), P(300, 1000), 1000)}
        <div class="abs eyebrow" id="Bey" style="{pos(M, P(130, 230))}">El piloto, día a día</div>
        <div class="abs h1 st" id="Bt" style="{pos(M - 4, P(176, 276))}">{L("Las primeras", "<em>2 semanas.</em>") if VERT else L("Las primeras <em>2 semanas.</em>")}</div>
        {cal("B", *P((M, 380, 100, 14, 14), (M, 500, 120, 15, 7)))}
        {"".join(phase(i, t, h, b) for i, (t, h, b, _) in enumerate(PH))}
        <div class="abs note" style="{pos(M, P(880, 1400))}">Calendario de ejemplo: cada piloto se ajusta a tu proceso.</div>
      </div></div>'''

C = f'''      <div class="sc dark" id="sC"><div class="cam">{BG(P(410, -10), P(-160, 300), 1100)}
        <div class="abs navlogo dk" id="Clg" style="{pos(0, P(150, 420), WW)};justify-content:center">{bars(64, "Cb", True)}<div>Scaly <span>AI</span></div></div>
        <div class="abs h1 ctr" id="Ct" style="{pos(0, P(290, 560), WW)}">{L("Empezamos con un piloto,", "<em>no con una apuesta.</em>") if not VERT else L("Empezamos con", "un piloto, no con", "<em>una apuesta.</em>")}</div>
        <div class="abs" id="Ccta" style="{pos(0, P(560, 960), WW)};display:flex;justify-content:center"><div class="btn" id="Cbtn">Conversemos de tu próximo piloto {icon("arrow-right", 40, WHITE, 2.4)}</div></div>
        <div class="abs micro" id="Cmic" style="{pos(0, P(704, 1110), WW)}">30 minutos · sin tarjeta · sin compromiso</div>
        <div class="abs url" id="Curl" style="{pos(0, P(800, 1200), WW)}">SCALYAI.DEV</div>
      </div></div>'''
SCN = "\n".join([A, B, C])

# ---------------------------------------------------------------- línea de tiempo
ENDS = S[1:] + [T]
for k, sid in enumerate("ABC"): cam(sid, S[k], ENDS[k] + 1.2)

# A
show("#Aey", 0.2, 0.5, 16); show("#At", 0.35, 0.8, 30)
t2 = W("p1", "semanas", -0.3)
js(f'tl.fromTo("#sA .day", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.35, stagger: 0.06, ease: {EASE} }}, {t2:.3f});')
ev("tick", t2); ev("chime2", t2 + 0.9)

# B
t_bars("#sA", "#sB", S[1] - 0.66); heading("B", S[1])
js('gsap.set(["#sB .phase", "#sB .bl"], { autoAlpha: 0 });')
js(f'tl.fromTo("#sB .day", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.03, ease: {EASE} }}, {S[1] + 0.3:.3f});')
for i, (tag, title, bullets, days) in enumerate(PH):
    sid = f"p{i + 2}"; t0 = SEG[sid]["start"] - 0.15
    if i: hide(f"#Bp{i - 1}", t0 - 0.25, 0.3, -14)
    show(f"#Bp{i}", t0, 0.55, 20); ev("tick", t0)
    for k, d in enumerate(days):
        js(f'tl.to("#Bd{d}", {{ backgroundColor: "{TEAL}", borderColor: "{TEAL}", color: "{WHITE}", duration: 0.3 }}, {t0 + 0.2 + k * 0.08:.3f});')
    words = SEG[sid]["dur"]
    for j in range(len(bullets)):
        show(f"#Bb{i}{j}", t0 + 0.6 + j * min(1.4, words * 0.3), 0.45, 12)
    if i == 3: ev("chime", t0 + 0.3)

# C
t_bars("#sB", "#sC", S[2] - 0.66)
grow("Cb", S[2] + 0.1, 0.12, 0.5); show("#Clg", S[2] + 0.1, 0.5, 0)
show("#Ct", W("p6", "empezamos", -0.2), 0.7, 30)
tc = W("p6", "conversemos", -0.2); show("#Ccta", tc, 0.6, 24); ev("chime", tc)
show("#Cmic", W("p6", "treinta", -0.15), 0.5, 16); show("#Curl", END("p6", 0.2), 0.5, 12)
js(f'tl.to("#Cbtn", {{ boxShadow: "0 0 0 14px rgba(71,212,212,.18), 0 16px 40px rgba(0,0,0,.35)", duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {END("p6", 0.4):.3f});')
js(f'tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {T:.2f}, ease: "none" }}, 0);')

render(SCN, "Scaly AI — Las primeras 2 semanas de un piloto")
