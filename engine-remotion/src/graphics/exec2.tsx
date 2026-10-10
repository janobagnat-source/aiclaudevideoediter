// Segunda tanda de gráficos ejecutivos (un set propio por ad, para no repetir interfaces).
import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';

type G = {dur: number};
const GOLD = '#FFBB00';
const RED = '#FF4D5E';
const GREEN = '#00E051';
const src = (s?: string | null) => (!s ? undefined : s.startsWith('http') ? s : staticFile(s));
const useU = () => useVideoConfig().width / 1080;
const fmt = (n: number, dec = 0) => n.toLocaleString('es-AR', {minimumFractionDigits: dec, maximumFractionDigits: dec});
const useIO = (dur: number, inF = 12, outF = 10) => {
	const f = useCurrentFrame();
	const i = interpolate(f, [0, inF], [0, 1], {...clamp, easing: EASE.out});
	const o = interpolate(f, [dur - outF, dur], [1, 0], {...clamp, easing: EASE.in});
	return {f, i, o, v: Math.min(i, o)};
};
const glass = (u: number, a = 0.72): React.CSSProperties => ({
	background: `linear-gradient(180deg, rgba(10,22,70,${a}) 0%, rgba(4,10,40,${a + 0.08}) 100%)`,
	border: `${1.5 * u}px solid rgba(255,255,255,.12)`,
	boxShadow: `0 ${30 * u}px ${80 * u}px rgba(0,0,0,.45), inset 0 ${1 * u}px 0 rgba(255,255,255,.08)`,
	backdropFilter: `blur(${18 * u}px)`,
});

