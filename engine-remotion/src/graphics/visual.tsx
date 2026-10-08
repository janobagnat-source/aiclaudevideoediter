import {evolvePath} from '@remotion/paths';
import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA, inOut} from '../lib/anim';
import {useBrand} from '../lib/brand';
import type {GProps} from './text';

const useU = () => {
	const {width, height} = useVideoConfig();
	return Math.min(width, height) / 1080;
};
const src = (s?: string | null) => (!s ? undefined : s.startsWith('http') ? s : staticFile(s));

/** Flash de color (impacto). props: color, peak (0-1) */
export const Flash: React.FC<GProps & {color?: string; peak?: number}> = ({dur, color, peak = 0.9}) => {
	const frame = useCurrentFrame();
	const {colors} = useBrand();
	return <AbsoluteFill style={{background: color ?? colors.light, opacity: interpolate(frame, [0, 1, dur], [peak, peak, 0], {...clamp, easing: EASE.out}), mixBlendMode: 'screen'}} />;
};

/** Explosión radial de líneas (acento en un beat/impacto). props: x, y, color, count */
export const ShapeBurst: React.FC<GProps & {x?: number; y?: number; color?: string; count?: number; radius?: number}> = ({dur, x = 0.5, y = 0.4, color, count = 14, radius = 1}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const {colors} = useBrand();
	const p = interpolate(frame, [0, dur], [0, 1], {...clamp, easing: EASE.out});
	const R0 = 80 * u * radius;
	const R1 = 420 * u * radius;
	return (
		<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
			{Array.from({length: count}, (_, i) => {
				const a = (i / count) * Math.PI * 2 + random(`b${i}`) * 0.3;
				const r1 = R0 + (R1 - R0) * p;
				const r0 = R0 + (R1 - R0) * Math.max(0, p - 0.35) * 1.5;
				return <line key={i} x1={x * width + Math.cos(a) * r0} y1={y * height + Math.sin(a) * r0} x2={x * width + Math.cos(a) * r1} y2={y * height + Math.sin(a) * r1} stroke={i % 3 === 0 ? colors.secondary : (color ?? colors.primary)} strokeWidth={14 * u * (1 - p)} strokeLinecap="round" />;
			})}
			<circle cx={x * width} cy={y * height} r={R0 + (R1 - R0) * p * 0.8} fill="none" stroke={color ?? colors.light} strokeWidth={10 * u * (1 - p)} opacity={1 - p} />
		</svg>
	);
};

/** Flecha dibujada a mano que apunta a (x,y) con etiqueta. props: x, y, from {x,y}, label */
export const ArrowCallout: React.FC<GProps & {x: number; y: number; from?: {x: number; y: number}; label?: string; color?: string}> = ({dur, x, y, from, label, color}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const f = from ?? {x: x > 0.5 ? x - 0.3 : x + 0.3, y: y - 0.15};
	const X0 = f.x * width;
	const Y0 = f.y * height;
	const X1 = x * width;
	const Y1 = y * height;
	const cx = (X0 + X1) / 2 + (Y1 - Y0) * 0.3;
	const cy = (Y0 + Y1) / 2 - (X1 - X0) * 0.3;
	const path = `M ${X0} ${Y0} Q ${cx} ${cy} ${X1} ${Y1}`;
	const p = interpolate(frame, [0, 14], [0, 1], {...clamp, easing: EASE.out});
	const {strokeDasharray, strokeDashoffset} = evolvePath(p, path);
	const ang = Math.atan2(Y1 - cy, X1 - cx);
	const head = 44 * u;
	const o = inOut(frame, dur, 1, 8);
	const c = color ?? colors.secondary;
	return (
		<AbsoluteFill style={{opacity: o}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0, filter: 'drop-shadow(0 6px 12px rgba(0,0,0,.5))'}}>
				<path d={path} fill="none" stroke={c} strokeWidth={14 * u} strokeLinecap="round" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
				{p > 0.95 && (
					<path d={`M ${X1 - head * Math.cos(ang - 0.5)} ${Y1 - head * Math.sin(ang - 0.5)} L ${X1} ${Y1} L ${X1 - head * Math.cos(ang + 0.5)} ${Y1 - head * Math.sin(ang + 0.5)}`} fill="none" stroke={c} strokeWidth={14 * u} strokeLinecap="round" strokeLinejoin="round" />
				)}
			</svg>
			{label && (
				<div style={{position: 'absolute', left: X0, top: Y0, transform: `translate(-50%, -120%) scale(${spring({frame: frame - 4, fps: 30, config: {damping: 12}})})`, background: c, color: colors.dark, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 46 * u, padding: `${8 * u}px ${20 * u}px`, borderRadius: 14 * u, whiteSpace: 'nowrap'}}>
					{label}
				</div>
			)}
		</AbsoluteFill>
	);
};

