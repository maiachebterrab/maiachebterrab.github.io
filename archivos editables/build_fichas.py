# -*- coding: utf-8 -*-
"""Arma el portfolio en fichas: un índice de cards y una página por proyecto.

Referencia: sofiarezs.com/projects. El índice es una grilla de cards —tapa,
nombre, año, tipo— y adentro de cada proyecto la columna izquierda queda quieta
con el texto mientras la derecha scrollea con las imágenes.

Tipografía: la misma del index-editorial, Saol Text para titular y TWK Lausanne
para todo lo demás. Los textos salen de contenido.py, así que se editan en un
solo lugar para la web larga, las fichas y el PDF.

    python3 build_fichas.py
"""
import hashlib, json, pathlib, re, html, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from contenido import GRUPOS, PARES, SECCIONES, PRESENTACION

AQUI = pathlib.Path(__file__).resolve().parent
WEB  = AQUI.parent

assets = json.loads((AQUI / "web_assets.json").read_text(encoding="utf-8"))
by = {}
for a in assets:
    by.setdefault(a["proj"], []).append(a)
for v in by.values():
    v.sort(key=lambda a: int(a["idx"]))

NOMBRE_GRUPO = dict(GRUPOS)


def ver(src):
    """src + ?v=<hash>: sin esto el navegador sirve la copia vieja cuando se
    regenera un asset con el mismo nombre."""
    f = WEB / src
    if not f.exists():
        return src
    return f"{src}?v={hashlib.md5(f.read_bytes()).hexdigest()[:8]}"


def anio(meta):
    m = re.search(r"\[(\d{4})\]", meta or "")
    return m.group(1) if m else ""


def piezas_de(sec):
    """Los assets que van en la columna derecha, en orden."""
    out = []
    for slug, _rot, _extra in sec["proyectos"]:
        if slug == "@pares":
            for dib, img, rot in PARES:
                out.append(("par", img, dib, rot))
        elif slug == "@embed":
            out.append(("embed", sec["embed"], None, None))
        else:
            for a in by.get(slug, []):
                out.append(("img", a, None, None))
    return out


def tapa(sec):
    """La imagen de la card. La primera pieza que sea imagen."""
    for tipo, a, _b, _c in piezas_de(sec):
        if tipo == "img":
            return a
        if tipo == "par":
            for x in assets:
                if x["src"] == a:
                    return x
    # un proyecto que solo tiene embed: el acordeón hace de tapa
    return (by.get("07-acordeon") or [None])[0]


# ---------------------------------------------------------------- estilos

FUENTES = """
@font-face{font-family:"Saol";src:url("assets/fonts/SaolText-Regular.otf") format("opentype");
           font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Saol";src:url("assets/fonts/SaolText-RegularItalic.otf") format("opentype");
           font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:"Lausanne";src:url("assets/fonts/TWKLausanne-300.otf") format("opentype");
           font-weight:300;font-display:swap}
@font-face{font-family:"Lausanne";src:url("assets/fonts/TWKLausanne-400.otf") format("opentype");
           font-weight:400;font-display:swap}
@font-face{font-family:"Lausanne";src:url("assets/fonts/TWKLausanne-500.otf") format("opentype");
           font-weight:500;font-display:swap}
"""

BASE = FUENTES + """
:root{--papel:#fff;--tinta:#131211;--suave:#8b8781;--linea:#e6e3de;
      --gut:clamp(16px,3.2vw,36px)}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--papel);color:var(--tinta);
     font-family:"Lausanne","Helvetica Neue",Arial,sans-serif;
     font-size:13.5px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{display:block}

/* ---- nav: el nombre a la izquierda, las tres secciones a la derecha ---- */
nav{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.92);
    backdrop-filter:blur(10px)}
nav .in{display:flex;align-items:baseline;gap:22px;padding:14px var(--gut)}
nav .yo{margin-right:auto}
nav a{color:var(--suave);transition:color .18s}
nav a:hover,nav .yo{color:var(--tinta)}
"""

