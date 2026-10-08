"""Recorta al sujeto (persona) de un corte del timeline → video con alfa para poner texto/gráficos DETRÁS.

  ve cutout <proyecto> <n_corte> [--quality best]
Genera _work/cutouts/cut<n>.webm (alineado al inicio del corte). Luego en overlays.json:
  "cuts": {"0": {"cutout": "_work/cutouts/cut0.webm", "zoom": [{"t":0,"s":1.0},{"t":3,"s":1.08}],
                 "behind": [{"component": "HookTitle", "start": 0, "duration": 2.5, "props": {...}}]}}
Usa `hyperframes remove-background` (modelo local, CPU). ~1-3 s de proceso por segundo de video.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from vecommon import ROOT, read_json, resolve_project, run, work_dir


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("cut", type=int)
    ap.add_argument("--quality", default="balanced", choices=["fast", "balanced", "best"])
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    w = work_dir(proj)
    edl = read_json(w / "edl.json")
    c = edl["cuts"][a.cut]
    ov = read_json(w / "overlays.json", {}) or {}
    o = ov.get("cuts", {}).get(str(a.cut), {})
    cin, cout = float(o.get("in", c["in"])), float(o.get("out", c["out"]))
    inv = {i["id"]: i for i in read_json(w / "analysis" / "inventory.json", [])}
    src = c.get("src") or inv[c["source"]].get("mezzanine") or inv[c["source"]]["path"]
    out_dir = w / "cutouts"
    out_dir.mkdir(exist_ok=True)
    seg = out_dir / f"cut{a.cut}_src.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cin:.3f}", "-i", src, "-t", f"{cout - cin:.3f}", "-an",
         "-c:v", "libx264", "-crf", "14", "-preset", "fast", seg])
    out = out_dir / f"cut{a.cut}.webm"
    env = {**os.environ, "HYPERFRAMES_PYTHON": str(ROOT / ".venv" / "bin" / "python")}
    ver = (ROOT / "engine-hyperframes.version").read_text().strip()
    run(["npx", "--yes", f"hyperframes@{ver}", "remove-background", seg, "-o", out, "--quality", a.quality], env=env)
    print(Path(out).relative_to(proj))


if __name__ == "__main__":
    main()
