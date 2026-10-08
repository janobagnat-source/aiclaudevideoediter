"""Procesado de voz de locutor (cadena broadcast) y medición de loudness de SFX.

  ve voice <entrada.mp4|wav> <salida> [--lufs -16]
Cadena: highpass 80 Hz → reducción de ruido suave → EQ (−2 dB a 250 Hz, +2.5 dB a 3.5 kHz, +1 dB aire 10 kHz)
→ compresor 3:1 → de-esser → loudnorm 2 pasadas a −16 LUFS / −2 dBTP. El video (si hay) se copia sin recomprimir.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from vecommon import read_json, run, write_json

CHAIN = ("highpass=f=80,afftdn=nf=-42:nr=8,"
         "equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=q:w=0.8:g=1,"
         "acompressor=threshold=-24dB:ratio=3:attack=6:release=90:makeup=3,"
         "deesser=i=0.4:m=0.5:f=0.5")


def process_voice(src: Path, dst: Path, lufs: float = -16.0) -> dict:
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af",
             f"{CHAIN},loudnorm=I={lufs}:TP=-2:LRA=9:print_format=json", "-f", "null", "-"], capture=True, check=False)
    t = r.stderr
    m = json.loads(t[t.rindex("{"): t.rindex("}") + 1])
    af = (f"{CHAIN},loudnorm=I={lufs}:TP=-2:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"aresample=48000")
    has_video = dst.suffix.lower() in (".mp4", ".mov", ".mkv")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", src]
    if has_video:
        cmd += ["-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", dst]
    else:
        cmd += ["-vn", "-af", af, "-c:a", "pcm_s16le", dst]
    run(cmd)
    return m


def momentary_max(path: Path) -> float:
    """Loudness momentáneo máximo (LUFS, ventana 400 ms) — sirve para sonidos cortos donde el integrado no mide."""
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "apad=pad_dur=0.5,ebur128", "-f", "null", "-"],
            capture=True, check=False)
    best = -70.0
    for line in r.stderr.splitlines():
        if " M:" in line:
            try:
                v = float(line.split(" M:")[1].split()[0])
                best = max(best, v)
            except ValueError:
                pass
    return best


def sfx_gain(path: Path, target: float = -20.0, cache: Path | None = None) -> float:
    """Ganancia lineal para que el pico momentáneo del SFX quede en `target` LUFS (con caché)."""
    c = read_json(cache, {}) if cache else {}
    key = str(path)
    if key not in c:
        c[key] = momentary_max(path)
        if cache:
            write_json(cache, c)
    m = c[key]
    if m <= -69:
        return 1.0
    return min(4.0, 10 ** ((target - m) / 20))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lufs", type=float, default=-16.0)
    a = ap.parse_args(argv)
    m = process_voice(Path(a.src), Path(a.dst), a.lufs)
    print(f"{a.dst}  (entrada {m['input_i']} LUFS → {a.lufs})")


if __name__ == "__main__":
    main()
