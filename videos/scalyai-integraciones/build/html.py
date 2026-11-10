# Scaly AI — "Excel, CRM y ERP conectados" (~45 s). FMT=h → 1920×1080 · FMT=v → 1080×1920.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

ERR = "#C2416B"
def pos(x, y, w=None, h=None):
    s = f"left:{x}px;top:{y}px"
    if w: s += f";width:{w}px"
    if h: s += f";height:{h}px"
    return s
M = P(160, 70)                  # margen lateral
TT = P(170, 250)                # top del título
def head(sid, eyebrow, title_html, cls="h1"):
    return (f'<div class="abs eyebrow" id="{sid}ey" style="{pos(M, TT - 46)}">{eyebrow}</div>'
            f'<div class="abs {cls}" id="{sid}t" style="{pos(M - 4, TT)}">{title_html}</div>')
L = lambda *parts: "".join(f'<span class="l">{p}</span>' for p in parts)

APPS = [("file-spreadsheet", "Excel"), ("users", "CRM"), ("boxes", "ERP")]
def app_card(i, ic, name):
    x, y, w, h = P((M + i * 540, 470, 500, 240), (M, 640 + i * 250, 940, 220))
    return (f'<div class="abs card appc" id="Aa{i}" style="{pos(x, y, w, h)}"><div class="ah"><div class="ni">{icon(ic, 30)}</div><b>{name}</b></div>'
            f'<div class="arow">Pedido #1042 · Polo básico M</div><span class="tag soft" id="Ac{i}">Copiado a mano</span></div>')
