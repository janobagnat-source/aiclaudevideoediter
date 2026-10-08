"""Fuentes locales (Google Fonts vía Fontsource/npm) para que el render no dependa de red.

  ve font "Montserrat" "Bebas Neue"      descarga pesos 400-900 (latin + latin-ext) a library/fonts/<Familia>/
  ve font --defaults                     set curado para ads (Montserrat, Inter, Anton, Bebas Neue, Poppins, ...)
También convierte la fuente a typeface.json (texto 3D) con --3d.
Manifest: library/fonts/manifest.json  {familia: [{weight, style, file}]}
"""
from __future__ import annotations

import argparse
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

from vecommon import ENGINE, LIBRARY, log, read_json, write_json

DEFAULTS = ["Montserrat", "Inter", "Anton", "Bebas Neue", "Poppins", "Oswald", "Playfair Display", "Archivo Black",
            "Space Grotesk", "DM Sans", "Sora", "Bricolage Grotesque", "Plus Jakarta Sans", "Outfit", "Barlow Condensed",
            "Permanent Marker", "Caveat"]
WEIGHTS = ("400", "500", "600", "700", "800", "900")
FONTS = LIBRARY / "fonts"


def slug(family: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def ensure(family: str, make3d: bool = False) -> list[dict]:
    manifest = read_json(FONTS / "manifest.json", {}) or {}
    if family in manifest and all(Path(FONTS / x["file"]).exists() for x in manifest[family]):
        return manifest[family]
    pkg = f"@fontsource/{slug(family)}"
    dest = FONTS / family.replace(" ", "")
    dest.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run(["npm", "pack", pkg, "--silent"], cwd=td, capture_output=True, text=True)
        if r.returncode != 0:
            log(f"⚠️ {family}: no está en Fontsource ({r.stderr.strip()[:120]})")
            return []
        tgz = next(Path(td).glob("*.tgz"))
        with tarfile.open(tgz) as t:
            t.extractall(td, filter="data")
        files = Path(td) / "package" / "files"
        entries = []
        for f in sorted(files.glob("*.woff2")):
            m = re.match(rf"{slug(family)}-(latin|latin-ext)-(\d+)-(normal|italic)\.woff2$", f.name)
            if not m:
                continue
            subset, w, st = m.groups()
            if w not in WEIGHTS and not (w == "400"):
                continue
            out = dest / f.name
            out.write_bytes(f.read_bytes())
            entries.append({"weight": w, "style": st, "subset": subset, "file": str(out.relative_to(FONTS))})
            if make3d and subset == "latin" and st == "normal" and w in ("800", "900", "400"):
                woff = files / f.name.replace(".woff2", ".woff")
                if woff.exists():
                    (ENGINE / "public" / "fonts3d").mkdir(parents=True, exist_ok=True)
                    subprocess.run(["node", str(ENGINE / "scripts" / "ttf2typeface.mjs"), str(woff),
                                    str(ENGINE / "public" / "fonts3d" / f"{family.replace(' ', '')}-{w}.typeface.json")],
                                   check=False)
    manifest[family] = entries
    write_json(FONTS / "manifest.json", manifest)
    log(f"{family}: {len(entries)} archivos")
    return entries


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("families", nargs="*")
    ap.add_argument("--defaults", action="store_true")
    ap.add_argument("--3d", dest="make3d", action="store_true")
    a = ap.parse_args(argv)
    fams = (DEFAULTS if a.defaults else []) + a.families
    for f in fams:
        ensure(f, a.make3d)
    print(FONTS / "manifest.json")


if __name__ == "__main__":
    main()
