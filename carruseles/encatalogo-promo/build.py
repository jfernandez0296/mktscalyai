# Carrusel de 2 imágenes (1080×1350, 4:5) para Instagram/TikTok — EnCatalogo.pe
# Uso: python3 build.py && node render.js   (genera slide-1.png y slide-2.png)
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, "..", "..", "videos", "encatalogo-promo", "assets", "img")
def icon(name, size, color, sw=2):
    src = open(os.path.join(ICONS, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')
TD, OK = "#A65353", "#3F7A4F"

rows = [("Vestido Emilia", "Miraflores", "24"), ("Blazer Siena", "San Isidro", "7"), ("Pantalón Nara", "Almacén", "86")]
caps = [("package", "Inventario y traslados", "Stock por tienda, almacén y variante. Traslados trazables entre sedes."),
        ("smartphone", "App móvil", "Ventas del día y alertas de stock desde el celular."),
        ("receipt", "Facturación y caja", "Cada venta actualiza caja, stock y comprobante."),
        ("sparkles", "Vendedor IA en WhatsApp", "Responde con stock real y valida pagos por Yape o Plin.")]

html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>EnCatalogo carrusel</title>
<link rel="stylesheet" href="../../brand/encatalogo/tokens.css">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#ccc; font-family: var(--ec-font-sans); color: var(--ec-ink); }}
  .slide {{ position:relative; width:1080px; height:1350px; overflow:hidden; margin-bottom:20px; padding:80px 80px 0; }}
  .s1 {{ background: var(--ec-cream); }}
  .s2 {{ background: var(--ec-light); }}
  .brand {{ display:flex; align-items:center; gap:16px; font-size:36px; font-weight:700; }}
  .brand img {{ height:56px; }}
  .num {{ position:absolute; right:80px; top:84px; font-family: var(--ec-font-display); font-size:40px; color: var(--ec-terracotta); }}
  .badge {{ display:inline-block; margin-top:70px; padding:14px 28px; border-radius:999px; background: var(--ec-terracotta-soft); color: var(--ec-terracotta-dark); font-size:24px; font-weight:700; letter-spacing:.12em; }}
  h1 {{ font-family: var(--ec-font-display); font-weight:400; font-size:104px; line-height:1.02; letter-spacing:-.01em; margin-top:28px; }}
  h1 em {{ color: var(--ec-terracotta-dark); }}
  h2 {{ font-family: var(--ec-font-display); font-weight:400; font-size:76px; line-height:1.05; margin-top:26px; }}
  .lead {{ font-size:34px; line-height:1.4; color: var(--ec-body); margin-top:26px; max-width:860px; }}
  .card {{ background:#fff; border:2px solid var(--ec-border); border-radius:36px; box-shadow: 0 2px 4px rgba(15,15,16,.04), 0 24px 60px rgba(15,15,16,.07); }}
  .inv {{ position:absolute; left:80px; right:80px; top:780px; padding:36px 40px; }}
  .eb {{ font-size:22px; font-weight:700; letter-spacing:.14em; color: var(--ec-terracotta-dark); }}
  .tr {{ display:grid; grid-template-columns:1.4fr 1fr .4fr; align-items:center; height:84px; border-top:2px solid var(--ec-border); font-size:30px; font-weight:600; }}
  .tr:first-of-type {{ margin-top:22px; }}
  .tr span.t {{ justify-self:start; padding:6px 18px; border-radius:999px; background: var(--ec-light); border:2px solid var(--ec-border); font-size:24px; font-weight:500; color: var(--ec-body); }}
  .tr b {{ text-align:right; font-size:36px; }}
  .alert {{ display:flex; align-items:center; gap:14px; margin-top:20px; padding:16px 22px; border-radius:20px; background: var(--ec-terracotta-soft); border-left:8px solid var(--ec-terracotta-dark); font-size:26px; font-weight:600; }}
  .swipe {{ position:absolute; right:80px; bottom:56px; display:flex; align-items:center; gap:12px; font-size:28px; font-weight:600; color: var(--ec-body); }}
  .list {{ margin-top:44px; display:flex; flex-direction:column; gap:20px; }}
  .it {{ display:flex; gap:26px; align-items:center; padding:26px 30px; }}
  .ic {{ flex:none; width:84px; height:84px; border-radius:22px; background: var(--ec-terracotta-soft); display:flex; align-items:center; justify-content:center; }}
  .it b {{ display:block; font-size:34px; font-weight:700; }}
  .it span {{ display:block; font-size:26px; color: var(--ec-body); margin-top:4px; line-height:1.3; }}
  .foot {{ position:absolute; left:80px; right:80px; bottom:70px; display:flex; align-items:center; justify-content:space-between; }}
  .price {{ font-size:28px; color: var(--ec-body); }}
  .price b {{ display:block; font-family: var(--ec-font-display); font-weight:400; font-size:72px; color: var(--ec-ink); line-height:1; }}
  .cta {{ display:flex; flex-direction:column; align-items:center; gap:12px; }}
  .btn {{ padding:28px 48px; border-radius:999px; background: var(--ec-ink); color:#fff; font-size:34px; font-weight:600; }}
  .cta small {{ font-size:24px; color: var(--ec-body); }}
</style></head><body>

<section class="slide s1" id="slide-1">
  <div class="brand"><img src="../../brand/encatalogo/logo/encatalogo-logo.svg" alt="">EnCatalogo.pe</div>
  <div class="num">01 / 02</div>
  <div class="badge">INVENTARIO CONECTADO A TUS VENTAS</div>
  <h1>Tu mercadería en orden. <em>Tu negocio bajo control.</em></h1>
  <p class="lead">Sabes qué tienes, dónde está y qué falta, en cada tienda y almacén.</p>
  <div class="card inv">
    <div class="eb">STOCK POR TIENDA</div>
    {"".join(f'<div class="tr"><span>{a}</span><span class="t">{b}</span><b>{c}</b></div>' for a, b, c in rows)}
    <div class="alert">{icon("bell-ring", 34, TD)} Reponer pronto · Blazer Siena, talla S · quedan 3</div>
  </div>
  <div class="swipe">Desliza {icon("arrow-right", 32, "#57534E")}</div>
</section>

<section class="slide s2" id="slide-2">
  <div class="brand"><img src="../../brand/encatalogo/logo/encatalogo-logo.svg" alt="">EnCatalogo.pe</div>
  <div class="num">02 / 02</div>
  <h2>Todo tu negocio,<br>en un solo lugar</h2>
  <div class="list">
    {"".join(f'<div class="card it"><div class="ic">{icon(ic, 46, TD)}</div><div><b>{t}</b><span>{d}</span></div></div>' for ic, t, d in caps)}
  </div>
  <div class="foot">
    <div class="price">Empieza hoy<b>7 días gratis</b>sin tarjeta · sin permanencia</div>
    <div class="cta"><div class="btn">Crea tu cuenta</div><small>encatalogo.pe</small></div>
  </div>
</section>
</body></html>
'''
open(os.path.join(HERE, "carrusel.html"), "w").write(html)
print("ok")
