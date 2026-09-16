# -*- coding: utf-8 -*-
"""Arma web/index.html: portfolio privado. Blanco y negro, Geist Mono.

El color quedó afuera a propósito: primero la estructura. --campo es el negro de
la tapa, las bandas y los avisos; si más adelante entra un color, se cambia ahí.
"""
import hashlib, json, pathlib, html, sys

CLARA = "claro" in sys.argv[1:]
SANS  = "sans" in sys.argv[1:]
SALIDA = ("index-sans.html" if SANS else
          "index-claro.html" if CLARA else "index.html")

AQUI = pathlib.Path(__file__).resolve().parent
WEB  = AQUI.parent
PENDIENTE = '<span class="falta">[ falta ]</span>'

assets = json.loads((AQUI / "web_assets.json").read_text(encoding="utf-8"))
by = {}
for a in assets: by.setdefault(a["proj"], []).append(a)
for v in by.values(): v.sort(key=lambda a: int(a["idx"]))

# id, titulo, meta (None = pendiente), bajada (None = pendiente), proyectos
SECCIONES = [
 {"grupo": "visuales", "id": "bestiario", "num": "01", "titulo": "Bestiario", "nav": "Bestiario",
  "meta": "@ Creadores de Imágenes, Julia Sbriller  ·  [2026]",
  "bajada": "Proyecto realizado en el marco de Creadores de Imágenes. Parte de los dibujos "
            "y la letra de mi infancia para llevarlos a otros universos: reformular hoy, con "
            "otras técnicas, lo que dibujé de chica.",
  "proyectos": [("@pares",       "Recreación de los dibujos", None),
                ("00b-alfabeto", "Alfabeto",                   None)]},
 {"grupo": "visuales", "id": "salto-de-fe", "num": "02", "titulo": "Salto de Fe", "nav": "Salto de Fe",
  "meta": "@ maiucheb-oss.github.io/salto-de-fe  ·  [2025]",
  "bajada": "Recopilación de fotografías propias sacadas en lo cotidiano. El nombre viene "
            "de algo que me pasa: encuentro mensajes en lo que me rodea. Quise darles una "
            "forma: en lo digital, esta página web; en lo material, un acordeón de fotos "
            "impreso como pieza editorial.",
  "embed": "https://maiucheb-oss.github.io/salto-de-fe/",
  "proyectos": [("@embed", None, None)]},
 {"grupo": "editoriales", "id": "fasciculos", "num": "03", "titulo": "Fascículos coleccionables", "nav": "Fascículos",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2023]",
  "bajada": "Colección de fascículos a partir de columnas y ensayos de Leila Guerriero, "
            "María Moreno y Juan Forn.",
  "proyectos": [("02-fasciculos-coleccionables", None, None)]},
 {"grupo": "editoriales", "id": "libros", "num": "04", "titulo": "Colección de libros", "nav": "Colección de libros",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2024]",
  "bajada": "Colección de libros para las obras completas de Samanta Schweblin.",
  "proyectos": [("05-coleccion-de-libros", None, None)]},
 {"grupo": "editoriales", "id": "perec", "num": "05", "titulo": "Plaquette Georges Perec", "nav": "Plaquette Perec",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2023]",
  "bajada": "Plaquette a partir de un fragmento de <i>Pensar/Clasificar</i>, de Georges Perec.",
  "proyectos": [("06-plaquette-perec", None, None)]},
 {"grupo": "identidad", "id": "espacios", "num": "06", "titulo": "Espacios", "nav": "Espacios",
  "meta": "@ MACBA  ·  [2021]",
  "bajada": "Identidad para una exposición de arte: sistema visual, piezas de comunicación "
            "y su aplicación en el espacio.",
  "proyectos": [("04-identidad-exposicion-arte", "Identidad para una exposición de arte", None)]},
 {"grupo": "identidad", "id": "medios", "num": "07", "titulo": "Televisión Pública",
  "nav": "Televisión Pública",
  "meta": "@ Cátedra Salomone, FADU  ·  [2023]",
  "bajada": "Rediseño de identidad para la Televisión Pública. Proyecto realizado en la "
            "FADU-UBA, en el marco de la materia de diseño, cátedra Salomone.",
  "proyectos": [("01-medios-publicos", None, None)]},
]

