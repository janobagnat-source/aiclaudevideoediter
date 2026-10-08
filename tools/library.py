"""Librería local de SFX y música (indexada, con licencias).

  ve library build            descarga SFX CC0 curados (Freesound vía Openverse o API) + música epic/cinematic
                              y regenera los SFX sintetizados. Crea library/index.json
  ve library search whoosh    busca en el índice local por tag/nombre (devuelve rutas + duración)
  ve library list             resumen por categoría
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vecommon import LIBRARY, log, media_info, read_json, write_json

SFX_QUERIES = {
    "whoosh": ["whoosh", "swoosh fast", "whoosh transition"],
    "impact": ["cinematic impact", "boom hit", "trailer hit"],
    "riser": ["riser", "tension rise", "uplifter"],
    "subdrop": ["sub drop", "bass drop"],
    "glitch": ["glitch", "digital glitch"],
    "pop": ["pop", "bubble pop"],
    "click": ["mouse click", "ui click"],
    "typing": ["keyboard typing", "typewriter"],
    "camera": ["camera shutter"],
    "notification": ["notification", "ding bell"],
    "cash": ["cash register", "coins"],
    "swipe": ["swipe", "paper swipe"],
    "reverse": ["reverse cymbal", "reverse"],
    "heartbeat": ["heartbeat"],
    "crowd": ["applause", "crowd cheer"],
    "tape": ["tape stop", "record scratch"],
}
MUSIC_QUERIES = {
    "epic": ["epic cinematic", "epic orchestral", "trailer"],
    "cinematic": ["cinematic", "cinematic ambient", "dramatic"],
    "motivational": ["inspiring", "motivational", "uplifting"],
    "tech": ["technology", "electronic corporate"],
    "hiphop": ["hip hop beat", "trap beat"],
    "dark": ["dark tension", "suspense"],
}


KENNEY_PACKS = ["impact-sounds", "interface-sounds", "sci-fi-sounds", "digital-audio", "casino-audio", "ui-audio"]


def kenney(pack: str):
    """Packs de audio CC0 de kenney.nl (se descomprimen en library/sfx/kenney/<pack>/)."""
    import io
    import re as _re
    import zipfile

    import requests

    from vecommon import add_credit
    dest = LIBRARY / "sfx" / "kenney" / pack
    if dest.exists() and any(dest.rglob("*.ogg")):
        return
    html = requests.get(f"https://kenney.nl/assets/{pack}", timeout=40).text
    m = _re.search(r"https://kenney\.nl/media/pages/assets/[^\"]+\.zip", html)
    if not m:
        log(f"kenney {pack}: no encontré el zip")
        return
    z = zipfile.ZipFile(io.BytesIO(requests.get(m.group(0), timeout=120).content))
    dest.mkdir(parents=True, exist_ok=True)
    for name in z.namelist():
        if name.lower().endswith((".ogg", ".wav", ".mp3")):
            out = dest / Path(name).name
            out.write_bytes(z.read(name))
            add_credit(None, {"local": str(out), "kind": "sfx", "title": Path(name).stem, "author": "Kenney.nl",
                              "license": "cc0", "page": f"https://kenney.nl/assets/{pack}"})
    log(f"kenney {pack}: ok")


def build(n_sfx: int, n_music: int):
    import subprocess

    from stock import fetch, search

    subprocess.run([sys.executable, str(Path(__file__).parent / "sfx_synth.py")], check=True)
    for pack in KENNEY_PACKS:
        try:
            kenney(pack)
        except Exception as e:
            log(f"kenney {pack}: {e}")
    for cat, qs in SFX_QUERIES.items():
        for q in qs:
            for it in search("sfx", q, n_sfx):
                try:
                    fetch(it, "sfx", LIBRARY / "sfx" / "_dl" / cat, None, q)
                except Exception as e:
                    log(f"falló {it['id']}: {e}")
    for cat, qs in MUSIC_QUERIES.items():
        for q in qs:
            for it in search("music", q, n_music):
                try:
                    fetch(it, "music", LIBRARY / "music" / "_dl" / cat, None, q)
                except Exception as e:
                    log(f"falló {it['id']}: {e}")
    index()


def index():
    credits = {c["local"]: c for c in read_json(LIBRARY / "credits.json", [])}
    items = []
    for p in sorted(LIBRARY.rglob("*")):
        if p.suffix.lower() not in (".wav", ".mp3", ".ogg", ".flac", ".m4a"):
            continue
        rel = p.relative_to(LIBRARY)
        kind = rel.parts[0]  # sfx | music
        if "synth" in rel.parts:
            cat = p.stem.split("_")[0]
            lic, src = "own", "synth"
        elif "kenney" in rel.parts:
            cat = "kenney-" + rel.parts[2]
            lic, src = "cc0", "kenney.nl"
        else:
            cat = rel.parts[2] if len(rel.parts) > 3 else rel.parts[-2]
            c = credits.get(str(p), {})
            lic, src = c.get("license", "?"), c.get("page")
        info = media_info(p)
        items.append({"path": str(p), "kind": kind, "category": cat, "name": p.stem,
                      "duration": info.get("duration"), "license": lic, "source": src,
                      "title": credits.get(str(p), {}).get("title"),
                      "author": credits.get(str(p), {}).get("author")})
    write_json(LIBRARY / "index.json", items)
    log(f"{len(items)} sonidos indexados")


def search_local(q: str, kind: str | None):
    items = read_json(LIBRARY / "index.json", [])
    ql = q.lower()
    res = [i for i in items if (ql in i["category"].lower() or ql in i["name"].lower()
                                or ql in (i.get("title") or "").lower()) and (not kind or i["kind"] == kind)]
    print(json.dumps(res, ensure_ascii=False, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--sfx", type=int, default=3)
    b.add_argument("--music", type=int, default=3)
    sub.add_parser("index")
    s = sub.add_parser("search")
    s.add_argument("q")
    s.add_argument("--kind", choices=["sfx", "music"])
    sub.add_parser("list")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        build(a.sfx, a.music)
    elif a.cmd == "index":
        index()
    elif a.cmd == "search":
        search_local(a.q, a.kind)
    else:
        items = read_json(LIBRARY / "index.json", [])
        from collections import Counter
        for (k, c), n in sorted(Counter((i["kind"], i["category"]) for i in items).items()):
            print(f"{k:6} {c:14} {n}")


if __name__ == "__main__":
    main()
