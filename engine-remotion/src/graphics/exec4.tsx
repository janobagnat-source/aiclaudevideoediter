// AD04 (“está caro”) — interfaces propias de este ad.
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';

type G = {dur: number};
const GOLD = '#FFBB00';
const RED = '#FF4D5E';
const GREEN = '#00E051';
const useU = () => useVideoConfig().width / 1080;
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

/** Respuesta del cliente que llega (“…está caro”) y debajo aparece la voz interna de duda. */
export const ObjectionCard: React.FC<G & {msg: string; hot?: string; hotAt?: number; inner?: string; innerAt?: number; y?: number}> = ({dur, msg, hot = 'está caro', hotAt = 40, inner, innerAt = 100, y = 0.58}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const typing = f < 22;
	const sp = spring({frame: f - 22, fps, config: {stiffness: 200, damping: 17}});
	const hp = interpolate(f, [hotAt, hotAt + 10], [0, 1], {...clamp, easing: EASE.out});
	const ip = interpolate(f, [innerAt, innerAt + 18], [0, 1], {...clamp, easing: EASE.out});
	const i0 = msg.indexOf(hot);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 6 * u, color: 'rgba(255,255,255,.55)', marginBottom: 12 * u}}>RESPUESTA A TU PROPUESTA</div>
				{typing ? (
					<div style={{display: 'inline-flex', gap: 10 * u, borderRadius: 30 * u, background: '#eef1fb', padding: `${22 * u}px ${28 * u}px`}}>
						{[0, 1, 2].map((i) => <div key={i} style={{width: 16 * u, height: 16 * u, borderRadius: '50%', background: '#8a93b0', opacity: 0.4 + 0.6 * Math.abs(Math.sin((f + i * 5) / 5))}} />)}
					</div>
				) : (
					<div style={{display: 'inline-block', maxWidth: W * 0.92, borderRadius: `${30 * u}px ${30 * u}px ${30 * u}px ${8 * u}px`, background: '#eef1fb', padding: `${24 * u}px ${30 * u}px`, transform: `scale(${0.9 + 0.1 * sp})`, transformOrigin: 'left bottom', opacity: sp, boxShadow: `0 ${20 * u}px ${50 * u}px rgba(0,0,0,.4)`}}>
						<div style={{fontFamily: fonts.body, fontWeight: 600, fontSize: 38 * u, color: '#0a1440', lineHeight: 1.3}}>
							{i0 >= 0 ? msg.slice(0, i0) : msg}
							{i0 >= 0 && (
								<span style={{position: 'relative', fontWeight: 800, color: hp > 0.5 ? '#c21f3a' : '#0a1440'}}>
									{hot}
									<span style={{position: 'absolute', left: 0, right: 0, bottom: -4 * u, height: 6 * u, background: RED, transform: `scaleX(${hp})`, transformOrigin: 'left', borderRadius: 3 * u}} />
								</span>
							)}
							{i0 >= 0 ? msg.slice(i0 + hot.length) : ''}
						</div>
					</div>
				)}
				{inner && (
					<div style={{marginTop: 34 * u, opacity: ip, transform: `translateY(${(1 - ip) * 24 * u}px)`, filter: `blur(${(1 - ip) * 6}px)`}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 600, fontStyle: 'italic', fontSize: 46 * u, color: 'rgba(200,212,255,.85)', lineHeight: 1.2}}>“{inner}”</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 22 * u, letterSpacing: 6 * u, color: 'rgba(255,255,255,.4)', marginTop: 10 * u}}>— LO QUE PENSÁS</div>
					</div>
				)}
			</div>
		</AbsoluteFill>
	);
};

/** Barra que se vacía (p.ej. TU SEGURIDAD 100% → 30%). */
export const ValueDrain: React.FC<G & {label: string; from?: number; to?: number; y?: number}> = ({dur, label, from = 100, to = 28, y = 0.82}) => {
	const {f, v} = useIO(dur, 8, 8);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = interpolate(f, [4, dur - 6], [from, to], {...clamp, easing: EASE.inOut});
	const W = width * 0.8;
	const col = p < 45 ? RED : GOLD;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, opacity: v}}>
				<div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 12 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, letterSpacing: 7 * u, color: '#fff'}}>{label}</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 44 * u, color: col, fontVariantNumeric: 'tabular-nums'}}>{Math.round(p)}%</span>
				</div>
				<div style={{height: 22 * u, borderRadius: 999, background: 'rgba(255,255,255,.1)', overflow: 'hidden'}}>
					<div style={{height: '100%', width: `${p}%`, background: col, borderRadius: 999, boxShadow: `0 0 ${20 * u}px ${hexA(col, 0.7)}`}} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Precio que se tacha y aparece el descuento con signo de pregunta (sobre el b-roll de la etiqueta). */