def ver(src):
    """src + ?v=<hash>. Sin esto el navegador sirve la version cacheada
    cuando se regenera un asset con el mismo nombre."""
    f = WEB / src
    if not f.exists():
        return src
    return f"{src}?v={hashlib.md5(f.read_bytes()).hexdigest()[:8]}"


GRILLA = {"00a-dibujos"}

# dibujo original  ->  imagen que lo reformula, en el orden que va en la página
PARES = [
    ("assets/00a-dibujos/04.jpg", "assets/00d-imagenes/01.jpg", "Mi casa"),
    ("assets/00a-dibujos/02.jpg", "assets/00d-imagenes/02.jpg", "Naturaleza emocional"),
    ("assets/00a-dibujos/05.jpg", "assets/00d-imagenes/03.jpg", "Familia unida"),
]
def rotulo(texto):
    """El nombre de la pieza sobre la imagen, en la misma Mono que el resto."""
    return f'<div class="rotulo">{html.escape(texto)}</div>'


def ficha(src):
    for a in assets:
        if a["src"] == src:
            return a
    raise KeyError(src)


def lupa(a, extra=""):
    return (f'<button class="lupa"{extra} data-src="{ver(a["src"])}" '
            f'data-w="{a["w"]}" data-h="{a["h"]}">'
            f'<img src="{ver(a["src"])}" width="{a["w"]}" height="{a["h"]}" '
            f'loading="lazy" decoding="async" alt=""></button>')


def pares():
    out = []
    for src_dib, src_img, texto in PARES:
        d, i = ficha(src_dib), ficha(src_img)
        out.append(f"""<div class="par-obra">
      <div class="obra">{lupa(i)}</div>
      {rotulo(texto)}
      <div class="fuente">{lupa(d)}</div>
    </div>""")
    return f'<div class="pares">{"".join(out)}</div>'




def grilla(slug):
    out = []
    for a in by.get(slug, []):
        out.append(
          f'<figure>'
          f'<button class="lupa" data-src="{ver(a["src"])}" data-w="{a["w"]}" data-h="{a["h"]}" '
          f'aria-label="Ver {html.escape(a.get("cap", ""))} en grande">'
          f'<img src="{ver(a["src"])}" width="{a["w"]}" height="{a["h"]}" loading="lazy" '
          f'decoding="async" alt=""></button>'
          f'<figcaption>{html.escape(a.get("cap", ""))}</figcaption></figure>')
    return f'<div class="grilla">{"".join(out)}</div>'


def piezas(slug):
    out = []
    for a in by.get(slug, []):
            out.append(
          f'<figure class="pieza" data-pieza="{a["proj"]}/{a["idx"]}" '
          f'data-px="{a["ow"]}×{a["oh"]}"{" data-gif" if a["gif"] else ""}>'
          f'<button class="lupa" data-src="{ver(a["src"])}" data-w="{a["w"]}" data-h="{a["h"]}" '
          f'aria-label="Ver la pieza {a["idx"]} en grande">'
          f'<img src="{ver(a["src"])}" width="{a["w"]}" height="{a["h"]}" loading="lazy" decoding="async" alt="">'
          f'</button>'
          f'</figure>')
    return "".join(out)

GRUPOS = [("visuales",    "Proyectos visuales"),
          ("editoriales", "Proyectos editoriales"),
          ("identidad",   "Identidad institucional")]

bloques, nav = [], []
for gid, gtit in GRUPOS:
    nav.append(f'<a href="#g-{gid}"><span class="hash">##</span> {html.escape(gtit)}</a>')

