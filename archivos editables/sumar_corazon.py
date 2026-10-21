# -*- coding: utf-8 -*-
"""Toma las fotos de 'Corazón/' (antes Descargas/AMORYCORAZONES) y las prepara para la web."""
import json, pathlib, subprocess

AQUI  = pathlib.Path(__file__).resolve().parent
WEB   = AQUI.parent
ORIG  = WEB.parent / "Corazón"
SLUG  = "09-corazon"
LARGO = 2400

# las fotos de palabras y carteles vinieron de costado: se giran para que se
# lean (grados en sentido horario)
ROTAR = {"Untitled-3-08.png": 90,    # Yo Tú Él
         "Untitled-3-09.jpg": 90,    # Amor / Roma (reflejo, se lee espejado)
         "Untitled-3-12.png": 270,   # Amor Escapes
         "Untitled-3-13.png": 90,    # Enamorarse
         "Untitled-3-14.jpg": 90,    # ¿Y si?
         "Untitled-4.jpg": 90}       # Emociones
# el gato a color repite al de blanco y negro (Untitled-3-04-2): queda el ByN
FUERA = {"Untitled-3-04.jpg"}

destino = WEB / "assets" / SLUG
destino.mkdir(parents=True, exist_ok=True)
for viejo in destino.glob("*.jpg"):
    viejo.unlink()

fuentes = sorted(f for f in ORIG.iterdir()
                 if f.suffix.lower() in (".png", ".jpg", ".jpeg") and not f.name.startswith(".")
                 and f.name not in FUERA)
nuevos = []
for i, f in enumerate(fuentes, 1):
    dst = destino / f"{i:02d}.jpg"
    giro = ["-r", str(ROTAR[f.name])] if f.name in ROTAR else []
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84",
                    "-Z", str(LARGO), *giro, str(f), "--out", str(dst)], capture_output=True)
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)],
                          capture_output=True, text=True).stdout
    ow = oh = 0
    for line in dims.splitlines():
        if "pixelWidth:" in line:  ow = int(line.split(":")[1])
        if "pixelHeight:" in line: oh = int(line.split(":")[1])
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)],
                          capture_output=True, text=True).stdout
    w = h = 0
    for line in dims.splitlines():
        if "pixelWidth:" in line:  w = int(line.split(":")[1])
        if "pixelHeight:" in line: h = int(line.split(":")[1])
    if f.name in ROTAR:  # girada de costado: el original queda al revés
        ow, oh = oh, ow
    nuevos.append({"proj": SLUG, "idx": f"{i:02d}", "gif": False,
                   "src": f"assets/{SLUG}/{dst.name}", "w": w, "h": h,
                   "kb": round(dst.stat().st_size / 1024), "ow": ow, "oh": oh})
    print(f"  {f.name[:46]:46} -> {dst.name}  {ow}x{oh}")

ruta = AQUI / "web_assets.json"
assets = [a for a in json.loads(ruta.read_text(encoding="utf-8")) if a["proj"] != SLUG] + nuevos
ruta.write_text(json.dumps(assets, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(nuevos)} imágenes · {len(assets)} piezas en total")
