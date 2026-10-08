"""Compila EDL + overlays (decisiones creativas) en _work/edit.json, el único input del motor Remotion.

Entradas:
  _work/edl.json          cortes (de ve align) — track principal y palabras
  _work/overlays.json     decisiones del editor: formato, zooms, brolls, gráficos, sfx, música, captions, fx
  clientes/<c>/marca/brand.json
  _work/analysis/faces/*  centro del sujeto para zooms y reencuadre

Anclas de tiempo (campo "at") aceptadas en overlays — todas se resuelven a segundos del TIMELINE final:
  2.5                                  segundos absolutos del timeline
  {"word": "gratis", "n": 1}           n-ésima aparición de la palabra (en el timeline), +"offset"
  {"sentence": 4}                      inicio de la frase 4 del guion (+"offset", "end": true para el final)
  {"cut": 7}                           inicio del corte 7 (+"offset", "end": true)
  {"end": true, "offset": -3}          relativo al final del video
Rutas de audio: "synth:impact_cinematic", "lib:whoosh" (mejor match del índice), o ruta del repo.
"""
from __future__ import annotations

import argparse
import os
import re
import unicodedata
from pathlib import Path

from vecommon import ENGINE, LIBRARY, ROOT, client_of, log, media_info, read_json, resolve_project, work_dir, write_json

FORMATS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350),
           "9:16-4k": (2160, 3840), "16:9-4k": (3840, 2160)}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ%]+", "", s)


def ensure_public_links():
    pub = ENGINE / "public"
    pub.mkdir(exist_ok=True)
    for name in ("clientes", "library"):
        link = pub / name
        target = ROOT / name
        target.mkdir(exist_ok=True)
        if not link.exists():
            os.symlink(os.path.relpath(target, pub), link)


def to_public(path: str | Path) -> str:
    """Convierte una ruta del repo en ruta relativa a engine-remotion/public (vía symlinks)."""
    p = Path(path).resolve()
    for name in ("clientes", "library"):
        base = (ROOT / name).resolve()
        if str(p).startswith(str(base)):
            return f"{name}/{p.relative_to(base).as_posix()}"
    if str(p).startswith(str((ENGINE / "public").resolve())):
        return p.relative_to((ENGINE / "public").resolve()).as_posix()
    raise SystemExit(f"El asset {p} debe estar dentro de clientes/ o library/ (cópialo a _work/assets)")


def resolve_audio(ref: str, proj: Path) -> str:
    if ref.startswith("synth:"):
        p = LIBRARY / "sfx" / "synth" / f"{ref[6:]}.wav"
    elif ref.startswith("lib:"):
        q = ref[4:].lower()
        idx = read_json(LIBRARY / "index.json", [])
        hits = [i for i in idx if q == i["name"].lower()] or [i for i in idx if q in i["name"].lower()] \
            or [i for i in idx if q in i["category"].lower()]
        if not hits:
            raise SystemExit(f"No hay sonido '{q}' en la librería (ve library search {q})")
        p = Path(hits[0]["path"])
    else:
        p = Path(ref)
        if not p.is_absolute():
            p = (proj / ref) if (proj / ref).exists() else (ROOT / ref)
    if not p.exists():
        raise SystemExit(f"No existe el audio {ref} -> {p}")
    return to_public(p)


def resolve_media(ref: str, proj: Path) -> Path:
    p = Path(ref)
    if not p.is_absolute():
        for base in (proj, proj / "_work", client_of(proj), ROOT):
            if (base / ref).exists():
                return (base / ref).resolve()
    if not p.exists():
        raise SystemExit(f"No existe el asset {ref}")
    return p.resolve()


class Timeline:
    def __init__(self, cuts: list[dict], tail: float = 0.0):
        self.cuts = cuts
        self.words = [w for c in cuts for w in c["words_tl"]]
        self.duration = (cuts[-1]["tl_end"] if cuts else 0) + tail  # incluye la cola final (end card)

    def at(self, a) -> float:
        if a is None:
            return 0.0
        if isinstance(a, (int, float)):
            return float(a)
        off = float(a.get("offset", 0))
        if "word" in a:
            target, n = norm(a["word"]), int(a.get("n", 1))
            hits = [w for w in self.words if norm(w["text"]) == target] or \
                   [w for w in self.words if target in norm(w["text"])]
            if len(hits) < n:
                raise SystemExit(f"Ancla: la palabra '{a['word']}' (n={n}) no está en el timeline")
            w = hits[n - 1]
            return (w["end"] if a.get("end") else w["start"]) + off
        if "sentence" in a:
            cs = [c for c in self.cuts if c["sentence"] == a["sentence"]]
            if not cs:
                raise SystemExit(f"Ancla: la frase {a['sentence']} no está en el timeline")
            return (cs[-1]["tl_end"] if a.get("end") else cs[0]["tl_start"]) + off
        if "cut" in a:
            c = self.cuts[int(a["cut"])]
            return (c["tl_end"] if a.get("end") else c["tl_start"]) + off
        if a.get("end"):
            return self.duration + off
        raise SystemExit(f"Ancla no reconocida: {a}")


