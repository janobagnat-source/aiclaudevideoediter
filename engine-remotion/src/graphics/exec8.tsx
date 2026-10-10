// AD08 (diez minutos para explicar lo que vendes) — interfaces propias de este ad.
import React from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
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

/** Presentación interminable: diapositivas que pasan, reloj a 10:00 y la atención del cliente que cae. */
export const SlideMarathon: React.FC<G & {total?: number; y?: number; endAt?: number}> = ({dur, total = 48, y = 0.565, endAt = 150}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.9;
	const p = interpolate(f, [4, endAt], [0, 1], {...clamp, easing: EASE.in});
	const slide = Math.max(1, Math.round(p * total));
	const secs = Math.round(p * 600);
	const att = 100 - p * 88;
	const titles = ['Metodología', 'Marco teórico', 'Herramientas', 'Proceso en 14 fases', 'Matriz de KPIs', 'Anexo técnico', 'Casos de estudio', 'Glosario'];
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{borderRadius: 24 * u, background: '#f4f6fc', height: 300 * u, padding: 26 * u, boxShadow: `0 ${24 * u}px ${60 * u}px rgba(0,0,0,.45)`, position: 'relative', overflow: 'hidden'}}>
					<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 40 * u, color: '#0a1440'}}>{titles[slide % titles.length]}</div>
					{Array.from({length: 5}).map((_, i) => <div key={i} style={{height: 12 * u, width: `${60 + random(`s${slide}${i}`) * 35}%`, borderRadius: 6 * u, background: 'rgba(10,20,64,.15)', marginTop: 18 * u}} />)}
					<div style={{position: 'absolute', right: 24 * u, bottom: 18 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 26 * u, color: '#5a6690', fontVariantNumeric: 'tabular-nums'}}>{slide}/{total}</div>
				</div>
				<div style={{display: 'flex', gap: 18 * u, marginTop: 18 * u}}>
					<div style={{flex: 1, borderRadius: 20 * u, ...glass(u, 0.8), padding: `${16 * u}px ${22 * u}px`}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, letterSpacing: 4 * u, color: 'rgba(255,255,255,.6)'}}>EXPLICANDO</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 60 * u, color: secs >= 590 ? RED : '#fff', fontVariantNumeric: 'tabular-nums'}}>{String(Math.floor(secs / 60)).padStart(2, '0')}:{String(secs % 60).padStart(2, '0')}</div>
					</div>
					<div style={{flex: 1.3, borderRadius: 20 * u, ...glass(u, 0.8), padding: `${16 * u}px ${22 * u}px`}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, letterSpacing: 4 * u, color: 'rgba(255,255,255,.6)'}}>ATENCIÓN DEL CLIENTE</div>
						<div style={{height: 22 * u, borderRadius: 999, background: 'rgba(255,255,255,.1)', marginTop: 16 * u, overflow: 'hidden'}}>
							<div style={{height: '100%', width: `${att}%`, background: att < 40 ? RED : GREEN, borderRadius: 999}} />
						</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, color: att < 40 ? RED : '#fff', marginTop: 8 * u}}>{Math.round(att)}%</div>
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Nube de tecnicismos que invade la pantalla (sobre el b-roll del hilo enredado). */
export const JargonCloud: React.FC<G & {words?: string[]; every?: number}> = ({dur, words = ['MÉTODOS', 'HERRAMIENTAS', 'KPIs', 'FUNNEL', 'CRM', 'OMNICANAL', 'SINERGIA', 'FRAMEWORK', 'DETALLES', 'ROI', 'PIPELINE', 'MÉTRICAS'], every = 4}) => {
	const {f, o} = useIO(dur, 1, 8);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{words.map((w, i) => {
				const p = spring({frame: f - i * every, fps, config: {stiffness: 200, damping: 14}});
				const x = 0.08 + random(`jx${i}`) * 0.7;
				const y = 0.08 + random(`jy${i}`) * 0.75;
				const r = (random(`jr${i}`) - 0.5) * 24;
				const big = i % 3 === 0;
				return (
					<div key={i} style={{position: 'absolute', left: x * width, top: y * height, transform: `scale(${p}) rotate(${r}deg)`, opacity: f >= i * every ? 0.9 : 0, fontFamily: fonts.heading, fontWeight: 900, fontSize: (big ? 70 : 44) * u, color: big ? 'rgba(255,255,255,.85)' : 'rgba(170,190,255,.7)', letterSpacing: 2 * u, textShadow: '0 4px 20px rgba(0,0,0,.6)', whiteSpace: 'nowrap'}}>{w}</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** La realidad del cliente: tres filas con dato concreto (cuesta / afecta / puedes ayudar). */
export const ClientReality: React.FC<G & {rows: {k: string; v: string; at: number; color?: string}[]; y?: number; title?: string}> = ({dur, rows, y = 0.585, title = 'SU REALIDAD'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 16 * u}}>{title}</div>
				{rows.map((r, i) => {
					const p = spring({frame: f - r.at, fps, config: {stiffness: 220, damping: 18}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 20 * u, borderRadius: 22 * u, ...glass(u, 0.78), borderLeft: `${6 * u}px solid ${r.color ?? GOLD}`, padding: `${18 * u}px ${24 * u}px`, marginBottom: 12 * u, opacity: f >= r.at ? p : 0, transform: `translateX(${(1 - p) * 60 * u}px)`}}>
							<div style={{width: 210 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 3 * u, color: r.color ?? GOLD, flexShrink: 0}}>{r.k}</div>
							<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 34 * u, color: '#fff', lineHeight: 1.15}}>{r.v}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Medidor semicircular de comprensión (¿entendió?) — aguja que apenas se mueve. */
export const ClarityGauge: React.FC<G & {to?: number; label?: string; y?: number; jargon?: string}> = ({dur, to = 18, label = '¿CUÁNTO ENTENDIÓ?', y = 0.73, jargon = 'Optimizo tu funnel omnicanal con KPIs de conversión'}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = interpolate(f, [16, 50], [0, to / 100], {...clamp, easing: EASE.out}) + Math.sin(f / 4) * 0.01;
	const R = 150 * u;
	const ang = Math.PI * (1 - p);
	const cx = width / 2;
	const cy = y * height + R + 90 * u;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: width * 0.08, right: width * 0.08, top: y * height, textAlign: 'center', fontFamily: fonts.body, fontWeight: 600, fontStyle: 'italic', fontSize: 30 * u, color: 'rgba(255,255,255,.75)'}}>“{jargon}”</div>
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				<path d={`M ${cx - R} ${cy} A ${R} ${R} 0 0 1 ${cx + R} ${cy}`} fill="none" stroke="rgba(255,255,255,.15)" strokeWidth={26 * u} strokeLinecap="round" />
				<path d={`M ${cx - R} ${cy} A ${R} ${R} 0 0 1 ${cx + R * Math.cos(ang)} ${cy - R * Math.sin(ang)}`} fill="none" stroke={RED} strokeWidth={26 * u} strokeLinecap="round" />
				<line x1={cx} y1={cy} x2={cx + (R - 30 * u) * Math.cos(ang)} y2={cy - (R - 30 * u) * Math.sin(ang)} stroke="#fff" strokeWidth={6 * u} strokeLinecap="round" />
				<circle cx={cx} cy={cy} r={12 * u} fill="#fff" />
			</svg>
			<div style={{position: 'absolute', left: 0, right: 0, top: cy + 24 * u, textAlign: 'center'}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 58 * u, color: RED, fontVariantNumeric: 'tabular-nums'}}>{Math.round(Math.max(0, p) * 100)}%</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 6 * u, color: '#fff'}}>{label}</div>
			</div>
		</AbsoluteFill>
	);
};