/** Círculo/marcador dibujado alrededor de una zona. props: x, y, w, h (0-1) */
export const CircleHighlight: React.FC<GProps & {x: number; y: number; w?: number; h?: number; color?: string}> = ({dur, x, y, w = 0.3, h = 0.12, color}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const {colors} = useBrand();
	const rx = (w * width) / 2;
	const ry = (h * height) / 2;
	const cx = x * width;
	const cy = y * height;
	const path = `M ${cx + rx} ${cy} C ${cx + rx} ${cy - ry * 1.1}, ${cx - rx * 1.05} ${cy - ry * 1.05}, ${cx - rx} ${cy} C ${cx - rx} ${cy + ry * 1.1}, ${cx + rx * 1.1} ${cy + ry}, ${cx + rx * 1.02} ${cy - ry * 0.2}`;
	const p = interpolate(frame, [0, 12], [0, 1], {...clamp, easing: EASE.out});
	const ev = evolvePath(p, path);
	return (
		<svg width={width} height={height} style={{position: 'absolute', inset: 0, opacity: inOut(frame, dur, 1, 6)}}>
			<path d={path} fill="none" stroke={color ?? colors.primary} strokeWidth={12 * u} strokeLinecap="round" {...ev} style={{filter: `drop-shadow(0 0 10px ${color ?? colors.primary})`}} />
		</svg>
	);
};

/** Icono (SVG de iconify descargado con `ve stock icon`) o emoji que hace pop. props: src | emoji, x, y, size, label */
export const IconPop: React.FC<GProps & {src?: string; emoji?: string; x?: number; y?: number; size?: number; label?: string; tint?: boolean}> = ({dur, src: s, emoji, x = 0.5, y = 0.3, size = 1, label, tint = true}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const sp = spring({frame, fps, config: {stiffness: 420, damping: 10, mass: 0.7}});
	const out = interpolate(frame, [dur - 6, dur], [1, 0], clamp);
	const S = 260 * u * size;
	const float = Math.sin(frame / 10) * 8 * u;
	return (
		<div style={{position: 'absolute', left: x * width - S / 2, top: y * height - S / 2 + float, width: S, display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `scale(${sp * out}) rotate(${(1 - sp) * 25}deg)`}}>
			<div style={{width: S, height: S, borderRadius: S * 0.28, background: tint ? `linear-gradient(145deg, ${colors.primary}, ${hexA(colors.primary, 0.7)})` : 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: tint ? `0 20px 60px ${hexA(colors.primary, 0.5)}, inset 0 2px 0 rgba(255,255,255,.35)` : undefined}}>
				{emoji ? <span style={{fontSize: S * 0.62}}>{emoji}</span> : s ? <Img src={src(s)!} style={{width: '62%', height: '62%', filter: tint ? 'brightness(0) invert(1)' : undefined}} /> : null}
			</div>
			{label && <div style={{marginTop: 16 * u, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 44 * u, color: colors.light, textShadow: '0 6px 20px rgba(0,0,0,.6)', textAlign: 'center', whiteSpace: 'nowrap'}}>{label}</div>}
		</div>
	);
};