export const PriceSlash: React.FC<G & {from: string; to: string; y?: number; slashAt?: number}> = ({dur, from, to, y = 0.8, slashAt = 14}) => {
	const {f, v} = useIO(dur, 8, 8);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const s = interpolate(f, [slashAt, slashAt + 8], [0, 1], {...clamp, easing: EASE.out});
	const n = spring({frame: f - slashAt - 6, fps, config: {stiffness: 230, damping: 13}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 40 * u, transform: 'translateY(-50%)'}}>
				<div style={{position: 'relative', fontFamily: fonts.heading, fontWeight: 900, fontSize: 96 * u, color: 'rgba(255,255,255,.75)'}}>
					{from}
					<div style={{position: 'absolute', left: -6 * u, right: -6 * u, top: '52%', height: 9 * u, background: RED, transform: `scaleX(${s}) rotate(-8deg)`, transformOrigin: 'left', borderRadius: 4 * u}} />
				</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 110 * u, color: GOLD, transform: `scale(${n})`, textShadow: `0 0 ${30 * u}px ${hexA(GOLD, 0.5)}`}}>{to}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Guía de respiración: línea que sube (inhala) y baja (exhala) con el texto que cambia. */
export const BreathLine: React.FC<G & {y?: number; period?: number}> = ({dur, y = 0.8, period = 2.6}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const t = f / fps;
	const ph = (t % period) / period;
	const inhale = ph < 0.5;
	const amp = Math.sin(ph * Math.PI * 2 - Math.PI / 2) * 0.5 + 0.5;
	const W = width * 0.84;
	const pts = Array.from({length: 60}, (_, i) => {
		const x = (i / 59) * W;
		const yy = 60 * u - Math.sin((i / 59) * Math.PI) * amp * 54 * u;
		return `${x},${yy}`;
	}).join(' ');
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<svg width={W} height={80 * u}>
					<polyline points={pts} fill="none" stroke={GOLD} strokeWidth={5 * u} strokeLinecap="round" style={{filter: `drop-shadow(0 0 ${8 * u}px ${GOLD})`}} />
				</svg>
				<div style={{display: 'flex', justifyContent: 'center', gap: 30 * u, marginTop: 10 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 34 * u, letterSpacing: 10 * u}}>
					<span style={{color: inhale ? '#fff' : 'rgba(255,255,255,.3)'}}>INHALA</span>
					<span style={{color: 'rgba(255,255,255,.3)'}}>·</span>
					<span style={{color: !inhale ? '#fff' : 'rgba(255,255,255,.3)'}}>EXHALA</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Diagnóstico: tres causas posibles; una aguja recorre y cada opción se ilumina cuando se nombra. */
export const Diagnosis: React.FC<G & {items: {text: string; at: number}[]; y?: number; title?: string}> = ({dur, items, y = 0.6, title = '¿QUÉ LE FALTA?'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const col = W / items.length;
	let pos = 0;
	items.forEach((it, i) => {
		pos += interpolate(f, [it.at - 4, it.at + 6], [0, i === 0 ? 0.5 : 1], {...clamp, easing: EASE.inOut});
	});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 20 * u, textAlign: 'center'}}>{title}</div>
				<div style={{position: 'relative', display: 'flex', borderRadius: 26 * u, ...glass(u, 0.75), overflow: 'hidden'}}>
					{items.map((it, i) => {
						const on = f >= it.at;
						return (
							<div key={i} style={{width: col, padding: `${44 * u}px 0`, textAlign: 'center', borderLeft: i ? `${1.5 * u}px solid rgba(255,255,255,.1)` : undefined, background: on ? `linear-gradient(180deg, ${hexA(GOLD, 0.22)}, transparent)` : undefined}}>
								<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, color: on ? '#fff' : 'rgba(255,255,255,.35)', letterSpacing: 1 * u}}>{it.text}</div>
							</div>
						);
					})}
					<div style={{position: 'absolute', bottom: 0, left: pos * col - col * 0.5 + col * 0.5, width: col, height: 6 * u, background: GOLD, boxShadow: `0 0 ${18 * u}px ${GOLD}`, opacity: f >= items[0].at - 4 ? 1 : 0}} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Tu mensaje enviado (burbuja dorada a la derecha) con doble check “leído”. */
