// AD10 (más publicidad no lo resuelve) — interfaces propias de este ad.
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

/** Panel de anuncios: el presupuesto diario sube, el gasto se dispara, las ventas siguen en 0. */
export const AdsDashboard: React.FC<G & {boostAt?: number; y?: number}> = ({dur, boostAt = 100, y = 0.565}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.9;
	const b = interpolate(f, [boostAt, boostAt + 20], [0, 1], {...clamp, easing: EASE.inOut});
	const budget = 20 + 180 * b;
	const spend = 140 + f * (2 + b * 14);
	const pts = Array.from({length: 24}, (_, i) => {
		const t = i / 23;
		const g = Math.pow(t, 1.6) * (0.4 + b * 0.6);
		return `${t * (W - 60 * u)},${130 * u - g * 120 * u}`;
	}).join(' ');
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 26 * u, ...glass(u, 0.85), padding: 26 * u, boxSizing: 'border-box'}}>
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 5 * u, color: 'rgba(255,255,255,.7)'}}>CAMPAÑA · VENTAS</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, color: GREEN}}>● ACTIVA</span>
				</div>
				<div style={{marginTop: 18 * u}}>
					<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, color: '#fff'}}>
						<span>Presupuesto diario</span>
						<span style={{fontWeight: 900, color: GOLD, fontVariantNumeric: 'tabular-nums'}}>US$ {Math.round(budget)}</span>
					</div>
					<div style={{height: 12 * u, borderRadius: 6 * u, background: 'rgba(255,255,255,.12)', marginTop: 10 * u, position: 'relative'}}>
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${10 + 85 * b}%`, background: GOLD, borderRadius: 6 * u}} />
						<div style={{position: 'absolute', left: `${10 + 85 * b}%`, top: '50%', width: 34 * u, height: 34 * u, borderRadius: '50%', background: '#fff', transform: 'translate(-50%,-50%)', boxShadow: `0 0 ${12 * u}px ${GOLD}`}} />
					</div>
				</div>
				<svg width={W - 52 * u} height={140 * u} style={{marginTop: 18 * u}}>
					<polyline points={pts} fill="none" stroke={RED} strokeWidth={4 * u} />
					<line x1={0} y1={128 * u} x2={W - 60 * u} y2={128 * u} stroke={GREEN} strokeWidth={4 * u} strokeDasharray={`${10 * u} ${8 * u}`} />
				</svg>
				<div style={{display: 'flex', gap: 16 * u, marginTop: 10 * u}}>
					{[
						['GASTADO', `US$ ${Math.round(spend).toLocaleString('es-AR')}`, RED],
						['VENTAS', '0', GREEN],
					].map(([k, v, c]) => (
						<div key={k} style={{flex: 1, borderRadius: 18 * u, background: 'rgba(255,255,255,.06)', padding: `${12 * u}px ${18 * u}px`}}>
							<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, letterSpacing: 4 * u, color: 'rgba(255,255,255,.6)'}}>{k}</div>
							<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 48 * u, color: c, fontVariantNumeric: 'tabular-nums'}}>{v}</div>
						</div>
					))}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Facturas vencidas que se apilan y un botón “solución rápida” que tienta. */
export const BillsStack: React.FC<G & {bills?: [string, string][]; quickAt?: number; y?: number}> = ({dur, bills = [['Alquiler', 'US$ 1.200'], ['Proveedores', 'US$ 2.100'], ['Sueldos', 'US$ 3.400']], quickAt = 80, y = 0.7}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.6;
	const q = spring({frame: f - quickAt, fps, config: {stiffness: 230, damping: 14}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{bills.map(([k, v], i) => {
				const p = spring({frame: f - i * 9, fps, config: {stiffness: 200, damping: 16}});
				return (
					<div key={i} style={{position: 'absolute', left: width * 0.06 + i * 22 * u, top: y * height + i * 26 * u, width: W, borderRadius: 18 * u, background: '#f6f7fb', padding: `${16 * u}px ${22 * u}px`, boxShadow: `0 ${16 * u}px ${40 * u}px rgba(0,0,0,.45)`, transform: `translateY(${(1 - p) * 160 * u}px) rotate(${(i - 1) * 3}deg)`, opacity: p}}>
						<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, color: '#0a1440'}}>{k}</span>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: '#c21f3a'}}>{v}</span>
						</div>
						<div style={{display: 'inline-block', marginTop: 6 * u, border: `${3 * u}px solid #c21f3a`, color: '#c21f3a', borderRadius: 8 * u, padding: `${2 * u}px ${10 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 20 * u, letterSpacing: 2 * u}}>VENCE MAÑANA</div>
					</div>
				);
			})}
			<div style={{position: 'absolute', right: width * 0.05, top: y * height + 40 * u, transform: `scale(${q})`, background: GOLD, color: '#020617', borderRadius: 999, padding: `${20 * u}px ${30 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, boxShadow: `0 0 ${36 * u + Math.sin(f / 4) * 10 * u}px ${hexA(GOLD, 0.7)}`}}>⚡ SOLUCIÓN RÁPIDA</div>
		</AbsoluteFill>
	);
};

/** Lista de personas que ya se acercaron (CRM) + auditoría por columnas: ¿respondiste? ¿entendió? ¿duda? */
export const LeadsList: React.FC<G & {y?: number; audit?: number[]}> = ({dur, y = 0.565, audit = [9999, 9999, 9999]}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.92;
	const leads = [
		{n: 'Laura G.', m: '¿Cuánto cuesta el programa?', marks: [false, false, true]},
		{n: 'Martín R.', m: 'Te escribo por la propuesta', marks: [true, false, true]},
		{n: 'Sofía P.', m: '¿Tienen cupo este mes?', marks: [false, false, false]},
		{n: 'Diego A.', m: 'Lo veo con mi socio y te aviso', marks: [true, true, false]},
		{n: 'Carla M.', m: '¿Hay facilidades de pago?', marks: [false, true, true]},
	];
	const cols = ['¿RESPONDISTE?', '¿ENTENDIÓ?', '¿DUDA RESUELTA?'];
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 24 * u, ...glass(u, 0.85), padding: `${16 * u}px ${18 * u}px`, boxSizing: 'border-box'}}>
				<div style={{display: 'flex', alignItems: 'center', fontFamily: fonts.heading, fontWeight: 800, fontSize: 18 * u, letterSpacing: 2 * u, color: 'rgba(255,255,255,.55)', paddingBottom: 10 * u, borderBottom: '1px solid rgba(255,255,255,.1)'}}>
					<span style={{flex: 2.6}}>YA SE ACERCARON</span>
					{cols.map((c, i) => <span key={c} style={{flex: 1, textAlign: 'center', color: f >= audit[i] ? GOLD : 'rgba(255,255,255,.35)'}}>{c}</span>)}
				</div>
				{leads.map((l, i) => {
					const p = spring({frame: f - 4 - i * 5, fps, config: {stiffness: 220, damping: 18}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', padding: `${12 * u}px 0`, borderBottom: i < leads.length - 1 ? '1px dashed rgba(255,255,255,.07)' : undefined, opacity: p, transform: `translateX(${(1 - p) * 40 * u}px)`}}>
							<div style={{flex: 2.6, display: 'flex', alignItems: 'center', gap: 12 * u}}>
								<div style={{width: 48 * u, height: 48 * u, borderRadius: '50%', background: `linear-gradient(135deg, hsl(${200 + i * 30},70%,55%), hsl(${240 + i * 25},60%,40%))`, flexShrink: 0}} />
								<div>
									<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, color: '#fff'}}>{l.n}</div>
									<div style={{fontFamily: fonts.body, fontSize: 20 * u, color: 'rgba(255,255,255,.6)'}}>{l.m}</div>
								</div>
							</div>
							{l.marks.map((ok, c) => {
								const mp = interpolate(f, [audit[c] + i * 3, audit[c] + i * 3 + 6], [0, 1], clamp);
								return <span key={c} style={{flex: 1, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 32 * u, color: ok ? GREEN : RED, opacity: mp, transform: `scale(${0.5 + 0.5 * mp})`}}>{ok ? '✓' : '✗'}</span>;
							})}
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Pendientes con contadores rojos (consultas / propuestas) y la marca “EMPIEZA AQUÍ”. */
export const BacklogBadges: React.FC<G & {items: {text: string; n: number; at: number}[]; hereAt?: number; y?: number}> = ({dur, items, hereAt = 100, y = 0.72}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const h = spring({frame: f - hereAt, fps, config: {stiffness: 230, damping: 12}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				{items.map((it, i) => {
					const p = spring({frame: f - it.at, fps, config: {stiffness: 220, damping: 17}});
					const cnt = Math.round(interpolate(f, [it.at, it.at + 16], [0, it.n], clamp));
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: 22 * u, ...glass(u, 0.85), padding: `${18 * u}px ${24 * u}px`, marginBottom: 14 * u, opacity: f >= it.at ? p : 0, transform: `translateY(${(1 - p) * 30 * u}px)`, border: f >= hereAt && i === 0 ? `${3 * u}px solid ${GOLD}` : undefined}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 34 * u, color: '#fff'}}>{it.text}</span>
							<span style={{minWidth: 62 * u, height: 62 * u, borderRadius: 31 * u, background: RED, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 32 * u, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>{cnt}</span>
						</div>
					);
				})}
			</div>
			<div style={{position: 'absolute', left: (width - W) / 2 + 20 * u, top: y * height - 60 * u, transform: `scale(${h})`, transformOrigin: 'left bottom', background: GOLD, color: '#020617', borderRadius: 12 * u, padding: `${8 * u}px ${18 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 26 * u, letterSpacing: 3 * u}}>EMPIEZA POR AHÍ ↓</div>
		</AbsoluteFill>
	);
};