/** Fondo animado de marca para escenas de motion graphics a pantalla completa. variant: 'mesh'|'grid'|'rays'|'dark' */
export const BrandBackground: React.FC<GProps & {variant?: 'mesh' | 'grid' | 'rays' | 'dark'}> = ({variant = 'mesh'}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const {colors} = useBrand();
	const t = frame / 60;
	const blob = (c: string, sx: string, i: number) => {
		const x = 50 + noise2D(sx + 'x', t * 0.4, i) * 40;
		const y = 50 + noise2D(sx + 'y', i, t * 0.4) * 40;
		return `radial-gradient(circle at ${x}% ${y}%, ${hexA(c, 0.85)} 0%, ${hexA(c, 0)} 45%)`;
	};
	if (variant === 'grid') {
		const off = (frame * 2) % 80;
		return (
			<AbsoluteFill style={{background: colors.dark}}>
				<AbsoluteFill style={{backgroundImage: `linear-gradient(${hexA(colors.light, 0.07)} 2px, transparent 2px), linear-gradient(90deg, ${hexA(colors.light, 0.07)} 2px, transparent 2px)`, backgroundSize: '80px 80px', backgroundPosition: `0 ${off}px`, transform: 'perspective(900px) rotateX(55deg) scale(2.2)', transformOrigin: '50% 100%'}} />
				<AbsoluteFill style={{background: `radial-gradient(circle at 50% 35%, ${hexA(colors.primary, 0.45)}, transparent 60%)`}} />
			</AbsoluteFill>
		);
	}
	if (variant === 'rays') {
		return (
			<AbsoluteFill style={{background: colors.dark, overflow: 'hidden'}}>
				<div style={{position: 'absolute', left: width / 2 - height, top: -height / 2, width: height * 2, height: height * 2, background: `repeating-conic-gradient(from ${frame * 0.4}deg, ${hexA(colors.primary, 0.35)} 0deg 8deg, transparent 8deg 22deg)`, borderRadius: '50%'}} />
				<AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, transparent 0%, ${colors.dark} 70%)`}} />
			</AbsoluteFill>
		);
	}
	if (variant === 'dark') return <AbsoluteFill style={{background: `radial-gradient(circle at 50% 40%, ${hexA(colors.primary, 0.25)}, ${colors.dark} 65%)`}} />;
	return <AbsoluteFill style={{background: [blob(colors.primary, 'a', 1), blob(colors.secondary, 'b', 2), blob(colors.accent, 'c', 3), colors.dark].join(',')}} />;
};

/** Reveal de logo con barrido de luz y glow. props: logo (ruta), tagline, bg */
export const LogoSting: React.FC<GProps & {logo?: string; tagline?: string; bg?: boolean; size?: number}> = ({dur, logo, tagline, bg = true, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useU();
	const brand = useBrand();
	const s = spring({frame, fps, config: {stiffness: 120, damping: 14}});
	const sweep = interpolate(frame, [10, 30], [-120, 220], clamp);
	const o = inOut(frame, dur, 1, 10);
	const L = logo ?? brand.logo;
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: o}}>
			{bg && <BrandBackground dur={dur} variant="dark" />}
			<div style={{position: 'relative', transform: `scale(${0.6 + 0.4 * s})`, filter: `blur(${(1 - s) * 12}px) drop-shadow(0 0 ${40 * u * s}px ${hexA(brand.colors.primary, 0.8)})`}}>
				{L && <Img src={src(L)!} style={{width: 620 * u * size, maxHeight: 420 * u * size, objectFit: 'contain'}} />}
				<div style={{position: 'absolute', inset: 0, background: `linear-gradient(100deg, transparent ${sweep - 20}%, rgba(255,255,255,.75) ${sweep}%, transparent ${sweep + 20}%)`, mixBlendMode: 'overlay', WebkitMaskImage: L ? `url(${src(L)})` : undefined, WebkitMaskSize: 'contain', WebkitMaskRepeat: 'no-repeat', WebkitMaskPosition: 'center'}} />
			</div>
			{tagline && <div style={{marginTop: 40 * u, fontFamily: `${brand.fonts.body}, sans-serif`, fontWeight: 700, fontSize: 46 * u, color: brand.colors.light, letterSpacing: 6, textTransform: 'uppercase', opacity: interpolate(frame, [18, 30], [0, 1], clamp), transform: `translateY(${interpolate(frame, [18, 30], [20, 0], clamp)}px)`}}>{tagline}</div>}
		</AbsoluteFill>
	);
};

/** Cierre con llamado a la acción. props: headline, button, sub, logo, arrow, bg */
export const CTAEndCard: React.FC<GProps & {headline: string; button?: string; sub?: string; logo?: string; bg?: 'mesh' | 'grid' | 'rays' | 'dark' | 'none'; arrow?: boolean; position?: number}> = ({
	dur,
	headline,
	button = 'Más información',
	sub,
	logo,
	bg = 'mesh',
	arrow = true,
	position = 0.45,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useU();
	const brand = useBrand();
	const {colors, fonts} = brand;
	const a = spring({frame, fps, config: {damping: 14, stiffness: 160}});
	const b = spring({frame: frame - 8, fps, config: {damping: 10, stiffness: 220}});
	const pulse = 1 + 0.05 * Math.max(0, Math.sin((frame - 20) / 5));
	const L = logo ?? brand.logo;
	const o = interpolate(frame, [0, 6], [0, 1], clamp);
	return (
		<AbsoluteFill style={{opacity: o}}>
			{bg !== 'none' && <BrandBackground dur={dur} variant={bg} />}
			<div style={{position: 'absolute', top: `${position * 100}%`, left: '8%', right: '8%', transform: 'translateY(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
				{L && <Img src={src(L)!} style={{width: 380 * u, maxHeight: 200 * u, objectFit: 'contain', marginBottom: 50 * u, transform: `scale(${a})`}} />}
				<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 96 * u * (headline.length > 28 ? 28 / headline.length + 0.2 : 1), lineHeight: 1, color: colors.light, textTransform: 'uppercase', transform: `translateY(${(1 - a) * 60}px)`, opacity: a, textShadow: '0 10px 40px rgba(0,0,0,.5)'}}>{headline}</div>
				{sub && <div style={{marginTop: 24 * u, fontFamily: `${fonts.body}, sans-serif`, fontWeight: 600, fontSize: 44 * u, color: hexA(colors.light, 0.85), opacity: a}}>{sub}</div>}
				<div style={{marginTop: 56 * u, transform: `scale(${b * pulse})`, background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`, color: colors.light, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 56 * u, padding: `${28 * u}px ${64 * u}px`, borderRadius: 999, boxShadow: `0 20px 60px ${hexA(colors.primary, 0.6)}, inset 0 2px 0 rgba(255,255,255,.4)`, textTransform: 'uppercase', position: 'relative', overflow: 'hidden'}}>
					{button}
					<div style={{position: 'absolute', inset: 0, background: `linear-gradient(100deg, transparent ${((frame * 3) % 200) - 60}%, rgba(255,255,255,.45) ${((frame * 3) % 200) - 40}%, transparent ${((frame * 3) % 200) - 20}%)`}} />
				</div>
				{arrow && <div style={{marginTop: 30 * u, fontSize: 90 * u, color: colors.light, transform: `translateY(${Math.sin(frame / 5) * 14 * u}px)`, opacity: b}}>↓</div>}
			</div>
		</AbsoluteFill>
	);
};

