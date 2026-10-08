import {fitText} from '@remotion/layout-utils';
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA, impactShake, inOut} from '../lib/anim';
import {useBrand} from '../lib/brand';

export type GProps = {dur: number};

const nrm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9ñ%$]/g, '');

const useUnit = () => {
	const {width, height} = useVideoConfig();
	return Math.min(width, height) / 1080; // 1 = 1080 de lado corto
};

/**
 * HOOK: titular de impacto para los primeros 1-3 s.
 * props: lines[], highlight[] (palabras en color), variant 'slam'|'stack'|'glitch'|'split', position 0-1, bg 'none'|'dim'|'brand'|'blur', size
 */
export const HookTitle: React.FC<GProps & {lines: string[]; highlight?: string[]; variant?: 'slam' | 'stack' | 'glitch' | 'split'; position?: number; bg?: 'none' | 'dim' | 'brand' | 'blur'; size?: number; stagger?: number}> = ({
	dur,
	lines,
	highlight = [],
	variant = 'slam',
	position = 0.42,
	bg = 'dim',
	size = 1,
	stagger = 5,
}) => {
	const frame = useCurrentFrame();
	const {fps, width} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const hl = new Set(highlight.map(nrm));
	const family = `${fonts.heading}, Anton, Montserrat, sans-serif`;
	const lineSize = (line: string) =>
		Math.min(150 * u * size, fitText({text: line, withinWidth: width * 0.86, fontFamily: fonts.heading, fontWeight: 900, textTransform: 'uppercase', letterSpacing: `${-2 * u}px`}).fontSize);
	const out = interpolate(frame, [dur - 7, dur], [1, 0], {...clamp, easing: EASE.in});
	let shake = {x: 0, y: 0};
	lines.forEach((_, i) => {
		const s = impactShake(frame, i * stagger + 3, fps, 22 * u, 0.28);
		shake = {x: shake.x + s.x, y: shake.y + s.y};
	});
	const bgOp = interpolate(frame, [0, 4], [0, 1], clamp) * out;
	return (
		<AbsoluteFill style={{transform: `translate(${shake.x}px, ${shake.y}px)`}}>
			{bg === 'dim' && <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.15), rgba(0,0,0,.55) 50%, rgba(0,0,0,.15))', opacity: bgOp}} />}
			{bg === 'brand' && <AbsoluteFill style={{background: `radial-gradient(circle at 50% 40%, ${colors.primary}, ${colors.dark} 75%)`, opacity: bgOp}} />}
			{bg === 'blur' && <AbsoluteFill style={{backdropFilter: 'blur(18px) brightness(.6)', opacity: bgOp}} />}
			<div style={{position: 'absolute', top: `${position * 100}%`, left: 0, right: 0, transform: 'translateY(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 * u}}>
				{lines.map((line, i) => {
					const d = i * stagger;
					const f = frame - d;
					const s = spring({frame: f, fps, config: {stiffness: 420, damping: 20, mass: 0.8}});
					const scale = variant === 'slam' ? interpolate(s, [0, 1], [2.4, 1]) : variant === 'stack' ? 1 : interpolate(s, [0, 1], [0.6, 1]);
					const ty = variant === 'stack' ? interpolate(s, [0, 1], [120 * u, 0]) : 0;
					const tx = variant === 'split' ? interpolate(s, [0, 1], [(i % 2 ? 1 : -1) * 600 * u, 0]) : 0;
					const blur = variant === 'slam' ? interpolate(f, [0, 4], [16, 0], clamp) : 0;
					const glitch = variant === 'glitch' && f >= 0 && f < 8 ? (f % 2 ? 10 : -10) * u : 0;
					const words = line.split(' ');
					return (
						<div key={i} style={{overflow: variant === 'stack' ? 'hidden' : 'visible', padding: `0 ${20 * u}px`}}>
							<div
								style={{
									opacity: f < 0 ? 0 : out,
									transform: `translate(${tx + glitch}px, ${ty}px) scale(${scale})`,
									filter: blur ? `blur(${blur}px)` : undefined,
									fontFamily: family,
									fontWeight: 900,
									fontSize: lineSize(line),
									lineHeight: 0.95,
									letterSpacing: -2 * u,
									textTransform: 'uppercase',
									color: colors.light,
									textAlign: 'center',
									textShadow: variant === 'glitch' ? `${4 * u}px 0 ${colors.accent}, ${-4 * u}px 0 ${colors.primary}, 0 10px 40px rgba(0,0,0,.6)` : '0 10px 40px rgba(0,0,0,.6)',
									whiteSpace: 'nowrap',
								}}
							>
								{words.map((w, k) => {
									const on = hl.has(nrm(w));
									const sweep = interpolate(f, [5, 11], [0, 1], {...clamp, easing: EASE.out});
									return (
										<span key={k} style={{position: 'relative', display: 'inline-block', marginRight: k < words.length - 1 ? '0.22em' : 0, color: on ? colors.dark : undefined, zIndex: 1}}>
											{on && <span style={{position: 'absolute', inset: '-0.02em -0.12em', background: colors.primary, transformOrigin: 'left', transform: `scaleX(${sweep}) skewX(-8deg)`, zIndex: -1, borderRadius: 8 * u}} />}
											{w}
										</span>
									);
								})}
							</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Texto cinético palabra por palabra (máscara). props: text, emphasis[], position, size, align, color, box */
export const KineticText: React.FC<GProps & {text: string; emphasis?: string[]; position?: number; size?: number; align?: 'center' | 'left'; perWord?: number; box?: boolean; uppercase?: boolean}> = ({
	dur,
	text,
	emphasis = [],
	position = 0.3,
	size = 1,
	align = 'center',
	perWord = 3,
	box = false,
	uppercase = true,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const em = new Set(emphasis.map(nrm));
	const o = inOut(frame, dur, 1, 8);
	const words = text.split(' ');
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: '7%', right: '7%', transform: 'translateY(-50%)', display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', gap: `${4 * u}px ${18 * u}px`, opacity: o, background: box ? hexA(colors.dark, 0.78) : undefined, padding: box ? 30 * u : 0, borderRadius: 28 * u}}>
				{words.map((w, i) => {
					const s = spring({frame: frame - i * perWord, fps, config: {damping: 16, stiffness: 260, mass: 0.6}});
					const on = em.has(nrm(w));
					return (
						<span key={i} style={{overflow: 'hidden', display: 'inline-block', paddingBottom: 6 * u}}>
							<span
								style={{
									display: 'inline-block',
									transform: `translateY(${(1 - s) * 110}%) rotate(${(1 - s) * 6}deg)`,
									fontFamily: `${fonts.heading}, Montserrat, sans-serif`,
									fontWeight: on ? 900 : 800,
									fontSize: 96 * u * size * (on ? 1.15 : 1),
									lineHeight: 1,
									color: on ? colors.primary : colors.light,
									textTransform: uppercase ? 'uppercase' : 'none',
									textShadow: '0 8px 30px rgba(0,0,0,.5)',
								}}
							>
								{w}
							</span>
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Lower third (nombre + cargo). props: name, title, side 'left'|'right', position */
export const LowerThird: React.FC<GProps & {name: string; title?: string; position?: number; side?: 'left' | 'right'}> = ({dur, name, title, position = 0.8, side = 'left'}) => {
	const frame = useCurrentFrame();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const a = interpolate(frame, [0, 12], [0, 1], {...clamp, easing: EASE.out});
	const b = interpolate(frame, [6, 18], [0, 1], {...clamp, easing: EASE.out});
	const out = interpolate(frame, [dur - 10, dur], [0, 1], {...clamp, easing: EASE.in});
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', top: `${position * 100}%`, [side]: '6%', transform: `translateX(${(side === 'left' ? -1 : 1) * out * 120}%)`, display: 'flex', flexDirection: 'column', alignItems: side === 'left' ? 'flex-start' : 'flex-end'}}>
				<div style={{background: colors.primary, height: 10 * u, width: `${a * 120}px`, marginBottom: 10 * u, borderRadius: 6}} />
				<div style={{clipPath: `inset(0 ${(1 - a) * 100}% 0 0)`, background: colors.light, color: colors.dark, padding: `${10 * u}px ${24 * u}px`, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 54 * u, borderRadius: 10 * u}}>{name}</div>
				{title && (
					<div style={{clipPath: `inset(0 ${(1 - b) * 100}% 0 0)`, background: colors.dark, color: colors.light, padding: `${8 * u}px ${24 * u}px`, fontFamily: `${fonts.body}, sans-serif`, fontWeight: 600, fontSize: 34 * u, marginTop: 6 * u, borderRadius: 10 * u}}>
						{title}
					</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/** Contador numérico. props: value, from, prefix, suffix, label, decimals, position, ring */
export const StatCounter: React.FC<GProps & {value: number; from?: number; prefix?: string; suffix?: string; label?: string; decimals?: number; position?: number; ring?: boolean; countFrames?: number}> = ({
	dur,
	value,
	from = 0,
	prefix = '',
	suffix = '',
	label,
	decimals = 0,
	position = 0.35,
	ring = true,
	countFrames = 28,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const p = interpolate(frame, [3, 3 + countFrames], [0, 1], {...clamp, easing: EASE.out});
	const v = from + (value - from) * p;
	const s = spring({frame, fps, config: {stiffness: 300, damping: 18}});
	const done = frame > 3 + countFrames ? spring({frame: frame - 3 - countFrames, fps, config: {stiffness: 500, damping: 12}}) : 0;
	const o = inOut(frame, dur, 1, 8);
	const R = 230 * u;
	const C = 2 * Math.PI * R;
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: 0, right: 0, transform: `translateY(-50%) scale(${(0.7 + 0.3 * s) * (1 + 0.06 * Math.sin(done * Math.PI))})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
				<div style={{position: 'relative', width: R * 2 + 40 * u, height: R * 2 + 40 * u, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					{ring && (
						<svg width="100%" height="100%" style={{position: 'absolute', inset: 0, transform: 'rotate(-90deg)'}} viewBox={`0 0 ${R * 2 + 40 * u} ${R * 2 + 40 * u}`}>
							<circle cx="50%" cy="50%" r={R} fill={hexA(colors.dark, 0.6)} stroke={hexA(colors.light, 0.15)} strokeWidth={22 * u} />
							<circle cx="50%" cy="50%" r={R} fill="none" stroke={colors.primary} strokeWidth={22 * u} strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - p)} style={{filter: `drop-shadow(0 0 ${18 * u}px ${colors.primary})`}} />
						</svg>
					)}
					<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: Math.min(170 * u, (R * 1.5) / Math.max(1, (prefix + Math.round(value).toLocaleString('es-AR') + (suffix.length <= 2 ? suffix : '')).length * 0.62)), color: colors.light, textShadow: '0 10px 40px rgba(0,0,0,.6)', fontVariantNumeric: 'tabular-nums', zIndex: 1, whiteSpace: 'nowrap', textAlign: 'center', lineHeight: 0.95}}>
						{prefix}
						{v.toLocaleString('es-AR', {minimumFractionDigits: decimals, maximumFractionDigits: decimals})}
						{suffix.length <= 2 ? suffix : null}
						{suffix.length > 2 && <div style={{fontSize: '0.32em', letterSpacing: 2, textTransform: 'uppercase', marginTop: 6 * u}}>{suffix.trim()}</div>}
					</div>
				</div>
				{label && <div style={{marginTop: 18 * u, fontFamily: `${fonts.body}, sans-serif`, fontWeight: 800, fontSize: 48 * u, color: colors.light, textTransform: 'uppercase', letterSpacing: 2, background: colors.primary, padding: `${8 * u}px ${24 * u}px`, borderRadius: 12 * u, opacity: interpolate(frame, [10, 18], [0, 1], clamp)}}>{label}</div>}
			</div>
		</AbsoluteFill>
	);
};

/** Lista con checks que aparecen en secuencia. props: items[], title, every (frames), position, icon '✓'|'✗'|'→'|n */
export const Checklist: React.FC<GProps & {items: string[]; title?: string; every?: number; position?: number; icon?: string; bad?: boolean}> = ({dur, items, title, every = 12, position = 0.4, icon = '✓', bad = false}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const o = inOut(frame, dur, 6, 8);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: '8%', right: '8%', transform: 'translateY(-50%)', background: hexA(colors.dark, 0.85), borderRadius: 36 * u, padding: 44 * u, boxShadow: '0 30px 90px rgba(0,0,0,.5)', border: `2px solid ${hexA(colors.light, 0.12)}`}}>
				{title && <div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 60 * u, color: colors.light, marginBottom: 26 * u, textTransform: 'uppercase'}}>{title}</div>}
				{items.map((it, i) => {
					const s = spring({frame: frame - 6 - i * every, fps, config: {stiffness: 300, damping: 16}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 22 * u, margin: `${14 * u}px 0`, transform: `translateX(${(1 - s) * -80}px)`, opacity: s}}>
							<div style={{width: 70 * u, height: 70 * u, flex: 'none', borderRadius: 18 * u, background: bad ? '#ff3b30' : colors.primary, color: colors.light, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 44 * u, fontWeight: 900, transform: `scale(${s})`, fontFamily: 'Inter, sans-serif'}}>
								{icon === 'n' ? i + 1 : bad ? '✕' : icon}
							</div>
							<div style={{fontFamily: `${fonts.body}, sans-serif`, fontWeight: 700, fontSize: 50 * u, color: colors.light, lineHeight: 1.1}}>{it}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Badge de oferta con starburst giratorio. props: text, sub, position {x,y}, size */
export const OfferBadge: React.FC<GProps & {text: string; sub?: string; x?: number; y?: number; size?: number}> = ({dur, text, sub, x = 0.72, y = 0.24, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const s = spring({frame, fps, config: {stiffness: 260, damping: 11}});
	const o = interpolate(frame, [dur - 8, dur], [1, 0], clamp);
	const R = 190 * u * size;
	const pts = Array.from({length: 32}, (_, i) => {
		const a = (i / 32) * Math.PI * 2;
		const r = i % 2 ? R * 0.84 : R;
		return `${R + Math.cos(a) * r},${R + Math.sin(a) * r}`;
	}).join(' ');
	return (
		<div style={{position: 'absolute', left: x * width - R, top: y * height - R, width: R * 2, height: R * 2, transform: `scale(${s}) rotate(${(1 - s) * -90 + Math.sin(frame / 8) * 4}deg)`, opacity: o}}>
			<svg width={R * 2} height={R * 2} style={{position: 'absolute', transform: `rotate(${frame * 0.6}deg)`, filter: `drop-shadow(0 12px 30px rgba(0,0,0,.5))`}}>
				<polygon points={pts} fill={colors.secondary} />
			</svg>
			<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: `${fonts.heading}, sans-serif`, color: colors.dark, textAlign: 'center', lineHeight: 0.95}}>
				<div style={{fontSize: 92 * u * size * (text.length > 5 ? 5 / text.length : 1), fontWeight: 900}}>{text}</div>
				{sub && <div style={{fontSize: 34 * u * size, fontWeight: 800, textTransform: 'uppercase'}}>{sub}</div>}
			</div>
		</div>
	);
};

/** Barra de progreso superior (retención en VSL). props: color, height */
export const ProgressBar: React.FC<GProps & {thickness?: number; top?: boolean}> = ({dur, thickness = 10, top = true}) => {
	const frame = useCurrentFrame();
	const {colors} = useBrand();
	const u = useUnit();
	return (
		<div style={{position: 'absolute', left: 0, [top ? 'top' : 'bottom']: 0, height: thickness * u, width: `${(frame / dur) * 100}%`, background: `linear-gradient(90deg, ${colors.primary}, ${colors.secondary})`, boxShadow: `0 0 20px ${colors.primary}`}} />
	);
};

/** Cuenta regresiva / urgencia. props: seconds (desde), label */
export const Countdown: React.FC<GProps & {from?: string; label?: string; position?: number}> = ({dur, from = '23:59:59', label = 'La oferta termina en', position = 0.3}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const [h, m, s] = from.split(':').map(Number);
	const total = h * 3600 + m * 60 + s - Math.floor(frame / fps);
	const f2 = (n: number) => String(Math.max(0, n)).padStart(2, '0');
	const txt = `${f2(Math.floor(total / 3600))}:${f2(Math.floor((total % 3600) / 60))}:${f2(total % 60)}`;
	const o = inOut(frame, dur);
	const tick = 1 + 0.04 * Math.max(0, 1 - (frame % fps) / 6);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: 0, right: 0, transform: 'translateY(-50%)', textAlign: 'center'}}>
				<div style={{fontFamily: `${fonts.body}, sans-serif`, fontWeight: 800, fontSize: 40 * u, color: colors.light, textTransform: 'uppercase', letterSpacing: 3}}>{label}</div>
				<div style={{display: 'inline-block', marginTop: 14 * u, fontFamily: `${fonts.heading}, monospace`, fontWeight: 900, fontSize: 130 * u, color: colors.light, background: colors.primary, padding: `${6 * u}px ${30 * u}px`, borderRadius: 20 * u, transform: `scale(${tick})`, fontVariantNumeric: 'tabular-nums', boxShadow: `0 0 60px ${hexA(colors.primary, 0.7)}`}}>{txt}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Cita / testimonio con estrellas. props: quote, author, stars */
export const Testimonial: React.FC<GProps & {quote: string; author?: string; stars?: number; position?: number}> = ({dur, quote, author, stars = 5, position = 0.35}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const s = spring({frame, fps, config: {damping: 18, stiffness: 200}});
	const o = inOut(frame, dur, 1, 8);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: '7%', right: '7%', transform: `translateY(-50%) translateY(${(1 - s) * 80}px) rotate(${(1 - s) * -3}deg)`, background: colors.light, borderRadius: 36 * u, padding: 46 * u, boxShadow: '0 40px 100px rgba(0,0,0,.5)'}}>
				<div style={{fontSize: 56 * u, color: colors.secondary, letterSpacing: 6}}>
					{Array.from({length: stars}, (_, i) => (
						<span key={i} style={{display: 'inline-block', transform: `scale(${spring({frame: frame - 8 - i * 3, fps, config: {stiffness: 500, damping: 12}})})`}}>
							★
						</span>
					))}
				</div>
				<div style={{fontFamily: `${fonts.body}, serif`, fontWeight: 700, fontSize: 52 * u, color: colors.dark, lineHeight: 1.2, marginTop: 12 * u}}>“{quote}”</div>
				{author && <div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontSize: 36 * u, color: colors.primary, marginTop: 20 * u}}>— {author}</div>}
			</div>
		</AbsoluteFill>
	);
};

/** Gráfico de barras animado. props: bars [{label, value}], title, unit */
export const BarChart: React.FC<GProps & {bars: {label: string; value: number; highlight?: boolean}[]; title?: string; unit?: string; position?: number}> = ({dur, bars, title, unit = '', position = 0.45}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const max = Math.max(...bars.map((b) => b.value));
	const o = inOut(frame, dur, 6, 8);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', top: `${position * 100}%`, left: '8%', right: '8%', height: 700 * u, transform: 'translateY(-50%)', background: hexA(colors.dark, 0.85), borderRadius: 36 * u, padding: 40 * u, display: 'flex', flexDirection: 'column'}}>
				{title && <div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 54 * u, color: colors.light, marginBottom: 20 * u}}>{title}</div>}
				<div style={{flex: 1, display: 'flex', alignItems: 'flex-end', gap: 26 * u}}>
					{bars.map((b, i) => {
						const s = spring({frame: frame - 8 - i * 5, fps, config: {damping: 14, stiffness: 120}});
						return (
							<div key={i} style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end'}}>
								<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 42 * u, color: colors.light, opacity: s}}>{Math.round(b.value * s)}{unit}</div>
								<div style={{width: '100%', height: `${(b.value / max) * 75 * s}%`, background: b.highlight ? `linear-gradient(180deg, ${colors.secondary}, ${colors.primary})` : hexA(colors.light, 0.25), borderRadius: `${16 * u}px ${16 * u}px 4px 4px`, boxShadow: b.highlight ? `0 0 40px ${hexA(colors.primary, 0.7)}` : undefined}} />
								<div style={{fontFamily: `${fonts.body}, sans-serif`, fontWeight: 700, fontSize: 32 * u, color: colors.light, marginTop: 12 * u, textAlign: 'center'}}>{b.label}</div>
							</div>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Antes / Después: etiquetas y divisor que barre. props: left, right, splitAt (0-1) */
export const SplitCompare: React.FC<GProps & {left?: string; right?: string; vertical?: boolean}> = ({dur, left = 'ANTES', right = 'DESPUÉS', vertical = true}) => {
	const frame = useCurrentFrame();
	const u = useUnit();
	const {colors, fonts} = useBrand();
	const p = interpolate(frame, [0, 14], [0, 1], {...clamp, easing: EASE.out});
	const o = inOut(frame, dur, 1, 8);
	const tag = (t: string, c: string, pos: React.CSSProperties) => (
		<div style={{position: 'absolute', ...pos, background: c, color: colors.light, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 52 * u, padding: `${8 * u}px ${24 * u}px`, borderRadius: 14 * u, transform: `scale(${p})`}}>{t}</div>
	);
	return (
		<AbsoluteFill style={{opacity: o}}>
			<div style={{position: 'absolute', background: colors.light, boxShadow: `0 0 30px ${colors.primary}`, ...(vertical ? {top: '50%', left: 0, height: 8 * u, width: `${p * 100}%`, transform: 'translateY(-50%)'} : {left: '50%', top: 0, width: 8 * u, height: `${p * 100}%`})}} />
			{tag(left, '#555', vertical ? {top: '4%', left: '5%'} : {top: '5%', left: '5%'})}
			{tag(right, colors.primary, vertical ? {top: '54%', left: '5%'} : {top: '5%', right: '5%'})}
		</AbsoluteFill>
	);
};
