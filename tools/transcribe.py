"""Transcripción con timestamps por palabra (faster-whisper, CPU int8).

Salida por archivo en _work/transcripts/<id>.json:
  {"language","duration","segments":[{start,end,text,words:[{text,start,end,prob}]}],
   "words":[{text,start,end,prob}]}
y además <id>.srt y <id>.hf.json (formato de palabras compatible con HyperFrames).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from vecommon import log, read_json, resolve_project, run, work_dir, write_json

DEFAULT_MODEL = "large-v3-turbo"


def srt_time(t: float) -> str:
    h, rem = divmod(max(t, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def extract_wav(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
             "-af", "highpass=f=70,lowpass=f=8000", dst])
    return dst


def transcribe_file(src: Path, out_base: Path, model_name: str, language: str | None,
                    initial_prompt: str | None) -> dict:
    from faster_whisper import WhisperModel

    wav = extract_wav(src, out_base.with_suffix(".16k.wav"))
    log(f"Transcribiendo {src.name} con {model_name}…")
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=0)
    import soundfile as sf
    audio, _sr = sf.read(str(wav), dtype="float32")
    segments, info = model.transcribe(
        audio, language=language, word_timestamps=True, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 250, "speech_pad_ms": 120},
        beam_size=5, condition_on_previous_text=False, initial_prompt=initial_prompt)
    segs, words = [], []
    for s in segments:
        ws = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
               "prob": round(w.probability, 3)} for w in (s.words or []) if w.word.strip()]
        segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": ws})
        words.extend(ws)
    data = {"source": str(src), "language": info.language, "duration": round(info.duration, 3),
            "model": model_name, "segments": segs, "words": words}
    write_json(out_base.with_suffix(".json"), data)

    with open(out_base.with_suffix(".srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n{s['text']}\n\n")
    hf = []
    for i, w in enumerate(words):
        hf.append({"text": w["text"], "start": w["start"], "end": w["end"], "type": "word"})
        if i + 1 < len(words):
            hf.append({"text": " ", "start": w["end"], "end": words[i + 1]["start"], "type": "spacing"})
    write_json(out_base.with_suffix(".hf.json"), {"words": hf})
    (out_base.with_suffix(".txt")).write_text(
        "\n".join(f"[{s['start']:7.2f}-{s['end']:7.2f}] {s['text']}" for s in segs) + "\n", encoding="utf-8")
    log(f"  {len(words)} palabras, idioma {info.language}")
    return data


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--files", nargs="*", help="ids o rutas; por defecto todo el crudo con audio")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="tiny|base|small|medium|large-v3|large-v3-turbo")
    ap.add_argument("--language", default="es")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)

    proj = resolve_project(a.project)
    w = work_dir(proj)
    inv = read_json(w / "analysis" / "inventory.json")
    if inv is None:
        raise SystemExit("Primero corre: ve analyze <proyecto>")
    # Prompt inicial con vocabulario del guion (nombres de marca, términos) mejora la precisión.
    vocab = None
    gl = w / "guion.json"
    if gl.exists():
        g = read_json(gl)
        vocab = " ".join(g.get("text", "").split()[:120])

    targets = []
    for it in inv:
        if it["kind"] != "video" and it["kind"] != "audio":
            continue
        if not it.get("audio"):
            continue
        if a.files:
            if it["id"] not in a.files and it["path"] not in a.files:
                continue
        elif it.get("role") not in ("crudo", "audio"):
            continue
        targets.append(it)
    for it in targets:
        base = w / "transcripts" / it["id"]
        if base.with_suffix(".json").exists() and not a.force:
            log(f"ya transcripto: {it['id']}")
            continue
        src = Path(it.get("mezzanine") or it["path"])
        transcribe_file(src, base, a.model, a.language, vocab)
    print(w / "transcripts")


if __name__ == "__main__":
    main()