/** Notificación estilo app (prueba social / venta). props: title, body, icon, y */
export const Notification: React.FC<GProps & {title: string; body: string; app?: string; y?: number; icon?: string}> = ({dur, title, body, app = 'Ahora', y = 0.12, icon}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const s = spring({frame, fps, config: {damping: 16, stiffness: 220}});
	const out = interpolate(frame, [dur - 10, dur], [0, 1], {...clamp, easing: EASE.in});
	return (
		<div style={{position: 'absolute', top: `${y * 100}%`, left: '5%', right: '5%', transform: `translateY(${(1 - s) * -220 * u - out * 260 * u}px)`, background: 'rgba(245,245,247,.92)', backdropFilter: 'blur(20px)', borderRadius: 40 * u, padding: `${26 * u}px ${30 * u}px`, display: 'flex', gap: 22 * u, alignItems: 'center', boxShadow: '0 20px 60px rgba(0,0,0,.35)'}}>
			<div style={{width: 96 * u, height: 96 * u, borderRadius: 24 * u, background: colors.primary, flex: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>{icon ? <Img src={src(icon)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : <span style={{fontSize: 54 * u}}>💰</span>}</div>
			<div style={{flex: 1, fontFamily: `${fonts.body}, -apple-system, sans-serif`, color: '#111'}}>
				<div style={{display: 'flex', justifyContent: 'space-between', fontWeight: 800, fontSize: 38 * u}}>
					<span>{title}</span>
					<span style={{fontWeight: 500, fontSize: 30 * u, color: '#666'}}>{app}</span>
				</div>
				<div style={{fontSize: 36 * u, fontWeight: 500, marginTop: 4 * u, lineHeight: 1.2}}>{body}</div>
			</div>
		</div>
	);
};

/** Imagen/captura flotante (mockup) con sombra y leve 3D. props: src, x, y, w, rotate, radius */
export const FloatingCard: React.FC<GProps & {src: string; x?: number; y?: number; w?: number; rotate?: number; radius?: number}> = ({dur, src: s, x = 0.5, y = 0.4, w = 0.7, rotate = -4, radius = 32}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const sp = spring({frame, fps, config: {damping: 15, stiffness: 140}});
	const out = interpolate(frame, [dur - 8, dur], [1, 0], clamp);
	const W = w * width;
	return (
		<div style={{position: 'absolute', left: x * width - W / 2, top: y * height, transform: `translateY(-50%) perspective(1400px) rotateY(${(1 - sp) * 35 + Math.sin(frame / 30) * 4}deg) rotateZ(${rotate * sp}deg) scale(${(0.7 + 0.3 * sp) * out})`, opacity: out}}>
			<Img src={src(s)!} style={{width: W, borderRadius: radius * u, boxShadow: '0 40px 120px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.12)'}} />
		</div>
	);
};