// ============================ AD02 ============================
/** Generador de IA: se tipea el prompt, sale un texto genérico con brillo, y cae un sello. */
export const PromptBox: React.FC<G & {prompt: string; output: string; stamp?: string; stampAt?: number; y?: number; cps?: number; label?: string}> = ({dur, prompt, output, stamp, stampAt = 120, y = 0.57, cps = 32, label = 'ASISTENTE IA'}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.9;
	const pN = Math.floor(interpolate(f, [6, 6 + (prompt.length / cps) * fps], [0, prompt.length], clamp));
	const t0 = 10 + (prompt.length / cps) * fps;
	const oN = Math.floor(interpolate(f, [t0, t0 + (output.length / (cps * 2.2)) * fps], [0, output.length], clamp));
	const sp = spring({frame: f - stampAt, fps, config: {stiffness: 260, damping: 13}});
	const blink = Math.floor(f / 8) % 2 === 0;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 34 * u, ...glass(u, 0.8), padding: 34 * u, boxSizing: 'border-box', opacity: v, transform: `translateY(${(1 - v) * 60 * u}px)`}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 14 * u, marginBottom: 22 * u}}>
					<div style={{width: 40 * u, height: 40 * u, borderRadius: 12 * u, background: 'conic-gradient(from 0deg, #7aa2ff, #b18cff, #57e3ff, #7aa2ff)', transform: `rotate(${f * 3}deg)`}} />
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 5 * u, color: 'rgba(255,255,255,.7)'}}>{label}</span>
				</div>
				<div style={{borderRadius: 18 * u, background: 'rgba(255,255,255,.06)', padding: `${18 * u}px ${22 * u}px`, fontFamily: fonts.body, fontSize: 30 * u, color: '#fff', minHeight: 40 * u}}>
					{prompt.slice(0, pN)}
					{oN === 0 && blink && <span style={{color: GOLD}}>|</span>}
				</div>
				<div style={{marginTop: 22 * u, fontFamily: fonts.body, fontSize: 31 * u, lineHeight: 1.35, color: 'rgba(225,232,255,.9)', minHeight: 170 * u, position: 'relative'}}>
					{output.slice(0, oN)}
					{oN > 0 && oN < output.length && blink && <span style={{color: GOLD}}>▍</span>}
				</div>
				{stamp && f >= stampAt && (
					<div style={{position: 'absolute', right: 40 * u, bottom: 60 * u, transform: `rotate(-10deg) scale(${2.2 - sp * 1.2})`, opacity: Math.min(1, sp * 1.4), border: `${6 * u}px solid ${GOLD}`, color: GOLD, borderRadius: 14 * u, padding: `${8 * u}px ${24 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 50 * u, letterSpacing: 3 * u, background: 'rgba(2,6,23,.6)'}}>{stamp}</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/** Fila de chips editoriales que entran uno a uno (franja baja). */
export const TagRow: React.FC<G & {tags: {text: string; at: number}[]; y?: number; strikeAt?: number}> = ({dur, tags, y = 0.82, strikeAt}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const strike = strikeAt != null ? interpolate(f, [strikeAt, strikeAt + 10], [0, 1], {...clamp, easing: EASE.out}) : 0;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height, transform: 'translateY(-50%)', display: 'flex', justifyContent: 'center', gap: 18 * u, flexWrap: 'wrap', padding: `0 ${40 * u}px`}}>
				{tags.map((t, i) => {
					const p = spring({frame: f - t.at, fps: 30, config: {stiffness: 240, damping: 18}});
					return (
						<div key={i} style={{position: 'relative', ...glass(u, 0.75), borderRadius: 999, padding: `${16 * u}px ${32 * u}px`, fontFamily: fonts.heading, fontWeight: 800, fontSize: 34 * u, letterSpacing: 3 * u, color: '#fff', opacity: p, transform: `translateY(${(1 - p) * 30 * u}px) scale(${0.9 + 0.1 * p})`}}>
							{t.text}
							<div style={{position: 'absolute', left: '8%', top: '50%', height: 4 * u, width: `${84 * strike}%`, background: GOLD, boxShadow: `0 0 ${10 * u}px ${GOLD}`}} />
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Lista editorial numerada 01/02/03 (grande, sin íconos) para el panel inferior del split. */
export const NumberedList: React.FC<G & {items: {text: string; at: number}[]; y?: number; title?: string}> = ({dur, items, y = 0.58, title}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: width * 0.08, right: width * 0.06, top: y * height}}>
				{title && <div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 28 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 20 * u, opacity: interpolate(f, [0, 10], [0, 1], clamp)}}>{title}</div>}
				{items.map((it, i) => {
					const p = interpolate(f, [it.at, it.at + 12], [0, 1], {...clamp, easing: EASE.out});
					const active = i === items.filter((x) => f >= x.at).length - 1;
					return (
						<div key={i} style={{display: 'flex', alignItems: 'baseline', gap: 26 * u, padding: `${18 * u}px 0`, borderTop: `${2 * u}px solid rgba(255,255,255,${0.12 * p})`, opacity: 0.25 + 0.75 * p}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 76 * u, color: active ? GOLD : 'rgba(255,255,255,.35)', fontVariantNumeric: 'tabular-nums', width: 120 * u}}>{String(i + 1).padStart(2, '0')}</span>
							<div style={{overflow: 'hidden'}}>
								<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 52 * u, color: '#fff', lineHeight: 1.05, transform: `translateY(${(1 - p) * 100}%)`}}>{it.text}</div>
							</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Nota de voz de un cliente (WhatsApp-like premium): onda que se dibuja y avanza. */
export const VoiceNote: React.FC<G & {name?: string; avatar?: string; secs?: number; y?: number; caption?: string}> = ({dur, name = 'Cliente', avatar, secs = 47, y = 0.79, caption}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const bars = 38;
	const prog = interpolate(f, [8, dur - 6], [0, 1], clamp);
	const el = Math.round(prog * secs);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 999, ...glass(u, 0.8), padding: `${20 * u}px ${30 * u}px`, display: 'flex', alignItems: 'center', gap: 22 * u, opacity: v, transform: `translateY(${(1 - v) * 50 * u}px)`, boxSizing: 'border-box'}}>
				<div style={{width: 84 * u, height: 84 * u, borderRadius: '50%', overflow: 'hidden', flexShrink: 0, background: `linear-gradient(135deg, #3474FF, #0034B7)`, border: `${3 * u}px solid ${GOLD}`}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
				<div style={{width: 0, height: 0, borderTop: `${18 * u}px solid transparent`, borderBottom: `${18 * u}px solid transparent`, borderLeft: `${28 * u}px solid #fff`, flexShrink: 0}} />
				<div style={{flex: 1, display: 'flex', alignItems: 'center', gap: 5 * u, height: 70 * u}}>
					{Array.from({length: bars}).map((_, i) => {
						const h = 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7) * random(`b${i}`));
						const played = i / bars < prog;
						const live = played && i / bars > prog - 0.06 ? 1 + 0.3 * Math.sin(f / 2 + i) : 1;
						return <div key={i} style={{flex: 1, height: `${h * 100 * live}%`, borderRadius: 4 * u, background: played ? GOLD : 'rgba(255,255,255,.35)'}} />;
					})}
				</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, color: 'rgba(255,255,255,.75)', fontVariantNumeric: 'tabular-nums', flexShrink: 0}}>0:{String(el).padStart(2, '0')}</div>
			</div>
			<div style={{position: 'absolute', left: (width - W) / 2 + 40 * u, top: y * height - 44 * u, fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 5 * u, color: GOLD, opacity: v}}>{caption ?? `${name.toUpperCase()} · NOTA DE VOZ`}</div>
		</AbsoluteFill>
	);
};

