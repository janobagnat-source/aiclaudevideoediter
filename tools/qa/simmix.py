"""Simula la mezcla de edit.json (misma lógica que AudioLayer) y mide cuánto sobresale la voz del fondo.
uso: python tools/qa/simmix.py <edit.json>"""
import json, sys, subprocess
import numpy as np
SR = 16000
e = json.load(open(sys.argv[1]))
pub = '/home/user/aiclaudevideoediter/engine-remotion/public/'
dur = e['durationInFrames'] / e['fps']
N = int(dur * SR)
def load(path, ss=0, t=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', path] + (['-t', str(t)] if t else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32).astype(np.float64)
voice = np.zeros(N); bed = np.zeros(N)
for c in e['cuts']:
    p = c['src'] if c['src'].startswith('/') else pub + c['src']
    x = load(p, c['in'], c['out'] - c['in'])
    i = int(c['tl_start'] * SR); n = min(len(x), N - i)
    voice[i:i + n] += x[:n] * c.get('volume', 1)
sp = e['speech']
def env(t, att, rel):
    v = 0.0
    for a, b in sp:
        if t < a - att or t > b + rel: continue
        v = max(v, (t - (a - att)) / att if t < a else 1.0 if t <= b else 1 - (t - b) / rel)
    return v
tt = np.arange(0, dur, 0.01)
E1 = np.array([env(t, 0.12, 0.4) for t in tt]); E2 = np.array([env(t, 0.05, 0.25) for t in tt])
def interp(E, i0, n): return np.interp((i0 + np.arange(n)) / SR, tt, E)
for m in e['music']:
    x = load(pub + m['src'], m['in'], m['duration']); i = int(m['start'] * SR); n = min(len(x), N - i)
    t = np.arange(n) / SR
    fade = np.minimum(np.clip(t / max(m['fadeIn'], .01), 0, 1), np.clip((m['duration'] - t) / max(m['fadeOut'], .01), 0, 1))
    bed[i:i + n] += x[:n] * m['volume'] * fade * (1 - (1 - m['duck']) * interp(E1, i, n))
for s in e['sfx']:
    x = load(pub + s['src']); i = int(s['start'] * SR); n = min(len(x), N - i)
    if n <= 0: continue
    bed[i:i + n] += x[:n] * s['volume'] * (1 - (1 - s.get('duck', 1)) * interp(E2, i, n))
def win(x):
    w = int(0.4 * SR)
    return np.array([10 * np.log10(np.mean(x[k:k + w] ** 2) + 1e-12) for k in range(0, len(x) - w, w // 2)])
V = win(voice); B = win(bed)
mask = V > np.percentile(V, 40)
d = V[mask] - B[mask]
print(f"voz sobre fondo mientras habla: mediana {np.median(d):.1f} dB · peor 5% {np.percentile(d, 5):.1f} dB · ventanas con <10 dB: {np.mean(d < 10) * 100:.1f}%")
bad = [round(k * 0.2, 1) for k in np.where(mask & (V - B < 10))[0]]
print("momentos con fondo a <10 dB de la voz (s):", bad[:40])
