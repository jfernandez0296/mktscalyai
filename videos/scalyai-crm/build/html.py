# Motor de videos verticales (1080×1920) de Scaly AI: lee build/spec.py y arma index.html.
# Escenas: hook → pasos (cada uno con módulos gráficos) → cta. Una locución por escena (audio/segmentos.json).
import sys, os
os.environ["FMT"] = "v"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import spec

M = 70
L = lambda parts: "".join(f'<span class="l">{p}</span>' for p in parts)
F = lambda seg, f: SEG[seg]["start"] + f * SEG[seg]["dur"]
ST = {"free": ("#FFFFFF", NAVY, CREAM3), "occ": (TEAL, WHITE, TEAL), "clean": ("#B5651D", WHITE, "#B5651D"), "block": ("#1F4FBF", WHITE, "#1F4FBF"),
      "low": ("#C2416B", WHITE, "#C2416B"), "ok": ("#1D6F42", WHITE, "#1D6F42")}
ACC = {"": ("#0D2F5C", "#007B83", "#7FE3E3"), "c-xls": ("#14532F", "#1D6F42", "#BDEFD0"), "c-crm": ("#163A8C", "#1F4FBF", "#CFE0FF"),
       "c-erp": ("#8A4A12", "#B5651D", "#FFE0BD"), "wa": ("#0B5E32", "#128C4A", "#C9F2D8")}
def acc(sc): return ACC["wa" if sc.get("icon") == "wa" else sc.get("cls", "")]
CUR = {"acc": TEAL, "w": 872}
Y0, Y1, ZMAX = 690, 1420, 1.36   # zona útil de los módulos y ampliación máxima
def big_icon(ic, size): return wa(size, WHITE) if ic == "wa" else icon(ic, size, WHITE, 1.1)

def tile(ic, size, cls=""): return gt("wa" if ic == "wa" else ic, size, cls=cls)

# ---------------------------------------------------------------- módulos (devuelven html, alto)
def tagw(t): return 0 if not t else 44 + 30 + int(len(t) * 14.5)
def m_rows(pid, m):
    rows = []; rsw = max([max(tagw(r.get("t0")), tagw(r.get("t1"))) for r in m["rows"]] + [120])
    txt = max(max(len(r["text"]) * 15.5, len(r.get("sub", "")) * 10.5) for r in m["rows"])
    m["_need"] = 84 + 44 + txt + rsw + 24
    for i, r in enumerate(m["rows"]):
        tags = f'<span class="tag soft" id="{pid}a{i}">{r["t0"]}</span>' if r.get("t0") else ""
        if r.get("t1"): tags += f'<span class="tag teal" id="{pid}b{i}">{icon("check", 20, "#00646B", 3)}{r["t1"]}</span>'
        left = person(r["person"], 84) if "person" in r else tile(r["icon"], 84, r.get("cls", ""))
        rows.append(f'<div class="rw" id="{pid}r{i}">{left}<div class="rt"><b>{r["text"]}</b>{f"<span>{r[chr(115)+chr(117)+chr(98)]}</span>" if r.get("sub") else ""}</div><div class="rs" style="width:{rsw}px">{tags}</div></div>')
    head = f'<div class="flab t">{m["title"]}</div>' if m.get("title") else ""
    return head + "".join(rows), 56 + len(m["rows"]) * 112 + (44 if m.get("title") else 0)
def a_rows(pid, m, seg):
    n = len(m["rows"]); a, b = m.get("span", (0.05, 0.95)); mid = a + (b - a) * 0.5
    js(f'gsap.set("#{pid} .tag.teal", {{ autoAlpha: 0 }});')
    for i in range(n):
        t = F(seg, a + (mid - a) * i / max(1, n)); show(f"#{pid}r{i}", t, 0.45, 16)
        if i % 2 == 0: ev("tick", t)
        if m["rows"][i].get("t1"):
            t2 = F(seg, mid + (b - mid) * i / max(1, n))
            if m["rows"][i].get("t0"): js(f'tl.to("#{pid}a{i}", {{ autoAlpha: 0, duration: 0.2 }}, {t2:.3f});')
            show(f"#{pid}b{i}", t2 + 0.1, 0.35, 0); ev("tick", t2)
            js(f'tl.fromTo("#{pid}r{i}", {{ backgroundColor: "rgba(71,212,212,.30)" }}, {{ backgroundColor: "rgba(71,212,212,0)", duration: 0.8, ease: "power1.out" }}, {t2:.3f});')
    ev("chime2", F(seg, b))

