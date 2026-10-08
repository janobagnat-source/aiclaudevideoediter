"""Corte multicámara automático de un ad desde una grabación larga (2 cámaras sincronizadas, audio de cam1).

  ve multicam <cliente>/<proyecto> --raw-start 180 --raw-end 260 [--guion guion.md]

1. Busca cada frase del guion dentro del rango [raw-start, raw-end] del crudo (última toma buena).
2. Dentro de cada toma alinea palabra por palabra con el guion: las palabras dichas que NO están en el guion
   (muletillas, agregados, repeticiones) se eliminan con un corte.
3. Refina cada punto de corte al valle de energía más cercano (5 ms) para no cortar sílabas.
4. Asigna cámara: frontal (cam1) en hook, CTA y frases clave; lateral (cam2) como apoyo y para ocultar cortes
   internos (cada corte dentro de una frase cambia de cámara).
5. Genera mezzanines 9:16 por cámara (crop a la cara, lanczos + unsharp) con la voz procesada (-16 LUFS).

Salida: _work/edl.json (palabras con ortografía del guion) y _work/MULTICAM.md (reporte de omisiones/cambios).
Config de cámaras/crops: clientes/<c>/multicam.json  {"cams": {"cam1": {"file": ..., "role": "frontal"}, ...}}
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from align import find_takes, norm
from rapidfuzz import fuzz
from guion import parse, read_any
from vecommon import client_of, log, read_json, resolve_project, run, work_dir, write_json


def energy_db(wav: Path) -> tuple[np.ndarray, int]:
    a, sr = sf.read(str(wav))
    if a.ndim > 1:
        a = a.mean(1)
    hop = sr // 200
    e = np.sqrt(np.convolve(a ** 2, np.ones(hop * 2) / (hop * 2), mode="same"))[::hop]
    return 20 * np.log10(e + 1e-6), 200


def valley(db, fps, t, lo, hi):
    """Punto de menor energía entre lo y hi (segundos), sesgado hacia t."""
    i0, i1 = int(max(lo, 0) * fps), min(int(hi * fps), len(db))
    if i1 <= i0:
        return t
    seg = db[i0:i1]
    dist = np.abs(np.arange(i0, i1) / fps - t)
    k = np.argmin(seg + dist * 8)  # 8 dB de penalización por segundo de distancia
    return (i0 + k) / fps


def word_end(db, fps, w_end, nxt_start):
    """Fin real de la palabra: último frame por encima del umbral antes del siguiente inicio."""
    i0, i1 = int(w_end * fps) - 6, min(int(min(nxt_start, w_end + 0.35) * fps), len(db))
    seg = db[i0:i1]
    if not len(seg):
        return w_end
    thr = np.percentile(db[max(0, i0 - 200):i0 + 200], 92) - 26
    idx = np.where(seg > thr)[0]
    return (i0 + idx[-1]) / fps + 0.02 if len(idx) else w_end


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--raw-start", type=float, required=True)
    ap.add_argument("--raw-end", type=float, required=True)
    ap.add_argument("--guion")
    ap.add_argument("--transcript", help="json de transcripción del crudo completo (cam1)")
    ap.add_argument("--max-gap", type=float, default=0.30)
    ap.add_argument("--keep-gap", type=float, default=0.06)
    ap.add_argument("--no-mezz", action="store_true")
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    client = client_of(proj)
    w = work_dir(proj)
    cfg = read_json(client / "multicam.json")
    tr = read_json(Path(a.transcript) if a.transcript else client / cfg["transcript"])
    words = [dict(x, n=norm(x["text"])) for x in tr["words"] if a.raw_start - 1 <= x["start"] <= a.raw_end + 1 and norm(x["text"])]
    for x in words:
        x["source"], x["src"] = "raw", None
    g = parse(read_any(Path(a.guion) if a.guion else proj / "guion.md"))
    OFF = a.raw_start - 1.0
    seg_dur = a.raw_end - a.raw_start + 2.0
    src = w / "src"
    src.mkdir(exist_ok=True)

    # ---- mezzanines 9:16 (crop por cámara a la cara) + voz procesada
    cams = cfg["cams"]
    if not a.no_mezz:
        from analyze import face_track
        from voice import process_voice
        for cid, c in cams.items():
            tmp = src / f"{cid}_seg.mp4"
            if (src / f"{cid}_9x16.mp4").exists():
                c["face_y"] = (read_json(src / f"{cid}_faces.json", {}) or {}).get("median", {}).get("y", 0.25)
                continue
            if not tmp.exists():
              run(["ffmpeg", "-v", "error", "-y", "-ss", f"{OFF:.3f}", "-i", client / c["file"], "-t", f"{seg_dur:.3f}",
                 "-vf", "fps=30", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-c:a", "aac", "-b:a", "256k", tmp])
            ft = read_json(src / f"{cid}_faces.json") or face_track(tmp, src / f"{cid}_faces.json", 0.5)
            fx = ft.get("median", {}).get("x", 0.5)
            iw, ih = 1920, 1080
            cw = int(round(ih * 9 / 16 / 2) * 2)
            x0 = int(min(max(fx * iw - cw / 2, 0), iw - cw))
            if not (src / f"{cid}_v.mp4").exists():
              run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-vf",
                 f"crop={cw}:{ih}:{x0}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,format=yuv420p",
                 "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "15", "-bf", "0", "-an", src / f"{cid}_v.mp4"])
            c["face_y"] = ft.get("median", {}).get("y", 0.25)
        voice_src = src / f"{cfg['audio_from']}_seg.mp4"
        if not (src / "voice_ok").exists():
            process_voice(voice_src, src / "voice.wav")
            (src / "voice_ok").write_text("ok")
        for cid in cams:
            if (src / f"{cid}_9x16.mp4").exists():
                continue
            run(["ffmpeg", "-v", "error", "-y", "-i", src / f"{cid}_v.mp4", "-i", src / "voice.wav", "-map", "0:v", "-map", "1:a",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", src / f"{cid}_9x16.mp4"])
            (src / f"{cid}_v.mp4").unlink(missing_ok=True)
        write_json(src / "cams.json", cams)
    cams = read_json(src / "cams.json", cams)
    wav = src / "voice16k.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", src / f"{cfg['audio_from']}_seg.mp4", "-ac", "1", "-ar", "16000", wav])
    db, efps = energy_db(wav)
    seg_tr = w / "transcript_seg.json"
    if not seg_tr.exists():
        # Parakeet (vía HyperFrames): transcribe TODO lo hablado (incluidas charlas y arranques fallidos)
        import os
        import tempfile
        ver = (Path(__file__).parent.parent / "engine-hyperframes.version").read_text().strip()
        with tempfile.TemporaryDirectory() as td:
            env = {**os.environ, "HYPERFRAMES_PYTHON": str(Path(__file__).parent.parent / ".venv" / "bin" / "python")}
            subprocess.run(["npx", "--yes", f"hyperframes@{ver}", "transcribe", str(wav.resolve()), "--engine", "parakeet",
                            "--language", "es", "--json", "-d", td], check=True, capture_output=True, text=True, env=env)
            raw = json.loads((Path(td) / "transcript.json").read_text())
        ww = [{"text": x["text"], "start": round(x["start"] + OFF, 3), "end": round(x["end"] + OFF, 3), "prob": 1.0} for x in raw]
        write_json(seg_tr, {"words": ww, "engine": "parakeet"})
    def nnorm(t):  # el ASR escribe números en dígitos («10») y el guion en letras («diez»)
        n = norm(t)
        if n.isdigit():
            try:
                from num2words import num2words
                return norm(num2words(int(n), lang="es"))
            except Exception:
                return n
        return n
    words = [dict(x, n=nnorm(x["text"]), source="raw", src=None) for x in read_json(seg_tr)["words"] if norm(x["text"])]

    # ---- alinear frases del guion y cortar fuera de guion
    report = ["# Multicam — reporte", ""]
    pieces = []
    def choose(text, after, min_score=62):
        """Última toma buena de `text` que empieza después de `after` (orden cronológico del guion)."""
        takes = find_takes(text, words, min_score)
        later = [x for x in takes if x["start"] >= after - 0.3]
        takes = later or takes
        if not takes:
            return None
        best = max(x["score"] for x in takes)
        return [x for x in takes if x["score"] >= best - 6][-1]

    def clauses(text, seps):
        parts = [x.strip() for x in re.split(rf"(?<=[{seps}])\s+", text) if x.strip()]
        out = []
        for x in parts:  # cláusulas de al menos 3 palabras
            if out and (len(x.split()) < 3 or len(out[-1].split()) < 3):
                out[-1] += " " + x
            else:
                out.append(x)
        return out

    units, after = [], 0.0
    for s in g["sentences"]:
        t = choose(s["text"], after)
        plan = [(s["text"], t)] if t else []
        if not t or t["score"] < 98:
            # retomas partidas: armar la frase por cláusulas desde las mejores tomas (en orden)
            for seps in (":;.?!", ":;.?!,"):
                cl = clauses(s["text"], seps)
                if len(cl) < 2:
                    continue
                alt, aft = [], after
                for c in cl:
                    tc = choose(c, aft, 80)
                    if not tc:
                        break
                    alt.append((c, tc))
                    aft = tc["end"]
                if len(alt) == len(cl) and sum(x[1]["score"] for x in alt) / len(alt) > (t["score"] + 1.5 if t else 0):
                    plan = alt
                    report.append(f"   [{s['i']}] armada por cláusulas: " + " | ".join(f"{x[1]['start']:.2f}" for x in alt))
                    break
        if not plan:
            report.append(f"⚠️ [{s['i']}] NO ENCONTRADA: {s['text']}")
            continue
        after = plan[-1][1]["end"]
        for text_u, tu in plan:
            units.append((s, text_u, tu))

    for s, text_u, t in units:
        ws = words[t["w0"]:t["w1"]]
        stoks = text_u.split()
        sm = difflib.SequenceMatcher(a=[x["n"] for x in ws], b=[norm(x) for x in stoks], autojunk=False)
        keep = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "replace" and i2 - i1 == j2 - j1 and any(
                    fuzz.ratio(ws[i1 + k]["n"], norm(stoks[j1 + k])) < 60 and max(len(ws[i1 + k]["n"]), len(norm(stoks[j1 + k]))) > 3
                    and not (ws[i1 + k]["n"] in norm(stoks[j1 + k]) or norm(stoks[j1 + k]) in ws[i1 + k]["n"])
                    for k in range(i2 - i1)):  # «el»↔«al», «lo»↔«la»: variación dicha, se conserva el audio
                # palabras distintas (no es variación ortográfica): lo dicho sobra y lo del guion falta
                report.append(f"   [{s['i']}] eliminado fuera de guion: «{' '.join(x['text'] for x in ws[i1:i2])}»")
                keep.append((None, None))
                if keep and len(keep) > 1 and keep[-2][0] is not None:
                    keep.pop()
                    wd, tx = keep[-1]
                    keep[-1] = (wd, tx + " " + " ".join(stoks[j1:j2]))
                    keep.append((None, None))
                    report.append(f"   ⚠️ [{s['i']}] no detectado por ASR, agregado al subtítulo (revisar): «{' '.join(stoks[j1:j2])}»")
            elif tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
                for k in range(i2 - i1):
                    keep.append((ws[i1 + k], stoks[j1 + k]))
            elif tag == "replace":
                # p.ej. "extras" vs "extra": se queda con la palabra dicha si es una sola
                if i2 - i1 == 1:
                    keep.append((ws[i1], " ".join(stoks[j1:j2])))
                else:
                    # el subtítulo solo lleva texto del guion: se reparte el texto del guion entre las palabras dichas
                    report.append(f"   [{s['i']}] reemplazo «{' '.join(x['text'] for x in ws[i1:i2])}» → «{' '.join(stoks[j1:j2])}» (subtítulo = guion)")
                    n_said, n_scr = i2 - i1, j2 - j1
                    for k in range(n_said):
                        a0, a1 = -(-k * n_scr // n_said), -(-(k + 1) * n_scr // n_said)
                        keep.append((ws[i1 + k], " ".join(stoks[j1 + a0:j1 + a1])))
            elif tag == "delete":
                report.append(f"   [{s['i']}] eliminado fuera de guion: «{' '.join(x['text'] for x in ws[i1:i2])}»")
                keep.append((None, None))  # marca de corte
            elif tag == "insert":
                if keep and keep[-1][0] is not None and j2 - j1 <= 2:
                    wd, tx = keep[-1]
                    keep[-1] = (wd, tx + " " + " ".join(stoks[j1:j2]))
                    report.append(f"   ⚠️ [{s['i']}] no detectado por ASR, agregado al subtítulo (revisar audio): «{' '.join(stoks[j1:j2])}»")
                else:
                    report.append(f"   ⚠️ [{s['i']}] del guion no dicho: «{' '.join(stoks[j1:j2])}»")
        # agrupar en tramos continuos (corta en eliminaciones y pausas largas)
        cur = []
        for wd, txt in keep + [(None, None)]:
            if wd is None or (cur and wd["start"] - cur[-1][0]["end"] > a.max_gap):
                if cur:
                    pieces.append({"sentence": s["i"], "section": s.get("section"), "ws": cur, "hard": wd is None})
                cur = [] if wd is None else [(wd, txt)]
            else:
                cur.append((wd, txt))
        report.append(f"[{s['i']}] {t['start']:.2f}-{t['end']:.2f} score={t['score']} «{text_u}»")

    # ---- límites refinados + recorte de silencios internos (por energía)
    def speech_thr(t):
        i = int((t - OFF) * efps)
        return np.percentile(db[max(0, i - 400):i + 400], 92) - 24
    cuts = []
    for k, p in enumerate(pieces):
        w0, w1 = p["ws"][0][0], p["ws"][-1][0]
        idx1 = next(i for i, x in enumerate(words) if x is w1)
        nxt = words[idx1 + 1]["start"] if idx1 + 1 < len(words) else w1["end"] + 0.5
        idx0 = next(i for i, x in enumerate(words) if x is w0)
        prv_end = words[idx0 - 1]["end"] if idx0 > 0 else w0["start"] - 0.5
        a_in = valley(db, efps, w0["start"] - 0.05 - OFF, max(prv_end, w0["start"] - 0.25) - OFF, w0["start"] + 0.04 - OFF) + OFF
        e_real = word_end(db, efps, w1["end"] - OFF, nxt - OFF) + OFF
        b_out = valley(db, efps, e_real + 0.05 - OFF, e_real - 0.02 - OFF, min(nxt, e_real + 0.22) - OFF) + OFF
        # silencios internos > max_gap
        i0, i1 = int((a_in - OFF) * efps), int((b_out - OFF) * efps)
        thr = speech_thr((a_in + b_out) / 2)
        quiet = db[i0:i1] < thr
        segs_, start, run_ = [], a_in, None
        for j, q in enumerate(quiet):
            t = OFF + (i0 + j) / efps
            if q and run_ is None:
                run_ = t
            elif not q and run_ is not None:
                if t - run_ > a.max_gap:
                    segs_.append((start, run_ + a.keep_gap))
                    start = t - a.keep_gap
                run_ = None
        segs_.append((start, b_out))
        segs_ = [x for x in segs_ if x[1] - x[0] >= 0.12] or [(a_in, b_out)]
        # cada palabra va al tramo más cercano (los tiempos del ASR pueden caer en un silencio recortado: nunca se pierde texto)
        assign = {}
        for wd, tx in p["ws"]:
            m = (wd["start"] + wd["end"]) / 2
            si = min(range(len(segs_)), key=lambda q: 0 if segs_[q][0] <= m <= segs_[q][1] else min(abs(m - segs_[q][0]), abs(m - segs_[q][1])))
            assign.setdefault(si, []).append((wd, tx))
        for si, (x0, x1) in enumerate(segs_):
            if si not in assign:
                continue
            cuts.append({"piece": {**p, "ws": assign[si]}, "in": x0, "out": x1, "intra": si > 0})
    for k in range(1, len(cuts)):
        if cuts[k]["in"] < cuts[k - 1]["out"]:
            mid = (cuts[k]["in"] + cuts[k - 1]["out"]) / 2
            cuts[k]["in"] = cuts[k - 1]["out"] = mid
    # ---- cámaras: cambio por frase; dentro de una frase solo si ambos planos duran >= 1.3 s (si no, jump cut + zoom)
    n_sent = len(g["sentences"])
    out = []
    cam = None
    for k, c in enumerate(cuts):
        p = c["piece"]
        s_i = p["sentence"]
        new_sentence = k == 0 or cuts[k - 1]["piece"]["sentence"] != s_i
        key = s_i == 0 or s_i == n_sent - 1 or (p.get("section") or "").upper() in ("HOOK", "CTA")
        dur = c["out"] - c["in"]
        if k == 0:
            cam = "cam1"
        elif new_sentence:
            cam = "cam1" if key else ("cam2" if cam == "cam1" else "cam1")
        elif c["in"] - cuts[k - 1]["out"] > 1.0 and not key:
            cam = "cam2" if cam == "cam1" else "cam1"  # otra toma dentro de la frase: cambiar de cámara disimula el salto
        elif dur >= 1.3 and (out and out[-1]["out"] - out[-1]["in"] >= 1.3):
            cam = "cam2" if cam == "cam1" else "cam1"
        ws = []
        for wd, txt in p["ws"]:
            e = {"text": txt, "start": round(max(wd["start"], c["in"]) - OFF, 3), "end": round(min(wd["end"], c["out"]) - OFF, 3)}
            if not txt.strip():
                if ws:
                    ws[-1]["end"] = e["end"]  # palabra dicha sin texto propio de guion: extiende la anterior
                continue
            ws.append(e)
        out.append({"sentence": s_i, "source": cam, "src": str((src / f"{cam}_9x16.mp4").resolve()),
                    "in": round(c["in"] - OFF, 3), "out": round(c["out"] - OFF, 3),
                    "text": " ".join(x["text"] for x in ws), "section": p.get("section"), "words": ws, "cues": [], "intra": c.get("intra", False)})
    # fusionar tramos contiguos en la misma cámara
    merged = []
    for c in out:
        if merged and merged[-1]["source"] == c["source"] and abs(merged[-1]["out"] - c["in"]) < 0.02 and merged[-1]["sentence"] == c["sentence"]:
            merged[-1]["out"] = c["out"]
            merged[-1]["words"] += c["words"]
            merged[-1]["text"] += " " + c["text"]
        else:
            merged.append(c)
    tot = sum(c["out"] - c["in"] for c in merged)
    write_json(w / "edl.json", {"cuts": merged, "duration": round(tot, 3), "raw_offset": OFF})
    report += ["", f"**{len(merged)} cortes · {tot:.2f}s**", ""] + [f"- {c['source']} {c['in'] + OFF:8.2f}-{c['out'] + OFF:8.2f} «{c['text']}»" for c in merged]
    (w / "MULTICAM.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(w / "MULTICAM.md")


if __name__ == "__main__":
    main()