INDICE_CSS = """
main{padding:clamp(28px,4vw,52px) var(--gut) clamp(70px,9vw,120px)}
.intro{max-width:46ch;margin-bottom:clamp(40px,6vw,86px)}
.intro h1{font-family:"Saol",Georgia,serif;font-weight:400;
          font-size:clamp(26px,3.6vw,42px);line-height:1.06;letter-spacing:-.012em}
/* interlineado de los parrafos: 130% */
.intro p{margin-top:14px;color:rgba(19,18,17,.72);line-height:1.3}

.banda+.banda{margin-top:clamp(46px,6vw,84px)}
/* el titulo de cada banda se lee igual que su entrada en el menu: Lausanne
   13,5px en gris, caja normal, sin tracking. El filete pasa a ser fino para no
   pesar mas que el titulo. */
.banda>h2{font-size:13.5px;font-weight:400;letter-spacing:0;text-transform:none;
          line-height:1.55;color:var(--suave);padding-top:12px;
          border-top:1px solid var(--linea);margin-bottom:clamp(18px,2.4vw,28px)}

.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));
       gap:clamp(24px,3vw,42px) clamp(16px,1.8vw,26px)}
.card{display:block}
/* 4px: lo justo para que la esquina no quede cruda, sin que se note redondeada */
.card .foto{background:#f3f1ee;aspect-ratio:16/10;overflow:hidden;border-radius:4px}
.card .foto img{width:100%;height:100%;object-fit:cover;
                transition:transform .5s cubic-bezier(.2,.7,.3,1)}
.card:hover .foto img{transform:scale(1.02)}
.card .pie{display:flex;justify-content:space-between;gap:12px;
           margin-top:9px;font-size:11.5px;color:var(--suave)}
.card .pie .n{color:var(--tinta);flex:1}
.card .pie .a{flex:none}
.card .pie .t{flex:none;text-align:right;min-width:9em}
.vacia .foto{display:flex;align-items:center;justify-content:center;
             border:1px dashed var(--linea);background:none;color:var(--suave);
             font-size:11.5px}
"""

FICHA_CSS = """
/* ---- dos columnas: la izquierda no se mueve, la derecha scrollea ---- */
.ficha{display:grid;grid-template-columns:minmax(280px,30%) 1fr;
       gap:clamp(20px,3vw,44px);padding:0 var(--gut) clamp(70px,9vw,120px);
       align-items:start}
.info{position:sticky;top:0;min-height:100vh;display:flex;flex-direction:column;
      padding:clamp(44px,7vw,104px) 0 clamp(22px,3vw,34px)}
.info h1{font-family:"Saol",Georgia,serif;font-weight:400;
         font-size:clamp(22px,2.4vw,30px);line-height:1.12;letter-spacing:-.008em}
.info .meta{margin-top:6px;font-size:11.5px;color:var(--suave)}
.info .raya{margin:clamp(18px,2.4vw,28px) 0;color:var(--suave)}
.info .bajada{max-width:42ch;color:rgba(19,18,17,.74);line-height:1.3}
.info .abajo{margin-top:auto;padding-top:34px;display:flex;
             justify-content:space-between;align-items:baseline;gap:16px}
.info .abajo a{font-family:"Saol",Georgia,serif;font-size:16px}
.info .abajo a:hover{opacity:.55}

.media{padding-top:clamp(44px,7vw,104px);display:flex;flex-direction:column;gap:0}
.media .lupa{padding:0;border:0;background:#f3f1ee;cursor:zoom-in;display:block;
             width:100%;line-height:0}
.media .lupa img{width:100%;height:auto;vertical-align:top}
.par{position:relative}
.par .fuente{position:absolute;z-index:2;width:clamp(72px,14%,160px);
             right:clamp(12px,1.8vw,26px);bottom:clamp(12px,1.8vw,26px);
             background:#fff;padding:clamp(4px,.55vw,8px);
             box-shadow:0 8px 24px rgba(0,0,0,.14)}
.par .rotulo{position:absolute;z-index:2;top:clamp(12px,1.8vw,26px);
             left:clamp(12px,1.8vw,26px);font-size:11.5px;color:#fff;
             text-shadow:0 1px 12px rgba(0,0,0,.55);pointer-events:none}
.embed{position:relative;height:clamp(300px,74vh,700px);
       border:1px solid var(--linea);overflow:hidden}
.embed iframe{width:100%;height:100%;border:0;display:block}

.visor{position:fixed;inset:0;z-index:90;background:rgba(255,255,255,.99);
       display:none;overflow:auto;cursor:zoom-out;padding:52px 0}
.visor.on{display:block}
.visor img{margin:0 auto;max-width:none}

@media (max-width:860px){
  .ficha{grid-template-columns:1fr}
  .info{position:static;min-height:0;padding-bottom:30px}
  .media{padding-top:0}
}
"""

