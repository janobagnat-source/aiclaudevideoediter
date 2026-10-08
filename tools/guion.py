"""Lee el guion del proyecto (md, txt, docx, pdf, srt) y lo normaliza en _work/guion.json.

Convenciones reconocidas dentro del guion (opcionales):
  [texto entre corchetes]        -> nota/indicación visual, no se busca en el audio
  VISUAL: / B-ROLL: / GRAFICO: / SFX: / MUSICA: al inicio de línea -> indicación ligada a la frase siguiente
  ## HOOK / ## CUERPO / ## CTA   -> secciones
Tablas markdown de 2 columnas (| locución | visual |) también se entienden.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from vecommon import resolve_project, work_dir, write_json

CUE_PREFIX = re.compile(r"^\s*(visual|b-?roll|grafico|gráfico|gfx|sfx|musica|música|texto|nota|zoom)\s*[:\-]\s*(.+)$", re.I)
SECTION = re.compile(r"^\s*#{1,4}\s*(.+?)\s*$")


def read_any(p: Path) -> str:
    e = p.suffix.lower()
    if e == ".docx":
        import zipfile
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml")
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        out = []
        for para in ET.fromstring(xml).iter(f"{{{ns['w']}}}p"):
            out.append("".join(t.text or "" for t in para.iter(f"{{{ns['w']}}}t")))
        return "\n".join(out)
    if e == ".pdf":
        import subprocess
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout
        raise SystemExit("No pude leer el PDF (instala poppler-utils) — convierte el guion a .md o .docx")
    if e == ".srt":
        lines = [l for l in p.read_text(encoding="utf-8", errors="ignore").splitlines()
                 if l.strip() and not l.strip().isdigit() and "-->" not in l]
        return "\n".join(lines)
    return p.read_text(encoding="utf-8", errors="ignore")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[\.\!\?…])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9\"“])", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # frases muy largas: partir por ; o : para poder elegir tomas más finas
        if len(p.split()) > 28:
            out.extend(x.strip() for x in re.split(r"(?<=[;:])\s+", p) if x.strip())
        else:
            out.append(p)
    return out


def parse(text: str) -> dict:
    sentences, cues_pending, section = [], [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = SECTION.match(line)
        if m and not line.startswith("#!"):
            section = m.group(1).strip()
            continue
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if cells and cells[0].lower() in ("locución", "locucion", "audio", "texto", "voz", "guion", "guión"):
                continue
            spoken = cells[0]
            visual = " | ".join(c for c in cells[1:] if c)
            for s in split_sentences(spoken):
                sentences.append({"text": s, "section": section, "cues": ([visual] if visual else []) + cues_pending})
                cues_pending = []
            continue
        m = CUE_PREFIX.match(line)
        if m:
            cues_pending.append(f"{m.group(1).upper()}: {m.group(2).strip()}")
            continue
        notes = re.findall(r"\[([^\]]+)\]|\(\(([^)]+)\)\)", line)
        spoken = re.sub(r"\[[^\]]+\]|\(\([^)]+\)\)", " ", line).strip(" -–—*>")
        spoken = re.sub(r"\*\*|__|`", "", spoken)
        note_txt = [a or b for a, b in notes]
        if not spoken:
            cues_pending.extend(note_txt)
            continue
        for i, s in enumerate(split_sentences(spoken)):
            sentences.append({"text": s, "section": section,
                              "cues": (cues_pending + note_txt) if i == 0 else []})
            cues_pending = []
    for i, s in enumerate(sentences):
        s["i"] = i
    full = " ".join(s["text"] for s in sentences)
    return {"sentences": sentences, "text": full, "words": len(full.split()),
            "est_duration_s": round(len(full.split()) / 2.7, 1)}  # ~160 ppm en español publicitario


def find_script(proj: Path) -> Path | None:
    cands = []
    for p in proj.rglob("*"):
        if "_work" in p.parts or "entregables" in p.parts or not p.is_file():
            continue
        n = p.name.lower()
        if any(k in n for k in ("guion", "guión", "script", "libreto")) and p.suffix.lower() in (
                ".md", ".txt", ".docx", ".pdf", ".srt", ".rtf"):
            cands.append(p)
    return sorted(cands, key=lambda x: (x.suffix != ".md", len(str(x))))[0] if cands else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--file")
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    src = Path(a.file) if a.file else find_script(proj)
    if not src:
        raise SystemExit("No encontré guion (archivo con 'guion' o 'script' en el nombre).")
    data = parse(read_any(src))
    data["source"] = str(src)
    out = write_json(work_dir(proj) / "guion.json", data)
    print(f"{out}  ({len(data['sentences'])} frases, ~{data['est_duration_s']}s estimados)")


if __name__ == "__main__":
    main()
