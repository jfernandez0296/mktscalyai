# Carrusel de Instagram (7 láminas, 1080×1350, 4:5) — Scaly AI con la identidad v1 (brand/scalyai).
# Uso: python3 build.py && node render.js   → slide-1.png … slide-7.png
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "..", "videos", "scalyai-promo", "assets", "img")
NAVY, TEAL, CYAN, CREAM, CREAM3, WHITE = "#041B3D", "#007B83", "#47D4D4", "#F0F1E8", "#D6D9CB", "#FFFFFF"
N = 7

def icon(name, size, color=TEAL, sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')
def wa(size, color):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, "logo-whatsapp.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}" fill="{color}"/></svg>'
def bars(u, dark=False):
    k = u / 64; low = CREAM if dark else NAVY
    spec = [(16, 0, 44, CYAN), (0, 21, 60, TEAL), (0, 42, 44, low)]
    return (f'<svg width="{60 * k:.0f}" height="{56 * k:.0f}" viewBox="0 0 60 56" aria-label="Scaly AI">'
            + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="7" fill="{c}"/>' for x, y, w, c in spec) + "</svg>")
def logo(dark=False, size=44):
    return f'<div class="logo">{bars(size, dark)}<span>Scaly <em>AI</em></span></div>'
def frame(i, body, dark=False, swipe=True):
    dots = "".join(f'<i class="{"on" if j == i else ""}"></i>' for j in range(1, N + 1))
    sw = f'<div class="swipe">Desliza {icon("arrow-right", 30, CYAN if dark else TEAL, 2.4)}</div>' if swipe else ""
    return (f'<section class="slide{" dark" if dark else ""}" id="slide-{i}"><div class="grid"></div><div class="glow"></div>'
            f'<header>{logo(dark)}<span class="count">{i:02d} / {N:02d}</span></header>{body}'
            f'<footer><div class="dots">{dots}</div>{sw}</footer></section>')

TASKS = [("file-spreadsheet", "Copiar el pedido #1042 a Excel"), ("users", "Pasar el pedido #1042 al CRM"),
         ("clock", "Perseguir el pago por WhatsApp"), ("chart-column", "Armar el reporte de la semana")]

S = []
# 1 · portada
S.append(frame(1, f'''
  <div class="hero" style="top:300px">
    <div class="eyebrow">Automatización · IA</div>
    <h1 class="xl">Son las 11:40 p. m. <em>Nadie responde.</em></h1>
    <p class="lead">Un cliente te escribe por WhatsApp. Mañana ya le compró a otro.</p>
  </div>
  <div class="notif" style="top:930px">
    <div class="wa">{wa(44, WHITE)}</div>
    <div><div class="who"><span>Cliente nuevo</span><span>11:40 p. m.</span></div><div class="msg">Hola, ¿tienen stock de la talla M?</div></div>
  </div>
  <div class="wait" style="top:1110px">{icon("clock", 32, CYAN)}Sin respuesta · 8 h</div>
  <div class="note" style="top:1125px;left:auto;right:80px">Caso ilustrativo</div>''', dark=True))

# 2 · el problema
rows = "".join(f'<div class="task"><div class="ti">{icon(ic, 30)}</div><div class="tx">{t}</div><span class="tag soft">Pendiente</span></div>' for ic, t in TASKS)
S.append(frame(2, f'''
  <div class="hero" style="top:220px">
    <div class="eyebrow">Tu operación hoy</div>
    <h1>De día, todo <em>a mano.</em></h1>
  </div>
  <div class="card list" style="top:540px">{rows}</div>
  <div class="card stat" style="top:1000px"><b>12 h</b><div><span>a la semana copiando datos entre sistemas</span><i>Dato ilustrativo</i></div></div>'''))

# 3 · la promesa
S.append(frame(3, f'''
  <div class="promise" style="top:320px">
    <div class="vbar"></div>
    <h1 class="xl">Construimos <em>software e IA</em> <span class="s">a la medida de tu negocio.</span></h1>
    <p class="lead">Automatizamos lo repetitivo y ponemos tus datos a trabajar.</p>
  </div>'''))

# 4 · qué hacemos (tres promesas de la web + integraciones)
P = [("zap", "Automatizamos lo repetitivo", "Los procesos que hoy hace tu equipo a mano, trabajan solos."),
     ("chart-column", "Ponemos tus datos a trabajar", "Ves lo que pasa en tu operación, cada día."),
     ("layers", "Ordenamos tu operación", "Tus herramientas, conectadas en un solo flujo.")]
cards = "".join(f'<div class="card pillar"><div class="pi">{icon(ic, 40)}</div><div><h3>{h}</h3><p>{p}</p></div></div>' for ic, h, p in P)
pills = "".join(f'<span class="pill">{wa(26, "#128C4A") if t == "WhatsApp" else icon(ic, 26)}{t}</span>' for ic, t in [("users", "CRM"), ("", "WhatsApp"), ("file-spreadsheet", "Hojas de cálculo"), ("boxes", "ERP")])
S.append(frame(4, f'''
  <div class="hero" style="top:220px">
    <div class="eyebrow">Lo que hacemos</div>
    <h1>Tres cosas, <em>bien hechas.</em></h1>
  </div>
  <div class="pillars" style="top:520px">{cards}</div>
  <div class="pills" style="top:1100px"><span class="lbl">Conectamos</span>{pills}</div>'''))

# 5 · asistente en WhatsApp
S.append(frame(5, f'''
  <div class="hero" style="top:220px;right:auto;width:470px">
    <div class="eyebrow">IA · WhatsApp</div>
    <h1 style="font-size:66px">Responde en <em>segundos.</em></h1>
    <p class="lead" style="max-width:420px">Y registra cada pedido en tu CRM, a cualquier hora.</p>
    <span class="tag cyan" style="margin-top:36px">{icon("zap", 22, NAVY, 2.4)}Respondió en 2 segundos</span>
    <div class="note" style="position:static;margin-top:20px">Conversación ilustrativa</div>
  </div>
  <div class="phone"><div class="screen">
    <div class="chd"><div class="av">{bars(36, True)}</div><div><b>Asistente Scaly AI</b><i>en línea</i></div></div>
    <div class="bub in" style="top:150px">Hola, ¿tienen stock de la talla M?<small>11:40 p. m.</small></div>
    <div class="bub out" style="top:290px">Sí, nos quedan 8. ¿Te la reservo?<small>11:40 p. m.</small></div>
    <div class="bub in" style="top:440px">Sí, por favor.<small>11:41 p. m.</small></div>
    <div class="rcpt" style="top:550px">{icon("circle-check", 30, TEAL, 2.2)}Pedido #1042 registrado en tu CRM</div>
  </div></div>'''))

# 6 · cómo empezamos
STEPS = [("01", "Elegimos un proceso", "", "el que más te cuesta"), ("02", "Lo ponemos a funcionar", "2 semanas", "en marcha"), ("03", "Medimos el retorno", "6 semanas", "ROI medible")]
steps = "".join(f'<div class="step"><div class="dot">{icon("check", 28, WHITE, 3)}</div><div class="card sc"><div class="num">{n}</div><h3>{h}</h3>{f"<b>{b}</b>" if b else ""}<i>{s}</i></div></div>' for n, h, b, s in STEPS)
S.append(frame(6, f'''
  <div class="hero" style="top:220px">
    <div class="eyebrow">Cómo trabajamos</div>
    <h1>Empezamos con <em>un piloto.</em></h1>
    <p class="lead">No con una apuesta.</p>
  </div>
  <div class="steps" style="top:585px"><div class="rail"></div>{steps}</div>'''))

# 7 · cierre
S.append(frame(7, f'''
  <div class="close">
    <div class="biglogo">{bars(150, True)}<span>Scaly <em>AI</em></span></div>
    <p class="lead">Software e IA a la medida de tu negocio.</p>
    <div class="btn">Conversemos de tu próximo piloto {icon("arrow-right", 36, WHITE, 2.4)}</div>
    <div class="micro">30 minutos · sin tarjeta · sin compromiso</div>
    <div class="url">SCALYAI.DEV</div>
  </div>''', dark=True, swipe=False))

F = "../../brand/scalyai/fonts"
CSS = "".join(f'@font-face {{ font-family:"Manrope"; font-weight:{w}; src:url("{F}/Manrope-{w}-latin.woff2") format("woff2"); }}\n' for w in (300, 400, 500, 700, 800)) + '''
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#999; font-family: var(--font-sans); color: var(--navy-900); }
.slide { position:relative; width:1080px; height:1350px; overflow:hidden; margin-bottom:20px; background: var(--cream-100); }
.slide.dark { background: var(--navy-900); color: var(--cream-100); }
.grid { position:absolute; inset:0; background-image: linear-gradient(var(--cream-300) 1px, transparent 1px), linear-gradient(90deg, var(--cream-300) 1px, transparent 1px); background-size:64px 64px; opacity:.45; }
.dark .grid { background-image: linear-gradient(rgba(240,241,232,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(240,241,232,.07) 1px, transparent 1px); opacity:1; }
.glow { position:absolute; right:-300px; top:300px; width:1000px; height:1000px; border-radius:50%; background: radial-gradient(closest-side, rgba(71,212,212,.35), rgba(71,212,212,0)); }
.dark .glow { background: radial-gradient(closest-side, rgba(71,212,212,.15), rgba(71,212,212,0)); top:-200px; }
header { position:absolute; left:80px; right:80px; top:72px; display:flex; justify-content:space-between; align-items:center; }
.logo { display:flex; align-items:center; gap:14px; font-size:34px; font-weight:800; letter-spacing:-.04em; }
.logo em, .biglogo em { font-style:normal; font-weight:500; color: var(--teal-600); letter-spacing:-.03em; }
.dark .logo em, .dark .biglogo em { color: var(--cyan-400); }
.count { font-size:22px; font-weight:800; letter-spacing:.14em; color: var(--slate-700); }
.dark .count { color:#b9c3cf; }
footer { position:absolute; left:80px; right:80px; bottom:64px; display:flex; justify-content:space-between; align-items:center; }
.dots { display:flex; gap:10px; }
.dots i { display:block; width:14px; height:14px; border-radius:7px; background: var(--cream-300); }
.dots i.on { width:44px; background: var(--teal-600); }
.dark .dots i { background: rgba(240,241,232,.22); }
.dark .dots i.on { background: var(--cyan-400); }
.swipe { display:flex; align-items:center; gap:12px; font-size:26px; font-weight:700; color: var(--teal-600); }
.dark .swipe { color: var(--cyan-400); }
.hero, .promise, .notif, .wait, .note, .card.list, .card.stat, .pillars, .pills, .steps { position:absolute; left:80px; right:80px; }
.eyebrow { font-size:24px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color: var(--teal-600); }
.dark .eyebrow { color: var(--cyan-400); }
h1 { font-size:92px; font-weight:800; letter-spacing:-.04em; line-height:1.05; margin-top:22px; }
h1.xl { font-size:110px; }
h1 em { font-style:normal; color: var(--teal-600); }
.dark h1 em { color: var(--cyan-400); }
h1 .s { font-weight:500; color: var(--slate-700); }
.lead { font-size:38px; font-weight:300; line-height:1.4; color: var(--slate-700); margin-top:28px; }
.dark .lead { color: var(--cream-200); }
.note { font-size:20px; font-weight:500; color: var(--slate-700); }
.dark .note { color:#b9c3cf; }
.tag { display:inline-flex; align-items:center; gap:10px; height:48px; padding:0 22px; border-radius:999px; font-size:19px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; white-space:nowrap; }
.tag.soft { background: var(--cream-200); color: var(--slate-700); }
.tag.cyan { background: var(--cyan-400); color: var(--navy-900); }
.card { background:#fff; border:1px solid var(--cream-300); border-radius:20px; box-shadow: var(--shadow-card); }
.notif { display:flex; gap:26px; align-items:flex-start; padding:30px 34px; background: var(--cream-100); color: var(--navy-900); border-radius:20px; box-shadow:0 24px 60px rgba(0,0,0,.35); }
.notif .wa { flex:none; width:76px; height:76px; border-radius:20px; background:#128c4a; display:flex; align-items:center; justify-content:center; }
.notif .who { display:flex; justify-content:space-between; width:760px; font-size:22px; font-weight:700; color: var(--slate-700); }
.notif .msg { font-size:36px; font-weight:500; margin-top:8px; }
.wait { right:auto; display:flex; align-items:center; gap:16px; height:76px; padding:0 30px; border-radius:999px; border:1px solid rgba(240,241,232,.22); background: rgba(240,241,232,.06); font-size:28px; font-weight:700; }
.task { display:flex; align-items:center; gap:22px; height:100px; padding:0 30px; border-bottom:1px solid var(--cream-300); font-size:30px; font-weight:500; }
.task:last-child { border-bottom:0; }
.ti { flex:none; width:56px; height:56px; border-radius:16px; background: var(--cream-100); display:flex; align-items:center; justify-content:center; }
.tx { flex:1; }
.card.stat { display:flex; align-items:center; gap:44px; padding:40px 48px; }
.stat b { font-size:150px; font-weight:800; letter-spacing:-.05em; line-height:1; color: var(--teal-600); flex:none; }
.stat span { display:block; font-size:34px; font-weight:700; line-height:1.3; }
.stat i { display:block; font-style:normal; font-size:24px; font-weight:300; color: var(--slate-700); margin-top:8px; }
.promise { padding-left:56px; }
.promise .vbar { position:absolute; left:0; top:12px; bottom:8px; width:10px; border-radius:5px; background: var(--teal-600); }
.promise h1 { margin-top:0; }
.pillars { display:flex; flex-direction:column; gap:22px; }
.pillar { display:flex; gap:28px; align-items:center; padding:30px 34px; }
.pi { flex:none; width:84px; height:84px; border-radius:22px; background:#d6eeee; display:flex; align-items:center; justify-content:center; }
.pillar h3 { font-size:38px; font-weight:700; letter-spacing:-.03em; }
.pillar p { font-size:27px; font-weight:300; color: var(--slate-700); margin-top:6px; line-height:1.35; }
.pills { display:flex; flex-wrap:wrap; gap:14px; align-items:center; }
.pills .lbl { flex-basis:100%; font-size:22px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color: var(--teal-600); margin-right:6px; }
.pill { display:inline-flex; align-items:center; gap:12px; height:68px; padding:0 26px 0 18px; border-radius:999px; background:#fff; border:1px solid var(--cream-300); font-size:26px; font-weight:700; }
.phone { position:absolute; right:56px; top:300px; width:500px; height:880px; border-radius:58px; background: var(--navy-900); padding:15px; box-shadow:0 30px 70px rgba(4,27,61,.28); }
.screen { position:relative; width:470px; height:850px; border-radius:44px; background: var(--cream-100); overflow:hidden; }
.chd { position:absolute; left:0; top:0; right:0; height:120px; padding:36px 24px 0; display:flex; gap:16px; align-items:center; background:#fff; border-bottom:1px solid var(--cream-300); }
.chd .av { width:60px; height:60px; border-radius:16px; background: var(--navy-900); display:flex; align-items:center; justify-content:center; }
.chd b { display:block; font-size:23px; font-weight:700; }
.chd i { display:block; font-style:normal; font-size:18px; font-weight:500; color: var(--teal-600); }
.bub { position:absolute; max-width:370px; padding:16px 20px; border-radius:22px; font-size:24px; font-weight:500; line-height:1.3; }
.bub small { display:block; font-size:16px; margin-top:6px; opacity:.75; text-align:right; }
.bub.in { left:22px; background:#fff; border:1px solid var(--cream-300); border-bottom-left-radius:6px; }
.bub.out { right:22px; background: var(--navy-900); color: var(--cream-100); border-bottom-right-radius:6px; }
.rcpt { position:absolute; left:22px; right:22px; display:flex; gap:14px; align-items:center; padding:16px 18px; border-radius:18px; background:#d6eeee; color:#00545a; font-size:22px; font-weight:700; }
.steps { display:flex; flex-direction:column; gap:20px; }
.rail { position:absolute; left:31px; top:80px; bottom:80px; width:10px; border-radius:5px; background: var(--gradient-brand); }
.step { position:relative; display:flex; align-items:center; gap:32px; }
.dot { flex:none; width:72px; height:72px; border-radius:36px; background: var(--teal-600); border:6px solid var(--cream-100); display:flex; align-items:center; justify-content:center; z-index:1; }
.card.sc { flex:1; position:relative; padding:24px 34px; min-height:150px; }
.sc .num { font-size:22px; font-weight:800; letter-spacing:.14em; color: var(--teal-600); }
.sc h3 { font-size:40px; font-weight:700; letter-spacing:-.03em; margin-top:8px; }
.sc b { display:block; font-size:58px; font-weight:800; letter-spacing:-.04em; color: var(--teal-600); margin-top:6px; }
.sc i { position:absolute; right:30px; top:26px; padding:6px 18px; border-radius:999px; background: var(--cream-100); font-style:normal; font-size:22px; font-weight:500; color: var(--slate-700); }
.close { position:absolute; left:0; right:0; top:330px; display:flex; flex-direction:column; align-items:center; text-align:center; }
.biglogo { display:flex; align-items:center; gap:34px; font-size:124px; font-weight:800; letter-spacing:-.045em; }
.close .lead { margin-top:44px; font-size:40px; }
.btn { display:inline-flex; align-items:center; gap:16px; margin-top:70px; height:104px; padding:0 52px; border-radius:999px; background: var(--gradient-brand); color:#fff; font-size:38px; font-weight:700; box-shadow:0 16px 40px rgba(0,0,0,.35); }
.micro { margin-top:34px; font-size:30px; font-weight:500; color: var(--cream-200); }
.url { margin-top:40px; font-size:30px; font-weight:800; letter-spacing:.14em; color: var(--cyan-400); }
'''
html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Scaly AI · carrusel</title>
<link rel="stylesheet" href="../../brand/scalyai/tokens.css">
<style>
{CSS}
</style></head><body>
{chr(10).join(S)}
</body></html>
'''
open(os.path.join(HERE, "carrusel.html"), "w").write(html)
print("slides", len(S))