grupo_abierto = None
for s in SECCIONES:
    if s["grupo"] != grupo_abierto:
        if grupo_abierto is not None:
            bloques.append("\n</div>")
        gtit = dict(GRUPOS)[s["grupo"]]
        bloques.append(f'\n<div class="grupo" id="g-{s["grupo"]}">'
                       f'<div class="grupo-tit" role="heading" aria-level="2">'
                       f'{html.escape(gtit)}</div>')
        grupo_abierto = s["grupo"]
    cuerpo = []
    for slug, sub, baj in s["proyectos"]:
        if sub:
            cuerpo.append(f'<h3><span class="barra">/</span> {html.escape(sub)}</h3>')
        if slug == "@embed":
            cuerpo.append(f'''<div class="embed">
      <iframe src="{s['embed']}" loading="lazy" title="{html.escape(s['titulo'])}"
              scrolling="no" tabindex="-1"></iframe>
      <button class="sobre" type="button"><span>ver a pantalla completa</span></button>
      <button class="cerrar" type="button">salir ✕</button>
    </div>''')
        elif slug == "@pares":
            cuerpo.append(pares())
        elif slug in GRILLA:
            cuerpo.append(grilla(slug))
        else:
            cuerpo.append(f'<div class="piezas">{piezas(slug)}</div>')
    for pend in s.get("falta_piezas", []):
        cuerpo.append(f'<p class="vacio">&gt; {PENDIENTE} {html.escape(pend)}</p>')
    if not s["proyectos"]:
        cuerpo.append('<p class="vacio">&gt; Piezas por sumar.</p>')
    bloques.append(f"""
<section id="{s['id']}">
  <header class="sec">
    <h2><span class="hash">##</span> {html.escape(s['titulo'])}</h2>
    <div class="meta">{(s['meta'] or PENDIENTE) + ('  ·  ' + PENDIENTE if s.get('fecha_falta') else '')}</div>
    <p class="bajada">{s['bajada'] or ('&gt; ' + PENDIENTE)}</p>
  </header>
  {''.join(cuerpo)}
</section>""")
if grupo_abierto is not None:
    bloques.append("\n</div>")

