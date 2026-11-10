# Scaly AI — "¿Qué pasa en las primeras 2 semanas de un piloto?" (~47 s), versión gráfica. FMT=h → 1920×1080 · FMT=v → 1080×1920.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

M = P(160, 70)
L = lambda *parts: "".join(f'<span class="l">{p}</span>' for p in parts)
CELL, GAP, COLS = P((100, 14, 14), (120, 15, 7))
CALW = COLS * (CELL + GAP) - GAP

def cal(sid, x, y, dark=False):
    out = []
    for d in range(1, 15):
        r, c = divmod(d - 1, COLS)
        out.append(f'<div class="abs day{" dk" if dark else ""}" id="{sid}d{d}" style="{pos(x + c * (CELL + GAP), y + r * (CELL + GAP), CELL, CELL)}"><b>{d}</b></div>')
    return "".join(out)

# A · gancho
A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(P(900, 100), -300, 1200)}{deco(P(1100, 700), P(300, 1480), P(1.0, 0.8), True)}
        <div class="abs bignum" id="Abig" style="{pos(*P((1180, 150, 640), (0, 1130, 1080)))}">14<small>días</small></div>
        <div class="abs eyebrow" id="Aey" style="{pos(M, P(150, 300))}">Cómo trabajamos</div>
        <div class="abs h1 big" id="At" style="{pos(M - 4, P(200, 350))}">{L("¿Qué pasa en las", "primeras <em>2 semanas</em>", "de un piloto?")}</div>
        {cal("A", M, P(660, 900), dark=True)}
      </div></div>'''

PH = [("Días 1–2", "Elegimos un proceso", "target", "", "#007B83", [0, 1], [("message-circle", "Conversamos 30 minutos sobre tu operación"), ("target", "Elegimos el proceso que más tiempo le cuesta a tu equipo")], [1, 2]),
      ("Días 3–5", "Mapeamos y conectamos", "link", "c-crm", "#1F4FBF", [1], [("layers", "Vemos cómo funciona hoy, paso a paso"), ("link", "Conectamos tus herramientas: WhatsApp, CRM, hojas de cálculo o ERP")], [3, 4, 5]),
      ("Semana 2", "Lo ponemos a funcionar", "zap", "c-erp", "#B5651D", [0, 2, 3], [("zap", "Funciona con casos reales de tu negocio"), ("users", "Lo ajustamos con tu equipo")], [8, 9, 10, 11, 12, 13]),
      ("Día 14", "El proceso trabaja solo", "chart-column", "c-xls", "#1D6F42", [0, 1], [("chart-column", "Empezamos a medir el retorno"), ("target", "ROI medible en 6 semanas")], [14])]
calY = P(380, 500); barY = P(512, 780)
cx, cy, cw, ch = P((M, 570, 1600, 300), (M, 850, 940, 480))
def phase(i, tag, title, ic, cls, ppl, bullets):
    bl = "".join(f'<div class="bl" id="Bb{i}{j}"><div class="ni">{icon(bic, 30)}</div><span>{t}</span></div>' for j, (bic, t) in enumerate(bullets))
    return (f'<div class="abs card phase" id="Bp{i}" style="{pos(cx, cy, cw, ch)}"><div class="pt">{gt(ic, P(170, 150), cls=cls)}<div class="pl"><div class="ptag"><span class="tag teal">{tag}</span>{avs(ppl, 56)}</div><h3>{title}</h3></div></div>'
            f'<div class="pr">{bl}</div><div class="pnum">0{i + 1}</div></div>')
B = f'''      <div class="sc" id="sB"><div class="cam">{BG(P(1100, -200), P(300, 1000), 1000)}{deco(P(1240, -350), P(380, 1500), P(0.9, 0.75))}
        <div class="abs eyebrow" id="Bey" style="{pos(M, P(130, 230))}">El piloto, día a día</div>
        <div class="abs h1 st" id="Bt" style="{pos(M - 4, P(176, 276))}">{L("Las primeras", "<em>2 semanas.</em>") if VERT else L("Las primeras <em>2 semanas.</em>")}</div>
        {cal("B", M, calY)}
        <div class="abs ptrack" style="{pos(M, barY, CALW, 12)}"><div id="Bfill"></div></div>
        {"".join(phase(i, t, h, ic, c, pp, b) for i, (t, h, ic, c, _col, pp, b, _) in enumerate(PH))}
        <div class="abs note" style="{pos(M, P(888, 1350))}">Calendario de ejemplo: cada piloto se ajusta a tu proceso.</div>
      </div></div>'''

C = f'''      <div class="sc dark" id="sC"><div class="cam">{BG(P(410, -10), P(-160, 300), 1100)}{deco(P(1180, 620), P(300, 1380), P(1.0, 0.85), True)}{deco(P(-520, -330), P(-420, -200), P(0.9, 0.8), True)}
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
drift()

# A
show("#Aey", 0.2, 0.5, 16); show("#At", 0.35, 0.8, 30)
t2 = W("p1", "semanas", -0.3)
js('gsap.set("#Abig", { autoAlpha: 0 });')
js(f'tl.fromTo("#Abig", {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.9, ease: {EASE} }}, {t2:.3f});')
js(f'tl.fromTo("#sA .day", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.35, stagger: 0.06, ease: {EASE} }}, {t2:.3f});')
ev("tick", t2); ev("chime2", t2 + 0.9)

# B
t_bars("#sA", "#sB", S[1] - 0.66); heading("B", S[1])
js('gsap.set(["#sB .phase", "#sB .bl"], { autoAlpha: 0 });')
js('gsap.set("#Bfill", { scaleX: 0 });')
js(f'tl.fromTo("#sB .day", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.03, ease: {EASE} }}, {S[1] + 0.3:.3f});')
for i, (tag, title, ic, cls, col, ppl, bullets, days) in enumerate(PH):
    sid = f"p{i + 2}"; t0 = SEG[sid]["start"] - 0.15
    if i: hide(f"#Bp{i - 1}", t0 - 0.25, 0.3, -14)
    show(f"#Bp{i}", t0, 0.55, 20); ev("tick", t0)
    for k, d in enumerate(days):
        js(f'tl.to("#Bd{d}", {{ backgroundColor: "{col}", borderColor: "{col}", color: "{WHITE}", duration: 0.3 }}, {t0 + 0.2 + k * 0.08:.3f});')
    js(f'tl.to("#Bfill", {{ scaleX: {days[-1] / 14:.3f}, duration: 0.9, ease: "power2.inOut" }}, {t0 + 0.2:.3f});')
    for j in range(len(bullets)):
        show(f"#Bb{i}{j}", t0 + 0.6 + j * min(1.4, SEG[sid]["dur"] * 0.3), 0.45, 12)
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
