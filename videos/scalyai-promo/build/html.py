# Scaly AI — promo 16:9 (~60 s). Identidad: brand/scalyai/frame.md (Guía de diseño v1).
# Genera index.html a partir de build/plan.json y audio/segmentos.json (los escribe build/audio.py).
import json, os, re, math, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
HL = {"scaly", "ia", "whatsapp", "crm", "erp", "excel", "segundos", "repetitivo", "datos", "piloto", "dos", "seis",
      "conversemos", "treinta", "minutos", "nadie", "medida"}
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
        n = min(len(words), max(1, math.ceil(chars(words) / 46)))
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

TASKS = [("file-spreadsheet", "Copiar el pedido #1042 a Excel"), ("users", "Pasar el pedido #1042 al CRM"),
         ("clock", "Perseguir el pago por WhatsApp"), ("chart-column", "Armar el reporte de la semana")]
def tasklist(sid, auto=False):
    rows = []
    for i, (ic, t) in enumerate(TASKS):
        st = (f'<span class="tag soft" id="{sid}pend{i}">Pendiente</span>'
              f'<span class="tag teal" id="{sid}a{i}">{icon("check", 22, "#00646B", 3)}Automático</span>')
        rows.append(f'<div class="task" id="{sid}r{i}"><div class="ti">{icon(ic, 30, TEAL)}</div><div class="tx">{t}</div><div class="st">{st}</div></div>')
    return "".join(rows)