CSS = """
@font-face{font-family:"Mono";src:url("assets/fonts/GeistMono-Regular.ttf");font-weight:400;font-display:swap}
@font-face{font-family:"Mono";src:url("assets/fonts/GeistMono-Medium.ttf");font-weight:500;font-display:swap}
/* Todo en Geist Mono, como el CV. La jerarquia la dan cuerpo, tracking y caja,
   no un cambio de familia. El negro es la base; --papel concentra el fondo. */
:root{--papel:#0d0c0b;--tinta:#ece8e1;--suave:#8d867e;--linea:#262320;
      --col:1600px;--medida:66ch;--gut:clamp(18px,4.2vw,44px)}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--papel);color:var(--tinta);
     font-family:"Mono",ui-monospace,monospace;font-size:13px;line-height:1.72;
     -webkit-font-smoothing:antialiased}
a{color:inherit}
img{display:block}

/* etiqueta: el registro de ficha, en mono */
.etq,.meta,.tapa .datos,.tapa .pie,nav .in,figcaption,.vacio,footer,h3 .barra{
  font-family:"Mono",ui-monospace,monospace;font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--suave);line-height:1.8}

/* ---- caratula ---- */
.tapa{min-height:100vh;padding:clamp(26px,5vw,74px) var(--gut);display:flex;
      flex-direction:column;justify-content:space-between}
/* los hijos de la tapa comparten la columna de main, si no la tapa arranca
   pegada al borde y el resto del portfolio aparece hundido hacia adentro */
.tapa>*{width:100%;max-width:calc(var(--col) - 2*var(--gut));margin-inline:auto}
.tapa h1{font-weight:700;font-size:clamp(32px,7.6vw,94px);line-height:1.02;
         letter-spacing:.02em;text-transform:uppercase}
.tapa .qué{font-size:clamp(13px,1.45vw,16px);line-height:1.66;max-width:54ch;
           margin-top:clamp(22px,3.4vw,42px);color:rgba(236,232,225,.84)}
.tapa .regla{border:0;border-top:1px solid var(--linea);margin:clamp(24px,3.6vw,42px) 0}
.tapa .pie{display:flex;flex-wrap:wrap;gap:4px 30px;text-transform:none;letter-spacing:.05em}

/* ---- nav ---- */
nav{position:sticky;top:0;z-index:40;background:rgba(13,12,11,.9);
    backdrop-filter:blur(10px);border-bottom:1px solid var(--linea)}
nav .in{max-width:var(--col);margin:0 auto;padding:14px var(--gut);
        display:flex;flex-wrap:nowrap;align-items:baseline;gap:26px;
        overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
nav .in::-webkit-scrollbar{display:none}
nav .yo{color:var(--tinta);margin-right:auto;white-space:nowrap}
nav a{text-decoration:none;white-space:nowrap;transition:color .18s}
nav a:hover{color:var(--tinta)}
nav .hash{color:#4d4741}

/* ---- grupos: la jerarquia de arriba. Adentro no cambia nada. ---- */
.grupo{padding-top:clamp(26px,3.4vw,46px);border-top:1px solid var(--tinta)}
.grupo+.grupo{margin-top:clamp(70px,10vw,150px)}
.grupo-tit{font-weight:700;font-size:clamp(26px,4.6vw,52px);line-height:1.04;
           letter-spacing:.012em;text-transform:uppercase}
.grupo>section:first-of-type{padding-top:clamp(44px,6.5vw,92px)}

/* ---- secciones ---- */
main{max-width:var(--col);margin:0 auto;padding:0 var(--gut)}
section{padding:clamp(72px,11vw,152px) 0}
.grupo section+section{border-top:1px solid var(--linea)}
.sec{margin-bottom:clamp(34px,5.4vw,68px)}
h2{font-weight:700;font-size:clamp(18px,2.8vw,30px);line-height:1.22;
   letter-spacing:.015em;text-transform:uppercase}
h2 .hash{color:var(--suave);font-weight:400}
.meta{margin-top:clamp(14px,1.8vw,22px)}
.bajada{max-width:var(--medida);margin-top:clamp(18px,2.4vw,30px);
        font-size:13px;line-height:1.72;color:rgba(236,232,225,.82)}

/* separador de proyecto: un filete a todo el ancho y el nombre en serif */
h3{margin-inline:calc(50% - 50vw);padding-inline:calc(50vw - 50%);
   margin-block:clamp(58px,8vw,108px) clamp(22px,3vw,36px);
   padding-top:clamp(14px,1.8vw,20px);border-top:1px solid var(--linea);
   font-weight:700;font-size:clamp(13px,1.6vw,17px);letter-spacing:.05em;
   text-transform:uppercase;display:flex;align-items:baseline;gap:13px}
h3 .barra{flex:none}
.vacio{margin-top:clamp(34px,5vw,54px);text-transform:none;letter-spacing:.05em}
.falta{background:var(--tinta);color:var(--papel);padding:1px 7px;letter-spacing:.06em}

/* ---- piezas: proporcion real, pegadas, un proyecto = una sabana ---- */
.piezas{display:flex;flex-direction:column;gap:0}
.pieza{display:block}
/* width:100% es necesario: un <button> se ajusta al contenido aunque sea
   display:block, y las piezas mas chicas que la columna no la llenaban */
.lupa{padding:0;border:0;background:#151311;cursor:zoom-in;display:block;
      width:100%;line-height:0}
.lupa img{width:100%;height:auto}
.lupa img{margin:0;vertical-align:top}

/* ---- pares: el dibujo apoyado sobre la imagen, abajo a la derecha.
       El margen blanco lo separa de la foto y lo lee como pieza aparte. ---- */
.pares{display:flex;flex-direction:column;gap:0}
.par-obra{position:relative}
.obra .lupa{background:#151311}
.fuente{position:absolute;z-index:2;
        width:clamp(78px,13.5%,170px);
        right:clamp(14px,2.2vw,34px);bottom:clamp(14px,2.2vw,34px);
        background:#fff;padding:clamp(5px,.62vw,9px);
        box-shadow:0 10px 30px rgba(0,0,0,.45)}
.fuente .lupa{background:#fff}

/* rotulo en la letra propia, arriba a la izquierda, opuesto al dibujo */
.rotulo{position:absolute;z-index:2;
        top:clamp(14px,2.2vw,34px);left:clamp(14px,2.2vw,34px);
        font-family:"Mono",monospace;font-size:10.5px;letter-spacing:.13em;
        text-transform:uppercase;color:#fff;max-width:60%;pointer-events:none;
        text-shadow:0 1px 10px rgba(0,0,0,.6)}

/* ---- grilla de dibujos ---- */
.grilla{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));
        gap:clamp(26px,3.6vw,50px) clamp(20px,2.6vw,38px)}
.grilla figure{display:flex;flex-direction:column;gap:12px;margin:0}
.grilla .lupa{height:clamp(140px,21vh,224px);display:flex;align-items:center;
              justify-content:center;background:none}
.grilla .lupa img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.grilla figcaption{text-transform:none;letter-spacing:.04em;line-height:1.5}
.grilla+h3{margin-top:clamp(58px,8vw,108px)}

/* ---- embed: la pieza viva, a todo el ancho ---- */
.embed{position:relative;margin-inline:calc(50% - 50vw);width:100vw;
       height:clamp(300px,74vh,720px);background:var(--papel);overflow:hidden;
       border-block:1px solid var(--linea)}
.embed iframe{width:100%;height:100%;border:0;display:block;pointer-events:none}
.embed .sobre{position:absolute;inset:0;display:flex;align-items:flex-end;
              justify-content:flex-end;padding:16px 18px;border:0;background:none;
              font-family:inherit;cursor:zoom-in}
.embed .sobre span{background:var(--tinta);color:var(--papel);
                   font-family:"Mono",monospace;font-size:10.5px;letter-spacing:.11em;
                   text-transform:uppercase;padding:7px 11px}
.embed .sobre:hover span{background:var(--papel);color:var(--tinta);
                         box-shadow:inset 0 0 0 1px var(--tinta)}
.embed:fullscreen{height:100%;margin:0;width:100%;border:0}
.embed:fullscreen iframe{pointer-events:auto}
.embed:fullscreen .sobre{inset:auto 0 0 auto;padding:18px 20px;cursor:default}
.embed.plena{position:fixed;inset:0;z-index:95;height:100%;width:100%;margin:0;border:0}
.embed.plena iframe{pointer-events:auto}
.embed .cerrar{position:absolute;top:16px;right:18px;display:none;background:var(--tinta);
               color:var(--papel);border:0;font-family:"Mono",monospace;font-size:10.5px;
               letter-spacing:.11em;text-transform:uppercase;padding:7px 11px;
               cursor:pointer;z-index:2}
.embed:fullscreen .cerrar,.embed.plena .cerrar{display:block}
.embed:fullscreen .sobre span,.embed.plena .sobre span{display:none}

/* ---- visor tamano real ---- */
.visor{position:fixed;inset:0;z-index:90;background:rgba(13,12,11,.985);
       display:none;overflow:auto;cursor:zoom-out;padding:52px 0}
.visor.on{display:block}
.visor img{margin:0 auto;max-width:none}
.visor .x{position:fixed;top:14px;right:18px;font-family:"Mono",monospace;font-size:10.5px;
          letter-spacing:.11em;text-transform:uppercase;color:var(--suave);
          background:#151311;border:1px solid var(--linea);padding:7px 11px;cursor:pointer}

footer{max-width:var(--col);margin:0 auto;padding:clamp(34px,5vw,56px) var(--gut) clamp(70px,9vw,110px);
       border-top:1px solid var(--linea);text-transform:none;letter-spacing:.05em}
@media (max-width:640px){body{font-size:12.5px}}
"""

GFONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
          '?family=Geist:wght@300;400;500;700&display=swap">')

SANS_CSS = """
/* ---- Geist Sans para leer y titular; la Mono queda para datos y etiquetas ---- */
body{font-family:"Geist","Helvetica Neue",Arial,sans-serif;font-size:15px;line-height:1.62;
     letter-spacing:.002em}
.tapa h1{font-family:"Geist",sans-serif;font-weight:500;font-size:clamp(40px,9.6vw,124px);
         line-height:.98;letter-spacing:-.025em;text-transform:none}
.tapa .qué{font-size:clamp(15px,1.5vw,19px);line-height:1.5;max-width:46ch}
h2{font-family:"Geist",sans-serif;font-weight:500;font-size:clamp(24px,4vw,44px);
   line-height:1.08;letter-spacing:-.021em;text-transform:none}
h2 .hash{display:block;font-family:"Mono",monospace;font-size:10.5px;letter-spacing:.13em;
         color:var(--suave);margin-bottom:clamp(10px,1.4vw,18px);font-weight:400}
.bajada{font-family:"Geist",sans-serif;font-size:clamp(14.5px,1.25vw,16.5px);
        line-height:1.58;max-width:60ch}
h3{font-family:"Geist",sans-serif;font-weight:500;font-size:clamp(15px,1.8vw,21px);
   letter-spacing:-.012em;text-transform:none}
h3 .barra{font-family:"Mono",monospace;font-size:10.5px;letter-spacing:.13em}
.grilla figcaption{font-family:"Geist",sans-serif;font-size:12px;letter-spacing:0}
"""

