# -*- coding: utf-8 -*-
"""Genera las miniaturas de las tapas del índice.

Las tapas son los originales de 2400px (alrededor de 1MB cada una) y se
muestran a 340px. Publicado eso son 5MB antes de que aparezca la primera
imagen. Acá se reducen a 680px —el doble del tamaño de la card, para que se
vean nítidas en pantalla Retina— con sips, que ya viene en la Mac.

No cambia nada a la vista: misma imagen, mismo recorte.

    python3 hacer_miniaturas.py
"""
import pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

AQUI = pathlib.Path(__file__).resolve().parent
WEB = AQUI.parent
DESTINO = WEB / "assets" / "miniaturas"
ANCHO = 680
CALIDAD = "72"


def mini(src):
    """Devuelve la ruta de la miniatura de src, relativa a web/."""
    return f"assets/miniaturas/{pathlib.Path(src).parent.name}-{pathlib.Path(src).name}"


def generar(fuentes):
    DESTINO.mkdir(parents=True, exist_ok=True)
    hechas, ahorro = 0, 0
    for src in fuentes:
        orig = WEB / src
        if not orig.exists():
            continue
        dest = WEB / mini(src)
        if dest.exists() and dest.stat().st_mtime >= orig.stat().st_mtime:
            continue
        subprocess.run(["sips", "-Z", str(ANCHO), "-s", "format", "jpeg",
                        "-s", "formatOptions", CALIDAD,
                        str(orig), "--out", str(dest)],
                       capture_output=True, check=True)
        ahorro += orig.stat().st_size - dest.stat().st_size
        hechas += 1
        print(f"  {src}  {orig.stat().st_size//1024}KB → {dest.stat().st_size//1024}KB")
    return hechas, ahorro


if __name__ == "__main__":
    from build_fichas import SECCIONES, tapa
    fuentes = [t["src"] for t in (tapa(s) for s in SECCIONES) if t]
    print(f"Miniaturas a {ANCHO}px:")
    n, ahorro = generar(fuentes)
    print(f"\n{n} generadas · {ahorro/1048576:.1f} MB menos en el índice")
