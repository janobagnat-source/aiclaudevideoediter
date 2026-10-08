"""Render, masterización de audio, control de calidad y entrega.

  ve render <proyecto> --stills 0.5,2,5.2      fotogramas sueltos para revisión visual (rápido)
  ve render <proyecto> --draft                 video a 50% de resolución para revisar ritmo/sonido
  ve render <proyecto>                         FINAL: render 100%, master -14 LUFS / -1 dBTP, QC y copia a entregables/
Opciones: --lufs -14 (redes) | -16 (VSL/YouTube) · --version 2 · --name sufijo
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from vecommon import ENGINE, client_of, log, media_info, read_json, resolve_project, run, work_dir

FMT_NAME = {(1080, 1920): "9x16", (1920, 1080): "16x9", (1080, 1080): "1x1", (1080, 1350): "4x5",
            (2160, 3840): "9x16_4K", (3840, 2160): "16x9_4K"}


def node_render(edit: Path, out: Path, extra: list[str]) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["node", ENGINE / "scripts" / "render.mjs", edit, out, *extra], cwd=ENGINE)


def master(src: Path, dst: Path, lufs: float, tp: float = -1.0) -> dict:
    """Loudnorm 2 pasadas (EBU R128) sobre el audio; el video se copia sin recomprimir."""
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af",
             f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"], capture=True, check=False)
    txt = r.stderr
    m = json.loads(txt[txt.rindex("{"): txt.rindex("}") + 1])
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k",
         "-movflags", "+faststart", dst])
    return m


def qc(path: Path) -> dict:
    info = media_info(path)
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", "blackdetect=d=0.25:pix_th=0.06",
             "-af", "ebur128=peak=true", "-f", "null", "-"], capture=True, check=False)
    blacks = [l.split("black_start:")[1].split()[0] for l in r.stderr.splitlines() if "black_start:" in l]
    lufs = tp = None
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    for line in tail.splitlines():
        if line.strip().startswith("I:"):
            lufs = float(line.split()[1])
        if line.strip().startswith("Peak:"):
            tp = float(line.split()[1])
    rep = {"duration": info.get("duration"), "video": info.get("video"), "audio": info.get("audio"),
           "lufs": lufs, "true_peak": tp, "black_segments_at": blacks, "MB": round(path.stat().st_size / 1e6, 1)}
    return rep


def write_srt(edit: dict, out: Path) -> None:
    words = edit["captions"]["words"]

    def ts(t):
        h, r = divmod(max(0, t), 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    lines, i, n = [], 0, 1
    while i < len(words):
        chunk = words[i:i + 7]
        lines.append(f"{n}\n{ts(chunk[0]['start'])} --> {ts(chunk[-1]['end'])}\n{' '.join(w['text'] for w in chunk)}\n")
        i += 7
        n += 1
    out.write_text("\n".join(lines), encoding="utf-8")


def contact_from_video(video: Path, out: Path, n: int = 24) -> None:
    d = media_info(video).get("duration", 10)
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
         f"fps={n}/{d:.3f},scale=270:-2,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x4:padding=3",
         "-frames:v", "1", out], check=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--stills")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--frames")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--version", type=int)
    ap.add_argument("--name", default="")
    ap.add_argument("--crf", default="16")
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    w = work_dir(proj)
    edit_p = w / "edit.json"
    edit = read_json(edit_p)
    if not edit:
        raise SystemExit("Falta _work/edit.json (corre ve build)")
    renders = w / "renders"
    if a.stills:
        node_render(edit_p, renders / "stills" / "frame.jpg", [f"--still={a.stills}", "--scale=0.5"])
        print(renders / "stills")
        return
    if a.draft:
        out = renders / "draft.mp4"
        extra = ["--scale=0.5", "--crf=24", "--preset=veryfast"] + ([f"--frames={a.frames}"] if a.frames else [])
        node_render(edit_p, out, extra)
        contact_from_video(out, renders / "draft_sheet.jpg")
        print(out)
        print(renders / "draft_sheet.jpg")
        return
    raw = renders / "final_raw.mp4"
    node_render(edit_p, raw, [f"--crf={a.crf}", "--preset=slow"])
    cliente = client_of(proj).name
    fmt = FMT_NAME.get((edit["width"], edit["height"]), f"{edit['width']}x{edit['height']}")
    ent = proj / "entregables"
    ent.mkdir(exist_ok=True)
    v = a.version or (1 + len(list(ent.glob(f"*_{fmt}_v*.mp4"))))
    base = f"{cliente}_{proj.name}_{fmt}{('_' + a.name) if a.name else ''}_v{v}"
    final = ent / f"{base}.mp4"
    m = master(raw, final, a.lufs)
    rep = qc(final)
    rep["loudnorm_input"] = {k: m[k] for k in ("input_i", "input_tp")}
    write_srt(edit, ent / f"{base}.srt")
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", final, "-frames:v", "1", "-q:v", "2", ent / f"{base}_thumb.jpg"])
    contact_from_video(final, w / "renders" / f"{base}_sheet.jpg")
    used = {s["src"] for s in edit["sfx"] + edit["music"]} | {b["src"] for b in edit["broll"]} | \
        {v for g in edit["graphics"] for v in g["props"].values() if isinstance(v, str)}
    lib_credits = read_json(Path(__file__).parent.parent / "library" / "credits.json", [])
    credits = [c for c in read_json(w / "credits.json", []) + lib_credits
               if any(c["local"].endswith(u.split("/", 1)[-1]) for u in used if "/" in u)]
    attributions = [c for c in credits if c.get("license") not in ("cc0", "pexels", "pixabay", "unsplash", "own", "iconify")]
    with open(ent / f"{base}_creditos.txt", "w", encoding="utf-8") as f:
        f.write("Assets de terceros usados (licencias libres)\n\n")
        for c in credits:
            f.write(f"- {c.get('kind')}: {c.get('title') or Path(c['local']).name} — {c.get('author') or ''} "
                    f"[{c.get('license')}] {c.get('page') or ''}\n")
        if attributions:
            f.write("\nREQUIEREN ATRIBUCIÓN (poner en descripción del anuncio/video):\n")
            for c in attributions:
                f.write(f"  {c.get('attribution') or (str(c.get('title')) + ' by ' + str(c.get('author')) + ' (' + str(c.get('license')) + ')')}\n")
    (w / "renders" / f"{base}_qc.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False))
    log(f"QC: {rep}")
    print(final)


if __name__ == "__main__":
    main()
