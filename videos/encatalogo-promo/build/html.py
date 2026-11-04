# EnCatalogo.pe — promo vertical 9:16 (~64 s). Identidad: brand/encatalogo/frame.md · datos: brand/encatalogo/producto.md
import json, os, re, math, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
SEG = {s["id"]: s for s in segs}
S, T = plan["S"], plan["T"]
CREAM, LIGHT, WHITE, INK = "#F2EDE4", "#FAF9F5", "#FFFFFF", "#0F0F10"
TERRA, TERRAD, SOFT, BORDER = "#D99873", "#A65353", "#F2E6CE", "#E7DDD1"
OK, BODY, MUTED, WA = "#3F7A4F", "#57534E", "#8A8178", "#25D366"

def p(i, k=0, off=0.0):
    s = SEG[i]; iv = s["speech"]; k = min(k, len(iv) - 1)
    return round(s["start"] + iv[k][0] + off, 3)
EV = []
def ev(kind, t): EV.append([kind, round(t, 3)])
def icon(name, size, color=INK, sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>')
def logo(name, size, color):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, f"logo-{name}.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-label="{name}"><path d="{d}" fill="{color}"/></svg>'
MARK = lambda h: f'<img src="assets/img/encatalogo-logo.svg" alt="EnCatalogo.pe" style="height:{h}px;width:auto;display:block">'

# ---------------------------------------------------------------- captions (same engine as earlier projects)
HL = {"encatalogo", "stock", "tienda", "traslado", "reponer", "celular", "agotando", "facturas", "comprobante", "whatsapp",
      "yape", "plin", "catálogo", "claude", "muñeca", "paris", "bullking", "gratis", "orden", "control", "vendido", "sola"}
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
        n = min(len(words), max(1, math.ceil(chars(words) / 22)))
        best = None
        for cut in itertools.combinations(range(1, len(words)), n - 1):
            gs = [words[i:j] for i, j in zip((0,) + cut, cut + (len(words),))]
            sc = max(chars(x) for x in gs) + (8 if any(len(x) == 1 and len(x[0]) < 6 for x in gs) else 0)
            if best is None or sc < best[0]: best = (sc, gs)
        t0 = a
        for x in best[1]:
            d = (b - a) * chars(x) / tot; caps.append([s["start"] + t0, s["start"] + t0 + d, x]); t0 += d
    WT[s["id"]] = lst
def W(i, word, off=0.0, nth=0):
    hits = [t for w_, t in WT[i] if w_.startswith(word)]
    if not hits: raise SystemExit(f"palabra no encontrada: {i} {word}")
    return round(hits[min(nth, len(hits) - 1)] + off, 3)
for i in range(len(caps)):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else caps[i][1] + 0.4
    caps[i][1] = min(nxt, caps[i][1] + 0.35) if nxt - caps[i][1] > 0.7 else nxt
def cw(w):
    k = re.sub(r"[^\wáéíóúñ]", "", w.lower())
    w = w.replace("EnCatalogo", "EnCatalogo")
    return f"<b>{w}</b>" if k in HL else w
CAPS = "\n".join(f'      <div class="cap" id="cap{i}" data-layout-allow-overlap="true"><span>{" ".join(cw(w) for w in c[2])}</span></div>' for i, c in enumerate(caps))
CAPJS = "\n".join(f'      capShow("#cap{i}", {c[0]:.3f}, {c[1]:.3f});' for i, c in enumerate(caps))

# ---------------------------------------------------------------- pieces
def head(sid, kick, title, dark=False, top=250, size=92):
    kc = TERRA if dark else TERRAD
    tc = WHITE if dark else INK
    badge = f'<div class="abs badge{" dk" if dark else ""}" id="{sid}k" style="left:70px;top:{top}px">{kick}</div>'
    return badge + f'<div class="abs ttl" id="{sid}t" style="left:70px;top:{top + 80}px;width:940px;font-size:{size}px;color:{tc}">{title}</div>'
BRAND = lambda sid, dark=False: (f'<div class="abs brand" id="{sid}br" style="left:70px;top:130px;color:{WHITE if dark else INK}">'
                                 f'<span class="bchip{" dk" if dark else ""}">{MARK(54)}</span>EnCatalogo.pe</div>')
def chip(sid, ic, text, x, y, bg=WHITE, fg=INK, icc=TERRAD, extra=""):
    return f'<div class="abs chip" id="{sid}" style="left:{x}px;top:{y}px;background:{bg};color:{fg}">{icon(ic, 40, icc)}<span>{text}</span>{extra}</div>'

# blazer illustration for the AI Studio before/after (vector, labelled as recreation)
BLAZER = '''<svg viewBox="0 0 200 240" width="{w}" height="{h}" aria-label="blazer">
  <path d="M62 20 L100 40 L138 20 L176 44 L190 200 L160 206 L156 120 L150 232 L50 232 L44 120 L40 206 L10 200 L24 44 Z" fill="{c}"/>
  <path d="M62 20 L100 120 L138 20" fill="none" stroke="{l}" stroke-width="5"/>
  <path d="M100 120 L100 232" stroke="{l}" stroke-width="3"/>
  <circle cx="108" cy="150" r="5" fill="{l}"/><circle cx="108" cy="180" r="5" fill="{l}"/>
  <path d="M70 170 L90 170" stroke="{l}" stroke-width="4"/><path d="M114 100 L132 100" stroke="{l}" stroke-width="4"/>
</svg>'''

# A · hook
A = f'''      <div class="sc" id="sA" style="background:{CREAM}">
        {BRAND("A")}
        {head("A", "INVENTARIO CONECTADO A TUS VENTAS", "¿Cuántas te quedan de tu más vendido?", top=290, size=100)}
        <div class="abs card" id="Acard" style="left:70px;top:690px;width:940px;height:330px">
          <div class="abs pic" style="left:40px;top:40px">{icon("shirt", 120, TERRAD, 1.6)}</div>
          <div class="abs ptitle" style="left:290px;top:58px">Blazer Siena</div>
          <div class="abs pmeta" style="left:290px;top:146px">Negro · Talla S</div>
          <div class="abs eyebrow" style="left:290px;top:220px;color:{MUTED}">STOCK</div>
          <div class="abs qmark" id="Aq" style="left:780px;top:70px">?</div>
        </div>
        {"".join(chip(f"As{i}", ic, t, x, 1080, extra=f'<b class="qq">?</b>') for i, (ic, t, x) in enumerate([("store", "Miraflores", 70), ("store", "San Isidro", 395), ("warehouse", "Almacén", 720)]))}
      </div>'''

# B · inventory
rows = [("Vestido Emilia", "Miraflores", "24"), ("Blazer Siena", "San Isidro", "7"), ("Pantalón Nara", "Almacén", "86")]
B = f'''      <div class="sc" id="sB" style="background:{LIGHT}">
        {head("B", "INVENTARIO", "Todo tu stock, en una sola vista")}
        <div class="abs card" id="Bcard" style="left:70px;top:560px;width:940px;height:780px">
          <div class="abs eyebrow" style="left:44px;top:44px">RESUMEN DE EXISTENCIAS</div>
          <div class="abs today" style="left:780px;top:38px">Hoy</div>
          {"".join(f'<div class="abs stat" id="Bst{i}" style="left:{44 + i * 290}px;top:110px"><b id="Bn{i}">{v}</b><span>{t}</span></div>' for i, (v, t) in enumerate([("1,248", "unidades"), ("12", "por reponer"), ("3", "traslados")]))}
          <div class="abs thead" style="left:44px;top:330px;width:852px"><span>Producto</span><span>Tienda</span><span>Stock</span></div>
          {"".join(f'<div class="abs trow" id="Br{i}" style="left:44px;top:{400 + i * 112}px;width:852px"><span>{a}</span><span class="tag">{b}</span><b>{c}</b></div>' for i, (a, b, c) in enumerate(rows))}
        </div>
        {"".join(f'<div class="abs vchip" id="Bv{i}" style="left:{70 + i * 250}px;top:1370px">{t}</div>' for i, t in enumerate(["Por tienda", "Por almacén", "Por talla", "Por color"]))}
      </div>'''

# C · transfers + restock alert
steps = ["Preparado", "En camino", "Recibido"]
C = f'''      <div class="sc" id="sC" style="background:{CREAM}">
        {head("C", "TRASLADOS ENTRE SEDES", "Mueve mercadería y síguela hasta que llega", size=86)}
        <div class="abs card" id="Ccard" style="left:70px;top:610px;width:940px;height:520px">
          <div class="abs eyebrow" style="left:44px;top:44px">TRASLADO #0142</div>
          <div class="abs route" style="left:44px;top:100px">Almacén central {icon("arrow-right", 44, TERRAD)} Miraflores</div>
          <div class="abs track" style="left:84px;top:290px;width:772px"><div id="Cfill"></div></div>
          <div class="abs truck" id="Ctruck" style="left:40px;top:208px">{icon("truck", 70, INK, 1.8)}</div>
          {"".join(f'<div class="abs step" id="Cs{i}" style="left:{44 + i * 386}px;top:270px"><div class="dot" id="Cd{i}">{icon("check", 30, WHITE, 3)}</div><span>{t}</span></div>' for i, t in enumerate(steps))}
          <div class="abs items" style="left:44px;top:430px">27 unidades · Vestido Emilia · Blazer Siena · Pantalón Nara</div>
        </div>
        <div class="abs callout" id="Calert" style="left:70px;top:1170px;width:940px">
          <div class="ich">{icon("bell-ring", 48, TERRAD)}</div>
          <div><b>Reponer pronto</b><span>Blazer Siena · Talla S · quedan 3</span></div>
        </div>
      </div>'''

# D · mobile app
bars = [42, 58, 50, 66, 74, 100, 62]
D = f'''      <div class="sc" id="sD" style="background:{LIGHT}">
        {head("D", "APP MÓVIL", "Tu tienda en el bolsillo")}
        <div class="abs phone" id="Dph" style="left:240px;top:520px">
          <div class="abs hi" style="left:44px;top:60px">Buenos días, Ana</div>
          <div class="abs eyebrow" style="left:44px;top:130px">VENTAS DE HOY</div>
          <div class="abs big" style="left:44px;top:170px">S/ <span id="Dsales">4,820</span></div>
          <div class="abs up" id="Dup" style="left:44px;top:292px">{icon("trending-up", 34, OK)} 18% vs. ayer</div>
          {"".join(f'<div class="abs bar" id="Db{i}" style="left:{52 + i * 70}px;top:{560 - h * 2.2:.0f}px;height:{h * 2.2:.0f}px{";background:" + TERRAD if i == 5 else ""}"></div><div class="abs dl" style="left:{52 + i * 70}px;top:575px">{"LMMJVSD"[i]}</div>' for i, h in enumerate(bars))}
          <div class="abs low" id="Dlow" style="left:28px;top:650px">
            <div class="eyebrow" style="margin-bottom:14px">PRODUCTOS CON MENOS STOCK</div>
            <div class="lr" id="Dl0"><span>Blazer Siena</span><b>Quedan 3</b></div>
            <div class="lr" id="Dl1"><span>Vestido Mía</span><b>Quedan 3</b></div>
          </div>
        </div>
      </div>'''

# E · invoicing
E = f'''      <div class="sc" id="sE" style="background:{CREAM}">
        {head("E", "FACTURACIÓN Y CAJA", "Vendes, cobras y facturas en un solo flujo", size=86)}
        <div class="abs card" id="Ecard" style="left:70px;top:610px;width:600px;height:690px">
          <div class="abs eyebrow" style="left:40px;top:40px">FACTURA ELECTRÓNICA</div>
          <div class="abs inv" style="left:40px;top:80px">F001-00004218</div>
          <div class="abs il" style="left:40px;top:180px;width:520px"><span>1 × Vestido Emilia · M</span><b>S/ 189.00</b></div>
          <div class="abs il" style="left:40px;top:250px;width:520px"><span>1 × Blazer Siena · S</span><b>S/ 200.00</b></div>
          <div class="abs il sm" style="left:40px;top:350px;width:520px"><span>Subtotal</span><b>S/ 329.66</b></div>
          <div class="abs il sm" style="left:40px;top:400px;width:520px"><span>IGV 18%</span><b>S/ 59.34</b></div>
          <div class="abs il tot" style="left:40px;top:470px;width:520px"><span>Total</span><b>S/ 389.00</b></div>
          <div class="abs stamp" id="Estamp" style="left:40px;top:590px">{icon("circle-check", 34, OK)} Aceptado por SUNAT</div>
        </div>
        {"".join(f'<div class="abs upd" id="Eu{i}" style="left:700px;top:{690 + i * 200}px"><div class="ich">{icon(ic, 46, TERRAD)}</div><span>{t}</span><div class="tick" id="Et{i}">{icon("check", 26, WHITE, 3)}</div></div>' for i, (ic, t) in enumerate([("wallet", "Caja"), ("package", "Stock"), ("receipt", "Comprobante")]))}
      </div>'''

# F · WhatsApp AI seller (dark contrast section)
F = f'''      <div class="sc" id="sF" style="background:{INK}">
        {head("F", "VENDEDOR IA · WHATSAPP", "No es un chatbot. Es tu vendedor.", True, size=90)}
        <div class="abs chat" id="Fchat" style="left:70px;top:590px;width:940px;height:780px">
          <div class="abs chd"><span class="wa">{logo("whatsapp", 40, WHITE)}</span><div><b>Tienda Demo</b><i>en línea</i></div></div>
          <div class="abs bub in" id="Fm0" style="top:150px">¿Tienes el Jean Araña en talla 30?</div>
          <div class="abs bub out" id="Fm1" style="top:270px">Sí, quedan 4 en talla 30 <span class="mono">Tallas 28 · 30 · 32</span></div>
          <div class="abs bub out ph" id="Fm2" style="top:430px"><div class="thumb">{icon("shirt", 64, TERRAD, 1.6)}</div><div><b>Jean Araña</b><span>S/ 129.00 · 3 fotos</span></div></div>
          <div class="abs bub in" id="Fm3" style="top:590px">Listo, ya te yapeé</div>
          <div class="abs paid" id="Fpay" style="top:676px">{icon("circle-check", 34, OK)} Pago validado · Yape</div>
        </div>
      </div>'''

# G · AI Studio + Claude
G = f'''      <div class="sc" id="sG" style="background:{INK}">
        {head("G", "AI STUDIO + CLAUDE", "De la foto del celular a la foto de catálogo", True, size=84)}
        <div class="abs frame" id="Gfr" style="left:70px;top:590px;width:940px;height:560px">
          <div class="abs before"><div class="abs" style="left:300px;top:70px;transform:rotate(-8deg)">{BLAZER.format(w=300, h=360, c="#2a2622", l="#4a433c")}</div>
            <div class="abs lab" style="left:24px;top:490px">Foto del celular</div></div>
          <div class="abs after" id="Gaf"><div class="abs" style="left:320px;top:80px">{BLAZER.format(w=300, h=360, c="#141414", l="#3d3d3d")}</div>
            <div class="abs lab lt" style="right:24px;top:490px">Lista para vender</div></div>
          <div class="abs handle" id="Ghd"><div class="knob">{icon("wand-sparkles", 36, INK)}</div></div>
        </div>
        <div class="abs ask" id="Gq" style="left:70px;top:1190px">¿Qué debo reponer?</div>
        <div class="abs ans" id="Ga" style="left:70px;top:1290px;width:940px"><span class="cl">{logo("claude", 40, TERRA)}</span>Blazer Siena y Vestido Mía: quedan 3 de cada uno.</div>
        <div class="abs illu" style="left:70px;top:1440px">Recreación ilustrativa · Claude es una marca de Anthropic</div>
      </div>'''

# H · pricing
H = f'''      <div class="sc" id="sH" style="background:{LIGHT}">
        {head("H", "YA VENDEN CON ENCATALOGO", "Marcas peruanas que ya lo usan")}
        {"".join(f'<div class="abs card brandrow" id="Hb{i}" style="left:70px;top:{560 + i * 150}px;width:940px;height:128px"><div class="ich">{icon("store", 46, TERRAD)}</div><span>{t}</span></div>' for i, t in enumerate(["Muñeca de Trapo", "Grupo Paris Import", "Bullking"]))}
        <div class="abs card" id="Hst" style="left:70px;top:1050px;width:940px;height:250px">
          {"".join(f'<div class="abs stat sm" style="left:{44 + i * 300}px;top:46px"><b>+<span id="Hn{i}">{v}</span>{u}</b><span>{t}</span></div>' for i, (v, u, t) in enumerate([("20", " mil", "clientes gestionados"), ("117", " mil", "mensajes de WhatsApp"), ("2.700", "", "chats atendidos por IA")]))}
        </div>
      </div>'''

# I · close
I = f'''      <div class="sc" id="sI" style="background:{CREAM}">
        <div class="abs" id="Ilg" style="left:390px;top:300px">{MARK(300)}</div>
        <div class="abs wm" id="Iwm" style="left:0;top:650px;width:1080px">EnCatalogo.pe</div>
        <div class="abs tag1" id="It1" style="left:0;top:770px;width:1080px">Tu mercadería en orden.</div>
        <div class="abs tag2" id="It2" style="left:0;top:880px;width:1080px">Tu negocio bajo control.</div>
        <div class="abs cta" id="Icta" style="left:240px;top:1060px;width:600px">Probar 7 días gratis</div>
        <div class="abs ctas" id="Isub" style="left:0;top:1190px;width:1080px">Sin tarjeta · encatalogo.pe</div>
      </div>'''

# ---------------------------------------------------------------- timeline
J = []
def js(s): J.append("      " + s)
def show(sel, t, d=0.45, y=30): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y} }}, {{ autoAlpha: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.3f});')
def popin(sel, t, d=0.4, snd=True):
    js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: {d}, ease: "back.out(1.8)" }}, {t:.3f});')
    if snd: ev("pop", t)