def m_flow(pid, m):
    ts = m["tiles"]; n = len(ts); S_ = 150; inner = CUR["w"]
    xs = [int(S_ / 2 + i * (inner - S_) / (n - 1)) for i in range(n)]
    out = [f'<div class="abs ftrack" id="{pid}tr" style="{pos(xs[0], 109, xs[-1] - xs[0], 10)}"></div>']
    for i, t in enumerate(ts):
        out.append(f'<div class="abs" id="{pid}t{i}" style="{pos(xs[i] - S_ // 2, 40)}">{tile(t["icon"], S_, t.get("cls", ""))}</div>'
                   f'<div class="abs flabel" id="{pid}l{i}" style="{pos(xs[i] - 130, 206, 260)}">{t["label"]}</div>')
    out.append(f'<div class="abs chipn" id="{pid}chip" style="{pos(xs[0] - 85, 86)}">{m["chip"]}</div>')
    m["_dx"] = xs[-1] - xs[0]
    return f'<div class="rel" style="height:250px">{"".join(out)}</div>', 330
def a_flow(pid, m, seg):
    n = len(m["tiles"]); a, b = m.get("span", (0.05, 0.9))
    js(f'gsap.set("#{pid}chip", {{ autoAlpha: 0 }});')
    for i in range(n):
        t = F(seg, a + (b - a) * 0.35 * i / n); show(f"#{pid}t{i}", t, 0.45, 16); show(f"#{pid}l{i}", t + 0.1, 0.4, 8); ev("tick", t)
    t0 = F(seg, a + (b - a) * 0.4); d = max(0.8, (b - a) * 0.5 * SEG[seg]["dur"])
    js(f'tl.fromTo("#{pid}tr", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: {d:.2f}, ease: "power2.inOut" }}, {t0:.3f});')
    js(f'tl.set("#{pid}chip", {{ autoAlpha: 1 }}, {t0:.3f});')
    js(f'tl.fromTo("#{pid}chip", {{ x: 0 }}, {{ x: {m["_dx"]}, duration: {d:.2f}, ease: "power2.inOut" }}, {t0:.3f});'); ev("chime2", t0 + d)
    js(f'tl.to("#{pid}chip", {{ autoAlpha: 0, duration: 0.3 }}, {t0 + d - 0.25:.3f});')

