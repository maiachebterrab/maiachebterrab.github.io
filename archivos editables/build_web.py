# -*- coding: utf-8 -*-
"""Arma web/index.html: portfolio privado, key visual del CV verde (Geist Mono, #bbf0a5, tinta #111)."""
import json, pathlib, html

AQUI = pathlib.Path(__file__).resolve().parent
WEB  = AQUI.parent
PENDIENTE = '<span class="falta">[ falta ]</span>'

assets = json.loads((AQUI / "web_assets.json").read_text(encoding="utf-8"))
by = {}
for a in assets: by.setdefault(a["proj"], []).append(a)
for v in by.values(): v.sort(key=lambda a: int(a["idx"]))

# id, titulo, meta (None = pendiente), bajada (None = pendiente), proyectos
SECCIONES = [
 {"id": "paradigma", "num": "01", "titulo": "Paradigma", "nav": "Paradigma", "meta": "@ PARADIGMA  ·  [2024 — 2026]",
  "bajada": None, "proyectos": []},
 {"id": "manela", "num": "02", "titulo": "Cátedra de Diseño Editorial Manela", "nav": "Manela",
  "meta": "@ FADU, UBA  ·  [2023]", "bajada": None,
  "proyectos": [("02-fasciculos-coleccionables", "Fascículos coleccionables", None),
                ("05-coleccion-de-libros",       "Colección de libros",       None),
                ("06-plaquette-perec",           "Plaquette Georges Perec",   None)]},
 {"id": "espacios", "num": "03", "titulo": "Espacios", "nav": "Espacios", "meta": None, "bajada": None,
  "proyectos": [("04-identidad-exposicion-arte", "Identidad para una exposición de arte", None)]},
 {"id": "medios", "num": "04", "titulo": "Diseño estratégico en medios públicos", "nav": "Medios públicos",
  "meta": None, "bajada": None,
  "proyectos": [("01-medios-publicos", None, None)]},
]

def piezas(slug):
    out = []
    for a in by.get(slug, []):
            out.append(
          f'<figure class="pieza" data-pieza="{a["proj"]}/{a["idx"]}" '
          f'data-px="{a["ow"]}×{a["oh"]}"{" data-gif" if a["gif"] else ""}>'
          f'<button class="lupa" data-src="{a["src"]}" data-w="{a["w"]}" data-h="{a["h"]}" '
          f'aria-label="Ver la pieza {a["idx"]} en grande">'
          f'<img src="{a["src"]}" width="{a["w"]}" height="{a["h"]}" loading="lazy" decoding="async" alt="">'
          f'</button>'
          f'</figure>')
    return "".join(out)

bloques, nav = [], []
for s in SECCIONES:
    nav.append(f'<a href="#{s["id"]}"><span class="hash">##</span> {html.escape(s["nav"])}</a>')
    n = sum(len(by.get(p[0], [])) for p in s["proyectos"])
    cuerpo = []
    for slug, sub, baj in s["proyectos"]:
        if sub:
            cuerpo.append(f'<h3><span class="barra">/</span> {html.escape(sub)}</h3>')
        cuerpo.append(f'<div class="piezas">{piezas(slug)}</div>')
    if not s["proyectos"]:
        cuerpo.append('<p class="vacio">&gt; Piezas por sumar.</p>')
    bloques.append(f"""
<section id="{s['id']}">
  <header class="sec">
    <h2><span class="hash">##</span> {html.escape(s['titulo'])}</h2>
    <div class="meta">{s['meta'] or PENDIENTE}</div>
    <p class="bajada">{s['bajada'] or ('&gt; ' + PENDIENTE)}</p>
    <div class="cuenta-sec">{n} piezas</div>
  </header>
  {''.join(cuerpo)}
</section>""")

