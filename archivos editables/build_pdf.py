# -*- coding: utf-8 -*-
"""PDF de una página con el link a la web y el índice de proyectos.

Se entrega esto en vez del portfolio volcado: la web muestra las piezas en
tamaño completo, las animaciones en movimiento y Salto de Fe como pieza viva.

  python3 build_pdf.py          -> Portfolio-Maia-Cheb-Terrab.pdf        (blanco)
  python3 build_pdf.py negro    -> Portfolio-Maia-Cheb-Terrab-negro.pdf  (negro)
"""
import html, pathlib, subprocess, sys, urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from contenido import GRUPOS, SECCIONES

AQUI   = pathlib.Path(__file__).resolve().parent
WEB    = AQUI.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LINK   = "maiucheb-oss.github.io/portfolio"
F      = "file:///Users/maiacheb/Library/Fonts/"

NEGRO = "negro" in sys.argv[1:]
PAPEL, TINTA, SUAVE, LINEA = (("#0d0c0b", "#ece8e1", "#8d867e", "#2b2824") if NEGRO
                              else ("#ffffff", "#141310", "#6f6a63", "#d9d5ce"))
SALIDA = WEB.parent / ("Portfolio-Maia-Cheb-Terrab-negro.pdf" if NEGRO
                       else "Portfolio-Maia-Cheb-Terrab.pdf")

filas = []
for gid, gtit in GRUPOS:
    proyectos = [s for s in SECCIONES if s["grupo"] == gid]
    items = "".join(
        f'<div class="it"><span class="t">{html.escape(s["titulo"])}</span>'
        f'<span class="f">{html.escape(s["meta"].replace("@ ", "").replace("  ·  ", " · "))}</span></div>'
        for s in proyectos)
    filas.append(f'<section><h2>{html.escape(gtit)}</h2>{items}</section>')

doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Mono";src:url("{F}GeistMono-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Mono";src:url("{F}GeistMono-Medium.ttf");font-weight:500}}
@font-face{{font-family:"Mono";src:url("{F}GeistMono-Bold.ttf");font-weight:700}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0}}
html,body{{background:{PAPEL};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{width:210mm;height:297mm;padding:22mm 20mm 18mm;color:{TINTA};
      font-family:"Mono",monospace;font-size:8.4pt;line-height:1.75;
      display:flex;flex-direction:column}}
.etq{{font-size:6.6pt;letter-spacing:.15em;text-transform:uppercase;color:{SUAVE};}}
h1{{font-size:30pt;font-weight:700;letter-spacing:.02em;text-transform:uppercase;
    line-height:1.05;margin:16mm 0 0}}
.link{{margin-top:7mm;font-size:12.5pt;font-weight:500;letter-spacing:.005em;
       word-break:break-all}}
.nota{{margin-top:6mm;max-width:118mm;font-size:8.4pt;color:{TINTA};opacity:.9}}
hr{{border:0;border-top:.5pt solid {LINEA};margin:12mm 0 0}}
.indice{{margin-top:11mm}}
section{{margin-bottom:8mm;break-inside:avoid}}
h2{{font-size:6.6pt;font-weight:400;letter-spacing:.15em;text-transform:uppercase;
    color:{SUAVE};padding-bottom:2.4mm;border-bottom:.5pt solid {LINEA};margin-bottom:3.4mm}}
.it{{display:flex;justify-content:space-between;gap:8mm;align-items:baseline;
     padding:1.1mm 0}}
.it .t{{font-weight:500}}
.it .f{{font-size:7pt;color:{SUAVE};text-align:right;white-space:nowrap}}
footer{{margin-top:auto;padding-top:8mm;border-top:.5pt solid {LINEA};
        display:flex;justify-content:space-between;gap:10mm;font-size:7.4pt;color:{SUAVE}}}
</style></head><body>

<div class="etq">Maia Cheb Terrab · Diseñadora gráfica (FADU-UBA) · Buenos Aires</div>
<h1>Portfolio</h1>
<div class="link">{LINK}</div>
<p class="nota">El portfolio es una página web. Las piezas se ven en su proporción
real y se abren en tamaño completo, las animaciones se ven en movimiento, y
<i>Salto de Fe</i> es una pieza web que se recorre sola.</p>
<hr>

<div class="indice">{''.join(filas)}</div>

<footer>
  <span>maiucheb@gmail.com · +54 11 6946-3209</span>
  <span>Septiembre 2026</span>
</footer>
</body></html>"""

src = AQUI / ("pdf-negro.html" if NEGRO else "pdf-claro.html")
src.write_text(doc, encoding="utf-8")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--virtual-time-budget=20000",
                f"--print-to-pdf={SALIDA}",
                "file://" + urllib.parse.quote(str(src))], capture_output=True, timeout=300)
print(f"{SALIDA.name} · {round(SALIDA.stat().st_size/1024)} KB")
