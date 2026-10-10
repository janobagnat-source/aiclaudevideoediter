// AD06 (contrataste para tener menos trabajo) — interfaces propias de este ad.
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

/** Tablero kanban: primero “contratado ✓”, después las tarjetas se multiplican en tus columnas. */
export const KanbanFlood: React.FC<G & {y?: number; hireAt?: number; floodAt?: number}> = ({dur, y = 0.56, hireAt = 4, floodAt = 90}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.92;
	const cols = [
		{t: 'MI TRABAJO', items: ['Propuesta cliente A', 'Reunión de ventas', 'Facturación', 'Post de la semana', 'Llamada 18:00']},
		{t: 'REVISAR LO SUYO', items: ['Corregir informe', 'Rehacer diseño', 'Revisar correo', 'Volver a explicar', 'Corregir otra vez']},
	];
	const hire = spring({frame: f - hireAt, fps, config: {stiffness: 220, damping: 16}});
	const colW = (W - 18 * u) / 2;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 16 * u, borderRadius: 20 * u, background: hexA(GREEN, 0.14), border: `${2 * u}px solid ${GREEN}`, padding: `${14 * u}px ${22 * u}px`, marginBottom: 18 * u, opacity: hire, transform: `scale(${0.9 + 0.1 * hire})`}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: GREEN}}>✓</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: '#fff'}}>Nuevo asistente contratado</span>
				</div>
				<div style={{display: 'flex', gap: 18 * u}}>
					{cols.map((c, ci) => (
						<div key={ci} style={{width: colW, borderRadius: 22 * u, ...glass(u, 0.75), padding: 16 * u, minHeight: 420 * u}}>
							<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: ci ? RED : GOLD, marginBottom: 12 * u}}>{c.t}</div>
							{c.items.map((it, k) => {
								const at = floodAt + k * 7 + ci * 4;
								const p = spring({frame: f - at, fps, config: {stiffness: 260, damping: 18}});
								return (
									<div key={k} style={{borderRadius: 12 * u, background: ci ? 'rgba(255,77,94,.16)' : 'rgba(255,255,255,.08)', borderLeft: `${5 * u}px solid ${ci ? RED : GOLD}`, padding: `${10 * u}px ${14 * u}px`, marginBottom: 10 * u, fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, color: '#fff', opacity: f >= at ? p : 0, transform: `translateY(${(1 - p) * -40 * u}px) rotate(${(random(`k${ci}${k}`) - 0.5) * 3}deg)`}}>{it}</div>
								);
							})}
						</div>
					))}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Respuesta automática “fuera de oficina”: se activa (ibas a respirar)… y se cancela. */
export const OOOToggle: React.FC<G & {y?: number; onAt?: number; offAt?: number}> = ({dur, y = 0.78, onAt = 6, offAt = 50}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const on = interpolate(f, [onAt, onAt + 8], [0, 1], {...clamp, easing: EASE.out}) * (1 - interpolate(f, [offAt, offAt + 6], [0, 1], clamp));
	const cancelled = f >= offAt;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 28 * u, ...glass(u, 0.85), padding: `${22 * u}px ${28 * u}px`, display: 'flex', alignItems: 'center', gap: 22 * u}}>
				<div style={{flex: 1}}>
					<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: '#fff'}}>Respuesta automática</div>
					<div style={{fontFamily: fonts.body, fontSize: 26 * u, color: 'rgba(255,255,255,.65)'}}>“Estoy de vacaciones, mi equipo te atiende” 🌴</div>
				</div>
				<div style={{width: 120 * u, height: 66 * u, borderRadius: 999, background: on > 0.5 ? GREEN : 'rgba(255,255,255,.2)', position: 'relative'}}>
					<div style={{position: 'absolute', top: 6 * u, left: 6 * u + on * 54 * u, width: 54 * u, height: 54 * u, borderRadius: '50%', background: '#fff', boxShadow: '0 2px 6px rgba(0,0,0,.4)'}} />
				</div>
			</div>
			{cancelled && (
				<div style={{position: 'absolute', right: width * 0.08, top: y * height - 50 * u, transform: 'rotate(-6deg)', background: RED, color: '#fff', borderRadius: 12 * u, padding: `${8 * u}px ${20 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, letterSpacing: 3 * u, boxShadow: `0 8px 24px rgba(0,0,0,.4)`}}>CANCELADO</div>
			)}
		</AbsoluteFill>
	);
};

/** Organigrama que crece: vos arriba, el equipo se suma debajo. */
export const OrgChartGrow: React.FC<G & {y?: number; levels?: number[]; title?: string}> = ({dur, y = 0.58, levels = [3, 6], title = 'TU EQUIPO CRECE'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const top = y * height + 80 * u;
	const node = (x: number, yy: number, at: number, you = false, key = '') => {
		const p = spring({frame: f - at, fps, config: {stiffness: 230, damping: 16}});
		const r = (you ? 58 : 40) * u;
		return (
			<div key={key} style={{position: 'absolute', left: x - r, top: yy - r, width: 2 * r, height: 2 * r, borderRadius: '50%', background: you ? `linear-gradient(135deg, ${GOLD}, #e08a00)` : 'linear-gradient(135deg,#3474FF,#0b2a9c)', border: `${3 * u}px solid rgba(255,255,255,.6)`, transform: `scale(${p})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: (you ? 30 : 22) * u, color: you ? '#020617' : '#fff', boxShadow: you ? `0 0 ${30 * u}px ${hexA(GOLD, 0.6)}` : undefined}}>{you ? 'TÚ' : ''}</div>
		);
	};
	const rows: {x: number; y: number; at: number; px: number; py: number}[] = [];
	levels.forEach((n, li) => {
		for (let i = 0; i < n; i++) {
			const x = width * (0.5 + (i - (n - 1) / 2) * (0.8 / Math.max(n, 3)));
			const parent = li === 0 ? {x: width / 2, y: top} : rows[Math.floor(i / 2)];
			rows.push({x, y: top + (li + 1) * 150 * u, at: 10 + li * 26 + i * 5, px: parent.x, py: parent.y});
		}
	});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD}}>{title}</div>
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				{rows.map((r, i) => {
					const p = interpolate(f, [r.at - 4, r.at + 4], [0, 1], clamp);
					return <line key={i} x1={r.px} y1={r.py} x2={r.px + (r.x - r.px) * p} y2={r.py + (r.y - r.py) * p} stroke="rgba(160,185,255,.55)" strokeWidth={3 * u} />;
				})}
			</svg>
			{node(width / 2, top, 2, true, 'you')}
			{rows.map((r, i) => node(r.x, r.y, r.at, false, `n${i}`))}
		</AbsoluteFill>
	);
};