export const AskBubble: React.FC<G & {text: string; y?: number; label?: string}> = ({dur, text, y = 0.8, label = 'TU RESPUESTA'}) => {
	const {f, v} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const sp = spring({frame: f - 4, fps, config: {stiffness: 200, damping: 17}});
	const read = f > 24;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', right: width * 0.07, top: y * height, display: 'flex', flexDirection: 'column', alignItems: 'flex-end', maxWidth: width * 0.82}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 22 * u, letterSpacing: 6 * u, color: 'rgba(255,255,255,.5)', marginBottom: 10 * u}}>{label}</div>
				<div style={{borderRadius: `${30 * u}px ${30 * u}px ${8 * u}px ${30 * u}px`, background: `linear-gradient(135deg, ${GOLD}, #f0a400)`, padding: `${24 * u}px ${30 * u}px`, transform: `scale(${0.9 + 0.1 * sp})`, transformOrigin: 'right bottom', opacity: sp, boxShadow: `0 ${18 * u}px ${44 * u}px rgba(0,0,0,.4)`}}>
					<div style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 38 * u, color: '#020617', lineHeight: 1.25}}>{text}</div>
					<div style={{textAlign: 'right', fontFamily: fonts.body, fontSize: 22 * u, color: read ? '#0b3bd6' : 'rgba(2,6,23,.5)', marginTop: 4 * u}}>{read ? 'Leído ✓✓' : '✓'}</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Pila de valor: bloques (tiempo, preparación, trabajo) que se apilan y sostienen el precio. */
export const ValueStack: React.FC<G & {items: {text: string; at: number; h?: number}[]; price?: string; priceAt?: number; y?: number}> = ({dur, items, price = '$ 1.500', priceAt = 110, y = 0.58}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.7;
	const baseY = y * height + height * 0.36;
	let acc = 0;
	const pr = spring({frame: f - priceAt, fps, config: {stiffness: 220, damping: 14}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{items.map((it, i) => {
				const hh = (it.h ?? 110) * u;
				const p = spring({frame: f - it.at, fps, config: {stiffness: 170, damping: 15}});
				const top = baseY - acc - hh;
				acc += hh + 10 * u;
				return (
					<div key={i} style={{position: 'absolute', left: (width - W) / 2, top: top - (1 - p) * 400 * u, width: W, height: hh, borderRadius: 18 * u, background: i % 2 ? 'linear-gradient(180deg,#1d4fd8,#0b2a9c)' : 'linear-gradient(180deg,#3474FF,#1d4fd8)', border: `${1.5 * u}px solid rgba(255,255,255,.2)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 46 * u, letterSpacing: 4 * u, color: '#fff', opacity: f >= it.at ? 1 : 0, boxShadow: `0 ${14 * u}px ${30 * u}px rgba(0,0,0,.35)`}}>
						{it.text}
					</div>
				);
			})}
			<div style={{position: 'absolute', left: '50%', top: baseY - acc - 120 * u, transform: `translate(-50%, 0) scale(${pr})`, background: GOLD, color: '#020617', borderRadius: 18 * u, padding: `${14 * u}px ${44 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 64 * u, boxShadow: `0 0 ${40 * u}px ${hexA(GOLD, 0.5)}`}}>{price}</div>
		</AbsoluteFill>
	);
};

/** Tabla comparativa compacta: TU PROPUESTA vs LA OTRA OFERTA (franja baja). */
export const CompareTable: React.FC<G & {rows: {label: string; a: boolean; b: boolean}[]; y?: number; delay?: number}> = ({dur, rows, y = 0.73, delay = 8}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const mark = (ok: boolean) => <span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 36 * u, color: ok ? GREEN : RED}}>{ok ? '✓' : '✗'}</span>;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 26 * u, ...glass(u, 0.8), padding: `${18 * u}px ${26 * u}px`, opacity: v, transform: `translateY(${(1 - v) * 40 * u}px)`}}>
				<div style={{display: 'flex', fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: 'rgba(255,255,255,.6)', paddingBottom: 10 * u, borderBottom: '1px solid rgba(255,255,255,.12)'}}>
					<span style={{flex: 1.6}}>¿QUÉ ESTÁ COMPARANDO?</span>
					<span style={{flex: 1, textAlign: 'center', color: GOLD}}>TU PROPUESTA</span>
					<span style={{flex: 1, textAlign: 'center'}}>LA OTRA</span>
				</div>
				{rows.map((r, i) => {
					const p = interpolate(f, [delay + i * 10, delay + i * 10 + 8], [0, 1], clamp);
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', padding: `${12 * u}px 0`, opacity: p, borderBottom: i < rows.length - 1 ? '1px dashed rgba(255,255,255,.08)' : undefined}}>
							<span style={{flex: 1.6, fontFamily: fonts.heading, fontWeight: 700, fontSize: 30 * u, color: '#fff'}}>{r.label}</span>
							<span style={{flex: 1, textAlign: 'center'}}>{mark(r.a)}</span>
							<span style={{flex: 1, textAlign: 'center'}}>{mark(r.b)}</span>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