/** Preguntas que se apilan y la activa se ilumina (1/3, 2/3, 3/3). */
export const QuestionStack: React.FC<G & {items: {text: string; at: number}[]; y?: number}> = ({dur, items, y = 0.78}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const cur = Math.max(0, items.filter((x) => f >= x.at).length - 1);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: width * 0.07, right: width * 0.07, top: y * height, display: 'flex', flexDirection: 'column', gap: 14 * u}}>
				{items.map((it, i) => {
					const p = spring({frame: f - it.at, fps, config: {stiffness: 230, damping: 19}});
					const act = i === cur;
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 22 * u, borderRadius: 22 * u, padding: `${16 * u}px ${26 * u}px`, ...glass(u, act ? 0.85 : 0.5), borderColor: act ? GOLD : 'rgba(255,255,255,.1)', opacity: f >= it.at ? (act ? 1 : 0.55) : 0, transform: `translateX(${(1 - p) * -60 * u}px) scale(${act ? 1 : 0.96})`, transformOrigin: 'left center'}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: act ? '#020617' : 'rgba(255,255,255,.7)', background: act ? GOLD : 'rgba(255,255,255,.12)', borderRadius: 12 * u, padding: `${6 * u}px ${14 * u}px`}}>{i + 1}/{items.length}</span>
							<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 42 * u, color: '#fff'}}>{it.text}</span>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Mini caso de éxito: PROBLEMA → SOLUCIÓN con flecha que se dibuja. */
export const CaseCard: React.FC<G & {before: string; after: string; label?: string; y?: number; arrowAt?: number}> = ({dur, before, after, label = 'CASO REAL', y = 0.6, arrowAt = 18}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const a = interpolate(f, [arrowAt, arrowAt + 12], [0, 1], {...clamp, easing: EASE.inOut});
	const b = interpolate(f, [arrowAt + 8, arrowAt + 20], [0, 1], {...clamp, easing: EASE.out});
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, opacity: v, transform: `translateY(${(1 - v) * 50 * u}px)`}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 18 * u}}>{label}</div>
				<div style={{display: 'flex', alignItems: 'stretch', gap: 18 * u}}>
					<div style={{flex: 1, borderRadius: 26 * u, ...glass(u, 0.7), padding: 26 * u}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: RED}}>DIFICULTAD</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 36 * u, color: '#fff', marginTop: 10 * u, lineHeight: 1.15}}>{before}</div>
					</div>
					<div style={{width: 70 * u, display: 'flex', alignItems: 'center'}}>
						<div style={{height: 4 * u, width: `${a * 100}%`, background: GOLD, boxShadow: `0 0 ${12 * u}px ${GOLD}`, position: 'relative'}}>
							<div style={{position: 'absolute', right: -6 * u, top: -11 * u, width: 0, height: 0, borderTop: `${13 * u}px solid transparent`, borderBottom: `${13 * u}px solid transparent`, borderLeft: `${18 * u}px solid ${GOLD}`, opacity: a > 0.9 ? 1 : 0}} />
						</div>
					</div>
					<div style={{flex: 1, borderRadius: 26 * u, background: `linear-gradient(160deg, ${hexA(GOLD, 0.22)}, rgba(4,10,40,.85))`, border: `${2 * u}px solid ${GOLD}`, padding: 26 * u, opacity: b, transform: `scale(${0.94 + 0.06 * b})`}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: GREEN}}>CÓMO LO RESOLVISTE</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 36 * u, color: '#fff', marginTop: 10 * u, lineHeight: 1.15}}>{after}</div>
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Medidor que se llena (confianza, claridad…) con porcentaje. */
export const MeterBar: React.FC<G & {label: string; to?: number; y?: number; at?: number; fillDur?: number; color?: string}> = ({dur, label, to = 100, y = 0.82, at = 6, fillDur = 40, color = GOLD}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = interpolate(f, [at, at + fillDur], [0, to / 100], {...clamp, easing: EASE.inOut});
	const W = width * 0.84;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, opacity: v, transform: `translateY(${(1 - v) * 40 * u}px)`}}>
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 14 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, letterSpacing: 7 * u, color: '#fff'}}>{label}</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 56 * u, color, fontVariantNumeric: 'tabular-nums'}}>{Math.round(p * 100)}%</span>
				</div>
				<div style={{height: 26 * u, borderRadius: 999, background: 'rgba(255,255,255,.1)', overflow: 'hidden', border: `${1.5 * u}px solid rgba(255,255,255,.15)`}}>
					<div style={{height: '100%', width: `${p * 100}%`, borderRadius: 999, background: `linear-gradient(90deg, ${hexA(color, 0.6)}, ${color})`, boxShadow: `0 0 ${24 * u}px ${hexA(color, 0.7)}`}} />
				</div>
			</div>
		</AbsoluteFill>
	);
};
