"""Elige `in` óptimo de una música para un video: energía creciente y el drop en el CTA.
uso: musicfit.py <dur_video> <t_cta> [archivos...]"""
import glob, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beats import analyze

def fit(path, L, T):
    p = Path(path); bj = p.with_suffix('.beats.json')
    b = json.load(open(bj)) if bj.exists() else analyze(p)
    if not bj.exists(): json.dump(b, open(bj, 'w'))
    t = np.array([x[0] for x in b['energy_curve']]); e = np.array([x[1] for x in b['energy_curve']])
    best = None
    for k, d in enumerate(b['drops']):
        i0 = d['t'] - T
        if i0 < 0 or i0 + L > b['duration']: continue
        m = (t >= i0) & (t <= i0 + L)
        if m.sum() < 6: continue
        tt, ee = t[m] - i0, e[m]
        slope = np.polyfit(tt, ee, 1)[0] * L
        pre = ee[tt < 4].mean() if (tt < 4).any() else 1
        post = ee[tt >= T].mean() if (tt >= T).any() else 0
        dip = ee[(tt > T - 1.5) & (tt < T - 0.2)].mean() if ((tt > T - 1.5) & (tt < T - 0.2)).any() else post
        score = slope + (post - pre) + 0.5 * (post - dip) + d['strength'] * 0.1
        if best is None or score > best[0]: best = (round(score, 2), k, round(i0, 2), round(pre, 2), round(post, 2))
    return best, b['tempo']

if __name__ == '__main__':
    L, T = float(sys.argv[1]), float(sys.argv[2])
    files = sys.argv[3:] or glob.glob('library/music/_dl/epic*/**/*.mp3', recursive=True)
    rows = []
    for f in files:
        try:
            best, tempo = fit(f, L, T)
        except Exception as ex:
            continue
        if best: rows.append((best[0], f, best, tempo))
    for r in sorted(rows, reverse=True)[:12]:
        print(r[0], Path(r[1]).name, 'drop#', r[2][1], 'in=', r[2][2], 'pre', r[2][3], 'post', r[2][4], 'bpm', round(r[3]))
