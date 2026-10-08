import {noise2D} from '@remotion/noise';
import {Easing, interpolate, spring} from 'remotion';
import type {ZoomKey} from '../types';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const EASE = {
	smooth: Easing.bezier(0.45, 0, 0.2, 1),
	out: Easing.bezier(0.16, 1, 0.3, 1), // expo-out: el "feel" premium
	in: Easing.bezier(0.7, 0, 0.84, 0),
	punch: Easing.bezier(0.2, 1.6, 0.35, 1), // overshoot
	snap: Easing.bezier(0.9, 0, 0.1, 1),
	linear: Easing.linear,
};

/** Interpola keyframes de zoom (t en segundos relativos al clip). */
export const zoomAt = (keys: ZoomKey[] | null | undefined, t: number) => {
	if (!keys || keys.length === 0) return {s: 1, x: 0, y: 0, r: 0};
	const k = [...keys].sort((a, b) => a.t - b.t);
	if (t <= k[0].t) return {s: k[0].s, x: k[0].x ?? 0, y: k[0].y ?? 0, r: k[0].r ?? 0};
	for (let i = 0; i < k.length - 1; i++) {
		const a = k[i];
		const b = k[i + 1];
		if (t >= a.t && t <= b.t) {
			const easing = EASE[b.ease ?? 'smooth'];
			const p = b.t === a.t ? 1 : easing((t - a.t) / (b.t - a.t));
			const lerp = (u: number, v: number) => u + (v - u) * p;
			return {s: lerp(a.s, b.s), x: lerp(a.x ?? 0, b.x ?? 0), y: lerp(a.y ?? 0, b.y ?? 0), r: lerp(a.r ?? 0, b.r ?? 0)};
		}
	}
	const l = k[k.length - 1];
	return {s: l.s, x: l.x ?? 0, y: l.y ?? 0, r: l.r ?? 0};
};

/** Cámara en mano orgánica (Perlin), amplitud en px. */
export const handheld = (frame: number, amp: number, seed = 'h') => ({
	x: noise2D(seed + 'x', frame / 40, 0) * amp,
	y: noise2D(seed + 'y', 0, frame / 40) * amp,
	r: noise2D(seed + 'r', frame / 60, frame / 60) * amp * 0.03,
});

/** Shake de impacto que decae. */
export const impactShake = (frame: number, at: number, fps: number, amp = 18, dur = 0.35) => {
	const t = (frame - at) / fps;
	if (t < 0 || t > dur) return {x: 0, y: 0};
	const decay = 1 - t / dur;
	return {x: noise2D('sx', frame * 0.9, 0) * amp * decay, y: noise2D('sy', 0, frame * 0.9) * amp * decay};
};

export const pop = (frame: number, fps: number, delay = 0, stiffness = 220, damping = 14) =>
	spring({frame: frame - delay, fps, config: {stiffness, damping, mass: 0.7}});

export const springIn = (frame: number, fps: number, delay = 0) =>
	spring({frame: frame - delay, fps, config: {damping: 200}, durationInFrames: Math.round(fps * 0.5)});

/** Entrada/salida estándar para un gráfico de duración `dur` frames. */
export const inOut = (frame: number, dur: number, inF = 10, outF = 8) =>
	Math.min(interpolate(frame, [0, inF], [0, 1], {...clamp, easing: EASE.out}), interpolate(frame, [dur - outF, dur], [1, 0], {...clamp, easing: EASE.in}));

export const hexA = (hex: string, a: number) => {
	const h = hex.replace('#', '');
	const n = parseInt(h.length === 3 ? h.split('').map((c) => c + c).join('') : h, 16);
	return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
};

export const sec = (s: number, fps: number) => Math.round(s * fps);