VISOR_JS = """
const visor=document.querySelector('.visor'),vimg=visor.querySelector('img');
document.querySelectorAll('.lupa').forEach(b=>b.addEventListener('click',()=>{
  vimg.src=b.dataset.src;vimg.width=b.dataset.w;vimg.height=b.dataset.h;
  visor.classList.add('on');visor.scrollTop=0;document.body.style.overflow='hidden';}));
const cerrar=()=>{visor.classList.remove('on');vimg.removeAttribute('src');
  document.body.style.overflow='';};
visor.addEventListener('click',cerrar);
document.addEventListener('keydown',e=>{if(e.key==='Escape')cerrar();});
"""


CARRUSEL_CSS = """
/* ---- carrusel de posteos: scroll-snap, sin libreria ----
   La pista es un scroll horizontal con scroll-snap-type:x mandatory; cada
   slide se imanta con scroll-snap-align:center. Asi funciona igual con el
   trackpad, con el dedo en el celular y con las flechas, que solo hacen
   scrollBy del ancho de un slide. El recurso es de julidalmasso.com/design. */
.clientes{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
          gap:clamp(22px,2.6vw,36px) clamp(14px,1.6vw,24px);
          padding:clamp(28px,4vw,52px) var(--gut) clamp(70px,9vw,120px)}
.post{position:relative}
.pista{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;
       scroll-behavior:smooth;aspect-ratio:4/5;background:#f3f1ee;
       border-radius:4px;scrollbar-width:none;-ms-overflow-style:none}
.pista::-webkit-scrollbar{display:none}
.pista>img,.pista>video{flex:0 0 100%;width:100%;height:100%;object-fit:cover;
           scroll-snap-align:start;scroll-snap-stop:always}
.post .flecha{position:absolute;top:50%;transform:translateY(-50%);z-index:2;
              width:30px;height:30px;border:0;border-radius:50%;cursor:pointer;
              background:rgba(255,255,255,.72);color:#131211;font-size:13px;
              line-height:1;display:grid;place-items:center;opacity:0;
              transition:opacity .2s}
.post:hover .flecha{opacity:1}
.post .flecha:hover{background:#fff}
.post .flecha[disabled]{opacity:0!important;pointer-events:none}
.post .ant{left:9px}
.post .sig{right:9px}
.post .puntos{position:absolute;bottom:9px;left:0;right:0;z-index:2;
              display:flex;justify-content:center;gap:5px;pointer-events:none}
.post .puntos i{width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.5)}
.post .puntos i.on{background:#fff}
.post .pie{display:flex;justify-content:space-between;gap:10px;margin-top:8px;
           font-size:11.5px;color:var(--suave)}
.post .pie .n{color:var(--tinta)}
"""

CARRUSEL_JS = """
document.querySelectorAll('.post').forEach(post=>{
  const pista=post.querySelector('.pista'),
        slides=[...pista.children],
        puntos=[...post.querySelectorAll('.puntos i')],
        ant=post.querySelector('.ant'), sig=post.querySelector('.sig');
  let i=0;
  // Con scroll-snap mandatory, scrollBy() y scrollTo() pelean con el snap y
  // quedan a mitad de camino. scrollIntoView sobre el slide cae justo.
  const ir=n=>{i=Math.max(0,Math.min(slides.length-1,n));
    // behavior:'smooth' no anima dentro de un contenedor con snap mandatory
    // (Chrome cancela la animacion y no se mueve). Con 'instant' cae justo.
    // El deslizado con el dedo o el trackpad sigue siendo nativo y suave.
    slides[i].scrollIntoView({inline:'start',block:'nearest',behavior:'instant'});
    pintar();};
  function pintar(){
    puntos.forEach((p,n)=>p.classList.toggle('on',n===i));
    ant.disabled = i===0;
    sig.disabled = i===slides.length-1;
  }
  ant.addEventListener('click',()=>ir(i-1));
  sig.addEventListener('click',()=>ir(i+1));
  // el dedo y el trackpad scrollean solos: leemos donde quedo y sincronizamos
  pista.addEventListener('scroll',()=>{clearTimeout(pista._t);
    pista._t=setTimeout(()=>{
      i=Math.round(pista.scrollLeft/(pista.clientWidth||1));pintar();},90);});
  new ResizeObserver(()=>slides[i].scrollIntoView(
      {inline:'start',block:'nearest',behavior:'instant'})).observe(pista);
  pintar();
});
"""

