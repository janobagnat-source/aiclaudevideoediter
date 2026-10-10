// AD09 (prometer lo que no puedes sostener) — interfaces propias de este ad.
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

/** Carrito de compra: sumás promesas… y el total es UN PROBLEMA. */
export const ShoppingCart: React.FC<G & {items: {text: string; at: number}[]; totalAt?: number; y?: number}> = ({dur, items, totalAt = 110, y = 0.57}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const tp = spring({frame: f - totalAt, fps, config: {stiffness: 230, damping: 14}});
	const count = items.filter((i) => f >= i.at).length;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 28 * u, background: '#f6f7fb', padding: `${22 * u}px ${28 * u}px`, boxShadow: `0 ${30 * u}px ${70 * u}px rgba(0,0,0,.5)`}}>
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 32 * u, color: '#0a1440'}}>🛒 Tu carrito</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, color: '#fff', background: '#0b3bd6', borderRadius: 999, padding: `${4 * u}px ${16 * u}px`}}>{count}</span>
				</div>
				{items.map((it, i) => {
					const p = spring({frame: f - it.at, fps, config: {stiffness: 240, damping: 18}});
					return (
						<div key={i} style={{display: 'flex', justifyContent: 'space-between', padding: `${12 * u}px 0`, borderTop: '1px solid rgba(10,20,64,.08)', opacity: f >= it.at ? p : 0, transform: `translateX(${(1 - p) * 50 * u}px)`}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 30 * u, color: '#0a1440'}}>{it.text}</span>
							<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 26 * u, color: '#0b8a3a'}}>“GRATIS”</span>
						</div>
					);
				})}
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 * u, paddingTop: 14 * u, borderTop: `${3 * u}px solid #0a1440`, opacity: f >= totalAt ? 1 : 0}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 32 * u, color: '#0a1440'}}>TOTAL</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 48 * u, color: '#c21f3a', transform: `scale(${tp})`}}>1 PROBLEMA</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Pedidos del cliente que entran como notificaciones apiladas. */
export const RequestToasts: React.FC<G & {items: {text: string; at: number}[]; y?: number}> = ({dur, items, y = 0.7}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{items.map((it, i) => {
				const p = spring({frame: f - it.at, fps, config: {stiffness: 220, damping: 18}});
				const n = items.filter((x) => f >= x.at).length;
				const depth = n - 1 - i;
				return (
					<div key={i} style={{position: 'absolute', left: (width - W) / 2, top: y * height + depth * -24 * u, width: W, borderRadius: 26 * u, ...glass(u, 0.88), padding: `${18 * u}px ${24 * u}px`, opacity: f >= it.at ? p * (1 - depth * 0.25) : 0, transform: `translateY(${(1 - p) * -60 * u}px) scale(${1 - depth * 0.05})`, zIndex: i}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, letterSpacing: 4 * u, color: GOLD}}>CLIENTE · AHORA</div>
						<div style={{fontFamily: fonts.body, fontWeight: 600, fontSize: 32 * u, color: '#fff', marginTop: 4 * u}}>{it.text}</div>
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Sellos “SÍ ✓” que se estampan junto a cada compromiso (sobre el b-roll de la torre). */
export const YesStamps: React.FC<G & {items: {text: string; at: number}[]; y?: number}> = ({dur, items, y = 0.62}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: width * 0.06, top: y * height, display: 'flex', flexDirection: 'column', gap: 16 * u}}>
				{items.map((it, i) => {
					const p = spring({frame: f - it.at, fps, config: {stiffness: 300, damping: 12}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 16 * u, opacity: f >= it.at ? 1 : 0}}>
							<div style={{border: `${5 * u}px solid ${GOLD}`, color: GOLD, borderRadius: 12 * u, padding: `${4 * u}px ${14 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, transform: `scale(${2 - p}) rotate(-8deg)`, background: 'rgba(2,6,23,.6)'}}>SÍ</div>
							<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 34 * u, color: '#fff', textShadow: '0 4px 16px rgba(0,0,0,.7)', opacity: p}}>{it.text}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Monitor de energía (electrocardiograma) que se aplana; etiquetas al nombrar cada efecto. */
export const EnergyEKG: React.FC<G & {labels: {text: string; at: number}[]; y?: number}> = ({dur, labels, y = 0.74}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.9;
	const H = 150 * u;
	const amp = interpolate(f, [0, dur], [1, 0.08], clamp);
	const head = (f * 9 * u) % W;
	const pts: string[] = [];
	for (let x = 0; x <= W; x += 6 * u) {
		const ph = ((x - head) / (120 * u)) % 1;
		const k = ((ph % 1) + 1) % 1;
		const spike = k > 0.42 && k < 0.5 ? -1 : k >= 0.5 && k < 0.56 ? 0.6 : 0;
		pts.push(`${x},${H / 2 + spike * H * 0.42 * amp}`);
	}
	const cur = labels.filter((l) => f >= l.at);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 24 * u, ...glass(u, 0.85), padding: `${14 * u}px 0`}}>
				<div style={{display: 'flex', justifyContent: 'space-between', padding: `0 ${24 * u}px`}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 5 * u, color: 'rgba(255,255,255,.65)'}}>TU ENERGÍA</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 26 * u, color: amp < 0.4 ? RED : GREEN, fontVariantNumeric: 'tabular-nums'}}>{Math.round(amp * 100)}%</span>
				</div>
				<svg width={W} height={H}>
					<polyline points={pts.join(' ')} fill="none" stroke={amp < 0.4 ? RED : GREEN} strokeWidth={4 * u} style={{filter: `drop-shadow(0 0 ${6 * u}px ${amp < 0.4 ? RED : GREEN})`}} />
				</svg>
				<div style={{display: 'flex', gap: 12 * u, padding: `0 ${24 * u}px`, flexWrap: 'wrap'}}>
					{cur.map((l, i) => (
						<span key={i} style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 2 * u, color: '#fff', background: hexA(RED, 0.25), border: `${1.5 * u}px solid ${RED}`, borderRadius: 999, padding: `${4 * u}px ${14 * u}px`}}>{l.text}</span>
					))}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Pregunta en tipografía serif elegante dentro de un marco dorado que se dibuja. */
export const SpotlightQuestion: React.FC<G & {kicker?: string; question: string; y?: number}> = ({dur, kicker = 'PREGÚNTATE', question, y = 0.6}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const H = height * 0.3;
	const d = interpolate(f, [0, 24], [0, 1], {...clamp, easing: EASE.inOut});
	const t = interpolate(f, [14, 30], [0, 1], {...clamp, easing: EASE.out});
	const per = 2 * (W + H);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				<rect x={(width - W) / 2} y={y * height} width={W} height={H} rx={6 * u} fill="none" stroke={GOLD} strokeWidth={3 * u} strokeDasharray={per} strokeDashoffset={per * (1 - d)} />
			</svg>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, height: H, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: `0 ${50 * u}px`, boxSizing: 'border-box', textAlign: 'center'}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 10 * u, color: GOLD, opacity: t, marginBottom: 18 * u}}>{kicker}</div>
				<div style={{fontFamily: 'Playfair Display', fontWeight: 700, fontStyle: 'italic', fontSize: 64 * u, color: '#fff', lineHeight: 1.15, opacity: t, transform: `translateY(${(1 - t) * 20 * u}px)`}}>{question}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Cláusulas que se tildan una a una (arriba, sobre el b-roll de la firma). */
export const ClauseTicks: React.FC<G & {items: {text: string; at: number}[]; y?: number; title?: string}> = ({dur, items, y = 0.06, title = 'POR ESCRITO'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: width * 0.08, right: width * 0.08, top: y * height}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 10 * u, color: GOLD, marginBottom: 14 * u}}>{title}</div>
				{items.map((it, i) => {
					const p = interpolate(f, [it.at, it.at + 10], [0, 1], {...clamp, easing: EASE.out});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 18 * u, marginBottom: 12 * u, opacity: 0.3 + 0.7 * p}}>
							<svg width={44 * u} height={44 * u} viewBox="0 0 24 24">
								<rect x={1} y={1} width={22} height={22} rx={5} fill="none" stroke="rgba(255,255,255,.7)" strokeWidth={2} />
								<path d="M6 12.5l4 4 8-9" fill="none" stroke={GOLD} strokeWidth={3} strokeLinecap="round" strokeDasharray={20} strokeDashoffset={20 * (1 - p)} />
							</svg>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 44 * u, color: '#fff', textShadow: '0 4px 16px rgba(0,0,0,.7)'}}>{it.text}</span>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Planilla de horas: trabajo hecho que nadie paga (FACTURADO $0, sello IMPAGO). */
export const TimesheetUnpaid: React.FC<G & {rows: [string, string][]; y?: number; stampAt?: number}> = ({dur, rows, y = 0.7, stampAt = 40}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const sp = spring({frame: f - stampAt, fps, config: {stiffness: 280, damping: 12}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 24 * u, background: '#f6f7fb', padding: `${18 * u}px ${26 * u}px`, boxShadow: `0 ${24 * u}px ${60 * u}px rgba(0,0,0,.45)`}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 20 * u, letterSpacing: 5 * u, color: '#5a6690', marginBottom: 6 * u}}>HORAS TRABAJADAS</div>
				{rows.map(([k, h], i) => (
					<div key={i} style={{display: 'flex', justifyContent: 'space-between', padding: `${8 * u}px 0`, borderTop: '1px solid rgba(10,20,64,.08)', opacity: interpolate(f, [4 + i * 6, 10 + i * 6], [0, 1], clamp)}}>
						<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 28 * u, color: '#0a1440'}}>{k}</span>
						<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, color: '#0a1440', fontVariantNumeric: 'tabular-nums'}}>{h}</span>
					</div>
				))}
				<div style={{display: 'flex', justifyContent: 'space-between', paddingTop: 10 * u, borderTop: `${3 * u}px solid #0a1440`, marginTop: 4 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: '#0a1440'}}>FACTURADO</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 40 * u, color: '#c21f3a'}}>$ 0</span>
				</div>
				{f >= stampAt && <div style={{position: 'absolute', right: 30 * u, top: 30 * u, transform: `rotate(-12deg) scale(${2 - sp})`, opacity: Math.min(1, sp * 1.4), border: `${6 * u}px solid #c21f3a`, color: '#c21f3a', borderRadius: 12 * u, padding: `${6 * u}px ${18 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 44 * u, letterSpacing: 3 * u, mixBlendMode: 'multiply'}}>IMPAGO</div>}
			</div>
		</AbsoluteFill>
	);
};
