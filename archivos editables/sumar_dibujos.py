# -*- coding: utf-8 -*-
"""Lleva los dibujos recortados a la web, con su epígrafe."""
import json, pathlib, subprocess

AQUI = pathlib.Path(__file__).resolve().parent
WEB  = AQUI.parent
ORIG = WEB.parent / "Las casas no vuelan" / "dibujos recortados"
SLUG = "00a-dibujos"

destino = WEB / "assets" / SLUG
destino.mkdir(parents=True, exist_ok=True)
for viejo in destino.glob("*.jpg"):
    viejo.unlink()

fichas = json.loads((ORIG / "epigrafes.json").read_text(encoding="utf-8"))
nuevos = []
for i, f in enumerate(fichas, 1):
    src = ORIG / f["archivo"]
    dst = destino / f"{i:02d}.jpg"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86",
                    "-Z", "1600", str(src), "--out", str(dst)], capture_output=True)
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)],
                          capture_output=True, text=True).stdout
    w = h = 0
    for line in dims.splitlines():
        if "pixelWidth:" in line:  w = int(line.split(":")[1])
        if "pixelHeight:" in line: h = int(line.split(":")[1])
    nuevos.append({"proj": SLUG, "idx": f"{i:02d}", "gif": False,
                   "src": f"assets/{SLUG}/{dst.name}", "w": w, "h": h,
                   "kb": round(dst.stat().st_size / 1024), "ow": w, "oh": h,
                   "cap": f["epigrafe"]})
    print(f"  {dst.name}  {w}x{h}  {f['epigrafe']}")

ruta = AQUI / "web_assets.json"
assets = [a for a in json.loads(ruta.read_text(encoding="utf-8")) if a["proj"] != SLUG] + nuevos
ruta.write_text(json.dumps(assets, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(nuevos)} dibujos · {len(assets)} piezas en total")