/** Frase entre comillas que se tacha con una línea dorada. */
export const QuoteStrike: React.FC<G & {quote: string; strikeAt?: number; y?: number; kicker?: string}> = ({dur, quote, strikeAt = 36, y = 0.79, kicker = 'ANTES DE DECIR'}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const s = interpolate(f, [strikeAt, strikeAt + 10], [0, 1], {...clamp, easing: EASE.out});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: width * 0.08, right: width * 0.08, top: y * height, textAlign: 'center'}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 10 * u}}>{kicker}</div>
				<div style={{position: 'relative', display: 'inline-block', fontFamily: fonts.heading, fontWeight: 800, fontStyle: 'italic', fontSize: 50 * u, color: s > 0.5 ? 'rgba(255,255,255,.5)' : '#fff', lineHeight: 1.15}}>
					“{quote}”
					<div style={{position: 'absolute', left: -10 * u, right: -10 * u, top: '52%', height: 6 * u, background: GOLD, transform: `scaleX(${s})`, transformOrigin: 'left', boxShadow: `0 0 ${12 * u}px ${GOLD}`}} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Autoevaluación: preguntas con casillas que quedan SIN tildar (el problema no es el equipo). */
export const SelfCheck: React.FC<G & {items: {text: string; at: number}[]; y?: number; title?: string}> = ({dur, items, y = 0.585, title = 'PREGÚNTATE'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 18 * u}}>{title}</div>
				{items.map((it, i) => {
					const p = spring({frame: f - it.at, fps, config: {stiffness: 230, damping: 18}});
					const x = interpolate(f, [it.at + 14, it.at + 22], [0, 1], clamp);
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 22 * u, borderRadius: 22 * u, ...glass(u, 0.75), padding: `${22 * u}px ${24 * u}px`, marginBottom: 14 * u, opacity: f >= it.at ? p : 0, transform: `translateY(${(1 - p) * 30 * u}px)`}}>
							<div style={{width: 54 * u, height: 54 * u, borderRadius: 12 * u, border: `${4 * u}px solid ${x > 0.5 ? RED : 'rgba(255,255,255,.5)'}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 36 * u, color: RED, flexShrink: 0}}>{x > 0.5 ? '✗' : ''}</div>
							<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 40 * u, color: '#fff'}}>{it.text}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Procedimiento de UNA tarea: título, pasos y “listo cuando…”. */
export const SOPCard: React.FC<G & {task: string; steps: string[]; done: string; y?: number; every?: number}> = ({dur, task, steps, done, y = 0.68, every = 14}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const dAt = 10 + steps.length * every;
	const dp = interpolate(f, [dAt, dAt + 10], [0, 1], clamp);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 26 * u, background: '#f6f7fb', padding: `${24 * u}px ${30 * u}px`, boxShadow: `0 ${26 * u}px ${60 * u}px rgba(0,0,0,.45)`, transform: `translateY(${(1 - v) * 50 * u}px)`}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 20 * u, letterSpacing: 5 * u, color: '#5a6690'}}>PROCESO · 1 TAREA</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 38 * u, color: '#0a1440', marginBottom: 12 * u}}>{task}</div>
				{steps.map((s, i) => {
					const p = interpolate(f, [10 + i * every, 18 + i * every], [0, 1], clamp);
					return (
						<div key={i} style={{display: 'flex', gap: 14 * u, alignItems: 'baseline', fontFamily: fonts.heading, fontWeight: 700, fontSize: 30 * u, color: '#0a1440', opacity: p, padding: `${4 * u}px 0`}}>
							<span style={{color: '#0b3bd6', fontWeight: 900}}>{i + 1}.</span>
							{s}
						</div>
					);
				})}
				<div style={{marginTop: 12 * u, borderRadius: 14 * u, background: hexA('#0b8a3a', 0.12), border: `${2 * u}px solid #0b8a3a`, padding: `${10 * u}px ${16 * u}px`, fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, color: '#0b6a2e', opacity: dp}}>✓ LISTO CUANDO: {done}</div>
			</div>
		</AbsoluteFill>
	);
};
