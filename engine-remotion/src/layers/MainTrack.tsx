import {chromaticAberration} from '@remotion/effects/chromatic-aberration';
import {zoomBlur} from '@remotion/effects/zoom-blur';
import {Video} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {REGISTRY_BEHIND} from './behind-registry';
import {clamp, EASE, handheld, impactShake, zoomAt} from '../lib/anim';
import type {Cut, TransitionName} from '../types';

export const GRADES: Record<string, string> = {
	none: 'none',
	clean: 'contrast(1.04) saturate(1.05)',
	punchy: 'contrast(1.12) saturate(1.18) brightness(1.02)',
	cinematic: 'contrast(1.15) saturate(0.92) sepia(0.08) hue-rotate(-6deg) brightness(0.98)',
	warm: 'contrast(1.08) saturate(1.12) sepia(0.14) brightness(1.03)',
	cold: 'contrast(1.1) saturate(0.95) hue-rotate(8deg) brightness(1.0)',
	moody: 'contrast(1.22) saturate(0.8) brightness(0.92)',
	bw: 'grayscale(1) contrast(1.25) brightness(1.02)',
	vivid: 'contrast(1.1) saturate(1.35)',
};

const tName = (t: Cut['transition']): {type: TransitionName; duration: number} | null => {
	if (!t) return null;
	if (typeof t === 'string') return {type: t, duration: 0.25};
	return {type: t.type, duration: t.duration ?? 0.25};
};

/** Transformación del clip saliente (phase=out) o entrante (phase=in) para una transición. p: 0→1 */
type TrStyle = {tx?: number; ty?: number; blur?: number; scale?: number; zb?: number; bright?: number; ca?: number};
const transitionStyle = (type: TransitionName, phase: 'in' | 'out', p: number, w: number): TrStyle => {
	const q = phase === 'in' ? 1 - p : p; // intensidad: máxima en el punto de corte
	switch (type) {
		case 'whip':
			return {tx: (phase === 'out' ? -1 : 1) * q * w * 0.45, blur: q * 34, scale: 1 + q * 0.08};
		case 'whip-up':
			return {ty: (phase === 'out' ? -1 : 1) * q * w * 0.6, blur: q * 34, scale: 1 + q * 0.08};
		case 'zoom-in':
			return {scale: phase === 'out' ? 1 + q * 0.7 : 1 + q * 0.45, zb: q * 70};
		case 'zoom-out':
			return {scale: phase === 'out' ? 1 - q * 0.25 : 1 + q * 0.6, zb: q * 50};
		case 'blur':
			return {blur: q * 26, bright: 1 + q * 0.25};
		case 'glitch':
		case 'rgb-split':
			return {ca: q * 28, tx: (Math.sin(p * 40) > 0 ? 1 : -1) * q * 24};
		default:
			return {};
	}
};

