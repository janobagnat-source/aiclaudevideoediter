import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {useBrand} from '../lib/brand';
import type {Layout} from '../types';

const smooth = (x: number) => {
	const k = Math.min(1, Math.max(0, x));
	return k * k * k * (k * (k * 6 - 15) + 10); // smootherstep
};

/** Layout activo y su intensidad (0→1 con entrada/salida suaves) */
export const useLayout = (layouts: Layout[]) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	for (const L of layouts) {
		const e = L.ease ?? 0.42;
		const a = L.start;
		const b = L.start + L.duration;
		if (t >= a - 0.001 && t < b) return {L, k: smooth(Math.min((t - a) / e, (b - t) / e)), t: t - a};
	}
	return {L: null as Layout | null, k: 0, t: 0};
};

/** Fondo de marca que aparece detrás de la ventana del split (degradado + grilla fina + glow) */
export const LayoutBackdrop: React.FC<{layouts: Layout[]}> = ({layouts}) => {
	const {L, k, t} = useLayout(layouts);
	const {width, height} = useVideoConfig();
	const {colors} = useBrand();
	if (!L || k <= 0) return null;
	const u = width / 1080;
	return (
		<AbsoluteFill style={{opacity: k, background: `radial-gradient(120% 60% at 50% 100%, ${colors.blueDeep ?? '#0034B7'}cc 0%, #031049 38%, ${colors.dark} 75%)`}}>
			<AbsoluteFill
				style={{
					backgroundImage: `linear-gradient(rgba(120,150,255,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(120,150,255,.07) 1px, transparent 1px)`,
					backgroundSize: `${54 * u}px ${54 * u}px`,
					backgroundPosition: `0 ${-t * 18 * u}px`,
					maskImage: 'linear-gradient(to bottom, transparent 40%, black 75%)',
				}}
			/>
			<div style={{position: 'absolute', left: '50%', top: height * 0.82, width: width * 1.2, height: width * 0.6, transform: 'translate(-50%,-50%)', background: `radial-gradient(closest-side, ${colors.blue ?? '#3474FF'}55, transparent)`, filter: `blur(${30 * u}px)`}} />
		</AbsoluteFill>
	);
};

/** Envuelve el track principal y lo convierte en una ventana flotante (split) sin recortar la cara */
export const LayoutFrame: React.FC<{layouts: Layout[]; children: React.ReactNode}> = ({layouts, children}) => {
	const {L, k} = useLayout(layouts);
	const {width, height} = useVideoConfig();
	const {colors} = useBrand();
	if (!L || k <= 0) return <AbsoluteFill>{children}</AbsoluteFill>;
	const u = width / 1080;
	const top = (L.top ?? 0.025) * k;
	const bottom = 1 - (1 - (L.bottom ?? 0.53)) * k; // borde inferior de la ventana (fracción del alto)
	const side = 0.035 * k;
	const r = (L.radius ?? 46) * u * k;
	// la imagen se desplaza levemente hacia arriba para que el rostro quede centrado en la ventana
	const shift = -height * 0.035 * k;
	const gold = colors.gold ?? colors.secondary;
	return (
		<AbsoluteFill>
			<AbsoluteFill
				style={{
					clipPath: `inset(${top * 100}% ${side * 100}% ${(1 - bottom) * 100}% ${side * 100}% round ${r}px)`,
				}}
			>
				<AbsoluteFill style={{transform: `translateY(${shift}px) scale(${1 - 0.04 * k})`, transformOrigin: '50% 20%'}}>{children}</AbsoluteFill>
			</AbsoluteFill>
			{/* filo dorado + sombra de la ventana */}
			<div
				style={{
					position: 'absolute',
					left: `${side * 100}%`,
					right: `${side * 100}%`,
					top: `${top * 100}%`,
					height: `${(bottom - top) * 100}%`,
					borderRadius: r,
					boxShadow: `0 ${40 * u}px ${90 * u}px rgba(0,0,0,${0.6 * k}), inset 0 0 0 ${2 * u}px rgba(255,255,255,${0.12 * k})`,
					pointerEvents: 'none',
				}}
			/>
			<div style={{position: 'absolute', left: '50%', top: `${bottom * 100}%`, width: width * 0.36 * k, height: 3 * u, transform: 'translate(-50%,-50%)', background: `linear-gradient(90deg, transparent, ${gold}, transparent)`, boxShadow: `0 0 ${18 * u}px ${gold}`}} />
		</AbsoluteFill>
	);
};
