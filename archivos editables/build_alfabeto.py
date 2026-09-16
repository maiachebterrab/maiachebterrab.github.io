# -*- coding: utf-8 -*-
"""Paneles de presentación del alfabeto. No toca las letras: solo las compone.

01  hero      palabra grande en negro sobre el verde del key visual
02  especimen la lámina del alfabeto elegida (ya existente)
03  variantes celdas comparando las dos versiones de cada letra
"""
import json, pathlib, subprocess, urllib.parse

AQUI   = pathlib.Path(__file__).resolve().parent
WEB    = AQUI.parent
LETRAS = WEB.parent / "Las casas no vuelan" / "letras escaneadas (png)"
PLACA  = WEB.parent / "Las casas no vuelan" / "pruebas" / "prueba-1-alfabeto.pdf"
SALIDA = WEB.parent / "Las casas no vuelan" / "paneles alfabeto"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CAMPO, TINTA = "#fff", "#111"   # blanco y negro: sin color por ahora
F = "file:///Users/maiacheb/Library/Fonts/"

SALIDA.mkdir(parents=True, exist_ok=True)
sizes = json.loads((LETRAS / "sizes.json").read_text())
CLAVE = {**{c: c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}, "Ñ": "NN"}


def furl(p): return "file://" + urllib.parse.quote(str(p))


def glifo(clave, alto_px, tinta="negro"):
    """Un glifo escaneado. Dos copias apiladas: el lápiz flojo gana cuerpo,
    el trazo firme no cambia. Mismo truco que en las pruebas."""
    w, h = sizes[clave]
    ancho = alto_px * w / h
    src = furl(LETRAS / f"{clave}-{tinta}.png")
    return (f'<span style="position:relative;display:inline-block;height:{alto_px}px;'
            f'width:{ancho:.1f}px;vertical-align:baseline">'
            f'<img src="{src}" style="position:absolute;inset:0;width:100%;height:100%">'
            f'<img src="{src}" style="position:absolute;inset:0;width:100%;height:100%"></span>')


def palabra(texto, alto_px, track=0.10, tinta="negro"):
    partes = []
    for ch in texto.upper():
        if ch == " ":
            partes.append(f'<span style="display:inline-block;width:{alto_px*0.42:.0f}px"></span>')
        elif CLAVE.get(ch) in sizes:
            partes.append(glifo(CLAVE[ch], alto_px, tinta))
            partes.append(f'<span style="display:inline-block;width:{alto_px*track:.0f}px"></span>')
    return "".join(partes)


def render(html, nombre, ancho, alto):
    src = SALIDA / f"{nombre}.html"
    src.write_text(html, encoding="utf-8")
    png = SALIDA / f"{nombre}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={ancho},{alto}", "--virtual-time-budget=30000",
                    f"--screenshot={png}", furl(src)], capture_output=True, timeout=300)
    return png


BASE = f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:"Mono";src:url("{F}GeistMono-Regular.ttf")}}
*{{box-sizing:border-box;margin:0}}
body{{font-family:"Mono",monospace;color:{TINTA};-webkit-font-smoothing:antialiased}}
</style>"""

# ---- 01 · hero: la palabra sobre el verde ----
W1, H1 = 2400, 1350
hero = BASE + f"""
<style>
body{{background:{CAMPO};width:{W1}px;height:{H1}px;padding:110px 130px;
      display:flex;flex-direction:column;justify-content:center;position:relative}}
.pie{{position:absolute;left:130px;bottom:96px}}
.linea{{white-space:nowrap;line-height:1;margin-bottom:46px}}
.pie{{font-size:30px;letter-spacing:.10em;text-transform:uppercase;color:rgba(17,17,17,.55)}}
</style>
<div>
  <div class="linea">{palabra("BESTIARIO", 240)}</div>
</div>
<div class="pie">Maia · alfabeto a partir de la letra de la infancia</div>
"""
p1 = render(hero, "01-hero", W1, H1)

# ---- 03 · variantes: las dos versiones de cada letra ----
PARES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")   # sin la Ñ, a pedido
celdas = []
for c in PARES:
    a = glifo(c, 130)
    wb, hb = sizes[f"lc_{c.lower()}"] if f"lc_{c.lower()}" in sizes else (None, None)
    b = glifo(f"lc_{c.lower()}", 130) if wb else ""
    celdas.append(f"""<div class="celda">
      <div class="par"><div class="caja">{a}</div><div class="caja">{b}</div></div>
      <div class="rot">{c}</div>
    </div>""")

W3, H3 = 2400, 2010
variantes = BASE + f"""
<style>
body{{background:#fff;width:{W3}px;height:{H3}px;padding:92px 120px;
      display:flex;flex-direction:column;justify-content:space-between}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:30px 28px}}
.par{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.caja{{height:196px;background:#f4f4f4;display:flex;align-items:center;justify-content:center}}
.rot{{margin-top:11px;font-size:24px;letter-spacing:.10em;color:rgba(17,17,17,.45)}}
.pie{{font-size:30px;letter-spacing:.10em;text-transform:uppercase;color:rgba(17,17,17,.5)}}
</style>
<div class="grid">{''.join(celdas)}</div>
<div class="pie">Dos versiones de cada letra, de dos hojas distintas</div>
"""
p3 = render(variantes, "03-variantes", W3, H3)

# ---- 02 · especimen: la lamina elegida, tal cual ----
import shutil
placa_web = WEB / "assets" / "00b-alfabeto" / "01.jpg"
p2 = SALIDA / "02-especimen.jpg"
if placa_web.exists() and not p2.exists():
    shutil.copy(placa_web, p2)

# ---- a la web, en orden: hero, especimen, variantes ----
destino = WEB / "assets" / "00b-alfabeto"
destino.mkdir(parents=True, exist_ok=True)
for viejo in destino.glob("*.jpg"):
    viejo.unlink()

CAPS = {1: "hero", 2: "especimen", 3: "variantes"}
nuevos = []
for i, src in enumerate([p1, p2, p3], 1):
    dst = destino / f"{i:02d}.jpg"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86",
                    "-Z", "2400", str(src), "--out", str(dst)], capture_output=True)
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)],
                          capture_output=True, text=True).stdout
    w = h = 0
    for line in dims.splitlines():
        if "pixelWidth:" in line:  w = int(line.split(":")[1])
        if "pixelHeight:" in line: h = int(line.split(":")[1])
    nuevos.append({"proj": "00b-alfabeto", "idx": f"{i:02d}", "gif": False,
                   "src": f"assets/00b-alfabeto/{dst.name}", "w": w, "h": h,
                   "kb": round(dst.stat().st_size / 1024), "ow": w, "oh": h})
    print(f"  {dst.name}  {w}x{h}  {round(dst.stat().st_size/1024)} KB  ({CAPS[i]})")

ruta = AQUI / "web_assets.json"
assets = [a for a in json.loads(ruta.read_text(encoding="utf-8"))
          if a["proj"] != "00b-alfabeto"] + nuevos
ruta.write_text(json.dumps(assets, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(assets)} piezas en total")