# ---------------------------------------------------------------- escenas
A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(900, -300, 1200)}
        <div class="abs eyebrow" id="Aey" style="left:160px;top:140px" data-layout-allow-overlap="true">Martes por la noche</div>
        <div class="abs clock" id="Aclk" style="left:150px;top:205px">11:40<small>p. m.</small></div>
        <div class="abs line" id="Al1" style="left:160px;top:560px">Un cliente te escribe.</div>
        <div class="abs line dim" id="Al2" style="left:160px;top:660px">Y nadie responde.</div>
        <div class="abs notif" id="Anot" style="left:1060px;top:300px">
          <div class="wa">{wa(46)}</div>
          <div><div class="who"><span>Cliente nuevo</span><span>11:40 p. m.</span></div>
          <div class="msg">Hola, ¿tienen stock de la talla M?</div></div>
        </div>
        <div class="abs wait" id="Await" style="left:1060px;top:520px">{icon("clock", 36, CYAN)}Sin respuesta<b id="Ah">0 min</b></div>
        <div class="abs note" style="left:1060px;top:860px">Caso ilustrativo</div>
      </div></div>'''

B = f'''      <div class="sc" id="sB"><div class="cam">{BG(1100, 200, 900)}
        <div class="abs eyebrow" id="Bey" style="left:160px;top:130px">Tu operación hoy</div>
        <div class="abs h1" id="Bt" style="left:156px;top:176px">De día, todo <em>a mano.</em></div>
        <div class="abs card" id="Bcard" style="left:160px;top:380px;width:1060px">{tasklist("B")}</div>
        <div class="abs card bigstat" id="Bst" style="left:1300px;top:380px;width:460px;height:418px;padding:44px 44px">
          <b id="Bh">0 h</b><span>a la semana copiando datos entre sistemas</span><i>Dato ilustrativo</i></div>
      </div></div>'''

C = f'''      <div class="sc" id="sC"><div class="cam">{BG(980, 0, 1200)}
        <div class="abs wm" id="Cwm" style="left:372px;top:420px">{bars(240, "Cb")}<div class="nm" id="Cnm">Scaly <span>AI</span></div></div>
        <div class="abs navlogo" id="Cnav" style="left:160px;top:110px">{bars(56, "Cs")}<div>Scaly <span>AI</span></div></div>
        <div class="abs hero" id="Chero" style="left:160px;top:240px">
          <div class="abs vbar" id="Cvb" style="left:0;top:8px;height:600px"></div>
          <div class="abs h1" id="Ch0" style="left:56px;top:0">Construimos</div>
          <div class="abs h1" id="Ch1" style="left:56px;top:140px"><em>software e IA</em> <span class="s">a la</span></div>
          <div class="abs h1" id="Ch2" style="left:56px;top:280px"><span class="s">medida de tu negocio.</span></div>
          <div class="abs lead" id="Csub" style="left:60px;top:455px;white-space:nowrap">Ponemos tus datos a trabajar y automatizamos lo repetitivo.</div>
        </div>
      </div></div>'''

D = f'''      <div class="sc" id="sD"><div class="cam">{BG(-200, 250, 1000)}
        <div class="abs eyebrow" id="Dey" style="left:160px;top:150px">IA · WhatsApp</div>
        <div class="abs h1" id="Dt" style="left:156px;top:196px">Responde en <em>segundos.</em></div>
        <div class="abs lead" id="Dsub" style="left:160px;top:330px;white-space:nowrap">Y registra cada pedido en tu CRM.</div>
        <div class="abs card crm" id="Dcrm" style="left:160px;top:470px">
          <div class="hd"><span class="tag navy">CRM</span><span class="tag teal" id="Dnew">Nuevo</span></div>
          <div class="row" style="margin-top:22px"><span>Pedido</span><b>#1042</b></div>
          <div class="row"><span>Producto</span><b>Polo básico · talla M</b></div>
          <div class="row"><span>Canal</span><b>WhatsApp · 11:40 p. m.</b></div>
        </div>
        <div class="abs tag cyan" id="Dfast" style="left:160px;top:830px">{icon("zap", 22, NAVY, 2.4)}Respondió en 2 segundos</div>
        <div class="abs phone" id="Dph" style="left:1200px;top:60px"><div class="screen">
          <div class="chd"><div class="av">{bars(40, "Dav", True)}</div><div><b>Asistente Scaly AI</b><i>en línea</i></div></div>
          <div class="bub in" id="Dm0" style="top:160px">Hola, ¿tienen stock de la talla M?<small>11:40 p. m.</small></div>
          <div class="typing" id="Dty" style="top:300px"><i></i><i></i><i></i></div>
          <div class="bub out" id="Dm1" style="top:300px">Sí, nos quedan 8. ¿Te la reservo?<small>11:40 p. m.</small></div>
          <div class="bub in" id="Dm2" style="top:450px">Sí, por favor.<small>11:41 p. m.</small></div>
          <div class="rcpt" id="Drc" style="top:566px">{icon("circle-check", 34, TEAL, 2.2)}Pedido #1042 registrado en tu CRM</div>
        </div></div>
        <div class="abs note" style="left:160px;top:900px">Conversación ilustrativa</div>
      </div></div>'''

# hub de integraciones (izquierda) + tareas automáticas (derecha)
HX, HY = 560, 640  # centro del hub
NODES = [("CRM", "users", 170, 420), ("WhatsApp", "message-circle", 620, 420), ("Hojas de cálculo", "file-spreadsheet", 120, 800), ("ERP", "boxes", 680, 800)]
def node_center(i):
    t, ic, x, y = NODES[i]; w = {0: 180, 1: 290, 2: 380, 3: 170}[i]
    return x + w / 2, y + 46
lines = "".join(f'<path id="Eln{i}" d="M{node_center(i)[0]:.0f} {node_center(i)[1]:.0f} L{HX} {HY}" pathLength="1" stroke="{TEAL}" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/>' for i in range(4))
E = f'''      <div class="sc" id="sE"><div class="cam">{BG(0, 120, 1100)}
        <div class="abs eyebrow" id="Eey" style="left:160px;top:130px">Integraciones</div>
        <div class="abs h1" id="Et" style="left:156px;top:176px">Automatizamos <em>lo repetitivo.</em></div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{lines}</svg>
        {"".join(f'<div class="abs pulse" id="Ep{i}" style="left:{node_center(i)[0] - 9:.0f}px;top:{node_center(i)[1] - 9:.0f}px"></div>' for i in range(4))}
        <div class="abs hub" id="Ehub" style="left:{HX - 85}px;top:{HY - 85}px">{bars(96, "Eb", True)}</div>
        {"".join(f'<div class="abs node" id="En{i}" style="left:{x}px;top:{y}px"><div class="ni">{wa(34, "#128C4A") if t == "WhatsApp" else icon(ic, 32, TEAL)}</div>{t}</div>' for i, (t, ic, x, y) in enumerate(NODES))}
        <div class="abs card" id="Ecard" style="left:940px;top:400px;width:820px">{tasklist("E", True)}</div>
      </div></div>'''

weeks = [(92, 8), (84, 22), (70, 40), (58, 58), (46, 72), (34, 84), (26, 92), (20, 100)]
F = f'''      <div class="sc dark" id="sF"><div class="cam">{BG(1000, -300, 1200)}
        <div class="abs eyebrow" id="Fey" style="left:160px;top:110px">Datos</div>
        <div class="abs h1" id="Ft" style="left:156px;top:156px">Ponemos tus datos <em>a trabajar.</em></div>
        {"".join(f'<div class="abs card kpi" id="Fk{i}" style="left:{160 + i * 540}px;top:320px"><b><em id="Fn{i}">{v}</em>{u}</b><span>{t}</span></div>' for i, (v, u, t) in enumerate([("0", "", "pedidos registrados solos"), ("0", " h", "ahorradas por semana"), ("24/7", "", "atención a tus clientes")]))}
        <div class="abs card chart" id="Fch" style="left:160px;top:560px">
          <div class="abs lg" style="left:36px;top:30px"><i style="background:#5D708A"></i>Horas de trabajo manual</div>
          <div class="abs lg" style="left:360px;top:30px"><i style="background:{CYAN}"></i>Tareas automatizadas</div>
          <div class="abs note" style="right:36px;top:32px">Datos ilustrativos</div>
          {"".join(f'<div class="abs cbar m" id="Fm{i}" style="left:{70 + i * 190}px;height:{m * 1.7:.0f}px"></div><div class="abs cbar a" id="Fa{i}" style="left:{130 + i * 190}px;height:{a * 1.7:.0f}px"></div><div class="wk" style="left:{52 + i * 190}px">Semana {i + 1}</div>' for i, (m, a) in enumerate(weeks))}
        </div>
      </div></div>'''

STEPS = [("01", "Elegimos un proceso", "1", "proceso", "que más te cuesta"), ("02", "Lo ponemos a funcionar", "2 semanas", "", "en marcha"), ("03", "Medimos el retorno", "6 semanas", "", "ROI medible")]
G = f'''      <div class="sc" id="sG"><div class="cam">{BG(1100, 300, 1000)}
        <div class="abs eyebrow" id="Gey" style="left:160px;top:130px">Cómo trabajamos</div>
        <div class="abs h1" id="Gt" style="left:156px;top:176px">Empezamos con <em>un piloto.</em></div>
        <div class="abs track" style="left:192px;top:432px;width:1500px"><div id="Gfill"></div></div>
        {"".join(f'<div class="abs dot" id="Gd{i}" style="left:{160 + i * 750}px;top:406px">{icon("check", 30, CREAM3, 3)}</div><div class="abs dot on" id="Gdo{i}" style="left:{160 + i * 750}px;top:406px">{icon("check", 30, WHITE, 3)}</div>' for i in range(3))}
        {"".join(f'<div class="abs card step" id="Gs{i}" style="left:{160 + i * 540}px;top:540px"><div class="num">{n}</div><h3>{h}</h3><b>{b if i else ""}</b><i>{sub}</i></div>' for i, (n, h, b, _, sub) in enumerate(STEPS))}
      </div></div>'''

H = f'''      <div class="sc dark" id="sH"><div class="cam">{BG(410, -160, 1100)}
        <div class="abs wm" id="Hwm" style="left:532px;top:190px">{bars(170, "Hb", True)}<div class="nm" style="font-size:134px">Scaly <span>AI</span></div></div>
        <div class="abs lead" id="Htag" style="left:0;top:430px;width:1920px;text-align:center">Software e IA a la medida de tu negocio.</div>
        <div class="abs" id="Hcta" style="left:0;top:560px;width:1920px;display:flex;justify-content:center"><div class="btn" id="Hbtn">Conversemos de tu próximo piloto {icon("arrow-right", 44, WHITE, 2.4)}</div></div>
        <div class="abs micro" id="Hmic" style="left:0;top:704px;width:1920px">30 minutos · sin tarjeta · sin compromiso</div>
        <div class="abs url" id="Hurl" style="left:0;top:800px;width:1920px">SCALYAI.DEV</div>
      </div></div>'''

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
    js(f'tl.fromTo(".tbar", {{ x: -2420 }}, {{ x: -220, duration: 0.5, ease: "power3.inOut", stagger: 0.07 }}, {t:.3f});')
    js(f'tl.set("{prev}", {{ autoAlpha: 0 }}, {t + 0.66:.3f});')
    js(f'tl.set("{nxt}", {{ autoAlpha: 1 }}, {t + 0.66:.3f});')
    js(f'tl.to(".tbar", {{ x: 2000, duration: 0.55, ease: "power3.inOut", stagger: 0.07 }}, {t + 0.7:.3f});')
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

ENDS = S[1:] + [T]
for k, sid in enumerate("ABCDEFGH"): cam(sid, S[k], ENDS[k] + 1.2)

# A · noche
show("#Aey", 0.2, 0.5, 16); show("#Aclk", 0.35, 0.7, 30)
tA = W("e1", "cliente", -0.25)
show("#Al1", tA, 0.55, 20); show("#Anot", tA + 0.1, 0.6, 0, 40); ev("ping", tA + 0.1)
tN = W("e1", "nadie", -0.2)
show("#Al2", tN, 0.55, 20); show("#Await", tN + 0.1, 0.5, 16)
js(f'(() => {{ const o = {{ v: 0 }}; const el = document.querySelector("#Ah"); tl.to(o, {{ v: 480, duration: 1.9, ease: "power2.in", onUpdate: () => {{ const m = Math.round(o.v); el.textContent = m < 60 ? m + " min" : Math.floor(m / 60) + " h"; }} }}, {tN + 0.3:.3f}); }})();')
js(f'tl.to("#Anot", {{ opacity: 0.45, duration: 1.2, ease: "power1.inOut" }}, {tN + 0.4:.3f});')

# B · tareas a mano
t_bars("#sA", "#sB", S[1] - 0.66); heading("B", S[1])
show("#Bcard", W("e2", "equipo", -0.3), 0.6, 30)
js('gsap.set(["#sB .tag.teal"], { autoAlpha: 0 });')
for i, w_ in enumerate(["copia", "pasa", "persigue", "mano"]):
    show(f"#Br{i} .ti", W("e2", w_, -0.1), 0.4, 0, -12); js(f'tl.to("#Br{i}", {{ backgroundColor: "#F7F7F1", duration: 0.3 }}, {W("e2", w_, -0.1):.3f});'); ev("tick", W("e2", w_, -0.1))
show("#Bst", W("e2", "pasa", 0), 0.6, 30)
count("#Bh", W("e2", "pasa", 0.3), 0, 12, 1.6, " h")

# C · marca
t_fade("#sB", "#sC", S[2] - 0.3)
js('gsap.set(["#Cnav", "#Chero"], { autoAlpha: 0 });')
tC = W("e3", "scaly", -0.45)
show("#Cwm", S[2] + 0.1, 0.01, 0)
grow("Cb", S[2] + 0.15, 0.14, 0.6); ev("chime", tC)
show("#Cnm", tC, 0.7, 0, -30)
tH = W("e3", "construimos", -0.35)
hide("#Cwm", tH - 0.2, 0.45, -30)
show("#Cnav", tH + 0.1, 0.5, 12); grow("Cs", tH + 0.1, 0.08, 0.4)
js(f'tl.set("#Chero", {{ autoAlpha: 1 }}, {tH:.3f});')
js(f'tl.fromTo("#Cvb", {{ scaleY: 0, transformOrigin: "50% 0%" }}, {{ scaleY: 1, duration: 0.8, ease: {EASE} }}, {tH:.3f});')
show("#Ch0", tH + 0.05, 0.6, 30); show("#Ch1", W("e3", "software", -0.15), 0.6, 30); show("#Ch2", W("e3", "medida", -0.25), 0.6, 30)
show("#Csub", END("e3", 0.1), 0.6, 20)

# D · chatbot
t_bars("#sC", "#sD", S[3] - 0.66); heading("D", S[3])
js('gsap.set(["#Dty", "#Dm1", "#Dm2", "#Drc", "#Dfast", "#Dsub", "#Dcrm"], { autoAlpha: 0 });')
show("#Dph", S[3] + 0.2, 0.7, 0, 60)
tick("#Dm0", S[3] + 0.6, "ping")
tq = W("e4", "responde", -0.2)
js(f'tl.set("#Dty", {{ autoAlpha: 1 }}, {tq - 0.5:.3f});')
js(f'tl.fromTo("#Dty i", {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.25, stagger: 0.12, repeat: 1, yoyo: true, ease: "sine.inOut" }}, {tq - 0.5:.3f});')
js(f'tl.set("#Dty", {{ autoAlpha: 0 }}, {tq:.3f});')
tick("#Dm1", tq); show("#Dfast", W("e4", "segundos", -0.1), 0.5, 16)
tick("#Dm2", W("e4", "segundos", 0.5))
tr = W("e4", "registra", -0.1)
tick("#Drc", tr, "chime"); show("#Dsub", tr, 0.5, 16); show("#Dcrm", tr + 0.25, 0.6, 24)

# E · conexiones
t_wipe("#sD", "#sE", S[4] - 0.4); heading("E", S[4])
js('gsap.set(["#Ehub", "#sE .pulse", "#sE .tag.soft"], { autoAlpha: 0 });')
show("#Ehub", S[4] + 0.3, 0.6, 0)
for i, w_ in enumerate(["crm", "whatsapp", "hojas", "erp"]):
    tw = W("e5", w_, -0.15)
    show(f"#En{i}", tw, 0.5, 16); ev("tick", tw)
    js(f'tl.to("#Eln{i}", {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut" }}, {tw + 0.15:.3f});')
show("#Ecard", W("e5", "conectamos", -0.1), 0.6, 0, 40)
ta = W("e5", "automatizamos", -0.15)
for i in range(4):
    tp = ta + 0.1 + i * 0.2
    js(f'tl.set("#Ep{i}", {{ autoAlpha: 1 }}, {tp - 0.5:.3f});')
    js(f'tl.fromTo("#Ep{i}", {{ x: 0, y: 0 }}, {{ x: {HX - node_center(i)[0]:.0f}, y: {HY - node_center(i)[1]:.0f}, duration: 0.7, ease: "power2.inOut" }}, {tp - 0.5:.3f});')
    js(f'tl.set("#Ep{i}", {{ autoAlpha: 0 }}, {tp + 0.2:.3f});')
    js(f'tl.fromTo("#Ea{i}", {{ autoAlpha: 0, y: 10 }}, {{ autoAlpha: 1, y: 0, duration: 0.4, ease: {EASE} }}, {tp:.3f});')
    ev("tick", tp)
js(f'tl.to("#Ehub", {{ boxShadow: "0 0 0 18px rgba(71,212,212,.22), 0 20px 50px rgba(4,27,61,.3)", duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {ta:.3f});')

# F · datos
t_bars("#sE", "#sF", S[5] - 0.66); heading("F", S[5])
td = W("e6", "ves", -0.4)
for i in range(3): show(f"#Fk{i}", W("e6", "datos", -0.1) + i * 0.15, 0.55, 24)
count("#Fn0", W("e6", "datos", 0.2), 0, 1240, 1.8); count("#Fn1", W("e6", "datos", 0.35), 0, 18, 1.6)
show("#Fch", td - 0.2, 0.6, 30)
js(f'tl.fromTo("#sF .cbar", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.7, stagger: 0.07, ease: {EASE} }}, {td:.3f});')
ev("tick", W("e6", "datos", -0.1)); ev("chime2", td + 0.6)

# G · piloto
t_wipe("#sF", "#sG", S[6] - 0.4); heading("G", S[6])
js('gsap.set(["#Gdo0", "#Gdo1", "#Gdo2"], { autoAlpha: 0 });')
js('gsap.set("#Gfill", { scaleX: 0 });')
marks = [W("e7", "elegimos", -0.2), W("e7", "funcionar", -0.2), W("e7", "medimos", -0.2)]
for i, tm in enumerate(marks):
    show(f"#Gs{i}", tm, 0.6, 30)
    js(f'tl.to("#Gfill", {{ scaleX: {i / 2:.2f}, duration: 0.7, ease: "power2.inOut" }}, {tm - 0.5:.3f});')
    js(f'tl.fromTo("#Gdo{i}", {{ autoAlpha: 0, scale: 0.8 }}, {{ autoAlpha: 1, scale: 1, duration: 0.4, ease: {EASE} }}, {tm + 0.15:.3f});')
    ev("tick", tm + 0.15)
ev("chime", W("e7", "funcionar", 0.3)); ev("chime2", W("e7", "retorno", 0))
js(f'tl.fromTo("#Gs1 b", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease: {EASE} }}, {W("e7", "funcionar", 0.25):.3f});')
js(f'tl.fromTo("#Gs2 b", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease: {EASE} }}, {W("e7", "retorno", -0.05):.3f});')

# H · cierre
t_bars("#sG", "#sH", S[7] - 0.66)
js('gsap.set(["#Hwm .nm"], { autoAlpha: 0 });')
grow("Hb", S[7] + 0.1, 0.14, 0.6)
show("#Hwm .nm", S[7] + 0.45, 0.7, 0, -30)
show("#Htag", S[7] + 0.9, 0.6, 16)
tcta = W("e8", "conversemos", -0.1)
show("#Hcta", tcta, 0.6, 24); ev("chime", tcta)
show("#Hmic", W("e8", "treinta", -0.15), 0.5, 16)
show("#Hurl", END("e8", 0.2), 0.5, 12)
js(f'tl.to("#Hbtn", {{ boxShadow: "0 0 0 14px rgba(71,212,212,.18), 0 16px 40px rgba(0,0,0,.35)", duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {END("e8", 0.4):.3f});')

js(f'tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {T:.2f}, ease: "none" }}, 0);')
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
TB = "".join(f'<div class="tbar" style="top:{i * 360}px;background:{c}"></div>' for i, c in enumerate([CYAN, TEAL, NAVY]))
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Scaly AI — promo</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1920" data-height="1080">
{A}
{B}
{C}
{D}
{E}
{F}
{G}
{H}
      <div class="abs" id="tbars" style="left:0;top:0;width:1920px;height:1080px" data-layout-allow-overlap="true">{TB}</div>
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