def nav(activo=None):
    ls = "".join(f'<a href="index.html#{g}">{html.escape(n)}</a>'
                 for g, n in GRUPOS)
    return (f'<nav><div class="in"><a class="yo" href="index.html">'
            f'Maia Cheb Terrab</a>{ls}</div></nav>')


def cabeza(titulo, css):
    return (f'<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<meta name="robots" content="noindex,nofollow">\n'
            f'<title>{html.escape(titulo)}</title>\n<style>{BASE}{css}</style>\n'
            f'</head>\n<body>\n')


# ---------------------------------------------------------------- índice

def card(sec):
    t = tapa(sec)
    # la card usa la miniatura de 680px si existe; si no, el original
    src = t["src"] if t else None
    if src:
        from hacer_miniaturas import mini
        chico = mini(src)
        if (WEB / chico).exists():
            src = chico
    foto = (f'<div class="foto"><img src="{ver(src)}" width="{t["w"]}" '
            f'height="{t["h"]}" alt="" loading="lazy"></div>') if t else \
           '<div class="foto">sin tapa todavía</div>'
    return (f'<a class="card" href="p-{sec["id"]}.html">{foto}'
            f'<div class="pie"><span class="n">{sec["titulo"]}</span>'
            f'<span class="a">({anio(sec["meta"])})</span>'
            f'<span class="t">({NOMBRE_GRUPO[sec["grupo"]]})</span></div></a>')


def indice():
    bandas = []
    for gid, nombre in GRUPOS:
        secs = [s for s in SECCIONES if s["grupo"] == gid]
        if not secs:
            continue
        bandas.append(f'<section class="banda" id="{gid}"><h2>{nombre}</h2>'
                      f'<div class="cards">{"".join(card(s) for s in secs)}'
                      f'</div></section>')
    doc = (cabeza("Maia Cheb Terrab — Portfolio", INDICE_CSS) + nav() +
           '<main>\n<div class="intro"><h1>Portfolio</h1>'
           f'<p>{PRESENTACION}</p></div>\n' +
           "\n".join(bandas) +
           '\n</main>\n</body>\n</html>\n')
    (WEB / "index.html").write_text(doc, encoding="utf-8")
    return sum(len([s for s in SECCIONES if s["grupo"] == g]) for g, _ in GRUPOS)


# ---------------------------------------------------------------- fichas

def lupa(a):
    return (f'<button class="lupa" data-src="{ver(a["src"])}" data-w="{a["ow"]}" '
            f'data-h="{a["oh"]}"><img src="{ver(a["src"])}" width="{a["w"]}" '
            f'height="{a["h"]}" alt="" loading="lazy"></button>')


def media(sec):
    fila = []
    for tipo, a, b, rot in piezas_de(sec):
        if tipo == "img":
            fila.append(lupa(a))
        elif tipo == "par":
            img = next((x for x in assets if x["src"] == a), None)
            dib = next((x for x in assets if x["src"] == b), None)
            if not img:
                continue
            adentro = lupa(img)
            if rot:
                adentro += f'<span class="rotulo">{html.escape(rot)}</span>'
            if dib:
                adentro += f'<span class="fuente">{lupa(dib)}</span>'
            fila.append(f'<div class="par">{adentro}</div>')
        elif tipo == "embed":
            fila.append(f'<div class="embed"><iframe src="{a}" loading="lazy" '
                        f'title="Salto de Fe"></iframe></div>')
    return "".join(fila)


def ficha(sec, siguiente):
    sig = (f'<a href="p-{siguiente["id"]}.html">{siguiente["titulo"]} →</a>'
           if siguiente else '<span></span>')
    doc = (cabeza(f'{sec["titulo"]} — Maia Cheb Terrab', FICHA_CSS) + nav() +
           f'''<div class="ficha">
  <aside class="info">
    <h1>{sec["titulo"]}</h1>
    <div class="meta">{sec["meta"]}</div>
    <div class="raya">—</div>
    <div class="bajada">{sec["bajada"]}</div>
    <div class="abajo"><a href="index.html">← Índice</a>{sig}</div>
  </aside>
  <div class="media">{media(sec)}</div>
</div>
<div class="visor"><img alt=""></div>
<script>{VISOR_JS}</script>
</body>
</html>
''')
    (WEB / f'p-{sec["id"]}.html').write_text(doc, encoding="utf-8")


