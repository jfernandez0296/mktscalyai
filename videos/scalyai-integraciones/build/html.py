# Scaly AI — "Excel, CRM y ERP conectados" (~41 s), versión gráfica. FMT=h → 1920×1080 · FMT=v → 1080×1920.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

ERR = "#C2416B"
M = P(160, 70)
TT = P(170, 250)
def head(sid, eyebrow, title_html, cls="h1"):
    return (f'<div class="abs eyebrow" id="{sid}ey" style="{pos(M, TT - 46)}">{eyebrow}</div>'
            f'<div class="abs {cls}" id="{sid}t" style="{pos(M - 4, TT)}">{title_html}</div>')
L = lambda *parts: "".join(f'<span class="l">{p}</span>' for p in parts)
def lab(cx, top, text, id_=""):
    return f'<div class="abs tlab"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""} style="{pos(cx - 170, top, 340)}">{text}</div>'

# A · el mismo pedido, tres veces
APPS = [("file-spreadsheet", "Excel", "c-xls"), ("users", "CRM", "c-crm"), ("boxes", "ERP", "c-erp")]
XLS, CRMC, ERPC = "#1D6F42", "#1F4FBF", "#C56A1A"
AS = P(180, 190)
AC = P([(720, 600), (1130, 600), (1540, 600)], [(220, 860), (540, 860), (860, 860)])
PS = P(170, 150); PC = P((300, 600), (540, 610))
a_lines = "".join(f'<path id="Al{i}" d="M{AC[i][0] + AS / 2 + 18} {AC[i][1]} L{AC[i + 1][0] - AS / 2 - 18} {AC[i + 1][1]}" pathLength="1" stroke="{CYAN}" stroke-width="5" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/>' for i in range(2))
a_pl = "" if VERT else f'<path id="Alp" d="M{PC[0] + PS / 2 + 18} {PC[1]} L{AC[0][0] - AS / 2 - 18} {AC[0][1]}" pathLength="1" stroke="{CYAN}" stroke-width="5" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/>'
def a_app(i, ic, name, c):
    cx, cy = AC[i]
    return (f'<div class="abs" id="Aa{i}" style="{pos(cx - AS // 2, cy - AS // 2)}">{gt(ic, AS, cls=c)}</div>' + lab(cx, cy + AS // 2 + 18, name, f"An{i}")
            + f'<div class="abs tk" id="Ac{i}" style="{pos(cx - 150, cy + AS // 2 + 74, 300)}"><span>#1042 · a mano</span></div>')
A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(P(1000, 100), -300, 1200)}{deco(P(1050, -260), P(760, 1450), P(1.0, 0.8), True)}
        {head("A", "Tu operación hoy", L("El mismo pedido,", "copiado <em>tres veces.</em>"))}
        <div class="abs x3" id="Ax3" style="{pos(*P((1470, 140), (0, 1120, 1080)))}">×3</div>
        <svg class="abs" style="left:0;top:0" width="{WW}" height="{HH}" viewBox="0 0 {WW} {HH}">{a_lines}{a_pl}</svg>
        <div class="abs" id="Ap" style="{pos(PC[0] - PS // 2, PC[1] - PS // 2)}">{person(0, PS)}</div>{lab(PC[0], PC[1] + PS // 2 + P(18, 8), "Tu equipo", "Apn")}
        {"".join(a_app(i, ic, n, c) for i, (ic, n, c) in enumerate(APPS))}
        <div class="abs note" style="{pos(M, P(880, 1400))}">Caso ilustrativo</div>
      </div></div>'''

# B · tiempo y errores
b1, b2 = P(((160, 500, 330, 210), (590, 500, 330, 210)), ((70, 620, 410, 230), (600, 620, 410, 230)))
RS = P(340, 380); rx, ry = P((1270, 440), (350, 930))
B = f'''      <div class="sc dark" id="sB"><div class="cam">{BG(P(900, 100), -300, 1200)}{deco(P(-420, 760), P(1100, -300), P(0.9, 0.8), True)}
        {head("B", "El costo", L("Tiempo perdido.", "<em>Errores.</em>"))}
        <div class="abs card bigtk" id="Bk0" style="{pos(*b1)}"><div class="flab">{wa(26, CYAN)}En WhatsApp</div><b>#1042</b></div>
        <div class="abs card bigtk" id="Bk1" style="{pos(*b2)}"><div class="flab">{icon("users", 26, CYAN)}En el CRM</div><b id="Bbad">#1024</b></div>
        <div class="abs neq" id="Bneq" style="{pos(498, b1[1] + b1[3] // 2 - 42)}">≠</div>
        <div class="abs" id="Brw" style="{pos(rx, ry)}">{ring("Brg", RS, 26, CYAN, "rgba(240,241,232,.12)")}</div>
        <div class="abs ringc" id="Brc" style="{pos(rx, ry, RS, RS)}"><b id="Bh">0 h</b><span>a la semana</span></div>
        <div class="abs note" style="{pos(rx, ry + RS + 16, RS)};text-align:center">copiando datos · dato ilustrativo</div>
      </div></div>'''

# C · un solo flujo
HX, HY = P((960, 640), (540, 1000))
NODES = [("WhatsApp", "message-circle", "#128C4A"), ("CRM", "users", CRMC), ("Hojas de cálculo", "file-spreadsheet", XLS), ("ERP", "boxes", ERPC)]
NPOS = P([(360, 430), (1340, 430), (310, 790), (1390, 790)], [(70, 640), (700, 640), (70, 1250), (760, 1250)])
NW = [290, 180, 380, 170]
def nc(i): return NPOS[i][0] + NW[i] / 2, NPOS[i][1] + 46
c_lines = "".join(f'<path id="Cln{i}" d="M{nc(i)[0]:.0f} {nc(i)[1]:.0f} L{HX} {HY}" pathLength="1" stroke="{TEAL}" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/>' for i in range(4))
c_rings = "".join(f'<circle id="Cr{j}" cx="{HX}" cy="{HY}" r="{r}" fill="none" stroke="{TEAL}" stroke-width="2" opacity="{o}"/>' for j, (r, o) in enumerate([(150, .35), (240, .22), (330, .12)]))
C = f'''      <div class="sc" id="sC"><div class="cam">{BG(P(500, 0), P(100, 600), 1100)}{deco(P(1180, -330), P(-260, 1500), P(1.0, 0.8))}
        {head("C", "Scaly AI", L("Un solo <em>flujo.</em>"))}
        <svg class="abs" style="left:0;top:0" width="{WW}" height="{HH}" viewBox="0 0 {WW} {HH}">{c_rings}{c_lines}</svg>
        {"".join(f'<div class="abs pulse" id="Cp{i}" style="{pos(int(nc(i)[0]) - 9, int(nc(i)[1]) - 9)}"></div>' for i in range(4))}
        <div class="abs hub" id="Chub" style="{pos(HX - 85, HY - 85)}">{bars(96, "Cb", True)}</div>
        {"".join(f'<div class="abs node" id="Cn{i}" style="{pos(*NPOS[i])}"><div class="ni">{wa(34, "#128C4A") if t == "WhatsApp" else icon(ic, 32, col)}</div>{t}</div>' for i, (t, ic, col) in enumerate(NODES))}
      </div></div>'''

# D · llega el pedido, se registra solo
DS = 150
dw, dk = P(((255, 460), (1515, 460)), ((70, 560), (70, 1020)))
dtr = P((430, 530, 1060, 10), (140, 730, 10, 270))
dchip = P((430, 507), (75, 730)); dmove = P(("x", 920), ("y", 214))
dm, dc = P(((160, 660, 620), (1140, 650, 620)), ((250, 560, 760), (250, 1000, 760)))
D = f'''      <div class="sc" id="sD"><div class="cam">{BG(P(-200, -200), P(300, 900), 1100)}{deco(P(1240, -340), P(380, 1480), P(0.9, 0.75))}
        {head("D", "Paso a paso", L("Llega el pedido.", "<em>Se registra solo.</em>"), "h1 st")}
        <div class="abs track2" id="Dtr" style="{pos(*dtr)}"></div>
        <div class="abs" id="Dw" style="{pos(*dw)}">{gt("wa", DS)}</div>
        <div class="abs" id="Dk" style="{pos(*dk)}">{gt("users", DS, cls="c-crm")}</div>
        <div class="abs chipn" id="Dchip" style="{pos(*dchip)}">#1042</div>
        <div class="abs card msgc" id="Dm" style="{pos(*dm)}"><div class="ah">{person(2, 64)}<b>Cliente</b><i>ahora</i></div><div class="bubx">Hola, quiero el polo básico en talla M.</div></div>
        <div class="abs card crm2" id="Dc" style="{pos(*dc)}"><div class="ah"><b>CRM</b><span class="tag teal" id="Dnew">Nuevo</span></div>
          <div class="row"><span>Pedido</span><b>#1042</b></div><div class="row"><span>Producto</span><b>Polo básico · M</b></div><div class="row"><span>Canal</span><b>WhatsApp</b></div></div>
      </div></div>'''

# E · todo se actualiza
ROWS = [("#1040", "Jean clásico · 30", "Entregado"), ("#1041", "Casaca · L", "En camino"), ("#1042", "Polo básico · M", "Registrado")]
E = f'''      <div class="sc" id="sE"><div class="cam">{BG(P(1100, -200), P(200, 900), 1000)}{deco(P(1200, -340), P(-300, 1480), P(0.9, 0.75))}
        {head("E", "Sin copiar nada", L("Todo se", "<em>actualiza.</em>"), "h1 st")}
        <div class="abs card sheet" id="Es" style="{pos(*P((M, 470, 860, 340), (M, 600, 940, 360)))}"><div class="ah">{gt("file-spreadsheet", 64, cls="c-xls")}<b>Hoja de pedidos</b></div>
          {"".join(f'<div class="srow{" new" if i == 2 else ""}" id="Er{i}"><span>{a}</span><span>{b}</span><span>{c}</span></div>' for i, (a, b, c) in enumerate(ROWS))}</div>
        <div class="abs card erpc" id="Ee" style="{pos(*P((1080, 470, 680, 340), (M, 1010, 940, 340)))}"><div class="ah">{gt("boxes", 64, cls="c-erp")}<b>ERP · Stock</b><i>Polo básico · M</i></div>
          <div class="erpb"><div class="grid9">{"".join(f'<div class="bx" id="Ex{i}"></div>' for i in range(9))}</div>
            <div class="stkn"><div class="num"><em id="Es9">9</em><em id="Es8">8</em></div><span>unidades</span></div></div>
          <div class="note">Datos ilustrativos</div></div>
      </div></div>'''

# F · resultado
FS = 150
FC = P([(280, 600), (560, 600), (840, 600)], [(220, 700), (540, 700), (860, 700)])
def f_app(i, ic, name, c):
    cx, cy = FC[i]
    return (f'<div class="abs" id="Ft{i}" style="{pos(cx - FS // 2, cy - FS // 2)}">{gt(ic, FS, cls=c)}</div><div class="abs badge" id="Fa{i}" style="{pos(cx + FS // 2 - 34, cy - FS // 2 - 18)}">{icon("check", 28, WHITE, 3.2)}</div>'
            + lab(cx, cy + FS // 2 + 16, name, f"Fn{i}"))
F = f'''      <div class="sc" id="sF"><div class="cam">{BG(P(1000, 0), P(200, 800), 1100)}{deco(P(1240, -340), P(360, 1480), P(0.9, 0.75))}
        {head("F", "El resultado", L("Menos copiar y pegar.", "<em>Más vender.</em>"), "h1 st")}
        {"".join(f_app(i, ic, n, c) for i, (ic, n, c) in enumerate(APPS))}
        <div class="abs card barsc" id="Fb" style="{pos(*P((1040, 440, 720, 410), (M, 930, 940, 420)))}">
          <div class="ah" style="margin-bottom:24px">{avs([0, 1, 3], 64)}<b>Tu equipo</b></div>
          <div class="brow"><label><span>Trabajo a mano</span></label><div class="btrack"><i id="Fb0" style="background:{SLATE}"></i></div></div>
          <div class="brow"><label><span>Automático</span></label><div class="btrack"><i id="Fb1" style="background:linear-gradient(90deg,#0d2f5c,#47d4d4)"></i></div></div>
          <div class="note">Gráfico ilustrativo</div></div>
      </div></div>'''

G = f'''      <div class="sc dark" id="sG"><div class="cam">{BG(P(410, -10), P(-160, 300), 1100)}{deco(P(1180, 620), P(300, 1380), P(1.0, 0.85), True)}{deco(P(-520, -330), P(-420, -200), P(0.9, 0.8), True)}
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
drift()

# A
heading("A", 0.0)
js('gsap.set(["#Ac0", "#Ac1", "#Ac2", "#Ax3"], { autoAlpha: 0 });')
tp_ = W("s1", "equipo", -0.3); show("#Ap", tp_, 0.55, 20); show("#Apn", tp_ + 0.1, 0.45, 10)
if not VERT: draw("#Alp", W("s1", "excel", -0.45), 0.5)
show("#Ax3", W("s1", "tres", -0.2), 0.7, 30); ev("chime2", W("s1", "tres", -0.2))
for i, w_ in enumerate(["excel", "crm", "erp"]):
    tw = W("s1", w_, -0.25)
    show(f"#Aa{i}", tw, 0.55, 24); show(f"#An{i}", tw + 0.1, 0.45, 12); show(f"#Ac{i}", tw + 0.35, 0.4, 10); ev("tick", tw)
    if i: draw(f"#Al{i - 1}", tw - 0.15, 0.5)
# B
t_fade("#sA", "#sB", S[1] - 0.3); heading("B", S[1])
js('gsap.set(["#Bneq"], { autoAlpha: 0 });')
tb = W("s2", "tiempo", -0.3)
show("#Brw", tb, 0.6, 20); show("#Brc", tb, 0.6, 20)
js(f'tl.to("#Brg", {{ strokeDashoffset: 0.28, duration: 1.5, ease: "power2.out" }}, {tb + 0.2:.3f});'); count("#Bh", tb + 0.2, 0, 12, 1.5, " h")
to = W("s2", "oportunidad", -0.3)
show("#Bk0", to, 0.5, 20); show("#Bk1", to + 0.15, 0.5, 20); ev("tick", to)
te = W("s2", "error", -0.25)
show("#Bneq", te, 0.4, 0); ev("ping", te)
js(f'tl.to("#Bbad", {{ color: "#F08BAA", duration: 0.3 }}, {te:.3f});')
js(f'tl.to("#Bk1", {{ borderColor: "{ERR}", duration: 0.3 }}, {te:.3f});')
# C
t_bars("#sB", "#sC", S[2] - 0.66); heading("C", S[2])
js('gsap.set(["#Chub", "#sC .pulse"], { autoAlpha: 0 });')
th = W("s3", "scaly", -0.2)
show("#Chub", th, 0.6, 0); grow("Cb", th + 0.1, 0.1, 0.5); ev("chime", th + 0.1)
for j in range(3):
    js(f'tl.fromTo("#Cr{j}", {{ scale: 0.6, autoAlpha: 0, svgOrigin: "{HX} {HY}" }}, {{ scale: 1, autoAlpha: 1, duration: 0.8, ease: {EASE} }}, {th + 0.15 + j * 0.12:.3f});')
tcn = W("s3", "conectamos", -0.2)
for i in range(4):
    show(f"#Cn{i}", tcn + i * 0.18, 0.5, 16); ev("tick", tcn + i * 0.18)
    draw(f"#Cln{i}", tcn + 0.3 + i * 0.18, 0.6)
tf = W("s3", "flujo", -0.3)
for i in range(4):
    js(f'tl.set("#Cp{i}", {{ autoAlpha: 1 }}, {tf + i * 0.12:.3f});')
    js(f'tl.fromTo("#Cp{i}", {{ x: 0, y: 0 }}, {{ x: {HX - nc(i)[0]:.0f}, y: {HY - nc(i)[1]:.0f}, duration: 0.7, ease: "power2.inOut" }}, {tf + i * 0.12:.3f});')
    js(f'tl.set("#Cp{i}", {{ autoAlpha: 0 }}, {tf + 0.72 + i * 0.12:.3f});')
js(f'tl.to("#Chub", {{ boxShadow: "0 0 0 18px rgba(71,212,212,.22), 0 20px 50px rgba(4,27,61,.3)", duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {tf + 0.6:.3f});')
# D
t_wipe("#sC", "#sD", S[3] - 0.4); heading("D", S[3])
js('gsap.set(["#Dnew", "#Dchip"], { autoAlpha: 0 });')
tl_ = W("s4", "llega", -0.25)
show("#Dw", tl_, 0.5, 20); show("#Dm", tl_ + 0.15, 0.55, 20); ev("ping", tl_ + 0.15)
tr_ = W("s4", "registra", -0.5)
ax = "X" if dmove[0] == "x" else "Y"
js(f'tl.fromTo("#Dtr", {{ scale{ax}: 0, transformOrigin: "0% 0%" }}, {{ scale{ax}: 1, duration: 0.9, ease: "power2.inOut" }}, {tr_:.3f});')
js(f'tl.set("#Dchip", {{ autoAlpha: 1 }}, {tr_:.3f});')
js(f'tl.fromTo("#Dchip", {{ {dmove[0]}: 0 }}, {{ {dmove[0]}: {dmove[1]}, duration: 0.9, ease: "power2.inOut" }}, {tr_:.3f});')
show("#Dk", tr_ + 0.5, 0.5, 20); show("#Dc", tr_ + 0.7, 0.55, 20)
show("#Dnew", W("s4", "crm", -0.1), 0.35, 0); ev("chime2", W("s4", "crm", -0.1))
# E
t_wipe("#sD", "#sE", S[4] - 0.4); heading("E", S[4])
js('gsap.set(["#Er2", "#Es8"], { autoAlpha: 0 });')
show("#Es", W("s5", "hoja", -0.3), 0.6, 24)
show("#Er2", W("s5", "actualiza", -0.2), 0.45, 12); ev("tick", W("s5", "actualiza", -0.2))
show("#Ee", W("s5", "erp", -0.3), 0.6, 24)
js(f'tl.fromTo("#sE .bx", {{ scale: 0.6, autoAlpha: 0 }}, {{ scale: 1, autoAlpha: 1, duration: 0.3, stagger: 0.04, ease: {EASE} }}, {W("s5", "erp", -0.1):.3f});')
ts_ = W("s5", "stock", -0.15)
js(f'tl.to("#Ex8", {{ backgroundColor: "rgba(217,130,43,0)", duration: 0.35 }}, {ts_:.3f});')
hide("#Es9", ts_, 0.3, -30); show("#Es8", ts_ + 0.2, 0.4, 30); ev("chime2", ts_ + 0.2)
# F
t_fade("#sE", "#sF", S[5] - 0.3); heading("F", S[5])
js('gsap.set(["#Fa0", "#Fa1", "#Fa2"], { autoAlpha: 0 });')
js('gsap.set("#Fb1", { scaleX: 0 });')
for i in range(3):
    show(f"#Ft{i}", S[5] + 0.4 + i * 0.12, 0.5, 20); show(f"#Fn{i}", S[5] + 0.5 + i * 0.12, 0.4, 10)
show("#Fb", S[5] + 0.7, 0.6, 24)
td_ = W("s6", "deja", 0.0)
for i in range(3):
    show(f"#Fa{i}", td_ + i * 0.25, 0.35, 0); ev("tick", td_ + i * 0.25)
js(f'tl.to("#Fb0", {{ scaleX: 0.14, duration: 1.4, ease: "power2.inOut" }}, {td_:.3f});')
js(f'tl.to("#Fb1", {{ scaleX: 1, duration: 1.4, ease: "power2.inOut" }}, {td_ + 0.3:.3f});')
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
