# -*- coding: utf-8 -*-
"""Recorta las fotos del acordeón físico y las suma a la web.

El recorte saca la tela de arriba y el vacío de abajo: el abanico llena el cuadro.
"""
import json, pathlib, subprocess, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
WEB  = AQUI.parent
ORIG = WEB.parent / "Salto de Fe" / "acordeon"
SLUG = "07-acordeon"
ALTO_DESDE, ALTO_HASTA = 0.17, 0.86   # fracción del alto que se conserva

destino = WEB / "assets" / SLUG
destino.mkdir(parents=True, exist_ok=True)
for viejo in destino.glob("*.jpg"):
    viejo.unlink()

fuentes = sorted(f for f in ORIG.iterdir()
                 if f.suffix.lower() in (".heic", ".jpg", ".jpeg", ".png")
                 and not f.name.startswith("."))
nuevos = []
for i, f in enumerate(fuentes, 1):
    with tempfile.TemporaryDirectory() as tmp:
        plano = pathlib.Path(tmp) / "plano.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "100",
                        str(f), "--out", str(plano)], capture_output=True)
        dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(plano)],
                              capture_output=True, text=True).stdout
        w = h = 0
        for line in dims.splitlines():
            if "pixelWidth:" in line:  w = int(line.split(":")[1])
            if "pixelHeight:" in line: h = int(line.split(":")[1])
        alto = round(h * (ALTO_HASTA - ALTO_DESDE))
        offset = round(h * ALTO_DESDE)
        # sips recorta centrado, así que primero se corre el encuadre y después se corta
        subprocess.run(["sips", "--cropOffset", str(offset), "0",
                        "-c", str(alto), str(w), str(plano)], capture_output=True)
        dst = destino / f"{i:02d}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86",
                        "-Z", "2400", str(plano), "--out", str(dst)], capture_output=True)
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)],
                          capture_output=True, text=True).stdout
    dw = dh = 0
    for line in dims.splitlines():
        if "pixelWidth:" in line:  dw = int(line.split(":")[1])
        if "pixelHeight:" in line: dh = int(line.split(":")[1])
    nuevos.append({"proj": SLUG, "idx": f"{i:02d}", "gif": False,
                   "src": f"assets/{SLUG}/{dst.name}", "w": dw, "h": dh,
                   "kb": round(dst.stat().st_size / 1024), "ow": dw, "oh": dh})
    print(f"  {f.name} -> {dst.name}  {dw}x{dh}  {round(dst.stat().st_size/1024)} KB")

ruta = AQUI / "web_assets.json"
assets = [a for a in json.loads(ruta.read_text(encoding="utf-8")) if a["proj"] != SLUG] + nuevos
ruta.write_text(json.dumps(assets, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(nuevos)} foto(s) del acordeón · {len(assets)} piezas en total")
