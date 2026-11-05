# Flyer ScalyAI — taller "Agentes de IA para ecommerce" (viernes 6 nov 2026, 6:30 p.m.)
# Uso: python3 build.py && node render.js
# Foto del ponente: guardar como assets/ponente.jpg (cuadrada) y volver a correr; si no existe, queda el espacio reservado.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
NAVY, CYAN, TEAL, WHITE, MUTED = "#041B3D", "#47D4D4", "#007B83", "#FFFFFF", "#9FB4D1"

def icon(name, size, color, sw=2):
    src = open(os.path.join(A, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')

foto = os.path.exists(os.path.join(A, "ponente.jpg"))
photo = ('<img src="assets/ponente.jpg" alt="Jaime Fernández Chávez">' if foto else
         f'<div class="ph">{icon("user", 92, "#5E7699", 1.5)}<span>FOTO</span></div>')

temas = [("bot", "Qué es un agente de IA", "y en qué se diferencia de un chatbot"),
         ("message-circle", "Atención y ventas por WhatsApp", "respuestas, catálogo y seguimiento 24/7"),
         ("rocket", "Cómo empezar en tu tienda", "pasos y herramientas para implementarlo")]

html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Taller agentes IA ecommerce</title>
<style>
  @font-face {{ font-family: "Manrope"; font-weight: 500; src: url("assets/Manrope-500-latin.woff2") format("woff2"); }}
  @font-face {{ font-family: "Manrope"; font-weight: 700; src: url("assets/Manrope-700-latin.woff2") format("woff2"); }}
  @font-face {{ font-family: "Manrope"; font-weight: 800; src: url("assets/Manrope-800-latin.woff2") format("woff2"); }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  @page {{ size: 1080px 1350px; margin: 0; }}
  body {{ width:1080px; height:1350px; font-family:"Manrope", system-ui, sans-serif; color:{WHITE}; background:{NAVY}; }}
  .fl {{ position:relative; width:1080px; height:1350px; overflow:hidden; background:{NAVY}; padding:72px 76px; }}
  .glow {{ position:absolute; right:-220px; top:-200px; width:720px; height:720px; border-radius:50%; background:radial-gradient(circle, rgba(71,212,212,.22), rgba(71,212,212,0) 65%); }}
  .glow2 {{ position:absolute; left:-260px; bottom:-280px; width:700px; height:700px; border-radius:50%; background:radial-gradient(circle, rgba(0,123,131,.35), rgba(0,123,131,0) 65%); }}
  .row {{ position:relative; display:flex; align-items:center; justify-content:space-between; }}
  .brand {{ display:flex; align-items:center; gap:18px; font-size:44px; font-weight:800; letter-spacing:-.02em; }}
  .mark {{ display:flex; flex-direction:column; gap:7px; }}
  .mark i {{ display:block; height:11px; border-radius:6px; }}
  .badge {{ padding:14px 26px; border-radius:999px; border:2px solid {CYAN}; color:{CYAN}; font-size:22px; font-weight:800; letter-spacing:.14em; }}
  .kick {{ position:relative; margin-top:64px; font-size:26px; font-weight:800; letter-spacing:.16em; color:{CYAN}; }}
  h1 {{ position:relative; margin-top:16px; font-size:104px; font-weight:800; line-height:.98; letter-spacing:-.035em; }}
  h1 span {{ color:{CYAN}; }}
  .when {{ position:relative; display:flex; gap:16px; margin-top:40px; }}
  .chip {{ display:flex; align-items:center; gap:14px; padding:20px 28px; border-radius:22px; background:rgba(255,255,255,.07); border:2px solid rgba(159,180,209,.25); font-size:32px; font-weight:800; }}
  .chip small {{ display:block; font-size:20px; font-weight:700; color:{MUTED}; letter-spacing:.06em; }}
  .temas {{ position:relative; margin-top:40px; display:flex; flex-direction:column; gap:14px; width:560px; }}
  .t {{ display:flex; gap:20px; align-items:center; }}
  .ic {{ flex:none; width:70px; height:70px; border-radius:20px; background:rgba(71,212,212,.14); display:flex; align-items:center; justify-content:center; }}
  .t b {{ display:block; font-size:28px; font-weight:800; line-height:1.15; }}
  .t span {{ display:block; font-size:21px; font-weight:500; color:{MUTED}; margin-top:3px; }}
  .sp {{ position:absolute; right:76px; top:650px; width:340px; display:flex; flex-direction:column; align-items:center; text-align:center; }}
  .frame {{ width:280px; height:280px; border-radius:50%; padding:8px; background:conic-gradient({CYAN}, {TEAL}, {CYAN}); }}
  .frame img, .ph {{ width:100%; height:100%; border-radius:50%; object-fit:cover; display:block; background:#0B2A55; }}
  .ph {{ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; border:3px dashed #2A4A78; }}
  .ph span {{ font-size:18px; font-weight:800; letter-spacing:.2em; color:#5E7699; }}
  .sp .lbl {{ margin-top:22px; font-size:20px; font-weight:800; letter-spacing:.18em; color:{CYAN}; }}
  .sp .nm {{ margin-top:8px; font-size:34px; font-weight:800; line-height:1.15; }}
  .cta {{ position:absolute; left:76px; right:76px; bottom:64px; display:flex; align-items:center; justify-content:space-between; padding-top:30px; border-top:2px solid rgba(159,180,209,.2); }}
  .cta p {{ font-size:24px; font-weight:600; color:{MUTED}; }}
  .cta p b {{ color:{WHITE}; }}
  .btn {{ padding:24px 44px; border-radius:999px; background:{CYAN}; color:{NAVY}; font-size:32px; font-weight:800; }}
</style></head><body>
<div class="fl">
  <div class="glow"></div><div class="glow2"></div>
  <div class="row">
    <div class="brand"><div class="mark"><i style="width:84px;background:linear-gradient(90deg,{TEAL},{CYAN})"></i><i style="width:104px;background:{TEAL}"></i><i style="width:84px;background:{CYAN}"></i></div>ScalyAI</div>
    <div class="badge">TALLER EN VIVO</div>
  </div>
  <div class="kick">ECOMMERCE · INTELIGENCIA ARTIFICIAL</div>
  <h1>Agentes de IA<br>para <span>ecommerce</span></h1>
  <div class="when">
    <div class="chip">{icon("calendar", 40, CYAN)}<div><small>VIERNES</small>6 de noviembre</div></div>
    <div class="chip">{icon("clock", 40, CYAN)}<div><small>HORA PERÚ</small>6:30 p.m.</div></div>
  </div>
  <div class="temas">
    {"".join(f'<div class="t"><div class="ic">{icon(ic, 36, CYAN)}</div><div><b>{a}</b><span>{b}</span></div></div>' for ic, a, b in temas)}
  </div>
  <div class="sp">
    <div class="frame">{photo}</div>
    <div class="lbl">PONENTE</div>
    <div class="nm">Jaime Fernández<br>Chávez</div>
  </div>
  <div class="cta">
    <p>Aprende a vender más con <b>agentes de IA</b></p>
    <div class="btn">Reserva tu cupo</div>
  </div>
</div>
</body></html>
'''
open(os.path.join(HERE, "flyer.html"), "w").write(html)
print("ok", "con foto" if foto else "sin foto (espacio reservado)")
