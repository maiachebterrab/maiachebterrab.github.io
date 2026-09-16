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
 {"id": "las-casas", "num": "01", "titulo": "Las casas no vuelan", "nav": "Las casas no vuelan",
  "meta": "@ proyecto propio  ·  [2026]",
  "bajada": "Dibujos que hice en la infancia, lápiz y crayón sobre papel. De esa "
            "letra salió <i>Maia</i>, un alfabeto propio. Las imágenes son "
            "representaciones de esos mismos dibujos llevadas a otras técnicas.",
  "proyectos": [("00a-dibujos",   "Dibujos de la infancia", None),
                ("00b-alfabeto",  "Alfabeto",               None),
                ("00d-imagenes",  "Imágenes",               None)]},
 {"id": "salto-de-fe", "num": "01", "titulo": "Salto de Fe", "nav": "Salto de Fe",
  "meta": "@ maiucheb-oss.github.io/salto-de-fe", "fecha_falta": True,
  "bajada": "Colección de imágenes de señales encontradas en lo cotidiano. "
            "Las fotos se recorren de corrido, como una sola imagen que avanza.",
  "embed": "https://maiucheb-oss.github.io/salto-de-fe/",
  "proyectos": []},
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

GRILLA = {"00a-dibujos"}


def grilla(slug):
    out = []
    for a in by.get(slug, []):
        out.append(
          f'<figure>'
          f'<button class="lupa" data-src="{a["src"]}" data-w="{a["w"]}" data-h="{a["h"]}" '
          f'aria-label="Ver {html.escape(a.get("cap", ""))} en grande">'
          f'<img src="{a["src"]}" width="{a["w"]}" height="{a["h"]}" loading="lazy" '
          f'decoding="async" alt=""></button>'
          f'<figcaption>{html.escape(a.get("cap", ""))}</figcaption></figure>')
    return f'<div class="grilla">{"".join(out)}</div>'


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
        if slug in GRILLA:
            cuerpo.append(grilla(slug))
        else:
            cuerpo.append(f'<div class="piezas">{piezas(slug)}</div>')
    for pend in s.get("falta_piezas", []):
        cuerpo.append(f'<p class="vacio">&gt; {PENDIENTE} {html.escape(pend)}</p>')
    if s.get("embed"):
        cuerpo.append(f'''<div class="embed">
      <iframe src="{s['embed']}" loading="lazy" title="{html.escape(s['titulo'])}"
              scrolling="no" tabindex="-1"></iframe>
      <button class="sobre" type="button"><span>ver a pantalla completa</span></button>
      <button class="cerrar" type="button">salir ✕</button>
    </div>''')
    elif not s["proyectos"]:
        cuerpo.append('<p class="vacio">&gt; Piezas por sumar.</p>')
    bloques.append(f"""
<section id="{s['id']}">
  <header class="sec">
    <h2><span class="hash">##</span> {html.escape(s['titulo'])}</h2>
    <div class="meta">{(s['meta'] or PENDIENTE) + ('  ·  ' + PENDIENTE if s.get('fecha_falta') else '')}</div>
    <p class="bajada">{s['bajada'] or ('&gt; ' + PENDIENTE)}</p>
    <div class="cuenta-sec">{('50 fotos · se mueve sola' if s.get('embed') else str(n) + ' piezas')}</div>
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
.vacio{color:var(--soft);font-size:13px;margin-top:clamp(34px,5vw,54px)}

/* ---- piezas: proporcion real, nada recortado ---- */
.piezas{display:flex;flex-direction:column;gap:0}
.pieza{display:block}
.lupa img{margin:0;vertical-align:top}
.lupa{padding:0;border:0;background:#fafafa;cursor:zoom-in;display:block;line-height:0}
.lupa img{width:100%;height:auto;display:block}
.falta{background:var(--verde);color:var(--ink);padding:0 6px}

/* ---- grilla de dibujos: cada uno con su epigrafe ---- */
.grilla{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));
        gap:clamp(24px,3.4vw,46px) clamp(20px,2.6vw,36px)}
.grilla figure{display:flex;flex-direction:column;gap:11px;margin:0}
.grilla .lupa{height:clamp(148px,22vh,236px);display:flex;align-items:center;
              justify-content:center;background:none;border:0;padding:0;cursor:zoom-in}
.grilla .lupa img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.grilla figcaption{font-size:10.5px;color:var(--soft);letter-spacing:.03em;line-height:1.5}
.grilla + h3{margin-top:clamp(66px,9vw,112px)}

/* ---- embed: la pieza viva, a todo el ancho ---- */
.embed{position:relative;margin-inline:calc(50% - 50vw);width:100vw;
       height:clamp(300px,74vh,720px);background:#fff;overflow:hidden;
       border-block:1px solid var(--linea)}
.embed iframe{width:100%;height:100%;border:0;display:block;pointer-events:none}
.embed .sobre{position:absolute;inset:0;display:flex;align-items:flex-end;
              justify-content:flex-end;padding:14px 16px;border:0;background:none;
              font-family:inherit;cursor:zoom-in}
.embed .sobre span{background:var(--verde);color:var(--ink);font-size:11px;
                   padding:6px 10px;letter-spacing:.02em}
.embed .sobre:hover span{background:var(--ink);color:var(--verde)}
/* a pantalla completa: la pista se puede recorrer a mano y se sale con Esc */
.embed:fullscreen{height:100%;margin:0;width:100%;border:0}
.embed:fullscreen iframe{pointer-events:auto}
.embed:fullscreen .sobre{inset:auto 0 0 auto;padding:16px 18px;cursor:default}
.embed.plena{position:fixed;inset:0;z-index:95;height:100%;width:100%;margin:0;border:0}
.embed.plena iframe{pointer-events:auto}
.embed .cerrar{position:absolute;top:14px;right:16px;display:none;background:var(--verde);
               color:var(--ink);border:0;font-family:inherit;font-size:11px;padding:6px 10px;
               cursor:pointer;z-index:2}
.embed:fullscreen .cerrar,.embed.plena .cerrar{display:block}
.embed:fullscreen .sobre span,.embed.plena .sobre span{display:none}

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

// el sitio embebido se auto-scrollea una sola vez y para al final:
// lo recargamos cada vez que la seccion vuelve a entrar en pantalla, asi siempre se ve moviendose
const emb = document.querySelector('.embed');
if (emb) {
  const f = emb.querySelector('iframe');
  let salio = false;
  new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) salio = true;
    else if (salio && !emb.classList.contains('plena') && !document.fullscreenElement) {
      salio = false; f.src = f.src;
    }
  }), { threshold: 0.2 }).observe(emb);

  // pantalla completa en el lugar: nunca se sale del portfolio
  const abrir = () => {
    if (emb.requestFullscreen) {
      emb.requestFullscreen().catch(() => emb.classList.add('plena'));
    } else {
      emb.classList.add('plena');
    }
    document.body.style.overflow = 'hidden';
  };
  const cerrarPlena = () => {
    if (document.fullscreenElement) document.exitFullscreen();
    emb.classList.remove('plena');
    document.body.style.overflow = '';
  };
  emb.querySelector('.sobre').addEventListener('click', abrir);
  emb.querySelector('.cerrar').addEventListener('click', e => { e.stopPropagation(); cerrarPlena(); });
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement) document.body.style.overflow = '';
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && emb.classList.contains('plena')) cerrarPlena();
  });
}
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