# ------------------------------------------------- posteos (Paradigma)

PARADIGMA = WEB / "assets" / "08-paradigma"
EXT_IMG = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
EXT_VID = {".mp4", ".mov", ".webm", ".m4v"}
EXT = EXT_IMG | EXT_VID


def post(nombre, handle, slides):
    """Una card = un posteo. Se desliza con el dedo, el trackpad o las flechas."""
    # tres de los posteos elegidos son video (un reel de Isla, el de Olivia
    # Mucida en Immigrant y el de El Ojo en Landia): el slide puede ser <img>
    # o <video>, se decide por la extension del archivo.
    def slide(x):
        if pathlib.Path(x).suffix.lower() in EXT_VID:
            return (f'<video src="{ver(x)}" muted loop playsinline autoplay '
                    f'preload="metadata"></video>')
        return f'<img src="{ver(x)}" alt="" loading="lazy">'
    imgs = "".join(slide(x) for x in slides)
    pts = "".join('<i></i>' for _ in slides)
    return (f'<div class="post"><div class="pista">{imgs}</div>'
            f'<button class="flecha ant" aria-label="Anterior">‹</button>'
            f'<button class="flecha sig" aria-label="Siguiente">›</button>'
            f'<div class="puntos">{pts}</div>'
            f'<div class="pie"><span class="n">{html.escape(nombre)}</span>'
            f'<span>{html.escape(handle)}</span></div></div>')


def pagina_posts(salida, titulo, intro, posts):
    doc = (cabeza(titulo, INDICE_CSS + CARRUSEL_CSS) + nav() +
           f'<main style="padding-bottom:0"><div class="intro"><h1>{titulo}</h1>'
           f'<p>{intro}</p></div></main>\n'
           f'<div class="clientes">{"".join(posts)}</div>\n'
           f'<script>{CARRUSEL_JS}</script>\n</body>\n</html>\n')
    (WEB / salida).write_text(doc, encoding="utf-8")


def paradigma():
    """Lee assets/08-paradigma/<cliente>/*.jpg — una carpeta por cliente."""
    if not PARADIGMA.exists():
        return 0
    posts = []
    for carpeta in sorted(d for d in PARADIGMA.iterdir() if d.is_dir()):
        slides = sorted(f"assets/08-paradigma/{carpeta.name}/{f.name}"
                        for f in carpeta.iterdir() if f.suffix.lower() in EXT)
        if not slides:
            continue
        posts.append(post(carpeta.name.replace("-", " ").title(),
                          f"{len(slides)} piezas", slides))
    if not posts:
        return 0
    pagina_posts("p-paradigma.html", "Paradigma",
                 "Piezas para productoras audiovisuales. Cada posteo se desliza.",
                 posts)
    return len(posts)


def demo_carrusel():
    """Prueba del recurso con material que ya existe, para verlo funcionando
    antes de que entren las piezas de Paradigma."""
    fuente = by.get("01-medios-publicos", [])
    if not fuente:
        return
    lotes = [fuente[i:i + 4] for i in range(0, min(len(fuente), 16), 4)]
    posts = [post(f"Posteo {n+1}", "demo", [a["src"] for a in lote])
             for n, lote in enumerate(lotes)]
    pagina_posts("demo-carrusel.html", "Carrusel",
                 "Prueba del recurso con imágenes prestadas de Medios públicos. "
                 "Se desliza con el dedo, el trackpad o las flechas; cada slide "
                 "se imanta. Cuando lleguen las piezas de Paradigma va igual, "
                 "una carpeta por cliente.", posts)

if __name__ == "__main__":
    n = indice()
    for i, sec in enumerate(SECCIONES):
        ficha(sec, SECCIONES[i + 1] if i + 1 < len(SECCIONES) else None)
    np = paradigma()
    demo_carrusel()
    print(f"index.html + {len(SECCIONES)} fichas · {n} cards · "
          f"paradigma: {np} posteos · demo-carrusel.html")
