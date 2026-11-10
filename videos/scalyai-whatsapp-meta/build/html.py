# Scaly AI — tutorial 16:9 (~90 s): conectar WhatsApp Business a la API de Meta con Claude. Identidad: brand/scalyai/frame.md (Guía de diseño v1).
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
HL = {"whatsapp", "meta", "claude", "paso", "uno", "dos", "tres", "cuatro", "cinco", "token", "webhook", "segundos", "ia", "escríbeme", "número"}
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

def html_escape(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------------------------------------------------------- escenas (tutorial: WhatsApp Business + Meta + Claude)
def step_head(sid, n, title_html, lead=None):
    h = (f'<div class="abs eyebrow" id="{sid}ey" style="left:160px;top:130px">Paso {n} de 5</div>'
         f'<div class="abs h1 st" id="{sid}t" style="left:156px;top:176px">{title_html}</div>')
    if lead: h += f'<div class="abs lead" id="{sid}ld" style="left:160px;top:420px;width:640px">{lead}</div>'
    dots = "".join(f'<i class="{"on" if j == n else ("done" if j < n else "")}"></i>' for j in range(1, 6))
    return h + f'<div class="abs pdots">{dots}</div>'
def win(sid, url, inner, x=980, y=190, w=780, h=700):
    return (f'<div class="abs card win" id="{sid}w" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="wbar"><i></i><i></i><i></i><span>{url}</span></div><div class="wbody">{inner}</div></div>')
def fld(sid, label, value, extra=""):
    return f'<div class="fld" id="{sid}"><label>{label}</label><div class="val">{value}{extra}</div></div>'

A = f'''      <div class="sc dark" id="sA"><div class="cam">{BG(900, -300, 1200)}
        <div class="abs eyebrow" id="Aey" style="left:160px;top:170px">Tutorial · 90 segundos</div>
        <div class="abs h1 big" id="At" style="left:156px;top:220px"><span class="l">Conecta tu WhatsApp Business</span><span class="l">a Meta, con <em>Claude</em></span><span class="l">como copiloto.</span></div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="Aln" d="M560 760 L1360 760" pathLength="1" stroke="{CYAN}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" fill="none"/></svg>
        <div class="abs flow" id="An0" style="left:160px;top:700px"><div class="ni" style="background:#128C4A">{wa(40, WHITE)}</div><div><b>WhatsApp Business</b><span>tu número</span></div></div>
        <div class="abs flow" id="An1" style="left:760px;top:700px"><div class="ni">{icon("link", 36, CYAN)}</div><div><b>API de Meta</b><span>WhatsApp Cloud API</span></div></div>
        <div class="abs flow" id="An2" style="left:1360px;top:700px"><div class="ni">{icon("sparkles", 36, CYAN)}</div><div><b>Claude</b><span>escribe y responde</span></div></div>
      </div></div>'''

NEED = [("building-2", "Una cuenta de Meta Business", "Desde business.facebook.com"),
        ("smartphone", "Un número verificable", "Por SMS o llamada. Si ya lo usas en la app de WhatsApp, revisa las opciones de migración de Meta."),
        ("sparkles", "Acceso a Claude", "Para escribir el webhook y responder con su API.")]
B = f'''      <div class="sc" id="sB"><div class="cam">{BG(1000, 200, 1000)}
        <div class="abs eyebrow" id="Bey" style="left:160px;top:130px">Antes de empezar</div>
        <div class="abs h1" id="Bt" style="left:156px;top:176px">Necesitas <em>tres cosas.</em></div>
        {"".join(f'<div class="abs card need" id="Bc{i}" style="left:{160 + i * 540}px;top:380px"><div class="pi">{icon(ic, 44)}</div><h3>{h}</h3><p>{p}</p></div>' for i, (ic, h, p) in enumerate(NEED))}
      </div></div>'''

C_IN = f'''<div class="ftitle">Crear una app</div>
  {fld("Cf0", "Nombre de la app", "Agente WhatsApp")}
  {fld("Cf1", "Tipo de app", "Negocio", f'<span class="ok" id="Cok">{icon("check", 22, WHITE, 3)}</span>')}
  <div class="sbtn" id="Cb0">Crear app</div>
  <div class="prod" id="Cpr"><div class="ni" style="background:#128C4A">{wa(36, WHITE)}</div><div><b>WhatsApp</b><span>Agregar producto</span></div><div class="sbtn sm" id="Cb1">Configurar</div></div>'''
C = f'''      <div class="sc" id="sC"><div class="cam">{BG(-200, 300, 1000)}
        {step_head("C", 1, '<span class="l">Crea una app</span><span class="l"><em>en Meta.</em></span>', 'Entra a developers.facebook.com, crea una app de tipo negocio y agrégale el producto WhatsApp.')}
        {win("C", "developers.facebook.com/apps", C_IN)}
      </div></div>'''

D_IN = f'''<div class="ftitle">WhatsApp › Configuración de la API</div>
  {fld("Df0", "Número de teléfono", "+51 9•• ••• •••")}
  <div class="fld" id="Df1"><label>Código de verificación</label><div class="code6">{"".join(f"<i>{d}</i>" for d in "482913")}<span class="ok" id="Dok">{icon("check", 22, WHITE, 3)}</span></div></div>
  {fld("Df2", "Nombre visible", "Tu negocio")}
  {fld("Df3", "ID del número de teléfono", "1098 7654 3210 123", f'<span class="copy" id="Dcp">Copiar</span>')}
  <div class="wnote">Datos de ejemplo</div>'''
D = f'''      <div class="sc" id="sD"><div class="cam">{BG(-200, 300, 1000)}
        {step_head("D", 2, '<span class="l">Agrega y verifica</span><span class="l"><em>tu número.</em></span>', 'Verifícalo con el código, define el nombre que verán tus clientes y anota el ID del número.')}
        {win("D", "developers.facebook.com › WhatsApp", D_IN)}
      </div></div>'''

E_IN = f'''<div class="ftitle">Configuración del negocio › Usuarios del sistema</div>
  <div class="urow" id="Eu"><div class="ni">{icon("user-cog", 30, TEAL)}</div><div><b>agente-whatsapp</b><span>Administrador · app y cuenta de WhatsApp asignadas</span></div></div>
  <div class="sbtn" id="Eb">Generar token</div>
  <div class="perm" id="Ep0"><span class="ok">{icon("check", 20, WHITE, 3)}</span>whatsapp_business_messaging</div>
  <div class="perm" id="Ep1"><span class="ok">{icon("check", 20, WHITE, 3)}</span>whatsapp_business_management</div>
  {fld("Etk", "Token de acceso", "EAAG•••••••••••••••••••••", f'<span class="copy">Permanente</span>')}'''
E = f'''      <div class="sc" id="sE"><div class="cam">{BG(-200, 300, 1000)}
        {step_head("E", 3, '<span class="l">Crea un token</span><span class="l"><em>permanente.</em></span>', 'Con un usuario del sistema y los permisos de WhatsApp.')}
        <div class="abs tag cyan" id="Esafe" style="left:160px;top:560px">{icon("shield-check", 22, NAVY, 2.4)}Guárdalo en un lugar seguro</div>
        {win("E", "business.facebook.com › Configuración", E_IN)}
      </div></div>'''

CODE = [("k", 'app.post("/webhook", async (req, res) => {'),
        ("", '  const msg = leerMensaje(req.body);'),
        ("", '  const respuesta = await claude.messages.create({'),
        ("", '    model: MODELO, max_tokens: 500, system: NEGOCIO,'),
        ("", '    messages: [{ role: "user", content: msg.texto }],'),
        ("", '  });'),
        ("", '  await enviarWhatsApp(msg.de, respuesta);'),
        ("", '  res.sendStatus(200);'),
        ("k", '});')]
F = f'''      <div class="sc dark" id="sF"><div class="cam">{BG(1000, -300, 1200)}
        {step_head("F", 4, '<span class="l">Claude escribe</span><span class="l"><em>el webhook.</em></span>')}
        <div class="abs prompt" id="Fq" style="left:160px;top:420px;width:640px"><div class="who">{icon("user-round", 26, CYAN)}Tú</div>Escribe un webhook para la API de WhatsApp Cloud: recibe cada mensaje, genera la respuesta con la API de Claude y envíala por WhatsApp.</div>
        <div class="abs envc" id="Fenv" style="left:160px;top:730px;width:640px"><div class="eh">.env<span class="tag cyan sm">Nunca en el chat</span></div><code>WHATSAPP_TOKEN=••••••••</code><code>ANTHROPIC_API_KEY=••••••••</code><code>VERIFY_TOKEN=••••••••</code></div>
        <div class="abs editor" id="Fed" style="left:880px;top:330px;width:880px"><div class="wbar dk"><i></i><i></i><i></i><span>webhook.js</span></div>
          <div class="lines">{"".join(f'<div class="ln {k}" id="Fl{i}"><em>{i + 1}</em>{html_escape(t)}</div>' for i, (k, t) in enumerate(CODE))}</div></div>
      </div></div>'''

G_IN = f'''<div class="ftitle">WhatsApp › Configuración › Webhook</div>
  {fld("Gf0", "URL de devolución de llamada", "https://tu-dominio.com/webhook")}
  {fld("Gf1", "Token de verificación", "••••••••••••")}
  <div class="sbtn" id="Gb">Verificar y guardar</div><span class="okt" id="Gok">{icon("circle-check", 26, TEAL, 2.4)}Verificado</span>
  <div class="ftitle sm" style="margin-top:30px">Campos del webhook</div>
  <div class="sub" id="Gs"><code>messages</code><div class="tog" id="Gtg"><i id="Gkn"></i></div><span class="okt" id="Gsub">Suscrito</span></div>'''
G = f'''      <div class="sc" id="sG"><div class="cam">{BG(-200, 300, 1000)}
        {step_head("G", 5, '<span class="l">Conecta el webhook</span><span class="l"><em>en Meta.</em></span>', 'Publícalo, pega su dirección y el token de verificación, y suscríbete al campo de mensajes.')}
        {win("G", "developers.facebook.com › WhatsApp", G_IN)}
      </div></div>'''

H = f'''      <div class="sc" id="sH"><div class="cam">{BG(-200, 250, 1000)}
        <div class="abs eyebrow" id="Hey" style="left:160px;top:250px">Prueba</div>
        <div class="abs h1" id="Ht" style="left:156px;top:296px"><span class="l">Escríbele a tu número.</span><span class="l"><em>Tu agente responde.</em></span></div>
        <div class="abs tag cyan" id="Hfast" style="left:160px;top:560px">{icon("zap", 22, NAVY, 2.4)}Respuesta en segundos</div>
        <div class="abs note" style="left:160px;top:640px">Conversación ilustrativa</div>
        <div class="abs phone" id="Hph" style="left:1200px;top:60px"><div class="screen">
          <div class="chd"><div class="av">{bars(40, "Hav", True)}</div><div><b>Tu negocio</b><i>en línea</i></div></div>
          <div class="bub in" id="Hm0" style="top:170px">Hola, ¿atienden hoy?<small>7:42 p. m.</small></div>
          <div class="typing" id="Hty" style="top:300px"><i></i><i></i><i></i></div>
          <div class="bub out" id="Hm1" style="top:300px">Hola. Sí, hoy atendemos hasta las 8 p. m. ¿En qué te ayudo?<small>7:42 p. m.</small></div>
        </div></div>
      </div></div>'''

I = f'''      <div class="sc dark" id="sI"><div class="cam">{BG(410, -160, 1100)}
        <div class="abs navlogo dk" id="Ilg" style="left:0;top:150px;width:1920px;justify-content:center">{bars(64, "Ib", True)}<div>Scaly <span>AI</span></div></div>
        <div class="abs h1 ctr" id="It" style="left:0;top:300px;width:1920px"><span class="l">¿Necesitas un agente de IA</span><span class="l">que responda en <em>tu WhatsApp?</em></span></div>
        <div class="abs lead ctr" id="Ild" style="left:0;top:560px;width:1920px">Yo te ayudo a configurarlo.</div>
        <div class="abs" id="Icta" style="left:0;top:670px;width:1920px;display:flex;justify-content:center"><div class="btn" id="Ibtn">Escríbeme {icon("arrow-right", 44, WHITE, 2.4)}</div></div>
        <div class="abs url" id="Iurl" style="left:0;top:820px;width:1920px">SCALYAI.DEV</div>
      </div></div>'''
SCN = "\n".join([A, B, C, D, E, F, G, H, I])

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
for k, sid in enumerate("ABCDEFGHI"): cam(sid, S[k], ENDS[k] + 1.2)
def press(sel, t):
    js(f'tl.to("{sel}", {{ scale: 0.95, duration: 0.1, yoyo: true, repeat: 1, ease: "power1.inOut" }}, {t:.3f});'); ev("tick", t)
def draw(sel, t, d=0.8): js(f'tl.to("{sel}", {{ strokeDashoffset: 0, duration: {d}, ease: "power2.inOut" }}, {t:.3f});')
def win_in(sid, t): show(f"#{sid}w", t, 0.7, 0, 50)
def step_in(sid, t):
    heading(sid, t)
    if sid in "CDG": show(f"#{sid}ld", t + 0.5, 0.6, 16)

# A · gancho
show("#Aey", 0.2, 0.5, 16); show("#At", 0.35, 0.8, 30)
for i, w_ in enumerate(["whatsapp", "meta", "claude"]):
    show(f"#An{i}", W("t1", w_, -0.2), 0.55, 20); ev("tick", W("t1", w_, -0.2))
draw("#Aln", W("t1", "meta", 0), 1.4)

# B · lo que necesitas
t_bars("#sA", "#sB", S[1] - 0.66); heading("B", S[1])
for i, w_ in enumerate(["cuenta", "número", "acceso"]):
    show(f"#Bc{i}", W("t2", w_, -0.25), 0.6, 30); ev("tick", W("t2", w_, -0.25))

# C · paso 1
t_fade("#sB", "#sC", S[2] - 0.3); step_in("C", S[2])
js('gsap.set(["#Cok", "#Cpr"], { autoAlpha: 0 });')
win_in("C", W("t3", "entra", -0.1))
show("#Cf0", W("t3", "crea", -0.3), 0.4, 10); show("#Cf1", W("t3", "crea", 0.1), 0.4, 10)
show("#Cok", W("t3", "negocio", -0.1), 0.3, 0); press("#Cb0", W("t3", "negocio", 0.4))
show("#Cpr", W("t3", "agrégale", -0.1), 0.55, 20); press("#Cb1", W("t3", "whatsapp", 0.2)); ev("chime2", W("t3", "whatsapp", 0.4))

# D · paso 2
t_wipe("#sC", "#sD", S[3] - 0.4); step_in("D", S[3])
js('gsap.set(["#Dok", "#Df1 .code6 i", "#Dcp"], { autoAlpha: 0 });')
win_in("D", S[3] + 0.4)
show("#Df0", W("t4", "agrega", -0.1), 0.4, 10)
tv = W("t4", "verifícalo", -0.3)
js(f'tl.fromTo("#Df1 .code6 i", {{ autoAlpha: 0, y: 8 }}, {{ autoAlpha: 1, y: 0, duration: 0.25, stagger: 0.09, ease: {EASE} }}, {tv:.3f});')
show("#Dok", tv + 0.7, 0.3, 0); ev("chime2", tv + 0.7)
show("#Df2", W("t4", "define", -0.1), 0.4, 10)
show("#Df3", W("t4", "anota", -0.2), 0.4, 10); show("#Dcp", W("t4", "teléfono", -0.2), 0.3, 0); press("#Dcp", W("t4", "teléfono", 0.2))

# E · paso 3
t_wipe("#sD", "#sE", S[4] - 0.4); step_in("E", S[4])
js('gsap.set(["#Esafe"], { autoAlpha: 0 });')
win_in("E", S[4] + 0.4)
show("#Eu", W("t5", "crea", -0.1), 0.5, 14); ev("tick", W("t5", "crea", -0.1))
press("#Eb", W("t5", "genera", -0.05))
show("#Ep0", W("t5", "permisos", -0.3), 0.4, 10); show("#Ep1", W("t5", "permisos", 0.0), 0.4, 10); ev("tick", W("t5", "permisos", -0.3))
show("#Etk", W("t5", "whatsapp", 0.1), 0.5, 10)
show("#Esafe", W("t5", "guárdalo", -0.2), 0.5, 16); ev("chime", W("t5", "guárdalo", -0.2))

# F · paso 4 (Claude)
t_bars("#sE", "#sF", S[5] - 0.66); heading("F", S[5])
js('gsap.set(["#sF .ln", "#Fenv"], { autoAlpha: 0 });')
show("#Fq", W("t6", "pídele", -0.2), 0.6, 24); ev("tick", W("t6", "pídele", -0.2))
show("#Fed", W("t6", "webhook", -0.3), 0.6, 0, 50)
t0, t1 = W("t6", "reciba", -0.2), W("t6", "whatsapp", 0.3)
for i in range(len(CODE)):
    tt_ = t0 + (t1 - t0) * i / (len(CODE) - 1)
    js(f'tl.fromTo("#Fl{i}", {{ autoAlpha: 0, x: -10 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, ease: {EASE} }}, {tt_:.3f});')
    if i % 2 == 0: ev("tick", tt_)
show("#Fenv", W("t6", "claves", -0.2), 0.6, 20); ev("chime2", W("t6", "nunca", -0.1))

# G · paso 5
t_wipe("#sF", "#sG", S[6] - 0.4); step_in("G", S[6])
js('gsap.set(["#Gok", "#Gsub"], { autoAlpha: 0 });')
win_in("G", S[6] + 0.4)
show("#Gf0", W("t7", "pega", -0.2), 0.4, 10); show("#Gf1", W("t7", "token", -0.1), 0.4, 10)
tg = W("t7", "verificación", 0.3); press("#Gb", tg); show("#Gok", tg + 0.3, 0.4, 0); ev("chime2", tg + 0.3)
ts = W("t7", "suscríbete", -0.1)
js(f'tl.to("#Gtg", {{ backgroundColor: "{TEAL}", duration: 0.3 }}, {ts:.3f});')
js(f'tl.to("#Gkn", {{ x: 30, duration: 0.3, ease: "power2.inOut" }}, {ts:.3f});'); ev("tick", ts)
show("#Gsub", W("t7", "mensajes", -0.1), 0.4, 0)

# H · prueba
t_fade("#sG", "#sH", S[7] - 0.3); show("#Hey", S[7] + 0.15, 0.5, 16); show("#Ht", S[7] + 0.28, 0.6, 30)
js('gsap.set(["#Hty", "#Hm1", "#Hfast", "#Hm0"], { autoAlpha: 0 });')
show("#Hph", S[7] + 0.2, 0.7, 0, 60)
tq = W("t8", "escríbele", 0.2); show("#Hm0", tq, 0.45, 16); ev("ping", tq)
js(f'tl.set("#Hty", {{ autoAlpha: 1 }}, {tq + 0.6:.3f});')
js(f'tl.fromTo("#Hty i", {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.25, stagger: 0.12, repeat: 1, yoyo: true, ease: "sine.inOut" }}, {tq + 0.6:.3f});')
ta = W("t8", "agente", -0.2)
js(f'tl.set("#Hty", {{ autoAlpha: 0 }}, {ta:.3f});'); show("#Hm1", ta, 0.45, 16); ev("chime", ta)
show("#Hfast", W("t8", "segundos", -0.1), 0.5, 16)

# I · llamado
t_bars("#sH", "#sI", S[8] - 0.66)
grow("Ib", S[8] + 0.1, 0.12, 0.5); show("#Ilg", S[8] + 0.1, 0.5, 0)
show("#It", W("t9", "necesitas", -0.2), 0.7, 30)
show("#Ild", W("t9", "yo", -0.15), 0.6, 16)
tc = W("t9", "escríbeme", -0.2); show("#Icta", tc, 0.6, 24); ev("chime", tc)
show("#Iurl", END("t9", 0.3), 0.5, 12)
js(f'tl.to("#Ibtn", {{ boxShadow: "0 0 0 14px rgba(71,212,212,.18), 0 16px 40px rgba(0,0,0,.35)", duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {END("t9", 0.5):.3f});')

js(f'tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {T:.2f}, ease: "none" }}, 0);')

json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
TB = "".join(f'<div class="tbar" style="top:{i * 360}px;background:{c}"></div>' for i, c in enumerate([CYAN, TEAL, NAVY]))
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Scaly AI — WhatsApp + Meta + Claude</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1920" data-height="1080">
{SCN}
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