def m_grid(pid, m):
    cols = m["cols"]; cw = (CUR["w"] - 8 - (cols - 1) * 12) // cols
    cells = "".join(f'<div class="gc" id="{pid}c{i}" style="width:{cw}px;background:{ST[s][0]};color:{ST[s][1]};border-color:{ST[s][2]}">{lab}</div>' for i, (lab, s) in enumerate(m["cells"]))
    leg = "".join(f'<span><i style="background:{ST[k][0]};border-color:{ST[k][2]}"></i>{v}</span>' for k, v in m["legend"])
    rows = -(-len(m["cells"]) // cols)
    return f'<div class="flab t">{m["title"]}</div><div class="gg">{cells}</div><div class="leg">{leg}</div>', 56 + 44 + rows * 96 + 60
def a_grid(pid, m, seg):
    js(f'tl.fromTo("#{pid} .gc", {{ autoAlpha: 0, y: 10 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.03, ease: {EASE} }}, {F(seg, 0.02):.3f});')
    for i, s, f in m["changes"]:
        t = F(seg, f)
        js(f'tl.to("#{pid}c{i}", {{ backgroundColor: "{ST[s][0]}", color: "{ST[s][1]}", borderColor: "{ST[s][2]}", duration: 0.35 }}, {t:.3f});'); ev("tick", t)

def m_chat(pid, m):
    h = (f'<div class="ah">{person(m["person"], 72)}<b>{m["name"]}</b><i>{m["time"]}</i></div>'
         f'<div class="cb in" id="{pid}i">{m["msg"]}</div><div class="cb out" id="{pid}o"><em>{bars(26, pid + "lg", True)}Asistente IA</em>{m["reply"]}</div>'
         f'<div class="rc" id="{pid}k">{icon("circle-check", 34, TEAL, 2.2)}{m["done"]}</div>')
    return h, 570
def a_chat(pid, m, seg):
    js(f'gsap.set(["#{pid}i", "#{pid}o", "#{pid}k"], {{ autoAlpha: 0 }});')
    show(f"#{pid}i", F(seg, 0.08), 0.45, 16); ev("ping", F(seg, 0.08))
    show(f"#{pid}o", F(seg, 0.55), 0.45, 16); ev("tick", F(seg, 0.55))
    show(f"#{pid}k", F(seg, 0.85), 0.45, 12); ev("chime", F(seg, 0.85))

def m_pipe(pid, m):
    cols = m["cols"]; n = len(cols); cw = (CUR["w"] - (n - 1) * 14) // n
    out = []
    for i, (name, col) in enumerate(cols):
        ghosts = "".join('<div class="pg"></div>' for _ in range(m.get("ghost", [2, 2, 1, 1])[i]))
        out.append(f'<div class="pc" style="width:{cw}px"><div class="ph" style="background:{col}">{name}</div><div class="pslot"></div>{ghosts}</div>')
    m["_need"] = 730
    card = f'<div class="abs pcard" id="{pid}card" style="{pos(8, 66, cw - 16)}">{person(m["person"], 44)}<div><b>{m["deal"]}</b><span>{m["amount"]}</span></div></div>'
    m["_step"] = cw + 14
    return f'<div class="flab t">{m["title"]}</div><div class="rel pp-wrap"><div class="pcols">{"".join(out)}</div>{card}</div>', 56 + 44 + 330
def a_pipe(pid, m, seg):
    n = len(m["cols"]); show(f"#{pid}card", F(seg, 0.05), 0.4, 12)
    for k in range(1, n):
        t = F(seg, m["at"][k - 1])
        js(f'tl.to("#{pid}card", {{ x: {k * m["_step"]}, duration: 0.55, ease: "power2.inOut" }}, {t:.3f});'); ev("tick", t)
    te = F(seg, m["at"][-1]) + 0.55
    js(f'tl.to("#{pid}card", {{ backgroundColor: "#1D6F42", duration: 0.3 }}, {te:.3f});'); ev("chime", te)

def m_kpis(pid, m):
    r = m["ring"]
    stats = "".join(f'<div class="ks"><b>{s.get("pre", "")}<em id="{pid}n{i}">0</em>{s.get("suf", "")}</b><span>{s["label"]}</span></div>' for i, s in enumerate(m["stats"]))
    return (f'<div class="kwrap"><div class="rel kring">{ring(pid + "rg", 300, 30, r.get("color", CUR["acc"]), CREAM2)}<div class="abs kin" style="{pos(0, 0, 300, 300)}"><b><em id="{pid}p">0</em>%</b><span>{r["label"]}</span></div></div>'
            f'<div class="kstats">{stats}</div></div>'), 384
def a_kpis(pid, m, seg):
    t = F(seg, 0.1); p = m["ring"]["pct"]
    js(f'tl.to("#{pid}rg", {{ strokeDashoffset: {1 - p / 100:.2f}, duration: 1.4, ease: "power2.out" }}, {t:.3f});'); count(f"#{pid}p", t, 0, p, 1.4)
    for i, s in enumerate(m["stats"]): count(f"#{pid}n{i}", t + 0.3 + i * 0.25, 0, s["value"], 1.3)
    ev("tick", t); ev("chime2", t + 1.4)

def m_bars(pid, m):
    mx = max(v for _, v in m["bars"])
    bs = "".join(f'<div class="bcol"><b>{v}{m.get("unit", "")}</b><i id="{pid}b{i}" style="height:{int(140 * v / mx)}px;background:{m.get("colors", {}).get(i, CUR["acc"])}"></i><span>{lab}</span></div>' for i, (lab, v) in enumerate(m["bars"]))
    return f'<div class="flab t">{m["title"]}</div><div class="bch">{bs}</div>', 56 + 44 + 236
def a_bars(pid, m, seg):
    js(f'tl.fromTo("#{pid} .bcol i", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.6, stagger: 0.07, ease: {EASE} }}, {F(seg, m.get("at", 0.45)):.3f});')
    js(f'tl.fromTo("#{pid} .bcol b", {{ autoAlpha: 0, y: 8 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.07, ease: {EASE} }}, {F(seg, m.get("at", 0.45)) + 0.35:.3f});')

def m_prompt(pid, m):
    lines = "".join(f'<div class="pl" id="{pid}l{i}">{t}</div>' for i, t in enumerate(m["lines"]))
    h = (f'<div class="ptop"><span class="pchip">{icon("terminal", 26, CYAN, 2.4)}Tú → Claude</span><i></i><i></i><i></i></div>'
         f'<div class="pbody">{lines}<span class="pcur" id="{pid}cur"></span></div>'
         f'<div class="pans" id="{pid}k">{bars(30, pid + "lg", True)}<b>Claude</b><span>{m["done"]}</span>{icon("circle-check", 34, CYAN, 2.2)}</div>')
    m["_need"] = max(len(re.sub(r"<[^>]+>", "", t)) for t in m["lines"]) * 18.8
    return h, 150 + len(m["lines"]) * 54 + 104
def a_prompt(pid, m, seg):
    n = len(m["lines"]); a, b = m.get("span", (0.04, 0.9))
    js(f'gsap.set(["#{pid} .pl", "#{pid}k"], {{ autoAlpha: 0 }});')
    for i in range(n):
        t = F(seg, a + (b - a) * 0.6 * i / n)
        js(f'tl.fromTo("#{pid}l{i}", {{ autoAlpha: 0, clipPath: "inset(0 100% 0 0)" }}, {{ autoAlpha: 1, clipPath: "inset(0 0% 0 0)", duration: 0.7, ease: "power1.out" }}, {t:.3f});'); ev("tick", t)
    js(f'tl.fromTo("#{pid}cur", {{ autoAlpha: 1 }}, {{ autoAlpha: 0, duration: 0.4, yoyo: true, repeat: 9, ease: "steps(1)" }}, {F(seg, a):.3f});')
    show(f"#{pid}k", F(seg, b), 0.45, 12); ev("chime", F(seg, b))

MODS = {"prompt": (m_prompt, a_prompt), "rows": (m_rows, a_rows), "flow": (m_flow, a_flow), "grid": (m_grid, a_grid), "chat": (m_chat, a_chat), "pipe": (m_pipe, a_pipe), "kpis": (m_kpis, a_kpis), "bars": (m_bars, a_bars)}

# ---------------------------------------------------------------- escenas
LET = "ABCDEFGHIJ"
html_scenes = []
steps = [s for s in spec.SCENES if s["kind"] == "step"]
OPOS = [(200, 840), (880, 870), (230, 1270), (860, 1250)]
for k, sc in enumerate(spec.SCENES):
    sid = LET[k]; seg = sc["seg"]
    if sc["kind"] == "hook":
        a1, a2, tint = acc(sc); cxh, cyh = 540, 1050
        rings = "".join(f'<circle id="{sid}r{j}" cx="{cxh}" cy="{cyh}" r="{r}" fill="none" stroke="{CYAN}" stroke-width="2" opacity="{o}"/>' for j, (r, o) in enumerate([(230, .4), (320, .25), (410, .14)]))
        spokes = "".join(f'<line id="{sid}k{j}" x1="{cxh}" y1="{cyh}" x2="{x}" y2="{y}" stroke="{CYAN}" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 14" opacity=".7"/>' for j, (x, y) in enumerate(OPOS[:len(sc["orbit"])]))
        orb = "".join(f'<div class="abs oi" id="{sid}o{j}" style="{pos(x - 65, y - 65)}">{tile(ic, 130, cls)}<span class="olab">{lab}</span></div>' for j, ((ic, cls, lab), (x, y)) in enumerate(zip(sc["orbit"], OPOS)))
        h = f'''      <div class="sc dark" id="s{sid}"><div class="cam">{BG(100, -200, 1200)}
        <div class="abs blob" style="{pos(-300, 1000, 1000, 1000)};background:radial-gradient(closest-side, {a2}AA, {a2}00)"></div>{deco(300, 1500, 0.8, True)}
        <div class="abs eyebrow" id="{sid}ey" style="{pos(M, 250)}">{sc["eyebrow"]}</div>
        <div class="abs h1 big" id="{sid}t" style="{pos(M - 4, 300)}">{L(sc["title"])}</div>
        <svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{rings}{spokes}</svg>
        {orb}
        <div class="abs" id="{sid}hero" style="{pos(cxh - 150, cyh - 150)}">{tile(sc["icon"], 300, sc.get("cls", ""))}</div>
        <div class="abs note" style="{pos(M, 1452)}">{spec.NOTE}</div>
      </div></div>'''
    elif sc["kind"] == "step":
        a1, a2, tint = acc(sc); CUR["acc"] = a2
        n = steps.index(sc) + 1
        dots = "".join(f'<i class="{"on" if j == n else ("done" if j < n else "")}"></i>' for j in range(1, len(steps) + 1))
        y0 = Y0 + (34 if sc.get("people") else 0); cards = []; GAP = 26
        CUR["w"] = 872; hs = [MODS[m["type"]][0](f"{sid}m{j}", dict(m))[1] for j, m in enumerate(sc["mods"])]
        mm = [dict(m) for m in sc["mods"]]
        for j, m in enumerate(mm): MODS[m["type"]][0](f"{sid}m{j}", m)
        zcap = max(1.0, min([ZMAX] + [940 / (m["_need"] + 68) for m in mm if m.get("_need")]))
        z = max(0.88, min(zcap, (Y1 - y0 - GAP * (len(hs) - 1)) / sum(hs)))
        used = sum(hs) * z + GAP * (len(hs) - 1); y = y0 + max(0, (Y1 - y0 - used) * 0.3)
        CUR["w"] = int(940 / z) - 68
        for j, m in enumerate(sc["mods"]):
            pid = f"{sid}m{j}"; inner, hh = MODS[m["type"]][0](pid, m)
            cards.append(f'<div class="abs card pan" id="{pid}" style="left:{M / z:.1f}px;top:{y / z:.1f}px;width:{940 / z:.1f}px;height:{hh}px;zoom:{z:.3f}">{inner}</div>'); y += hh * z + GAP
        ppl = f'<div class="abs" id="{sid}pp" style="{pos(M, 600)}">{avs(sc["people"], 88)}</div>' if sc.get("people") else ""
        h = f'''      <div class="sc" id="s{sid}" style="--acc:{a2};--emc:{tint}"><div class="cam">{BG(-200, 900, 1100)}{deco(380, 1500, 0.75)}
        <div class="abs band" id="{sid}band" style="background:linear-gradient(135deg, {a1}, {a2})"><div class="abs wmk" id="{sid}wm">{big_icon(sc["icon"], 460)}</div>
          <div class="abs num">{sc.get("num", f"0{n}")}</div></div>
        <div class="abs eyebrow lt" id="{sid}ey" style="{pos(M, 200)}">{sc["eyebrow"]}</div>
        <div class="abs pdots lt" style="left:auto;right:{M}px;top:204px">{dots}</div>
        <div class="abs h1 st lt" id="{sid}t" style="{pos(M - 4, 244)}">{L(sc["title"])}</div>
        <div class="abs lead lt" id="{sid}ld" style="{pos(M, 468, 700)}">{sc["lead"]}</div>{ppl}
        {"".join(cards)}
        <div class="abs note" style="{pos(M, 1452)}">{spec.NOTE}</div>
      </div></div>'''
    else:
        recap = "".join(f'<div class="ri" id="{sid}ri{j}">{tile(st["icon"], 120, st.get("cls", ""))}</div>' for j, st in enumerate(steps))
        h = f'''      <div class="sc dark" id="s{sid}"><div class="cam">{BG(-10, 300, 1100)}{deco(300, 1380, 0.85, True)}{deco(-420, -200, 0.8, True)}
        <div class="abs recap" style="{pos(0, 260, 1080)}">{recap}</div>
        <div class="abs navlogo dk" id="{sid}lg" style="{pos(0, 470, 1080)};justify-content:center">{bars(64, sid + "b", True)}<div>Scaly <span>AI</span></div></div>
        <div class="abs h1 ctr" id="{sid}t" style="{pos(0, 600, 1080)}">{L(sc["title"])}</div>
        <div class="abs" id="{sid}cta" style="{pos(0, 1000, 1080)};display:flex;justify-content:center"><div class="btn" id="{sid}btn">{sc.get("btn", "Conversemos de tu próximo piloto")} {icon("arrow-right", 40, WHITE, 2.4)}</div></div>
        <div class="abs micro" id="{sid}mic" style="{pos(0, 1150, 1080)}">{sc.get("micro", "30 minutos · sin tarjeta · sin compromiso")}</div>
        <div class="abs url" id="{sid}url" style="{pos(0, 1240, 1080)}">SCALYAI.DEV</div>
      </div></div>'''
    html_scenes.append(h)
SCN = "\n".join(html_scenes)

# ---------------------------------------------------------------- línea de tiempo
ENDS = S[1:] + [T]
for k in range(len(spec.SCENES)): cam(LET[k], S[k], ENDS[k] + 1.2)
drift()
TR = [t_bars, t_wipe, t_fade]
for k, sc in enumerate(spec.SCENES):
    sid = LET[k]; seg = sc["seg"]
    if k:
        fn = t_bars if sc["kind"] == "cta" or k == 1 else TR[k % 3]
        fn(f"#s{LET[k - 1]}", f"#s{sid}", S[k] - (0.66 if fn is t_bars else 0.4 if fn is t_wipe else 0.3))
    if sc["kind"] == "hook":
        show(f"#{sid}ey", 0.2, 0.5, 16); show(f"#{sid}t", 0.35, 0.8, 30)
        th = F(seg, 0.25)
        show(f"#{sid}hero", th, 0.7, 30); ev("chime2", th)
        for j in range(3):
            js(f'tl.fromTo("#{sid}r{j}", {{ scale: 0.6, autoAlpha: 0, svgOrigin: "540 1050" }}, {{ scale: 1, autoAlpha: 1, duration: 0.8, ease: {EASE} }}, {th + 0.15 + j * 0.12:.3f});')
        js(f'tl.fromTo("#{sid}hero", {{ y: 0 }}, {{ y: -16, duration: 1.8, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {th + 0.8:.3f});')
        for j in range(len(sc["orbit"])):
            to = F(seg, 0.5) + j * 0.18
            js(f'tl.fromTo("#{sid}k{j}", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.5 }}, {to:.3f});')
            js(f'tl.fromTo("#{sid}o{j}", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: {EASE} }}, {to:.3f});'); ev("tick", to)
            js(f'tl.fromTo("#{sid}o{j}", {{ y: 0 }}, {{ y: {-14 if j % 2 else 14}, duration: {1.6 + j * 0.2:.1f}, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {to + 0.55:.3f});')
    elif sc["kind"] == "step":
        heading(sid, S[k]); show(f"#{sid}ld", S[k] + 0.45, 0.5, 16)
        js(f'tl.fromTo("#{sid}wm", {{ x: 60, rotation: -6 }}, {{ x: -30, rotation: 4, duration: {ENDS[k] - S[k] + 1.2:.2f}, ease: "none" }}, {S[k] - 0.6:.3f});')
        if sc.get("people"): show(f"#{sid}pp", S[k] + 0.6, 0.5, 12)
        for j, m in enumerate(sc["mods"]):
            pid = f"{sid}m{j}"; show(f"#{pid}", S[k] + 0.5 + j * 0.2, 0.6, 24)
            if m["type"] == "rows": js(f'gsap.set("#{pid} .rw", {{ autoAlpha: 0 }});')
            MODS[m["type"]][1](pid, m, m.get("seg", seg))
    else:
        grow(sid + "b", S[k] + 0.1, 0.12, 0.5); show(f"#{sid}lg", S[k] + 0.1, 0.5, 0)
        for j in range(len(steps)): show(f"#{sid}ri{j}", S[k] + 0.3 + j * 0.12, 0.5, 20)
        show(f"#{sid}t", F(seg, 0.0) - 0.2, 0.7, 30)
        tc = W(seg, sc.get("word", "conversemos"), -0.2); show(f"#{sid}cta", tc, 0.6, 24); ev("chime", tc)
        show(f"#{sid}mic", tc + 0.6, 0.5, 16); show(f"#{sid}url", END(seg, 0.2), 0.5, 12)
        js(f'tl.to("#{sid}btn", {{ boxShadow: "0 0 0 14px rgba(71,212,212,.18), 0 16px 40px rgba(0,0,0,.35)", duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {END(seg, 0.4):.3f});')
js(f'tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {T:.2f}, ease: "none" }}, 0);')

render(SCN, spec.TITLE)
