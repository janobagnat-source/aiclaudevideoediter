"""Alinea el guion con las transcripciones del crudo y arma la lista de cortes (EDL).

- Encuentra TODAS las tomas de cada frase del guion (repeticiones/retakes) en todos los clips.
- Elige la mejor toma: mayor similitud con el guion + claridad (probabilidad ASR), y ante empate la ÚLTIMA
  (en grabación, la última toma suele ser la buena).
- Recorta cada toma a palabra exacta con colas (pad) y elimina pausas internas largas (tighten).
- Sin guion (--free): limpia muletillas, silencios y arranques fallidos (se queda con la última repetición).

Salida: _work/edl.json + _work/EDL.md (con tomas alternativas para revisar/cambiar).
Para forzar una toma: _work/edl_overrides.json  {"<frase_i>": {"take": <n>} | {"skip": true} |
                                                  {"in": s, "out": s, "source": id}}
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

from rapidfuzz import fuzz

from vecommon import log, read_json, resolve_project, work_dir, write_json

FILLERS = {"eh", "ehh", "em", "emm", "mm", "mmm", "este", "o sea", "ah", "uh", "um", "hmm", "eeh", "ehm"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9ñ% ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_words(w: Path, inv: list[dict]) -> list[dict]:
    words = []
    by_id = {it["id"]: it for it in inv}
    for tj in sorted((w / "transcripts").glob("*.json")):
        if tj.name.endswith(".hf.json"):
            continue
        t = read_json(tj)
        sid = tj.stem
        it = by_id.get(sid, {})
        src = it.get("mezzanine") or it.get("path") or t.get("source")
        for wd in t["words"]:
            n = norm(wd["text"])
            if not n:
                continue
            words.append({**wd, "n": n, "source": sid, "src": src})
    return words


def find_takes(sent: str, words: list[dict], min_score: float) -> list[dict]:
    target = norm(sent)
    n = len(target.split())
    if n == 0:
        return []
    cands = []
    first_tokens = set(target.split()[:2])
    for i in range(len(words)):
        if words[i]["n"] not in first_tokens and fuzz.ratio(words[i]["n"], target.split()[0]) < 70:
            continue
        for L in range(max(1, int(n * 0.7)), int(n * 1.35) + 2):
            j = i + L
            if j > len(words):
                break
            if words[j - 1]["source"] != words[i]["source"]:
                break
            seg = " ".join(x["n"] for x in words[i:j])
            sc = fuzz.ratio(seg, target)
            if sc >= min_score:
                cands.append((sc, i, j))
    # NMS: quedarse con la mejor ventana por zona
    cands.sort(reverse=True)
    picked: list[tuple] = []
    for sc, i, j in cands:
        if all(j <= pi or i >= pj or words[i]["source"] != words[pi]["source"] for _, pi, pj in picked):
            picked.append((sc, i, j))
    takes = []
    for sc, i, j in picked:
        ws = words[i:j]
        clarity = sum(x.get("prob", 1) for x in ws) / len(ws)
        gaps = [ws[k + 1]["start"] - ws[k]["end"] for k in range(len(ws) - 1)]
        takes.append({"score": round(sc, 1), "clarity": round(clarity, 3), "source": ws[0]["source"],
                      "src": ws[0]["src"], "w0": i, "w1": j, "start": ws[0]["start"], "end": ws[-1]["end"],
                      "max_gap": round(max(gaps), 2) if gaps else 0, "text": " ".join(x["text"] for x in ws)})
    takes.sort(key=lambda t: (t["source"], t["start"]))
    return takes


def choose(takes: list[dict]) -> int:
    if not takes:
        return -1
    best = max(t["score"] + 20 * t["clarity"] - 3 * max(0, t["max_gap"] - 0.8) for t in takes)
    ok = [k for k, t in enumerate(takes)
          if t["score"] + 20 * t["clarity"] - 3 * max(0, t["max_gap"] - 0.8) >= best - 4]
    return ok[-1]  # la última toma buena


def respell(ws: list[dict], sentence: str) -> list[dict]:
    """Copia la ortografía del guion (marcas, tildes, números, signos) sobre las palabras con timing del ASR."""
    import difflib
    script_tokens = sentence.split()
    a = [norm(w["text"]) for w in ws]
    b = [norm(t) for t in script_tokens]
    out = [dict(w) for w in ws]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag in ("equal", "replace") and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                out[i1 + k]["text"] = script_tokens[j1 + k]
        elif tag == "replace" and (i2 - i1) == 1:
            out[i1]["text"] = " ".join(script_tokens[j1:j2])  # p.ej. "90%" dicho "noventa por ciento"
    return out


def tighten(ws: list[dict], pad_in: float, pad_out: float, max_gap: float, keep_gap: float) -> list[tuple]:
    """Divide una toma en sub-cortes eliminando pausas internas > max_gap (deja keep_gap de aire)."""
    pieces, cur = [], [ws[0]]
    for a, b in zip(ws, ws[1:]):
        if b["start"] - a["end"] > max_gap:
            pieces.append(cur)
            cur = [b]
        else:
            cur.append(b)
    pieces.append(cur)
    out = []
    for k, p in enumerate(pieces):
        a = p[0]["start"] - (pad_in if k == 0 else keep_gap / 2)
        b = p[-1]["end"] + (pad_out if k == len(pieces) - 1 else keep_gap / 2)
        out.append((max(0.0, a), b, p))
    return out


def free_mode(words: list[dict], max_gap: float) -> list[dict]:
    """Sin guion: frases por pausas, quita muletillas y arranques repetidos (se queda con la última)."""
    phrases, cur = [], []
    for a in words:
        if cur and (a["start"] - cur[-1]["end"] > max_gap or a["source"] != cur[-1]["source"]):
            phrases.append(cur)
            cur = []
        if a["n"] in FILLERS:
            continue
        cur.append(a)
    if cur:
        phrases.append(cur)
    keep = []
    for k, ph in enumerate(phrases):
        txt = " ".join(x["n"] for x in ph)
        nxt = " ".join(x["n"] for x in phrases[k + 1]) if k + 1 < len(phrases) else ""
        # arranque fallido: la frase siguiente empieza igual y es más larga/similar
        if nxt and (fuzz.partial_ratio(txt, nxt) > 85 and len(nxt) >= len(txt) * 0.8):
            continue
        keep.append(ph)
    return [{"text": " ".join(x["text"] for x in ph), "words": ph} for ph in keep]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--min-score", type=float, default=68)
    ap.add_argument("--pad-in", type=float, default=0.05, help="aire antes de la 1a palabra (s)")
    ap.add_argument("--pad-out", type=float, default=0.10, help="aire después de la última palabra (s)")
    ap.add_argument("--max-gap", type=float, default=0.38, help="pausa interna que se corta (s)")
    ap.add_argument("--keep-gap", type=float, default=0.10, help="aire que se deja al cortar una pausa (s)")
    ap.add_argument("--free", action="store_true", help="sin guion: limpieza automática del discurso")
    ap.add_argument("--asr-spelling", action="store_true", help="subtítulos con el texto del ASR en vez del guion")
    a = ap.parse_args(argv)

    proj = resolve_project(a.project)
    w = work_dir(proj)
    inv = read_json(w / "analysis" / "inventory.json", [])
    words = load_words(w, inv)
    if not words:
        raise SystemExit("No hay transcripciones. Corre: ve transcribe <proyecto>")
    overrides = read_json(w / "edl_overrides.json", {})
    guion = read_json(w / "guion.json")
    cuts, report = [], ["# EDL — lista de cortes", ""]

    if guion and not a.free:
        missing = []
        for s in guion["sentences"]:
            ov = overrides.get(str(s["i"]), {})
            if ov.get("skip"):
                continue
            takes = find_takes(s["text"], words, a.min_score)
            ch = ov.get("take", choose(takes))
            report.append(f"## [{s['i']}] {s['text']}")
            if s.get("cues"):
                report.append(f"   cues: {' / '.join(s['cues'])}")
            for k, t in enumerate(takes):
                mark = "**→**" if k == ch else "   "
                report.append(f"{mark} toma {k}: {t['source']} {t['start']:.2f}-{t['end']:.2f} "
                              f"score={t['score']} clar={t['clarity']} gap={t['max_gap']} «{t['text']}»")
            if "in" in ov:
                cuts.append({"sentence": s["i"], "source": ov["source"], "src": ov.get("src"),
                             "in": ov["in"], "out": ov["out"], "text": s["text"], "section": s.get("section"),
                             "cues": s.get("cues", []), "words": [], "manual": True})
                continue
            if ch < 0 or ch >= len(takes):
                missing.append(s)
                report.append("   ⚠️  NO ENCONTRADA en el crudo")
                continue
            t = takes[ch]
            ws = words[t["w0"]:t["w1"]]
            if t["score"] >= 80 and not a.asr_spelling:
                ws = respell(ws, s["text"])
            for k, (i0, i1, piece) in enumerate(tighten(ws, a.pad_in, a.pad_out, a.max_gap, a.keep_gap)):
                cuts.append({"sentence": s["i"], "piece": k, "source": t["source"], "src": t["src"],
                             "in": round(i0, 3), "out": round(i1, 3), "text": " ".join(x["text"] for x in piece),
                             "section": s.get("section"), "cues": s.get("cues", []) if k == 0 else [],
                             "score": t["score"],
                             "words": [{"text": x["text"], "start": x["start"], "end": x["end"]} for x in piece]})
            report.append("")
        if missing:
            report.insert(2, f"⚠️ {len(missing)} frases del guion no aparecen en el crudo: "
                             + "; ".join(f"[{m['i']}] {m['text'][:50]}" for m in missing) + "\n")
    else:
        for k, ph in enumerate(free_mode(words, a.max_gap)):
            for j, (i0, i1, piece) in enumerate(tighten(ph["words"], a.pad_in, a.pad_out, a.max_gap, a.keep_gap)):
                cuts.append({"sentence": k, "piece": j, "source": piece[0]["source"], "src": piece[0]["src"],
                             "in": round(i0, 3), "out": round(i1, 3), "text": " ".join(x["text"] for x in piece),
                             "cues": [], "words": [{"text": x["text"], "start": x["start"], "end": x["end"]} for x in piece]})
            report.append(f"- [{k}] {ph['text']}")

    # evitar solapes entre cortes consecutivos del mismo clip
    for prev, nxt in zip(cuts, cuts[1:]):
        if prev["source"] == nxt["source"] and prev["out"] > nxt["in"] and prev["in"] < nxt["in"]:
            mid = (prev["words"][-1]["end"] + nxt["words"][0]["start"]) / 2 if prev["words"] and nxt["words"] else nxt["in"]
            prev["out"], nxt["in"] = round(mid, 3), round(mid, 3)
    total = sum(c["out"] - c["in"] for c in cuts)
    report.insert(2, f"**{len(cuts)} cortes · duración {total:.1f}s**\n")
    write_json(w / "edl.json", {"cuts": cuts, "duration": round(total, 3),
                                "params": vars(a) | {"project": str(proj)}})
    (w / "EDL.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    log(f"{len(cuts)} cortes, {total:.1f}s")
    print(w / "EDL.md")


if __name__ == "__main__":
    main()