CLARO = """
/* ---- version clara, para el PDF de entrega ---- */
:root{--papel:#fbfaf8;--tinta:#16150f;--suave:#6f6a63;--linea:#dcd8d1}
.tapa .qué,.bajada{color:rgba(22,21,15,.8)}
nav{background:rgba(251,250,248,.9)}
nav .hash{color:#b4aea6}
.lupa,.obra .lupa{background:#f1efec}
.grilla .lupa,.fuente .lupa{background:none}
.visor{background:rgba(251,250,248,.985)}
.visor .x{background:#fff}
.embed{background:var(--papel)}
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
  const recargar = () => { f.src = f.src; };
  let salio = false, enVista = false;
  new IntersectionObserver(es => es.forEach(e => {
    enVista = e.isIntersecting;
    if (!e.isIntersecting) salio = true;
    else if (salio && !emb.classList.contains('plena') && !document.fullscreenElement) {
      salio = false; recargar();
    }
  }), { threshold: 0.2 }).observe(emb);

  // El acordeón recorre las fotos una vez y se detiene al final. Publicado en el
  // mismo dominio podemos leer su scroll y reiniciarlo justo al terminar; desde
  // otro origen no se puede leer, así que se recarga por tiempo.
  let porTiempo = null;
  setInterval(() => {
    if (!enVista || emb.classList.contains('plena') || document.fullscreenElement) return;
    try {
      const v = f.contentWindow.document.querySelector('.viewport');
      if (!v || !v.scrollWidth) return;
      if (v.scrollLeft + v.offsetWidth >= v.scrollWidth - 4) recargar();
    } catch (e) {
      if (!porTiempo) porTiempo = setInterval(() => { if (enVista) recargar(); }, 210000);
    }
  }, 2000);

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
<meta name="robots" content="noindex,nofollow">{GFONTS if SANS else ""}
<title>Maia Cheb Terrab — Portfolio</title>
<style>{CSS}{CLARO if CLARA else ""}{SANS_CSS if SANS else ""}</style>
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
    </div>
  </div>
</div>

<nav><div class="in"><span class="yo">Maia Cheb Terrab</span>{''.join(nav)}</div></nav>

<main>{''.join(bloques)}</main>

<footer>Clic en cualquier pieza para abrirla en tamaño completo.</footer>

<div class="visor"><button class="x">cerrar ✕</button><img alt=""></div>
<script>{JS}</script>
</body>
</html>"""

(WEB / SALIDA).write_text(doc, encoding="utf-8")
print(f"{SALIDA} escrito ·", round(len(doc)/1024, 1), "KB ·", len(assets), "piezas")