CSS = """
@font-face{font-family:"Mono";src:url("assets/fonts/GeistMono-Regular.ttf");font-weight:400;font-display:swap}
@font-face{font-family:"Mono";src:url("assets/fonts/GeistMono-Medium.ttf");font-weight:500;font-display:swap}
@font-face{font-family:"Mono";src:url("assets/fonts/GeistMono-Bold.ttf");font-weight:700;font-display:swap}
:root{--verde:#bbf0a5;--ink:#111;--soft:#6f6f6f;--linea:#dcdcdc;--col:1120px}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:#fff;color:var(--ink);font-family:"Mono",ui-monospace,monospace;
     font-size:13px;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:inherit}
.hash{color:var(--soft)}

/* ---- caratula ---- */
.tapa{background:var(--verde);min-height:100vh;padding:clamp(24px,5vw,64px);
      display:flex;flex-direction:column;justify-content:space-between}
.tapa h1{font-size:clamp(30px,7.4vw,86px);font-weight:700;line-height:1.02;
         letter-spacing:.02em;text-transform:uppercase}
.tapa .qué{font-size:clamp(13px,1.5vw,17px);max-width:52ch;margin-top:clamp(18px,3vw,34px)}
.tapa .datos{font-size:12px;line-height:1.9}
.tapa .regla{border:0;border-top:1px dashed rgba(17,17,17,.42);margin:clamp(18px,3vw,30px) 0}
.tapa .pie{display:flex;flex-wrap:wrap;gap:6px 28px;font-size:11.5px;color:#2c2c2c}

/* ---- nav ---- */
nav{position:sticky;top:0;z-index:40;background:var(--verde);
    border-bottom:1px solid rgba(17,17,17,.2)}
nav .in{max-width:var(--col);margin:0 auto;padding:11px clamp(16px,4vw,40px);
        display:flex;flex-wrap:nowrap;align-items:baseline;gap:22px;font-size:11.5px;
        overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
nav .in::-webkit-scrollbar{display:none}
nav a{white-space:nowrap}
nav .yo{white-space:nowrap}
nav .yo{font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-right:auto;color:var(--ink)}
nav a{text-decoration:none;color:rgba(17,17,17,.62)}
nav a:hover{color:var(--ink)}
nav .hash{color:rgba(17,17,17,.4)}

/* ---- secciones ---- */
main{max-width:var(--col);margin:0 auto;padding:0 clamp(16px,4vw,40px)}
section{padding:clamp(52px,9vw,110px) 0;border-bottom:1px dashed var(--linea)}
section:last-child{border-bottom:0}
.sec{margin-bottom:clamp(28px,5vw,52px)}
h2{font-size:clamp(17px,2.6vw,27px);font-weight:700;text-transform:uppercase;letter-spacing:.01em}
.meta{font-size:11.5px;color:var(--soft);margin-top:9px;letter-spacing:.02em}
.bajada{max-width:62ch;margin-top:16px;font-size:13px}
.cuenta-sec{font-size:11px;color:var(--soft);margin-top:14px;padding-top:9px;
            border-top:1px solid var(--linea);display:inline-block;min-width:150px}
h3{background:var(--verde);color:var(--ink);
   /* sangra a todo el ancho pero el texto cae en el borde de la columna */
   margin-inline:calc(50% - 50vw);
   padding-block:15px;
   padding-inline:calc(50vw - 50% + clamp(16px,4vw,40px));
   margin-block:clamp(34px,5vw,54px) clamp(22px,3vw,34px);
   font-size:13.5px;font-weight:700;text-transform:uppercase;letter-spacing:.035em;
   display:flex;align-items:baseline;gap:11px}
.piezas + h3{margin-top:clamp(66px,9vw,112px)}
h3 .barra{color:rgba(17,17,17,.45);font-weight:400}
.vacio{color:var(--soft);font-size:13px}

/* ---- piezas: proporcion real, nada recortado ---- */
.piezas{display:flex;flex-direction:column;gap:0}
.pieza{display:block}
.lupa img{margin:0;vertical-align:top}
.lupa{padding:0;border:0;background:#fafafa;cursor:zoom-in;display:block;line-height:0}
.lupa img{width:100%;height:auto;display:block}
.falta{background:var(--verde);color:var(--ink);padding:0 6px}

/* ---- visor tamano real ---- */
.visor{position:fixed;inset:0;z-index:90;background:rgba(255,255,255,.98);
       display:none;overflow:auto;cursor:zoom-out;padding:44px 0}
.visor.on{display:block}
.visor img{display:block;margin:0 auto;max-width:none}
.visor .x{position:fixed;top:12px;right:16px;font-size:11.5px;color:var(--soft);
          background:#fff;border:1px solid var(--linea);padding:5px 10px;cursor:pointer}
footer{max-width:var(--col);margin:0 auto;padding:40px clamp(16px,4vw,40px) 80px;
       font-size:11px;color:var(--soft);border-top:1px solid var(--linea)}
@media (max-width:640px){body{font-size:12.5px}.piezas{gap:26px}}
"""

JS = """
const visor = document.querySelector('.visor'), vimg = visor.querySelector('img');
document.querySelectorAll('.lupa').forEach(b => b.addEventListener('click', () => {
  vimg.src = b.dataset.src; vimg.width = b.dataset.w; vimg.height = b.dataset.h;
  visor.classList.add('on'); visor.scrollTop = 0;
  document.body.style.overflow = 'hidden';
}));
function cerrar(){ visor.classList.remove('on'); vimg.removeAttribute('src');
  document.body.style.overflow = ''; }
visor.addEventListener('click', cerrar);
document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrar(); });
"""

doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Maia Cheb Terrab — Portfolio</title>
<style>{CSS}</style>
</head>
<body>

<div class="tapa">
  <div class="datos">MAIA CHEB TERRAB<br>DISEÑADORA GRÁFICA (FADU-UBA) · BUENOS AIRES</div>
  <div>
    <h1>Portfolio</h1>
    <p class="qué">Diseño identidades y universos visuales para artistas, proyectos culturales
    y productoras audiovisuales. Mi práctica cruza diseño, imagen, fotografía y escritura.</p>
    <hr class="regla">
    <div class="pie">
      <span>maiucheb@gmail.com</span><span>+54 11 6946-3209</span>
      <span>behance.net/maiacheb</span>
    </div>
  </div>
  <div class="datos">CLÍNICA DE DISEÑO · INSTITUTO PROA<br>SEPTIEMBRE 2026</div>
</div>

<nav><div class="in"><span class="yo">Maia Cheb Terrab</span>{''.join(nav)}</div></nav>

<main>{''.join(bloques)}</main>

<footer>Las piezas se ven en su proporción real. Hacé clic en cualquiera para abrirla en grande.</footer>

<div class="visor"><button class="x">cerrar ✕</button><img alt=""></div>
<script>{JS}</script>
</body>
</html>"""

(WEB / "index.html").write_text(doc, encoding="utf-8")
print("index.html escrito ·", round(len(doc)/1024, 1), "KB ·", len(assets), "piezas")
