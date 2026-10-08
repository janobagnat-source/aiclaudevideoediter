"""Análisis musical: tempo, beats, downbeats (compases), picos de energía (drops) y secciones.

  ve beats <audio> [--out x.json]
Úsalo para: cortar en beat, sincronizar entradas de gráficos, ubicar el DROP de la música en el clímax/CTA,
y elegir el punto de entrada de la música (in) para que el drop caiga donde queremos.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from vecommon import write_json


def analyze(path: Path) -> dict:
    import librosa

    y, sr = librosa.load(str(path), sr=22050, mono=True)
    dur = len(y) / sr
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time", tightness=100)
    tempo = float(np.atleast_1d(tempo)[0])
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    t_rms = librosa.times_like(rms, sr=sr, hop_length=512)
    # energía suavizada a ~1s
    k = max(1, int(sr / 512))
    sm = np.convolve(rms, np.ones(k) / k, mode="same")
    sm_n = (sm - sm.min()) / (np.ptp(sm) or 1)
    # drops: subidas fuertes de energía
    d = np.diff(sm_n, prepend=sm_n[0])
    w = int(2 * sr / 512)
    drops = []
    for i in np.argsort(d)[::-1]:
        t = float(t_rms[i])
        if sm_n[min(i + w, len(sm_n) - 1)] < 0.5:
            continue
        if all(abs(t - x["t"]) > 6 for x in drops):
            drops.append({"t": round(t, 2), "strength": round(float(d[i] * 100), 2)})
        if len(drops) >= 5:
            break
    drops.sort(key=lambda x: x["t"])
    # downbeats aproximados: cada 4 beats empezando en el beat con mayor onset promedio
    beats = [float(b) for b in beats]
    best_phase, best = 0, -1
    for ph in range(4):
        idx = [librosa.time_to_frames(b, sr=sr) for b in beats[ph::4]]
        sc = float(np.mean([onset_env[min(i, len(onset_env) - 1)] for i in idx])) if idx else 0
        if sc > best:
            best, best_phase = sc, ph
    downbeats = beats[best_phase::4]
    # secciones por energía (bajo/medio/alto) cada 2 compases
    sections = []
    seg = 8 * 60 / tempo if tempo else 4
    t = 0.0
    while t < dur:
        m = sm_n[(t_rms >= t) & (t_rms < t + seg)]
        lvl = float(m.mean()) if len(m) else 0
        sections.append({"start": round(t, 2), "end": round(min(dur, t + seg), 2),
                         "energy": round(lvl, 2), "label": "alta" if lvl > 0.66 else "media" if lvl > 0.33 else "baja"})
        t += seg
    return {"path": str(path), "duration": round(dur, 2), "tempo": round(tempo, 2),
            "beats": [round(b, 3) for b in beats], "downbeats": [round(b, 3) for b in downbeats],
            "drops": drops, "sections": sections,
            "energy_curve": [[round(float(a), 2), round(float(b), 3)] for a, b in zip(t_rms[::43], sm_n[::43])]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    p = Path(a.audio)
    res = analyze(p)
    out = Path(a.out) if a.out else p.with_suffix(".beats.json")
    write_json(out, res)
    print(f"{out}\n tempo {res['tempo']} bpm · {len(res['beats'])} beats · drops "
          f"{[d['t'] for d in res['drops']]} · dur {res['duration']}s")


if __name__ == "__main__":
    main()