A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(P(1000, 100), -300, 1200)}
        {head("A", "Tu operación hoy", L("El mismo pedido,", "copiado <em>tres veces.</em>"))}
        {"".join(app_card(i, ic, n) for i, (ic, n) in enumerate(APPS))}
        <div class="abs note" style="{pos(M, P(820, 1420))}">Caso ilustrativo</div>
      </div></div>'''

B = f'''      <div class="sc dark" id="sB"><div class="cam">{BG(P(900, 100), -300, 1200)}
        {head("B", "El costo", L("Tiempo perdido.", "<em>Errores.</em>"))}
        <div class="abs card errc" id="Bc0" style="{pos(*P((M, 470, 780, 330), (M, 640, 940, 300)))}">
          <div class="flab">Pedido en WhatsApp</div><div class="fv">#1042</div>
          <div class="flab" style="margin-top:22px">Pedido en el CRM</div><div class="fv bad" id="Bbad">#1024<span class="tag errt">Mal copiado</span></div></div>
        <div class="abs card clk" id="Bc1" style="{pos(*P((1000, 470, 760, 330), (M, 990, 940, 300)))}"><div class="ni">{icon("clock", 44, CYAN)}</div><div><b id="Bh">0 h</b><span>a la semana copiando datos</span><i>Dato ilustrativo</i></div></div>
      </div></div>'''

HX, HY = P((960, 640), (540, 1000))
NODES = [("WhatsApp", "message-circle"), ("CRM", "users"), ("Hojas de cálculo", "file-spreadsheet"), ("ERP", "boxes")]
NPOS = P([(360, 430), (1340, 430), (310, 790), (1390, 790)], [(70, 640), (700, 640), (70, 1250), (760, 1250)])
NW = [290, 180, 380, 170]
def nc(i): return NPOS[i][0] + NW[i] / 2, NPOS[i][1] + 46
lines = "".join(f'<path id="Cln{i}" d="M{nc(i)[0]:.0f} {nc(i)[1]:.0f} L{HX} {HY}" pathLength="1" stroke="{TEAL}" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/>' for i in range(4))
C = f'''      <div class="sc" id="sC"><div class="cam">{BG(P(500, 0), P(100, 600), 1100)}
        {head("C", "Scaly AI", L("Un solo <em>flujo.</em>"))}
        <svg class="abs" style="left:0;top:0" width="{WW}" height="{HH}" viewBox="0 0 {WW} {HH}">{lines}</svg>
        <div class="abs hub" id="Chub" style="{pos(HX - 85, HY - 85)}">{bars(96, "Cb", True)}</div>
        {"".join(f'<div class="abs node" id="Cn{i}" style="{pos(*NPOS[i])}"><div class="ni">{wa(34, "#128C4A") if t == "WhatsApp" else icon(ic, 32, TEAL)}</div>{t}</div>' for i, (t, ic) in enumerate(NODES))}
      </div></div>'''

D = f'''      <div class="sc" id="sD"><div class="cam">{BG(P(-200, -200), P(300, 900), 1100)}
        {head("D", "Paso a paso", L("Llega el pedido.", "<em>Se registra solo.</em>"), "h1 st")}
        <div class="abs card msgc" id="Dm" style="{pos(*P((M, 470, 700, 300), (M, 620, 940, 280)))}"><div class="ah"><div class="ni" style="background:#128C4A">{wa(30, WHITE)}</div><b>WhatsApp</b><i>ahora</i></div>
          <div class="bubx">Hola, quiero el polo básico en talla M.</div></div>
        <div class="abs arrow" id="Dar" style="{pos(*P((900, 590), (500, 930)))}">{icon("arrow-right", 64, TEAL, 2.4) if not VERT else '<div style="transform:rotate(90deg)">' + icon("arrow-right", 64, TEAL, 2.4) + '</div>'}</div>
        <div class="abs card crm2" id="Dc" style="{pos(*P((1020, 470, 740, 300), (M, 1040, 940, 300)))}"><div class="ah"><div class="ni">{icon("users", 30)}</div><b>CRM</b><span class="tag teal" id="Dnew">Nuevo</span></div>
          <div class="row"><span>Pedido</span><b>#1042</b></div><div class="row"><span>Producto</span><b>Polo básico · M</b></div><div class="row"><span>Canal</span><b>WhatsApp</b></div></div>
      </div></div>'''

ROWS = [("#1040", "Jean clásico · 30", "Entregado"), ("#1041", "Casaca · L", "En camino"), ("#1042", "Polo básico · M", "Registrado")]
E = f'''      <div class="sc" id="sE"><div class="cam">{BG(P(1100, -200), P(200, 900), 1000)}
        {head("E", "Sin copiar nada", L("Todo se", "<em>actualiza.</em>"), "h1 st")}
        <div class="abs card sheet" id="Es" style="{pos(*P((M, 470, 900, 340), (M, 620, 940, 380)))}"><div class="ah"><div class="ni">{icon("file-spreadsheet", 30)}</div><b>Hoja de pedidos</b></div>
          {"".join(f'<div class="srow{" new" if i == 2 else ""}" id="Er{i}"><span>{a}</span><span>{b}</span><span>{c}</span></div>' for i, (a, b, c) in enumerate(ROWS))}</div>
        <div class="abs card erpc" id="Ee" style="{pos(*P((1120, 470, 640, 340), (M, 1060, 940, 300)))}"><div class="ah"><div class="ni">{icon("boxes", 30)}</div><b>ERP · Stock</b></div>
          <div class="stk"><span>Polo básico · M</span><b><em id="Es9">9</em><em id="Es8">8</em></b></div><div class="note">Datos ilustrativos</div></div>
      </div></div>'''

TASKS = ["Copiar el pedido a Excel", "Pasar el pedido al CRM", "Descontar el stock en el ERP"]
F = f'''      <div class="sc" id="sF"><div class="cam">{BG(P(1000, 0), P(200, 800), 1100)}
        {head("F", "El resultado", L("Menos copiar y pegar.", "<em>Más vender.</em>"), "h1 st")}
        <div class="abs card tlist" id="Fl" style="{pos(*P((M, 480, 1000, 330), (M, 640, 940, 350)))}">
          {"".join(f'<div class="task"><div class="ti">{icon("check", 30)}</div><div class="tx">{t}</div><span class="tag teal" id="Fa{i}">{icon("check", 20, "#00646B", 3)}Automático</span></div>' for i, t in enumerate(TASKS))}</div>
      </div></div>'''

G = f'''      <div class="sc dark" id="sG"><div class="cam">{BG(P(410, -10), P(-160, 300), 1100)}
        <div class="abs wm" id="Gwm" style="{pos(*P((532, 200), (205, 520)))};gap:{P(48, 36)}px">{bars(P(170, 150), "Gb", True)}<div class="nm" style="font-size:{P(134, 124)}px">Scaly <span>AI</span></div></div>
        <div class="abs lead ctr" id="Gtag" style="{pos(0, P(440, 760), WW)}">Software e IA a la medida de tu negocio.</div>
        <div class="abs" id="Gcta" style="{pos(0, P(560, 900), WW)};display:flex;justify-content:center"><div class="btn" id="Gbtn">Conversemos de tu próximo piloto {icon("arrow-right", 40, WHITE, 2.4)}</div></div>
        <div class="abs micro" id="Gmic" style="{pos(0, P(704, 1050), WW)}">30 minutos · sin tarjeta · sin compromiso</div>
        <div class="abs url" id="Gurl" style="{pos(0, P(800, 1140), WW)}">SCALYAI.DEV</div>
      </div></div>'''
SCN = "\n".join([A, B, C, D, E, F, G])

# ---------------------------------------------------------------- línea de tiempo
ENDS = S[1:] + [T]
for k, sid in enumerate("ABCDEFG"): cam(sid, S[k], ENDS[k] + 1.2)

# A
heading("A", 0.0)
js('gsap.set(["#Ac0", "#Ac1", "#Ac2"], { autoAlpha: 0 });')
for i, w_ in enumerate(["excel", "crm", "erp"]):
    tw = W("s1", w_, -0.2)
    show(f"#Aa{i}", tw, 0.55, 24); show(f"#Ac{i}", tw + 0.35, 0.4, 0); ev("tick", tw)
# B
t_fade("#sA", "#sB", S[1] - 0.3); heading("B", S[1])
js('gsap.set(["#Bbad .errt"], { autoAlpha: 0 });')
show("#Bc0", W("s2", "tiempo", -0.3), 0.6, 24)
show("#Bc1", W("s2", "tiempo", 0.1), 0.6, 24); count("#Bh", W("s2", "tiempo", 0.3), 0, 12, 1.4, " h")
te = W("s2", "error", -0.3)
js(f'tl.to("#Bbad", {{ borderColor: "{ERR}", color: "{ERR}", duration: 0.3 }}, {te:.3f});')
show("#Bbad .errt", te + 0.1, 0.35, 0); ev("ping", te)
# C
t_bars("#sB", "#sC", S[2] - 0.66); heading("C", S[2])
js('gsap.set(["#Chub"], { autoAlpha: 0 });')
show("#Chub", W("s3", "scaly", -0.2), 0.6, 0); grow("Cb", W("s3", "scaly", -0.1), 0.1, 0.5); ev("chime", W("s3", "scaly", -0.1))
tcn = W("s3", "conectamos", -0.2)
for i in range(4):
    show(f"#Cn{i}", tcn + i * 0.18, 0.5, 16); ev("tick", tcn + i * 0.18)
    js(f'tl.to("#Cln{i}", {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut" }}, {tcn + 0.3 + i * 0.18:.3f});')
js(f'tl.to("#Chub", {{ boxShadow: "0 0 0 18px rgba(71,212,212,.22), 0 20px 50px rgba(4,27,61,.3)", duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {W("s3", "flujo", -0.1):.3f});')
# D
t_wipe("#sC", "#sD", S[3] - 0.4); heading("D", S[3])
js('gsap.set(["#Dnew"], { autoAlpha: 0 });')
show("#Dm", W("s4", "llega", -0.2), 0.6, 24); ev("ping", W("s4", "whatsapp", -0.1))
show("#Dar", W("s4", "registra", -0.4), 0.4, 0, -20)
show("#Dc", W("s4", "registra", -0.2), 0.6, 0, 40); show("#Dnew", W("s4", "crm", -0.1), 0.35, 0); ev("chime2", W("s4", "crm", -0.1))
# E
t_wipe("#sD", "#sE", S[4] - 0.4); heading("E", S[4])
js('gsap.set(["#Er2"], { autoAlpha: 0 });')
show("#Es", W("s5", "hoja", -0.3), 0.6, 24)
show("#Er2", W("s5", "actualiza", -0.2), 0.45, 12); ev("tick", W("s5", "actualiza", -0.2))
show("#Ee", W("s5", "erp", -0.3), 0.6, 0, 40)
js('gsap.set(["#Es8"], { autoAlpha: 0 });')
hide("#Es9", W("s5", "stock", -0.2), 0.3, -30); show("#Es8", W("s5", "stock", 0.0), 0.4, 30)
ev("chime2", W("s5", "stock", 0))
# F
t_fade("#sE", "#sF", S[5] - 0.3); heading("F", S[5])
js('gsap.set(["#Fa0", "#Fa1", "#Fa2"], { autoAlpha: 0 });')
show("#Fl", S[5] + 0.4, 0.6, 24)
for i in range(3):
    tt_ = W("s6", "deja", 0.1) + i * 0.35
    show(f"#Fa{i}", tt_, 0.35, 0); ev("tick", tt_)
ev("chime", W("s6", "vender", -0.1))
# G
t_bars("#sF", "#sG", S[6] - 0.66)
js('gsap.set(["#Gwm .nm"], { autoAlpha: 0 });')
grow("Gb", S[6] + 0.1, 0.14, 0.6); show("#Gwm .nm", S[6] + 0.45, 0.7, 0, -30)
show("#Gtag", S[6] + 0.8, 0.6, 16)
tc = W("s7", "conversemos", -0.1); show("#Gcta", tc, 0.6, 24); ev("chime", tc)
show("#Gmic", W("s7", "treinta", -0.15), 0.5, 16); show("#Gurl", END("s7", 0.2), 0.5, 12)
js(f'tl.to("#Gbtn", {{ boxShadow: "0 0 0 14px rgba(71,212,212,.18), 0 16px 40px rgba(0,0,0,.35)", duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {END("s7", 0.4):.3f});')
js(f'tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {T:.2f}, ease: "none" }}, 0);')

render(SCN, "Scaly AI — Excel, CRM y ERP conectados")
