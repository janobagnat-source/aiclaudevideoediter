"""Inventario y análisis visual/sonoro de todo el material de un proyecto.

Genera en _work/analysis/:
  inventory.json        todos los archivos con metadatos (duración, resolución, fps, audio)
  sheets/<n>.jpg        hojas de contacto (grilla de fotogramas con timecode) para revisar visualmente
  scenes/<n>.json       cortes de escena (brolls) con un frame representativo por escena
  audio/<n>.json        loudness integrado, picos y tramos de silencio
  faces/<n>.json        centro de la cara/sujeto por segundo (para zooms y reencuadre 9:16)
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from vecommon import (client_of, kind_of, log, media_info, read_json, resolve_project, run,
                      work_dir, write_json)

SKIP_DIRS = {"_work", "entregables", "node_modules", ".git"}


def iter_media(base: Path):
    for p in sorted(base.rglob("*")):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(base).parts) \
                and not p.name.startswith("."):
            yield p


def safe_name(p: Path, base: Path) -> str:
    rel = p.relative_to(base).with_suffix("")
    return "__".join(rel.parts).replace(" ", "_")


def contact_sheet(src: Path, out: Path, duration: float, cols: int = 6, rows: int = 5) -> None:
    n = cols * rows
    step = max(duration / n, 0.04)
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (f"fps=1/{step:.4f},scale=320:-2:force_original_aspect_ratio=decrease,"
          f"drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{rows}:padding=4:margin=4")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-frames:v", "1", "-q:v", "4", out], check=False)


def detect_scenes(src: Path, out_json: Path, thumbs_dir: Path) -> list[dict]:
    try:
        from scenedetect import ContentDetector, detect
    except ImportError:
        log("scenedetect no instalado; salto detección de escenas")
        return []
    scenes = detect(str(src), ContentDetector(threshold=27.0), show_progress=False)
    res = []
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    for i, (a, b) in enumerate(scenes or []):
        s, e = a.get_seconds(), b.get_seconds()
        mid = (s + e) / 2
        th = thumbs_dir / f"{out_json.stem}_s{i:03d}.jpg"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{mid:.3f}", "-i", src, "-frames:v", "1",
             "-vf", "scale=480:-2", "-q:v", "4", th], check=False)
        res.append({"i": i, "start": round(s, 3), "end": round(e, 3), "dur": round(e - s, 3), "thumb": str(th)})
    write_json(out_json, res)
    return res


def audio_stats(src: Path, out_json: Path) -> dict:
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af",
             "loudnorm=print_format=json,silencedetect=noise=-38dB:d=0.35", "-f", "null", "-"],
            capture=True, check=False)
    txt = r.stderr or ""
    stats: dict = {}
    try:
        j = txt[txt.rindex("{"): txt.rindex("}") + 1]
        ln = json.loads(j)
        stats["lufs"] = float(ln["input_i"])
        stats["true_peak"] = float(ln["input_tp"])
        stats["lra"] = float(ln["input_lra"])
    except Exception:
        pass
    sil, cur = [], None
    for line in txt.splitlines():
        if "silence_start:" in line:
            cur = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end:" in line and cur is not None:
            end = float(line.split("silence_end:")[1].split()[0])
            sil.append([round(cur, 3), round(end, 3)])
            cur = None
    stats["silences"] = sil
    write_json(out_json, stats)
    return stats


def face_track(src: Path, out_json: Path, every: float = 0.5) -> dict:
    """Centro del rostro principal (normalizado 0-1) muestreado cada `every` s (detector YuNet de OpenCV)."""
    import cv2

    model = Path(__file__).parent / "models" / "face_detection_yunet_2023mar.onnx"
    cap = cv2.VideoCapture(str(src))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    det = None
    samples = []
    step = max(int(fps * every), 1)
    for fi in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]
        sc = 640 / max(w, h)
        small = cv2.resize(frame, (int(w * sc), int(h * sc)))
        if det is None:
            det = cv2.FaceDetectorYN.create(str(model), "", (small.shape[1], small.shape[0]), 0.7, 0.3, 50)
        _, faces = det.detect(small)
        if faces is not None and len(faces):
            x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])[:4]
            samples.append({"t": round(fi / fps, 2), "x": round(float(x + fw / 2) / small.shape[1], 3),
                            "y": round(float(y + fh / 2) / small.shape[0], 3),
                            "size": round(float(fh) / small.shape[0], 3)})
    cap.release()
    res = {"fps": fps, "samples": samples}
    if samples:
        xs = sorted(s["x"] for s in samples)
        ys = sorted(s["y"] for s in samples)
        res["median"] = {"x": xs[len(xs) // 2], "y": ys[len(ys) // 2]}
        res["coverage"] = round(len(samples) / max(1, math.ceil(total / step)), 2)
    write_json(out_json, res)
    return res


def prep_media(src: Path, dst: Path, fps: int, max_h: int) -> None:
    """Mezzanine CFR H.264 apto para edición precisa (keyframes frecuentes, sin VFR, sin HDR)."""
    info = media_info(src)
    v = info.get("video", {})
    dst.parent.mkdir(parents=True, exist_ok=True)
    vf = [f"fps={fps}"]
    if v.get("height") and max(v["height"], v.get("width") or 0) > max_h:
        if (v.get("height") or 0) >= (v.get("width") or 0):
            vf.append(f"scale=-2:{max_h}")
        else:
            vf.append(f"scale={max_h}:-2" if max_h <= 1080 else f"scale=-2:{max_h}")
    if v.get("hdr"):
        vf.insert(0, "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
                     "zscale=t=bt709:m=bt709:r=tv")
    vf.append("format=yuv420p")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:v:0", "-map", "0:a:0?",
           "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-g", str(fps // 2), "-bf", "0", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
           "-movflags", "+faststart", dst]
    run(cmd)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--fps", type=int, default=30, help="fps del mezzanine/edición (30 por defecto)")
    ap.add_argument("--max-h", type=int, default=2160, help="lado máximo del mezzanine (2160 por defecto)")
    ap.add_argument("--no-prep", action="store_true", help="no transcodificar mezzanines")
    ap.add_argument("--no-faces", action="store_true")
    ap.add_argument("--include-client-broll", action="store_true", default=True)
    a = ap.parse_args(argv)

    proj = resolve_project(a.project)
    client = client_of(proj)
    w = work_dir(proj)
    an = w / "analysis"
    roots = [("proyecto", proj)]
    for sub in ("marca", "broll"):
        if (client / sub).exists():
            roots.append((f"cliente/{sub}", client / sub))

    inv = []
    for label, base in roots:
        for p in iter_media(base):
            k = kind_of(p)
            if k == "other":
                continue
            item = media_info(p) if k in ("video", "audio") else {"path": str(p), "kind": k, "bytes": p.stat().st_size}
            item["origin"] = label
            item["role"] = p.relative_to(base).parts[0] if len(p.relative_to(base).parts) > 1 else label
            item["id"] = safe_name(p, base) if label == "proyecto" else f"{label.split('/')[1]}__{safe_name(p, base)}"
            if k == "image":
                try:
                    from PIL import Image
                    with Image.open(p) as im:
                        item["image"] = {"width": im.width, "height": im.height, "mode": im.mode}
                except Exception:
                    pass
            inv.append(item)
    write_json(an / "inventory.json", inv)
    log(f"{len(inv)} archivos inventariados")

    for item in inv:
        p = Path(item["path"])
        if item["kind"] == "video" and item.get("duration"):
            sid = item["id"]
            contact_sheet(p, an / "sheets" / f"{sid}.jpg", item["duration"])
            if item["role"] in ("broll", "cliente/broll") or item["origin"] == "cliente/broll":
                item["scenes"] = detect_scenes(p, an / "scenes" / f"{sid}.json", an / "scenes" / "thumbs")
            if item.get("audio"):
                item["audio_stats"] = audio_stats(p, an / "audio" / f"{sid}.json")
            if not a.no_faces:
                item["faces"] = {k: v for k, v in face_track(p, an / "faces" / f"{sid}.json").items() if k != "samples"}
            if not a.no_prep:
                dst = w / "media" / f"{sid}.mp4"
                if not dst.exists():
                    prep_media(p, dst, a.fps, a.max_h)
                item["mezzanine"] = str(dst)
        elif item["kind"] == "audio":
            item["audio_stats"] = audio_stats(p, an / "audio" / f"{item['id']}.json")
    write_json(an / "inventory.json", inv)

    # Resumen legible
    lines = ["# Inventario de material", ""]
    for item in inv:
        v = item.get("video", {})
        desc = f"{v.get('width')}x{v.get('height')} {v.get('fps')}fps" if v else ""
        dur = f"{item.get('duration', 0):.1f}s" if item.get("duration") else ""
        lufs = item.get("audio_stats", {}).get("lufs")
        lines.append(f"- [{item['kind']}] `{item['id']}` {dur} {desc} {'LUFS ' + str(lufs) if lufs else ''}"
                     f" — {item['origin']} ({Path(item['path']).name})")
    (an / "INVENTARIO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(an / "INVENTARIO.md")


if __name__ == "__main__":
    main()