def slide(sel, t, x=-80, snd=True):
    js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, x: {x} }}, {{ autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {t:.3f});')
    if snd: ev("pop", t)
def tap(sel, t): js(f'tl.to("{sel}", {{ scale: 0.93, duration: 0.09, yoyo: true, repeat: 1 }}, {t:.3f});'); ev("click", t)
def wipe(sel, prev, t):
    js(f'tl.set("{sel}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{sel}", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.inOut" }}, {t:.3f});')
    js(f'tl.set("{prev}", {{ autoAlpha: 0 }}, {t + 0.65:.3f});')
def count(sel, t, frm, to, d=1.0, fmt="comma"):
    js(f'(() => {{ const o = {{ v: {frm} }}; tl.to(o, {{ v: {to}, duration: {d}, ease: "power2.out", onUpdate: () => {{ document.querySelector("{sel}").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {t:.3f}); }})();')
def heading(sid, t): show(f"#{sid}k", t + 0.2, 0.4, 20); show(f"#{sid}t", t + 0.35, 0.5, 40)

# A
js('gsap.set(["#Aq", ".qq"], { autoAlpha: 0 });')
show("#Abr", 0.1, 0.4, 20); show("#Ak", 0.25, 0.4, 20); show("#At", 0.4, 0.55, 40)
show("#Acard", W("e1", "producto", -0.2), 0.5, 60)
popin("#Aq", W("e1", "vendido", 0.1), 0.45)
js(f'tl.to("#Aq", {{ rotation: 12, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {W("e1", "vendido", 0.6):.3f});')
for i in range(3): slide(f"#As{i}", W("e1", "qué", -0.2 + i * 0.12), 0, i == 0)
js(f'tl.fromTo(".qq", {{ autoAlpha: 0, scale: 0.4 }}, {{ autoAlpha: 1, scale: 1, duration: 0.3, stagger: 0.1, ease: "back.out(2)" }}, {W("e1", "tienda"):.3f});')
# B
wipe("#sB", "#sA", S[1]); heading("B", S[1])
show("#Bcard", W("e2", "ves", -0.2), 0.5, 60)
for i, (a, b) in enumerate([(0, 1248), (0, 12), (0, 3)]): count(f"#Bn{i}", W("e2", "ves", 0.2), a, b, 1.2)
for i, w_ in enumerate(["stock", "tienda", "almacén"]): slide(f"#Br{i}", W("e2", w_, -0.1), 80)
for i, w_ in enumerate(["tienda", "almacén", "talla", "color"]): popin(f"#Bv{i}", W("e2", w_, 0.05), 0.35, i > 1)
js(f'tl.to("#Bcard", {{ scale: 1.02, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {W("e2", "sola"):.3f});')
# C
wipe("#sC", "#sB", S[2]); heading("C", S[2])
js('gsap.set(["#Calert", "#Cd1", "#Cd2"], { autoAlpha: 0 });')
show("#Ccard", W("e3", "mueves", 0.1), 0.5, 60)
ts = W("e3", "sigues", -0.2); te = W("e3", "llega", 0.2)
js(f'tl.fromTo("#Cfill", {{ scaleX: 0 }}, {{ scaleX: 1, transformOrigin: "0% 50%", duration: {te - ts:.2f}, ease: "power1.inOut" }}, {ts:.3f});')
js(f'tl.fromTo("#Ctruck", {{ x: 0 }}, {{ x: 772, duration: {te - ts:.2f}, ease: "power1.inOut" }}, {ts:.3f});')
popin("#Cd1", ts + (te - ts) * 0.5, 0.3); popin("#Cd2", te, 0.35); ev("chime2", te)
slide("#Calert", W("e3", "avisa", -0.1), 0)
js(f'tl.to("#Calert .ich", {{ rotation: 14, duration: 0.1, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {W("e3", "avisa", 0.3):.3f});')
# D
wipe("#sD", "#sC", S[3]); heading("D", S[3])
show("#Dph", W("e4", "celular", -0.4), 0.6, 120)
count("#Dsales", W("e4", "ventas", -0.2), 0, 4820, 1.1)
js(f'tl.fromTo("#sD .bar", {{ scaleY: 0 }}, {{ scaleY: 1, transformOrigin: "50% 100%", duration: 0.5, stagger: 0.06, ease: "power2.out" }}, {W("e4", "ventas"):.3f});')
show("#Dup", W("e4", "día"), 0.35, 15)
show("#Dlow", W("e4", "productos", -0.2), 0.45, 40)
js(f'tl.fromTo(["#Dl0 b", "#Dl1 b"], {{ color: "{INK}" }}, {{ color: "{TERRAD}", duration: 0.3 }}, {W("e4", "agotando"):.3f});'); ev("pop", W("e4", "agotando"))
# E
wipe("#sE", "#sD", S[4]); heading("E", S[4])
js('gsap.set(["#Estamp", ".tick"], { autoAlpha: 0 });')
show("#Ecard", W("e5", "vendes", 0.1), 0.5, 60)
popin("#Estamp", W("e5", "facturas", 0.2), 0.45); ev("chime", W("e5", "facturas", 0.2))
for i, w_ in enumerate(["caja", "stock", "comprobante"]):
    slide(f"#Eu{i}", W("e5", w_, -0.35), 80, False); popin(f"#Et{i}", W("e5", w_, 0.05), 0.3)
# F
wipe("#sF", "#sE", S[5]); heading("F", S[5])
show("#Fchat", W("e6", "whatsapp", -0.1), 0.5, 60)
for sel, w_ in [("#Fm0", "vendedor"), ("#Fm1", "responde"), ("#Fm2", "fotos"), ("#Fm3", "valida")]: popin(sel, W("e6", w_, -0.1), 0.35)
js(f'tl.to("#Fm1 .mono", {{ color: "{TERRA}", duration: 0.25 }}, {W("e6", "tallas"):.3f});')
popin("#Fpay", W("e6", "yape", -0.1), 0.4); ev("chime2", W("e6", "yape", -0.1))
# G
wipe("#sG", "#sF", S[6]); heading("G", S[6])
show("#Gfr", W("e7", "foto", -0.3), 0.5, 60)
tw0, tw1 = W("e7", "vuelve", -0.2), W("e7", "catálogo", 0.3)
js(f'tl.fromTo("#Gaf", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: {tw1 - tw0:.2f}, ease: "power2.inOut" }}, {tw0:.3f});')
js(f'tl.fromTo("#Ghd", {{ x: 940 }}, {{ x: 0, duration: {tw1 - tw0:.2f}, ease: "power2.inOut" }}, {tw0:.3f});'); ev("chime", tw1)
js(f'tl.to("#Ghd", {{ autoAlpha: 0, duration: 0.3 }}, {tw1 + 0.2:.3f});')
popin("#Gq", W("e7", "claude", -0.1), 0.35); show("#Ga", W("e7", "reponer", 0.1), 0.45, 30); ev("pop", W("e7", "reponer", 0.1))
# H
wipe("#sH", "#sG", S[7]); heading("H", S[7])
for i, w_ in enumerate(["muñeca", "grupo", "bullking"]): slide(f"#Hb{i}", W("e8", w_, -0.15), 80)
show("#Hst", W("e8", "bullking", 0.5), 0.45, 40)
count("#Hn0", W("e8", "bullking", 0.6), 0, 20, 0.8); count("#Hn1", W("e8", "bullking", 0.6), 0, 117, 0.8)
# I
wipe("#sI", "#sH", S[8])
popin("#Ilg", S[8] + 0.35, 0.6); show("#Iwm", W("e9", "encatalogo", 0.2), 0.45, 20)
show("#It1", W("e9", "tu", -0.1), 0.5, 30); show("#It2", W("e9", "tu", -0.1, 2), 0.5, 30)
popin("#Icta", W("e9", "prueba", -0.15), 0.5); ev("chime", W("e9", "prueba", -0.15))
show("#Isub", W("e9", "sin", -0.1), 0.4, 15)
js(f'tl.to("#Icta", {{ scale: 1.05, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {W("e9", "sin", 0.6):.3f});')
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>EnCatalogo.pe — promo</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1080" data-height="1920">
{A}
{B}
{C}
{D}
{E}
{F}
{G}
{H}
{I}
{CAPS}
{"".join(f'      <audio id="v_{s["id"]}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for s in segs)}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.8"></audio>
      <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.45"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const capShow = (sel, a, b) => {{
        tl.fromTo(sel, {{ autoAlpha: 0, y: 12, scale: 0.96 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.15, ease: "back.out(2)" }}, a - 0.04);
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
print("captions", len(caps), "events", len(EV))
