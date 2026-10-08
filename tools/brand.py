"""Extrae la línea gráfica del cliente a clientes/<cliente>/marca/brand.json.

Lee logos/imágenes de referencia (paleta dominante por k-means), fuentes incluidas (.ttf/.otf/.woff2)
y un brand.md / paleta.md opcional con HEX explícitos (tienen prioridad). El resultado es la fuente de
verdad de colores y tipografías para todos los motion graphics.
"""
from __future__ import annotations

import argparse
import colorsys
import re
from pathlib import Path

import numpy as np

from vecommon import CLIENTES, FONT_EXT, IMAGE_EXT, read_json, write_json

HEX = re.compile(r"#[0-9a-fA-F]{6}\b")


def palette(img_path: Path, k: int = 6) -> list[tuple[str, float]]:
    from PIL import Image
    from sklearn.cluster import KMeans

    with Image.open(img_path) as im:
        im = im.convert("RGBA")
        im.thumbnail((256, 256))
        arr = np.asarray(im).reshape(-1, 4)
    arr = arr[arr[:, 3] > 200][:, :3]  # ignora transparencia
    if len(arr) < k:
        return []
    km = KMeans(n_clusters=k, n_init=4, random_state=0).fit(arr)
    counts = np.bincount(km.labels_)
    out = []
    for c, n in sorted(zip(km.cluster_centers_, counts), key=lambda x: -x[1]):
        r, g, b = (int(v) for v in c)
        out.append((f"#{r:02x}{g:02x}{b:02x}", round(n / counts.sum(), 3)))
    return out


def lum(hx: str) -> float:
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(hx: str) -> float:
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(r, g, b)[1]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cliente")
    a = ap.parse_args(argv)
    marca = CLIENTES / a.cliente / "marca"
    if not marca.exists():
        raise SystemExit(f"No existe {marca}")
    prev = read_json(marca / "brand.json", {}) or {}
    explicit, labeled, font_h, font_b = [], {}, None, None
    roles = {"primary": ("primario", "primary", "principal"), "secondary": ("secundario", "secondary"),
             "accent": ("acento", "accent"), "dark": ("oscuro", "fondo", "dark", "background"),
             "light": ("claro", "texto", "light", "blanco")}
    for md in list(marca.glob("*.md")) + list(marca.glob("*.txt")):
        for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
            hx = HEX.findall(line)
            low = line.lower()
            explicit += hx
            if hx:
                for role, keys in roles.items():
                    if role not in labeled and any(k in low for k in keys):
                        labeled[role] = hx[0].lower()
                        break
            m = re.search(r"tipograf[ií]a\s*(t[ií]tulos|titulares|headings?)\W+([A-Za-z][\w ]+)", line, re.I)
            if m:
                font_h = m.group(2).strip().split(" (")[0]
            m = re.search(r"tipograf[ií]a\s*(textos?|cuerpo|body)\W+([A-Za-z][\w ]+)", line, re.I)
            if m:
                font_b = m.group(2).strip().split(" (")[0]
    logos = [p for p in marca.rglob("*") if p.suffix.lower() in IMAGE_EXT and p.suffix.lower() != ".svg"]
    svgs = [p for p in marca.rglob("*.svg")]
    for s in svgs:
        explicit += HEX.findall(s.read_text(encoding="utf-8", errors="ignore"))
    extracted = []
    for lg in logos[:12]:
        try:
            extracted += [c for c, share in palette(lg) if share > 0.03]
        except Exception:
            pass
    colors = list(dict.fromkeys([c.lower() for c in explicit] + extracted))
    vivid = sorted([c for c in colors if sat(c) > 0.35 and 0.12 < lum(c) < 0.9], key=lambda c: -sat(c))
    darks = sorted([c for c in colors if lum(c) < 0.15], key=lum)
    lights = sorted([c for c in colors if lum(c) > 0.85], key=lambda c: -lum(c))
    fonts = [str(p) for p in marca.rglob("*") if p.suffix.lower() in FONT_EXT]
    logo_main = next((str(p) for p in sorted(marca.rglob("*")) if "logo" in p.name.lower()
                      and p.suffix.lower() in IMAGE_EXT), str(logos[0]) if logos else None)
    brand = {
        "cliente": a.cliente,
        "colors": {
            "primary": labeled.get("primary") or (vivid[0] if vivid else "#ff3b30"),
            "secondary": labeled.get("secondary") or (vivid[1] if len(vivid) > 1 else "#ffd60a"),
            "accent": labeled.get("accent") or (vivid[2] if len(vivid) > 2 else (vivid[0] if vivid else "#00e5ff")),
            "dark": labeled.get("dark") or (darks[0] if darks else "#0b0b0f"),
            "light": labeled.get("light") or (lights[0] if lights else "#ffffff"),
        },
        "palette_all": colors[:16],
        "fonts": {
            "heading": font_h or prev.get("fonts", {}).get("heading") or "Montserrat",
            "body": font_b or prev.get("fonts", {}).get("body") or "Inter",
            "files": fonts,
        },
        "logo": prev.get("logo") or logo_main,
        "logos": [str(p) for p in logos + svgs],
        "style_notes": prev.get("style_notes", ""),
    }
    for fam in {brand["fonts"]["heading"], brand["fonts"]["body"]}:
        try:
            from fonts import ensure
            ensure(fam, make3d=True)
        except Exception as e:  # fuente no disponible en Fontsource: usar archivos locales
            print(f"aviso fuente {fam}: {e}")
    write_json(marca / "brand.json", brand)
    print(marca / "brand.json")
    print(brand["colors"], brand["fonts"]["heading"], brand["logo"])


if __name__ == "__main__":
    main()
