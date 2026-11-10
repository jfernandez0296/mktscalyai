# Carruseles de Instagram de Scaly AI (1080×1350, 4:5) para el cronograma: semanas 1 y 2.
# Uso: python3 build.py && node render.js   → <carrusel>/slide-N.png
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "..", "videos", "scalyai-crm", "assets", "img")
NAVY, TEAL, CYAN, CREAM, WHITE, SLATE = "#041B3D", "#007B83", "#47D4D4", "#F0F1E8", "#FFFFFF", "#2F4560"

def icon(name, size, color=TEAL, sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
def wa(size, color=WHITE):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, "logo-whatsapp.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path d="{d}" fill="{color}"/></svg>'
def bars(u, dark=False):
    low = CREAM if dark else NAVY
    return (f'<svg width="{60 * u / 64:.0f}" height="{56 * u / 64:.0f}" viewBox="0 0 60 56">'
            + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="7" fill="{c}"/>' for x, y, w, c in [(16, 0, 44, CYAN), (0, 21, 60, TEAL), (0, 42, 44, low)]) + "</svg>")
def gt(ic, size, cls=""):
    inner = wa(int(size * .52)) if ic == "wa" else icon(ic, int(size * .5), WHITE, 1.8)
    return f'<div class="gt{" wa" if ic == "wa" else ""} {cls}" style="width:{size}px;height:{size}px;border-radius:{int(size * .28)}px">{inner}</div>'
PEOPLE = [dict(skin="#E9B48A", hair="#2B1B12", shirt="#007B83", bg="#D6EEEE", long=False), dict(skin="#C68655", hair="#1A1A1A", shirt="#0D2F5C", bg="#E3E5D9", long=True),
          dict(skin="#F2C9A5", hair="#7A4A21", shirt="#D9822B", bg="#D6EEEE", long=True), dict(skin="#8D5A3B", hair="#111111", shirt="#47D4D4", bg="#E3E5D9", long=False)]
def person(i, size):
    p = PEOPLE[i % 4]
    back = f'<path d="M29 42 C26 62 31 70 36 72 L64 72 C69 70 74 62 71 42Z" fill="{p["hair"]}"/>' if p["long"] else ""
    return (f'<div class="pp" style="width:{size}px;height:{size}px"><svg width="{size}" height="{size}" viewBox="0 0 100 100"><rect width="100" height="100" fill="{p["bg"]}"/>{back}'
            f'<path d="M16 100 C16 78 33 68 50 68 C67 68 84 78 84 100 Z" fill="{p["shirt"]}"/><rect x="44" y="54" width="12" height="16" rx="5" fill="{p["skin"]}"/>'
            f'<circle cx="50" cy="42" r="18" fill="{p["skin"]}"/><path d="M31 42 C29 24 42 18 51 19 C62 19 71 27 69 42 C64 34 56 30 50 31 C42 31 35 35 31 42Z" fill="{p["hair"]}"/></svg></div>')
def avs(ids, size): return '<div class="avs">' + "".join(person(i, size) for i in ids) + "</div>"
def deco(x, y, k, dark=False):
    u = 16 * k; low = CREAM if dark else NAVY; op = .10 if dark else .14
    return f'<div class="deco" style="left:{x}px;top:{y}px;opacity:{op}">' + "".join(f'<i style="left:{a * u:.0f}px;top:{b * u:.0f}px;width:{w * u:.0f}px;height:{14 * u:.0f}px;background:{c}"></i>' for a, b, w, c in [(16, 0, 44, CYAN), (0, 21, 60, TEAL), (0, 42, 44, low)]) + "</div>"
L = lambda parts: "".join(f"<span>{p}</span>" for p in parts)

def frame(i, n, body, dark=False, last=False):
    dots = "".join(f'<i class="{"on" if j == i else ""}"></i>' for j in range(1, n + 1))
    sw = "" if last else f'<div class="swipe">Desliza {icon("arrow-right", 30, CYAN if dark else TEAL, 2.4)}</div>'
    return (f'<section class="slide{" dark" if dark else ""}" id="slide-{i}"><div class="grid"></div><div class="glow"></div>{deco(520, 1010, .7, dark)}'
            f'<header><div class="logo">{bars(44, dark)}<span>Scaly <em>AI</em></span></div><span class="count">{i:02d} / {n:02d}</span></header>{body}'
            f'<footer><div class="dots">{dots}</div>{sw}</footer></section>')

def s_cover(s):
    rings = "".join(f'<circle cx="760" cy="1000" r="{r}" fill="none" stroke="{CYAN}" stroke-width="2" opacity="{o}"/>' for r, o in [(190, .4), (270, .25), (350, .14)])
    orb = "".join(f'<div class="abs" style="left:{x - 55}px;top:{y - 55}px">{gt(ic, 110, cls)}</div>' for (ic, cls), (x, y) in zip(s["orbit"], [(500, 880), (990, 800), (560, 1180)]))
    return (f'<svg class="abs" style="left:0;top:0" width="1080" height="1350">{rings}</svg>{orb}<div class="abs" style="left:650px;top:890px">{gt(s["icon"], 220, s.get("cls", ""))}</div>'
            f'<div class="blk" style="top:230px"><div class="eyebrow">{s["eyebrow"]}</div><h1 class="xl">{L(s["title"])}</h1></div>')
def s_item(s):
    tags = ""
    if s.get("t0"): tags = f'<div class="swap"><span class="tag soft">{s["t0"]}</span>{icon("arrow-right", 40, TEAL, 2.4)}<span class="tag teal">{icon("check", 24, "#00646B", 3)}{s["t1"]}</span></div>'
    if s.get("chip"): tags = f'<div class="swap"><span class="tag navy">{s["chip"]}</span></div>'
    ppl = f'<div class="abs" style="left:350px;top:330px">{avs(s["people"], 96)}</div>' if s.get("people") else ""
    return (f'<div class="bignum">{s["num"]}</div><div class="abs" style="left:80px;top:230px">{gt(s["icon"], 240, s.get("cls", ""))}</div>{ppl}'
            f'<div class="blk" style="top:540px"><h1>{L(s["title"])}</h1><p class="lead">{s["text"]}</p>{tags}</div>')
def s_compare(s):
    no = "".join(f'<div class="cr"><span class="ci no">{icon("x", 30, WHITE, 3)}</span>{t}</div>' for t in s["no"])
    si = "".join(f'<div class="cr"><span class="ci si">{icon("check", 30, WHITE, 3)}</span>{t}</div>' for t in s["si"])
    return (f'<div class="blk" style="top:200px"><div class="eyebrow">{s["eyebrow"]}</div><h1 class="md">{L(s["title"])}</h1></div>'
            f'<div class="card cmp" style="top:480px"><div class="flab no">No es</div>{no}</div><div class="card cmp" style="top:830px"><div class="flab">Sí es</div>{si}</div>')
def s_quote(s):
    return f'<div class="quote" style="top:330px"><div class="vbar"></div><h1 class="xl">{L(s["title"])}</h1><p class="lead">{s["text"]}</p></div><div class="abs" style="left:136px;top:960px">{avs([0, 1, 3], 120)}</div>'
def s_hub(s):
    P = [(250, 620), (830, 620), (250, 1010), (830, 1010)]
    lines = "".join(f'<line x1="{x}" y1="{y}" x2="540" y2="815" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>' for x, y in P)
    rings = "".join(f'<circle cx="540" cy="815" r="{r}" fill="none" stroke="{TEAL}" stroke-width="2" opacity="{o}"/>' for r, o in [(150, .3), (230, .18)])
    nodes = "".join(f'<div class="abs" style="left:{x - 80}px;top:{y - 80}px">{gt(ic, 160, cls)}</div><div class="abs nl" style="left:{x - 170}px;top:{y + 92}px">{lab}</div>' for (ic, cls, lab), (x, y) in zip(s["nodes"], P))
    return (f'<div class="blk" style="top:200px"><div class="eyebrow">{s["eyebrow"]}</div><h1 class="md">{L(s["title"])}</h1></div>'
            f'<svg class="abs" style="left:0;top:0" width="1080" height="1350">{rings}{lines}</svg>{nodes}<div class="abs hub" style="left:455px;top:730px">{bars(96, True)}</div>')
def s_cta(s):
    return (f'<div class="close"><div class="biglogo">{bars(150, True)}<span>Scaly <em>AI</em></span></div><h1 class="md ctr">{L(s["title"])}</h1>'
            f'<div class="btn">Conversemos de tu próximo piloto {icon("arrow-right", 36, WHITE, 2.4)}</div><div class="micro">30 minutos · sin tarjeta · sin compromiso</div><div class="url">SCALYAI.DEV</div></div>')
KIND = {"cover": s_cover, "item": s_item, "compare": s_compare, "quote": s_quote, "hub": s_hub, "cta": s_cta}

A2 = dict(t0="A mano", t1="Automático")
CAR = {
 "s1-tareas-a-mano": [
  dict(k="cover", eyebrow="Automatización", title=["5 tareas que", "tu equipo no", "debería hacer", "<em>a mano.</em>"], icon="zap", cls="c-erp", orbit=[("file-spreadsheet", "c-xls"), ("users", "c-crm"), ("wa", "")]),
  dict(k="item", num="01", icon="file-spreadsheet", cls="c-xls", title=["Copiar pedidos", "<em>a Excel.</em>"], text="Cada pedido que llega por WhatsApp se registra solo en tu hoja.", **A2),
  dict(k="item", num="02", icon="users", cls="c-crm", title=["Pasar datos", "<em>al CRM.</em>"], text="El contacto y su pedido entran al CRM sin que nadie los copie.", **A2),
  dict(k="item", num="03", icon="wa", title=["Responder lo mismo", "<em>en WhatsApp.</em>"], text="Un asistente con IA responde horarios, precios y stock en segundos.", **A2),
  dict(k="item", num="04", icon="bell", cls="c-erp", title=["Perseguir", "<em>pagos.</em>"], text="Los recordatorios salen solos, antes del vencimiento.", **A2),
  dict(k="item", num="05", icon="chart-column", title=["Armar el reporte", "<em>de la semana.</em>"], text="Tus números se actualizan solos y los ves cuando quieras.", **A2),
  dict(k="cta", title=["¿Cuál de estas hace", "<em>tu equipo hoy?</em>"])],
 "s1-piloto-3-pasos": [
  dict(k="cover", eyebrow="Cómo trabajamos", title=["El piloto,", "en <em>3 pasos.</em>"], icon="target", orbit=[("link", "c-crm"), ("zap", "c-erp"), ("chart-column", "c-xls")]),
  dict(k="item", num="01", icon="target", title=["Elegimos", "<em>un proceso.</em>"], text="El que más tiempo le cuesta a tu equipo. Uno solo, para empezar bien.", chip="30 minutos de conversación", people=[0, 1]),
  dict(k="item", num="02", icon="zap", cls="c-erp", title=["Lo ponemos", "<em>a funcionar.</em>"], text="Conectamos tus herramientas y lo probamos con casos reales de tu negocio.", chip="2 semanas", people=[0, 2, 3]),
  dict(k="item", num="03", icon="chart-column", cls="c-xls", title=["Medimos", "<em>el retorno.</em>"], text="Con números, no con impresiones.", chip="ROI medible en 6 semanas"),
  dict(k="quote", title=["Empezamos con", "un piloto,", "<em>no con una</em>", "<em>apuesta.</em>"], text="Si funciona, lo hacemos crecer. Contigo."),
  dict(k="cta", title=["¿Qué proceso", "<em>elegirías tú?</em>"])],
 "s2-chatbot-ia": [
  dict(k="cover", eyebrow="IA · WhatsApp", title=["¿Qué es", "realmente un", "<em>“chatbot</em>", "<em>con IA”?</em>"], icon="bot", orbit=[("wa", ""), ("users", "c-crm"), ("clock", "c-erp")]),
  dict(k="compare", eyebrow="Para empezar", title=["No es lo que", "<em>imaginas.</em>"], no=["Un menú de opciones 1, 2, 3", "Respuestas genéricas", "Un reemplazo de tu equipo"], si=["Entiende lo que escribe tu cliente", "Responde con datos de tu negocio", "Pasa a una persona cuando hace falta"]),
  dict(k="item", num="01", icon="clock", cls="c-erp", title=["Responde en", "<em>segundos.</em>"], text="A cualquier hora, también a las 11:40 p. m., cuando tu equipo descansa.", chip="24/7"),
  dict(k="item", num="02", icon="users", cls="c-crm", title=["Registra cada", "<em>pedido.</em>"], text="Lo que conversa con tu cliente queda guardado en tu CRM, sin copiar nada.", chip="Directo a tu CRM"),
  dict(k="item", num="03", icon="handshake", cls="c-xls", title=["Sabe cuándo", "<em>pasar la posta.</em>"], text="Si hay una duda o un caso especial, deriva la conversación a una persona.", chip="Con tu equipo", people=[1, 3]),
  dict(k="cta", title=["¿Quieres uno", "<em>para tu negocio?</em>"])],
 "s2-tres-cosas": [
  dict(k="cover", eyebrow="Scaly AI", title=["Tres cosas,", "<em>bien hechas.</em>"], icon="layers", cls="c-crm", orbit=[("zap", "c-erp"), ("chart-column", "c-xls"), ("wa", "")]),
  dict(k="item", num="01", icon="zap", cls="c-erp", title=["Automatizamos", "<em>lo repetitivo.</em>"], text="Lo que hoy tu equipo hace a mano, empieza a hacerse solo.", **A2),
  dict(k="item", num="02", icon="chart-column", cls="c-xls", title=["Ponemos tus datos", "<em>a trabajar.</em>"], text="Ves lo que pasa en tu operación cada día, sin armar reportes.", chip="Tus números, al día"),
  dict(k="item", num="03", icon="layers", cls="c-crm", title=["Ordenamos", "<em>tu operación.</em>"], text="Tus herramientas dejan de ser islas y trabajan en un solo flujo.", chip="Un solo flujo", people=[0, 1, 2]),
  dict(k="hub", eyebrow="Integraciones", title=["Conectamos lo que", "<em>ya usas.</em>"], nodes=[("wa", "", "WhatsApp"), ("users", "c-crm", "CRM"), ("file-spreadsheet", "c-xls", "Hojas de cálculo"), ("boxes", "c-erp", "ERP")]),
  dict(k="cta", title=["Software e IA", "<em>a la medida</em>", "de tu negocio."])],
}

F = "../../../brand/scalyai/fonts"
CSS = "".join(f'@font-face {{ font-family:"Manrope"; font-weight:{w}; src:url("{F}/Manrope-{w}-latin.woff2") format("woff2"); }}\n' for w in (300, 400, 500, 700, 800)) + open(os.path.join(HERE, "style.css")).read()
for name, slides in CAR.items():
    os.makedirs(os.path.join(HERE, name), exist_ok=True); n = len(slides)
    body = "\n".join(frame(i + 1, n, KIND[s["k"]](s), dark=s["k"] in ("cover", "cta"), last=i == n - 1) for i, s in enumerate(slides))
    open(os.path.join(HERE, name, "carrusel.html"), "w").write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{name}</title><link rel="stylesheet" href="../../../brand/scalyai/tokens.css"><style>\n{CSS}\n</style></head><body>\n{body}\n</body></html>\n')
    print(name, n)
