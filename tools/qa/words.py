"""Lista los cortes y palabras del timeline (para anclar gráficos). uso: words.py <cliente/proyecto>"""
import json, subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
p = root / "clientes" / sys.argv[1].split("/")[0] / "proyectos" / sys.argv[1].split("/")[1] / "_work"
ov = p / "overlays.json"
if not ov.exists():
    ov.write_text(json.dumps({"format": "9:16", "zoom": {"auto": False}, "captions": {"style": "premium"}}))
subprocess.run([str(root / "ve"), "build", sys.argv[1]], check=True, capture_output=True)
e = json.load(open(p / "edit.json"))
for c in e["cuts"]:
    print(f"cut {c['i']:2} {c['source']} [{c['tl_start']:6.2f}-{c['tl_end']:6.2f}] " + " ".join(f"{w['text']}@{w['start']:.2f}" for w in c["words_tl"]))
