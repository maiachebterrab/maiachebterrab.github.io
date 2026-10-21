# -*- coding: utf-8 -*-
"""PDF de una página: la carátula que lleva a la web.

Se entrega esto en vez del portfolio volcado, porque la web muestra las piezas
en tamaño completo, las animaciones en movimiento y Salto de Fe como pieza viva.

El listado de proyectos salió (21/9): duplicaba el índice de la web y le robaba
peso a lo único que esta hoja tiene que lograr, que es que hagan clic. El link
es un <a> de verdad, así que en el PDF se puede clickear.

Tipografía: la misma de la web, Saol Text y TWK Lausanne.

  python3 build_pdf.py          -> Portfolio-Maia-Cheb-Terrab.pdf        (blanco)
  python3 build_pdf.py negro    -> Portfolio-Maia-Cheb-Terrab-negro.pdf  (negro)
"""
import pathlib, subprocess, sys, urllib.parse

AQUI   = pathlib.Path(__file__).resolve().parent
WEB    = AQUI.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL    = "https://maiachebterrab.github.io/"
VISIBLE = "maiachebterrab.github.io"
F      = "file:///Users/maiacheb/Library/Fonts/"

NEGRO = "negro" in sys.argv[1:]
PAPEL, TINTA, SUAVE, LINEA = (("#0d0c0b", "#ece8e1", "#8d867e", "#2b2824") if NEGRO
                              else ("#ffffff", "#131211", "#8b8781", "#e6e3de"))
SALIDA = WEB.parent / ("Portfolio-Maia-Cheb-Terrab-negro.pdf" if NEGRO
                       else "Portfolio-Maia-Cheb-Terrab.pdf")

doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Saol";src:url("{F}SaolText-Regular.otf");font-weight:400}}
@font-face{{font-family:"Saol";src:url("{F}SaolText-RegularItalic.otf");
           font-weight:400;font-style:italic}}
@font-face{{font-family:"Lausanne";src:url("{F}TWKLausanne-400.otf");font-weight:400}}
@font-face{{font-family:"Lausanne";src:url("{F}TWKLausanne-500.otf");font-weight:500}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0}}
html,body{{background:{PAPEL};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{width:210mm;height:297mm;padding:22mm 20mm 18mm;color:{TINTA};
      font-family:"Lausanne",sans-serif;font-size:9pt;line-height:1.3;
      display:flex;flex-direction:column}}
.etq{{font-size:8pt;color:{SUAVE}}}
h1{{font-family:"Saol",serif;font-size:34pt;font-weight:400;letter-spacing:-.012em;
    line-height:1.04;margin:42mm 0 0}}

/* el link es lo unico que esta hoja tiene que conseguir: subrayado, con flecha
   y con aire alrededor. Es un <a> real, clickeable en el PDF. */
.link{{display:inline-block;margin-top:9mm;font-family:"Saol",serif;
       font-size:17pt;line-height:1.2;color:{TINTA};text-decoration:underline;
       text-underline-offset:3.5pt;text-decoration-thickness:.6pt}}
.link .flecha{{font-family:"Lausanne",sans-serif;font-size:13pt;
               text-decoration:none;display:inline-block;margin-left:2mm}}

.nota{{margin-top:10mm;max-width:104mm;color:{SUAVE}}}
footer{{margin-top:auto;padding-top:7mm;border-top:.5pt solid {LINEA};
        display:flex;justify-content:space-between;gap:10mm;
        font-size:8pt;color:{SUAVE}}}
</style></head><body>

<div class="etq">Maia Cheb Terrab · Diseñadora gráfica (FADU-UBA) · Buenos Aires</div>

<h1>Portfolio</h1>
<a class="link" href="{URL}">{VISIBLE}<span class="flecha">&#8599;</span></a>

<p class="nota">El portfolio es una página web. Las piezas se ven en su proporción
real y se abren en tamaño completo, las animaciones se ven en movimiento, y
<i>Salto de Fe</i> es una pieza web que se recorre sola.</p>

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