def auto_zooms(cuts: list[dict], emphasis: set[str], intensity: float, faces: dict) -> None:
    """Patrón de zoom dinámico tipo 'editor de ads': alterna planos, punch-ins en énfasis y drift suave."""
    level = 0
    for i, c in enumerate(cuts):
        if c.get("zoom") is not None:
            continue
        dur = c["tl_end"] - c["tl_start"]
        same_sentence = i > 0 and cuts[i - 1]["sentence"] == c["sentence"]
        # cambiar de "plano" en cada corte para disimular el jump cut
        level = (level + 1) % 3 if (same_sentence or i % 2 == 0) else (level + 2) % 3
        base = [1.0, 1.12, 1.24][level]
        base = 1 + (base - 1) * intensity
        kf = [{"t": 0, "s": base}, {"t": dur, "s": base + 0.035 * intensity * min(dur, 4) / 4}]
        for w in c["words_tl"]:
            if norm(w["text"]) in emphasis:
                t0 = w["start"] - c["tl_start"]
                kf += [{"t": max(0, t0 - 0.02), "s": None}, {"t": t0 + 0.12, "s": base + 0.12 * intensity, "ease": "punch"}]
        kf = sorted(kf, key=lambda k: k["t"])
        last = base
        for k in kf:
            if k["s"] is None:
                k["s"] = last
            last = k["s"]
        c["zoom"] = kf
        f = faces.get(c["source"], {}).get("median")
        c["focus"] = c.get("focus") or ({"x": f["x"], "y": max(0.25, f["y"] - 0.05)} if f else {"x": 0.5, "y": 0.42})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--overlays", default=None)
    a = ap.parse_args(argv)
    proj = resolve_project(a.project)
    w = work_dir(proj)
    ensure_public_links()
    edl = read_json(w / "edl.json")
    if not edl:
        raise SystemExit("Falta _work/edl.json (corre ve align)")
    ov = read_json(Path(a.overlays) if a.overlays else w / "overlays.json", {}) or {}
    brand = read_json(client_of(proj) / "marca" / "brand.json", {}) or {}
    fmt = ov.get("format", "9:16")
    width, height = FORMATS.get(fmt, (1080, 1920))
    fps = int(ov.get("fps", 30))
    inv = {i["id"]: i for i in read_json(w / "analysis" / "inventory.json", [])}
    faces = {fid.stem: read_json(fid) for fid in (w / "analysis" / "faces").glob("*.json")} \
        if (w / "analysis" / "faces").exists() else {}

    # ---- track principal con tiempos de timeline
    cuts, t = [], 0.0
    per_cut = ov.get("cuts", {})
    for i, c in enumerate(edl["cuts"]):
        o = per_cut.get(str(i), {})
        if o.get("skip"):
            continue
        speed = float(o.get("speed", 1.0))
        cin, cout = float(o.get("in", c["in"])), float(o.get("out", c["out"]))
        dur = (cout - cin) / speed
        src = c.get("src") or inv.get(c["source"], {}).get("mezzanine") or inv.get(c["source"], {}).get("path")
        words_tl = [{"text": x["text"], "start": round(t + (x["start"] - cin) / speed, 3),
                     "end": round(t + (x["end"] - cin) / speed, 3)} for x in c.get("words", [])
                    if x["start"] >= cin - 0.05 and x["end"] <= cout + 0.05]
        cuts.append({"i": i, "sentence": c["sentence"], "source": c["source"], "src": to_public(src),
                     "in": cin, "out": cout, "speed": speed, "tl_start": round(t, 3), "tl_end": round(t + dur, 3),
                     "text": c["text"], "section": c.get("section"), "words_tl": words_tl,
                     "zoom": o.get("zoom"), "focus": o.get("focus"), "transition": o.get("transition"),
                     "fx": o.get("fx"), "mirror": o.get("mirror", False), "volume": o.get("volume", 1.0),
                     "cutout": to_public(resolve_media(o["cutout"], proj)) if o.get("cutout") else None,
                     "behind": o.get("behind", [])})
        t += dur
    tl = Timeline(cuts, float(ov.get("tail", 0)))
    cap = ov.get("captions", {})
    emphasis = {norm(x) for x in cap.get("emphasis", [])}
    zcfg = ov.get("zoom", {"auto": True, "intensity": 1.0})
    if zcfg.get("auto", True):
        auto_zooms(cuts, emphasis, float(zcfg.get("intensity", 1.0)), faces)
    for c in cuts:
        c["focus"] = c.get("focus") or {"x": 0.5, "y": 0.42}

    def span(item, default_dur):
        st = tl.at(item.get("at", 0))
        if "until" in item:
            en = tl.at(item["until"])
        else:
            en = st + float(item.get("duration", default_dur))
        return round(st, 3), round(max(en - st, 1 / fps), 3)

    broll = []
    for b in ov.get("broll", []):
        st, du = span(b, 2.0)
        p = resolve_media(b["src"], proj)
        info = media_info(p) if p.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp") else {"kind": "image"}
        broll.append({**b, "src": to_public(p), "start": st, "duration": du,
                      "isImage": info.get("kind") == "image", "in": float(b.get("in", 0)),
                      "srcDuration": info.get("duration")})
    graphics = []
    for g in ov.get("graphics", []):
        st, du = span(g, 2.0)
        props = dict(g.get("props", {}))
        for k, v in list(props.items()):  # assets dentro de props (logos, modelos 3D, imágenes)
            if isinstance(v, str) and (k.endswith("src") or k.endswith("Src") or k in ("logo", "model", "image", "hdri")):
                if not v.startswith("http"):
                    props[k] = to_public(resolve_media(v, proj))
        graphics.append({**g, "props": props, "start": st, "duration": du})
    sfx = []
    for s in ov.get("sfx", []):
        st = tl.at(s.get("at", 0)) + float(s.get("offset", 0))
        sfx.append({"src": resolve_audio(s["src"], proj), "start": round(max(0, st), 3),
                    "volume": float(s.get("volume", 0.7)), "trim": s.get("trim")})
    music = []
    for m in ov.get("music", []):
        st = tl.at(m.get("at", 0))
        mp = resolve_media(m["src"], proj) if not str(m["src"]).startswith(("synth:", "lib:")) else None
        src = resolve_audio(m["src"], proj)
        mi = float(m.get("in", 0))
        if "dropAt" in m and mp:  # alinear el drop de la música con un momento del video
            bj = mp.with_suffix(".beats.json")
            if not bj.exists():
                from beats import analyze
                write_json(bj, analyze(mp))
            beats = read_json(bj)
            drop_idx = int(m.get("drop", 0))
            if beats["drops"]:
                drop_t = beats["drops"][min(drop_idx, len(beats["drops"]) - 1)]["t"]
                mi = max(0.0, drop_t - (tl.at(m["dropAt"]) - st))
        end = tl.at(m["until"]) if "until" in m else tl.duration
        music.append({"src": src, "start": round(st, 3), "in": round(mi, 3), "duration": round(end - st, 3),
                      "volume": float(m.get("volume", 0.22)), "duck": float(m.get("duck", 0.4)),
                      "fadeIn": float(m.get("fadeIn", 0.3)), "fadeOut": float(m.get("fadeOut", 1.2))})
    speech = []
    for c in cuts:
        if c["words_tl"]:
            speech.append([c["words_tl"][0]["start"], c["words_tl"][-1]["end"]])

    colors = {**{"primary": "#ff3b30", "secondary": "#ffd60a", "accent": "#00e5ff", "dark": "#0b0b0f",
                 "light": "#ffffff"}, **brand.get("colors", {}), **ov.get("colors", {})}
    fonts = {**{"heading": "Montserrat", "body": "Inter"}, **brand.get("fonts", {}), **ov.get("fonts", {})}
    font_files = [to_public(f) for f in fonts.get("files", []) if Path(f).exists()]
    logo = ov.get("logo") or brand.get("logo")
    edit = {
        "id": proj.name, "width": width, "height": height, "fps": fps,
        "durationInFrames": max(1, round(tl.duration * fps)),
        "brand": {"colors": colors, "fonts": {"heading": fonts["heading"], "body": fonts["body"]},
                  "fontFiles": font_files, "logo": to_public(resolve_media(logo, proj)) if logo else None},
        "cuts": cuts, "broll": broll, "graphics": graphics, "sfx": sfx, "music": music, "speech": speech,
        "captions": {"enabled": cap.get("enabled", True), "style": cap.get("style", "bold-pop"),
                     "emphasis": sorted(emphasis), "position": cap.get("position", 0.70),
                     "maxWords": cap.get("maxWords", 3), "uppercase": cap.get("uppercase", True),
                     "hideDuring": cap.get("hideDuring", []), "words": tl.words},
        "fx": {"grain": 0.045, "vignette": 0.22, "grade": "punchy", "chromatic": 0, **ov.get("fx", {})},
        "background": ov.get("background", colors["dark"]),
    }
    write_json(w / "edit.json", edit)
    lines = [f"# Timeline ({tl.duration:.2f}s · {fmt} · {fps}fps)", ""]
    for c in cuts:
        lines.append(f"- cut {c['i']:>3} [{c['tl_start']:6.2f}–{c['tl_end']:6.2f}] s{c['sentence']} «{c['text']}»")
    lines += ["", "## Gráficos"] + [f"- {g['start']:.2f}+{g['duration']:.2f} {g['component']}" for g in graphics]
    lines += ["", "## B-roll"] + [f"- {b['start']:.2f}+{b['duration']:.2f} {b['src']}" for b in broll]
    lines += ["", "## SFX"] + [f"- {s['start']:.2f} {s['src']} vol {s['volume']}" for s in sfx]
    lines += ["", "## Música"] + [f"- {m['start']:.2f} in={m['in']} {m['src']}" for m in music]
    (w / "TIMELINE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"edit.json: {tl.duration:.2f}s, {len(cuts)} cortes, {len(graphics)} gráficos, {len(broll)} brolls, {len(sfx)} sfx")
    print(w / "edit.json")


if __name__ == "__main__":
    main()