/** Dos líneas: gasto que sube vs ventas planas (franja baja). */
export const TwinLines: React.FC<G & {y?: number}> = ({dur, y = 0.72}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const H = 200 * u;
	const p = interpolate(f, [4, dur - 10], [0, 1], {...clamp, easing: EASE.out});
	const N = 30;
	const line = (fn: (t: number) => number) => Array.from({length: Math.max(2, Math.round(N * p))}, (_, i) => {
		const t = i / N;
		return `${t * W},${H - fn(t) * H}`;
	}).join(' ');
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 24 * u, ...glass(u, 0.85), padding: `${16 * u}px ${18 * u}px`, boxSizing: 'content-box'}}>
				<div style={{display: 'flex', gap: 24 * u, marginBottom: 8 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 3 * u}}>
					<span style={{color: RED}}>━ TU GASTO</span>
					<span style={{color: GREEN}}>━ TUS VENTAS</span>
				</div>
				<svg width={W} height={H}>
					<polyline points={line((t) => 0.08 + 0.85 * Math.pow(t, 1.3) + random(`a${Math.round(t * 30)}`) * 0.03)} fill="none" stroke={RED} strokeWidth={5 * u} />
					<polyline points={line((t) => 0.12 + random(`b${Math.round(t * 30)}`) * 0.04)} fill="none" stroke={GREEN} strokeWidth={5 * u} />
				</svg>
			</div>
		</AbsoluteFill>
	);
};
