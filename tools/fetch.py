"""Descarga el material listado en links.md del proyecto (Google Drive, Dropbox, WeTransfer*, YouTube/Vimeo, URLs).

Formato de links.md (las secciones definen la carpeta de destino):
  ## crudo
  https://drive.google.com/drive/folders/XXXX
  ## broll
  https://www.dropbox.com/scl/fo/...?dl=0
  ## referencias        (videos de referencia de estilo: se descargan a referencias/)
  https://www.youtube.com/watch?v=...
  ## musica / audio / marca / guion ...

* WeTransfer: los links expiran; mejor Drive/Dropbox.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from vecommon import log, resolve_project, run

URL = re.compile(r"https?://\S+")
SECTIONS = {"crudo": "crudo", "raw": "crudo", "broll": "broll", "b-roll": "broll", "referencias": "referencias",
            "referencia": "referencias", "musica": "audio", "música": "audio", "audio": "audio", "marca": "../../marca",
            "linea grafica": "../../marca", "línea gráfica": "../../marca", "guion": ".", "guión": "."}


def dl(url: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    u = url.rstrip(").,>")
    if "drive.google.com" in u or "docs.google.com" in u:
        import gdown
        if "/folders/" in u:
            gdown.download_folder(u, output=str(dest), quiet=False, remaining_ok=True)
        elif "docs.google.com/document" in u:
            doc_id = re.search(r"/d/([\w-]+)", u).group(1)
            gdown.download(f"https://docs.google.com/document/d/{doc_id}/export?format=docx",
                           str(dest / f"guion_{doc_id[:6]}.docx"), quiet=False)
        else:
            gdown.download(u, output=str(dest) + "/", quiet=False, fuzzy=True)
    elif "dropbox.com" in u:
        direct = re.sub(r"([?&])dl=0", r"\1dl=1", u)
        if "dl=1" not in direct:
            direct += ("&" if "?" in direct else "?") + "dl=1"
        tmp = dest / "_dropbox_download"
        run(["curl", "-L", "--fail", "-o", tmp, direct])
        if run(["unzip", "-tq", tmp], check=False, capture=True).returncode == 0:
            run(["unzip", "-o", "-q", tmp, "-d", dest])
            tmp.unlink()
        else:
            name = Path(u.split("?")[0]).name or "archivo"
            tmp.rename(dest / name)
    elif any(h in u for h in ("youtube.com", "youtu.be", "vimeo.com", "instagram.com", "tiktok.com", "loom.com")):
        run(["yt-dlp", "-f", "bv*[height<=2160]+ba/b", "--merge-output-format", "mp4",
             "-o", str(dest / "%(title).80s_%(id)s.%(ext)s"), u])
    else:
        name = Path(u.split("?")[0]).name or "descarga"
        run(["curl", "-L", "--fail", "-o", dest / name, u])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    links = proj / "links.md"
    if not links.exists():
        raise SystemExit("No hay links.md en el proyecto")
    section = "crudo"
    n = 0
    for line in links.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^\s*#+\s*(.+)$", line)
        if h:
            section = SECTIONS.get(h.group(1).strip().lower(), h.group(1).strip().lower())
            continue
        for u in URL.findall(line):
            try:
                dl(u, (proj / section).resolve())
                n += 1
            except Exception as e:
                log(f"⚠️ no pude descargar {u}: {e}")
    log(f"{n} links procesados")


if __name__ == "__main__":
    main()
