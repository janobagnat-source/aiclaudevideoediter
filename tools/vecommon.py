"""Utilidades compartidas por las herramientas del editor (rutas, ffprobe, JSON, créditos)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENTES = ROOT / "clientes"
LIBRARY = ROOT / "library"
ENGINE = ROOT / "engine-remotion"

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mts", ".mxf", ".hevc"}
AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".aif", ".aiff"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".heic", ".tif", ".tiff", ".bmp"}
MODEL_EXT = {".glb", ".gltf", ".fbx", ".obj", ".usdz"}
DOC_EXT = {".md", ".txt", ".docx", ".pdf", ".rtf", ".srt", ".vtt", ".json"}
FONT_EXT = {".ttf", ".otf", ".woff", ".woff2"}


def log(msg: str) -> None:
    print(f"[ve] {msg}", file=sys.stderr, flush=True)


def run(cmd: list[str], check: bool = True, capture: bool = False, **kw) -> subprocess.CompletedProcess:
    log(" ".join(str(c) for c in cmd)[:300])
    return subprocess.run([str(c) for c in cmd], check=check, text=True,
                          capture_output=capture, **kw)


def kind_of(p: Path) -> str:
    e = p.suffix.lower()
    if e in VIDEO_EXT:
        return "video"
    if e in AUDIO_EXT:
        return "audio"
    if e in IMAGE_EXT:
        return "image"
    if e in MODEL_EXT:
        return "model3d"
    if e in FONT_EXT:
        return "font"
    if e in DOC_EXT:
        return "doc"
    return "other"


def ffprobe(path: Path) -> dict:
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
            capture=True, check=False)
    if r.returncode != 0:
        return {}
    return json.loads(r.stdout or "{}")


def media_info(path: Path) -> dict:
    """Resumen compacto de un archivo multimedia."""
    d = ffprobe(path)
    info: dict = {"path": str(path), "kind": kind_of(path), "bytes": path.stat().st_size}
    fmt = d.get("format", {})
    if "duration" in fmt:
        info["duration"] = round(float(fmt["duration"]), 3)
    for s in d.get("streams", []):
        if s.get("codec_type") == "video" and "video" not in info:
            fr = s.get("avg_frame_rate") or s.get("r_frame_rate") or "0/1"
            num, den = (fr.split("/") + ["1"])[:2]
            fps = float(num) / float(den) if float(den or 0) else 0.0
            rot = 0
            for sd in s.get("side_data_list", []) or []:
                if "rotation" in sd:
                    rot = int(sd["rotation"])
            rot = int(s.get("tags", {}).get("rotate", rot))
            w, h = s.get("width"), s.get("height")
            if abs(rot) in (90, 270):
                w, h = h, w
            info["video"] = {"codec": s.get("codec_name"), "width": w, "height": h,
                             "fps": round(fps, 3), "pix_fmt": s.get("pix_fmt"), "rotation": rot,
                             "vfr": s.get("avg_frame_rate") != s.get("r_frame_rate"),
                             "hdr": s.get("color_transfer") in ("smpte2084", "arib-std-b67")}
        if s.get("codec_type") == "audio" and "audio" not in info:
            info["audio"] = {"codec": s.get("codec_name"), "sample_rate": int(s.get("sample_rate", 0)),
                             "channels": s.get("channels")}
    return info


def read_json(p: Path, default=None):
    p = Path(p)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data) -> Path:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def resolve_project(arg: str) -> Path:
    """Acepta ruta absoluta/relativa o 'cliente/proyecto'."""
    p = Path(arg)
    if p.exists():
        return p.resolve()
    parts = arg.strip("/").split("/")
    if len(parts) == 2:
        cand = CLIENTES / parts[0] / "proyectos" / parts[1]
        if cand.exists():
            return cand
    raise SystemExit(f"No encuentro el proyecto '{arg}'. Usa clientes/<cliente>/proyectos/<proyecto> o <cliente>/<proyecto>.")


def client_of(project: Path) -> Path:
    # clientes/<cliente>/proyectos/<proyecto>
    return project.parent.parent


def work_dir(project: Path) -> Path:
    w = project / "_work"
    w.mkdir(exist_ok=True)
    return w


def add_credit(project: Path | None, entry: dict) -> None:
    """Registra licencia/atribución de cada asset externo descargado."""
    target = (work_dir(project) / "credits.json") if project else (LIBRARY / "credits.json")
    data = read_json(target, [])
    entry = {**entry, "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if not any(e.get("local") == entry.get("local") for e in data):
        data.append(entry)
    write_json(target, data)


def which(name: str) -> bool:
    return shutil.which(name) is not None


def env(name: str) -> str | None:
    v = os.environ.get(name)
    return v.strip() if v else None
