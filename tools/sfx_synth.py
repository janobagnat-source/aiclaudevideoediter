"""Genera una librería propia de SFX cinematográficos (48 kHz estéreo, sin licencias de terceros).

Se usa como base garantizada offline; se complementa con Freesound/Openverse (ve library).
Salida: library/sfx/synth/<categoria>_<variante>.wav
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

from vecommon import LIBRARY, log

SR = 48000
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def norm(x, peak_db=-1.0):
    m = np.max(np.abs(x)) or 1
    return x / m * (10 ** (peak_db / 20))


def env_adsr(n, a=0.01, d=0.1, s=0.6, r=0.3):
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    S = max(n - A - D - R, 0)
    e = np.concatenate([np.linspace(0, 1, A, endpoint=False), np.linspace(1, s, D, endpoint=False),
                        np.full(S, s), np.linspace(s, 0, R)])
    return np.pad(e, (0, max(0, n - len(e))))[:n]


def bandsweep(x, f0, f1, q=2.0, steps=64):
    """Filtro pasabanda con frecuencia central que barre f0→f1 (exponencial)."""
    out = np.zeros_like(x)
    n = len(x)
    seg = n // steps + 1
    zi = None
    for k in range(steps):
        a, b = k * seg, min((k + 1) * seg, n)
        if a >= n:
            break
        fc = f0 * (f1 / f0) ** (k / (steps - 1))
        bw = fc / q
        lo, hi = max(fc - bw / 2, 20), min(fc + bw / 2, SR / 2 - 100)
        sos = signal.butter(2, [lo, hi], btype="band", fs=SR, output="sos")
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        out[a:b], zi = signal.sosfilt(sos, x[a:b], zi=zi)
    return out


def reverb(x, decay=1.6, mix=0.3, predelay=0.012):
    n = int(SR * decay)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    ir = signal.sosfilt(signal.butter(2, 6000, fs=SR, output="sos"), ir)
    ir = np.concatenate([np.zeros(int(predelay * SR)), ir])
    wet = signal.fftconvolve(x, ir)[: len(x) + n]
    dry = np.pad(x, (0, len(wet) - len(x)))
    return (1 - mix) * dry + mix * norm(wet, -6) * np.max(np.abs(dry))


def stereo(x, width=0.3, pan_curve=None):
    d = int(0.011 * SR)
    l = x
    r = np.concatenate([np.zeros(d), x[:-d]]) * (1 - width) + x * width
    if pan_curve is not None:
        p = np.interp(np.arange(len(x)), np.linspace(0, len(x), len(pan_curve)), pan_curve)
        l = l * np.cos((p + 1) * np.pi / 4)
        r = r * np.sin((p + 1) * np.pi / 4)
    return np.stack([l, r], axis=1)


def whoosh(dur=0.8, f0=300, f1=4500, peak=0.55, pan=(-0.7, 0.7)):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    pk = int(n * peak)
    e = np.concatenate([np.linspace(0, 1, pk) ** 2.2, np.linspace(1, 0, n - pk) ** 1.6])
    sw = np.concatenate([np.geomspace(f0, f1, pk), np.geomspace(f1, f0 * 1.5, n - pk)])
    y = bandsweep(x, sw[0], sw[pk - 1], q=1.6) * e
    y += 0.25 * bandsweep(x, f0 / 2, f1 / 2, q=3) * e
    return stereo(norm(y), 0.4, pan_curve=np.linspace(pan[0], pan[1], 32))


def riser(dur=3.0, f0=120, f1=2400):
    tt = t_(dur)
    n = len(tt)
    phase = 2 * np.pi * np.cumsum(np.geomspace(f0, f1, n)) / SR
    tone = sum(np.sin(phase * h + d) / h for h, d in ((1, 0), (1.005, 1), (2, 2), (3.01, 0.5)))
    noise = bandsweep(rng.standard_normal(n), 400, 9000, q=1.2)
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(np.geomspace(3, 22, n)) / SR)
    e = (tt / dur) ** 2.4
    y = (0.6 * tone + 0.8 * noise) * e * trem
    y[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return stereo(norm(reverb(y, 1.2, 0.25)), 0.5)


def impact(dur=2.5, sub=55, punch=1.0, tail=1.8):
    tt = t_(dur)
    f = sub * (1 + 2.5 * np.exp(-tt * 18))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (2.2 / tail))
    click = rng.standard_normal(len(tt)) * np.exp(-tt * 60) * punch
    click = signal.sosfilt(signal.butter(2, [800, 9000], btype="band", fs=SR, output="sos"), click)
    mid = signal.sosfilt(signal.butter(2, [120, 900], btype="band", fs=SR, output="sos"),
                         rng.standard_normal(len(tt))) * np.exp(-tt * 9)
    y = np.tanh(1.6 * (1.0 * body + 0.7 * click + 0.6 * mid))
    return stereo(norm(reverb(y, tail, 0.22)), 0.35)


def subdrop(dur=2.0, f0=90, f1=28):
    tt = t_(dur)
    f = np.geomspace(f0, f1, len(tt))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_adsr(len(tt), 0.005, 0.2, 0.8, dur * 0.6)
    return stereo(norm(np.tanh(2 * y)), 0.0)


def braam(dur=3.2, root=41.2):
    tt = t_(dur)
    y = np.zeros_like(tt)
    for k, det in enumerate((-0.12, 0, 0.09, 0.2)):
        for mult in (1, 2, 1.5):
            y += signal.sawtooth(2 * np.pi * root * mult * (1 + det / 100) * tt + k) / mult
    y = signal.sosfilt(signal.butter(4, 1400, fs=SR, output="sos"), y)
    y = np.tanh(2.2 * y) * env_adsr(len(tt), 0.03, 0.4, 0.7, 1.6)
    return stereo(norm(reverb(y, 2.4, 0.35)), 0.6)


def reverse_swell(dur=1.6):
    tt = t_(dur)
    x = rng.standard_normal(len(tt))
    x = signal.sosfilt(signal.butter(2, 2500, btype="high", fs=SR, output="sos"), x)
    shimmer = sum(np.sin(2 * np.pi * f * tt) for f in (880, 1320, 1760, 2640)) * 0.15
    y = (x * 0.7 + shimmer) * (tt / dur) ** 3.5
    y[-200:] *= np.linspace(1, 0, 200)
    return stereo(norm(reverb(y, 0.8, 0.3)), 0.6)


def glitch(dur=0.45):
    n = int(SR * dur)
    y = np.zeros(n)
    pos = 0
    while pos < n:
        L = int(SR * rng.uniform(0.008, 0.05))
        kind = rng.integers(0, 3)
        tt = np.arange(L) / SR
        if kind == 0:
            seg = signal.square(2 * np.pi * rng.uniform(200, 2000) * tt)
        elif kind == 1:
            seg = rng.standard_normal(L)
        else:
            seg = np.sin(2 * np.pi * rng.uniform(60, 400) * tt)
        q = rng.choice([4, 8, 16])
        seg = np.round(seg * q) / q
        y[pos:pos + L] = seg[: max(0, min(L, n - pos))] * rng.uniform(0.3, 1)
        pos += L + int(SR * rng.uniform(0, 0.02))
    return stereo(norm(y, -3), 0.8)


def pop(dur=0.12, f=900):
    tt = t_(dur)
    fr = f * (1 + 1.5 * np.exp(-tt * 60))
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 45)
    return stereo(norm(y, -3), 0.1)


def click(dur=0.05):
    tt = t_(dur)
    y = rng.standard_normal(len(tt)) * np.exp(-tt * 250)
    y = signal.sosfilt(signal.butter(2, [2000, 9000], btype="band", fs=SR, output="sos"), y)
    return stereo(norm(y, -4), 0.1)


def ding(dur=1.8, f=1318.5):
    tt = t_(dur)
    y = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * d)
            for m, a, d in ((1, 1, 2.5), (2.76, 0.4, 4), (5.4, 0.2, 7), (8.93, 0.1, 10)))
    y *= np.minimum(tt / 0.002, 1)
    return stereo(norm(reverb(y, 1.2, 0.2), -3), 0.3)


def shutter(dur=0.25):
    a = click(0.04)[:, 0]
    b = click(0.06)[:, 0] * 0.8
    y = np.zeros(int(SR * dur))
    y[: len(a)] += a
    o = int(0.07 * SR)
    y[o:o + len(b)] += b
    return stereo(norm(y, -3), 0.2)


def tick(dur=0.03):
    return click(dur)


def swipe(dur=0.32):
    return whoosh(dur, 1200, 8000, peak=0.35, pan=(0.6, -0.6))


def heartbeat(dur=1.0):
    tt = t_(dur)
    y = np.zeros_like(tt)
    for off, amp in ((0.0, 1.0), (0.22, 0.7)):
        k = (tt - off).clip(0)
        y += amp * np.sin(2 * np.pi * 50 * k) * np.exp(-k * 18) * (tt >= off)
    return stereo(norm(np.tanh(2 * y)), 0)


def cash(dur=1.2):
    d = ding(dur, 2093)[:, 0] * 0.6
    c = click(0.05)[:, 0]
    y = d + np.pad(c, (0, len(d) - len(c)))
    return stereo(norm(y, -3), 0.3)


def tape_stop(dur=0.9):
    tt = t_(dur)
    f = 220 * (1 - tt / dur) ** 2 + 20
    y = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (1 - tt / dur)
    y = signal.sosfilt(signal.butter(2, 1800, fs=SR, output="sos"), y)
    return stereo(norm(y, -3), 0.2)


RECIPES = {
    "whoosh_fast": lambda: whoosh(0.45, 600, 7000, 0.5),
    "whoosh_medium": lambda: whoosh(0.8, 300, 5000, 0.55),
    "whoosh_heavy": lambda: whoosh(1.3, 120, 3200, 0.6),
    "whoosh_reverse": lambda: whoosh(0.9, 200, 6000, 0.85, (0.7, -0.7)),
    "swipe_01": lambda: swipe(0.3),
    "swipe_02": lambda: swipe(0.22),
    "riser_short": lambda: riser(1.5, 200, 3000),
    "riser_medium": lambda: riser(3.0, 120, 2400),
    "riser_long": lambda: riser(6.0, 80, 2000),
    "impact_cinematic": lambda: impact(3.0, 48, 1.0, 2.2),
    "impact_punch": lambda: impact(1.2, 70, 1.2, 0.6),
    "impact_soft": lambda: impact(1.5, 60, 0.4, 1.0),
    "subdrop_01": lambda: subdrop(2.0, 90, 28),
    "subdrop_short": lambda: subdrop(1.0, 110, 35),
    "braam_01": lambda: braam(3.2, 41.2),
    "braam_02": lambda: braam(3.8, 36.7),
    "reverse_swell": lambda: reverse_swell(1.6),
    "reverse_swell_long": lambda: reverse_swell(3.0),
    "glitch_01": lambda: glitch(0.45),
    "glitch_02": lambda: glitch(0.25),
    "glitch_03": lambda: glitch(0.8),
    "pop_01": lambda: pop(0.12, 900),
    "pop_02": lambda: pop(0.1, 1400),
    "pop_low": lambda: pop(0.15, 500),
    "click_ui": lambda: click(0.05),
    "tick_01": lambda: tick(0.03),
    "ding_01": lambda: ding(1.8, 1318.5),
    "ding_success": lambda: ding(1.6, 1760),
    "shutter_01": lambda: shutter(),
    "heartbeat_01": lambda: heartbeat(),
    "cash_01": lambda: cash(),
    "tape_stop": lambda: tape_stop(),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(LIBRARY / "sfx" / "synth"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in RECIPES.items():
        p = out / f"{name}.wav"
        if p.exists() and not a.force:
            continue
        sf.write(p, fn().astype(np.float32), SR, subtype="PCM_24")
    log(f"{len(RECIPES)} SFX en {out}")
    print(out)


if __name__ == "__main__":
    main()