const ClipInner: React.FC<{cut: Cut; next: Cut | undefined; grade: string}> = ({cut, next, grade}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const dur = Math.max(1, Math.round((cut.tl_end - cut.tl_start) * fps));
	const t = frame / fps;
	const z = zoomAt(cut.zoom, t);
	const hh = cut.fx?.shake ? handheld(frame + cut.i * 100, cut.fx.shake) : {x: 0, y: 0, r: 0};

	// transición de entrada (propia) y de salida (definida por el siguiente corte)
	let tr: TrStyle = {};
	const tin = tName(cut.transition);
	if (tin) {
		const n = Math.max(1, Math.round(tin.duration * fps * 0.5));
		if (frame < n) tr = transitionStyle(tin.type, 'in', interpolate(frame, [0, n], [0, 1], {...clamp, easing: EASE.out}), width);
		if (tin.type === 'shake') {
			const s = impactShake(frame, 0, fps, 26, 0.3);
			tr = {tx: s.x, ty: s.y};
		}
	}
	const tout = tName(next?.transition);
	if (tout && tout.type !== 'shake') {
		const n = Math.max(1, Math.round(tout.duration * fps * 0.5));
		if (frame >= dur - n) tr = transitionStyle(tout.type, 'out', interpolate(frame, [dur - n, dur], [0, 1], {...clamp, easing: EASE.in}), width);
	}

	const scale = z.s * (tr.scale ?? 1);
	const filters = [GRADES[cut.fx?.grade ?? grade] ?? grade, cut.fx?.bw ? 'grayscale(1)' : '', tr.blur ? `blur(${tr.blur}px)` : '', tr.bright ? `brightness(${tr.bright})` : '', cut.fx?.blur ? `blur(${cut.fx.blur}px)` : '']
		.filter((f) => f && f !== 'none')
		.join(' ');
	const ox = cut.focus.x * 100;
	const oy = cut.focus.y * 100;
	// Solo se crean efectos WebGL si este corte los necesita (cada uno abre un contexto WebGL y Chrome tiene límite)
	const GL_TR = ['zoom-in', 'zoom-out', 'glitch', 'rgb-split'];
	const needsFx = GL_TR.includes(tin?.type ?? '') || GL_TR.includes(tout?.type ?? '');
	const effects = needsFx
		? [zoomBlur({amount: tr.zb ?? 0, center: [cut.focus.x, cut.focus.y], samples: 16, disabled: !tr.zb}), chromaticAberration({amount: tr.ca ?? 0, angle: 0, disabled: !tr.ca})]
		: [];
	return (
		<AbsoluteFill style={{overflow: 'hidden'}}>
			<AbsoluteFill
				style={{
					transformOrigin: `${ox}% ${oy}%`,
					transform: `translate(${(tr.tx ?? 0) + z.x * width + hh.x}px, ${(tr.ty ?? 0) + z.y * height + hh.y}px) scale(${scale}) rotate(${z.r + hh.r}deg)${cut.mirror ? ' scaleX(-1)' : ''}`,
					filter: filters || undefined,
				}}
			>
				<Video
					src={staticFile(cut.src)}
					trimBefore={Math.round(cut.in * fps)}
					playbackRate={cut.speed}
					volume={cut.volume ?? 1}
					objectFit="cover"
					style={{width: '100%', height: '100%', objectPosition: `${ox}% ${oy}%`}}
					effects={effects}
				/>
				{(cut.behind ?? []).map((b, k) => {
					const C = REGISTRY_BEHIND()[b.component];
					const bd = Math.max(1, Math.round((b.duration ?? cut.tl_end - cut.tl_start) * fps));
					return C ? (
						<Sequence key={k} from={Math.round((b.start ?? 0) * fps)} durationInFrames={bd} name={`detrás: ${b.component}`}>
							<C dur={bd} {...b.props} />
						</Sequence>
					) : null;
				})}
				{cut.cutout && (
					<AbsoluteFill>
						<OffthreadVideo src={staticFile(cut.cutout)} transparent muted playbackRate={cut.speed} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${ox}% ${oy}%`}} />
					</AbsoluteFill>
				)}
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

export const MainTrack: React.FC<{cuts: Cut[]; grade: string}> = ({cuts, grade}) => {
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill>
			{cuts.map((c, k) => {
				const from = Math.round(c.tl_start * fps);
				const to = Math.round(c.tl_end * fps);
				return (
					<Sequence key={`${c.i}-${k}`} name={`cut ${c.i}: ${c.text.slice(0, 30)}`} from={from} durationInFrames={Math.max(1, to - from)} premountFor={fps}>
						<ClipInner cut={c} next={cuts[k + 1]} grade={grade} />
					</Sequence>
				);
			})}
		</AbsoluteFill>
	);
};

/** Overlays de transición que no alteran el timing (flash, dip, glitch bars). Se dibujan sobre todo el video. */
export const TransitionOverlays: React.FC<{cuts: Cut[]; color: string}> = ({cuts, color}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<>
			{cuts.map((c) => {
				const tr = tName(c.transition);
				if (!tr) return null;
				const at = Math.round(c.tl_start * fps);
				const d = frame - at;
				const n = Math.max(2, Math.round(tr.duration * fps * 0.5));
				if (d < -n || d > n * 2) return null;
				if (tr.type === 'flash') {
					const o = interpolate(d, [-2, 0, n * 1.5], [0, 1, 0], clamp);
					return <AbsoluteFill key={c.i} style={{background: '#fff', opacity: o, mixBlendMode: 'screen'}} />;
				}
				if (tr.type === 'dip-black') {
					const o = interpolate(d, [-n, 0, n], [0, 1, 0], clamp);
					return <AbsoluteFill key={c.i} style={{background: '#000', opacity: o}} />;
				}
				if (tr.type === 'glitch') {
					if (d < -2 || d > n) return null;
					const bars = Array.from({length: 7}, (_, i) => {
						const y = ((Math.sin((at + i * 13) * 12.9898) * 43758.5453) % 1 + 1) % 1;
						return <div key={i} style={{position: 'absolute', left: 0, right: 0, top: `${y * 100}%`, height: `${2 + (i % 3) * 3}%`, background: i % 2 ? color : '#00e5ff', opacity: 0.5, mixBlendMode: 'screen', transform: `translateX(${(i % 2 ? 1 : -1) * 6}%)`}} />;
					});
					return <AbsoluteFill key={c.i}>{bars}</AbsoluteFill>;
				}
				return null;
			})}
		</>
	);
};
