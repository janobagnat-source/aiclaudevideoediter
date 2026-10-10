// AD05 (emigrar no borra tu experiencia) — interfaces propias de este ad.
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

/** Contador mecánico que rueda hacia atrás hasta 00 (“empezar de cero”). */
export const OdometerReset: React.FC<G & {from?: number; label?: string; y?: number; delay?: number}> = ({dur, from = 15, label = 'AÑOS DE EXPERIENCIA', y = 0.79, delay = 4}) => {
	const {f, v} = useIO(dur, 8, 8);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = interpolate(f, [delay, delay + 26], [0, 1], {...clamp, easing: EASE.inOut});
	const val = from * (1 - p);
	const digits = [Math.floor(val / 10), val % 10];
	const H = 150 * u;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
				<div style={{display: 'flex', gap: 10 * u}}>
					{digits.map((d, i) => (
						<div key={i} style={{width: 120 * u, height: H, borderRadius: 18 * u, overflow: 'hidden', ...glass(u, 0.85), position: 'relative'}}>
							<div style={{position: 'absolute', left: 0, right: 0, top: -d * H, transition: 'none'}}>
								{Array.from({length: 11}).map((_, k) => (
									<div key={k} style={{height: H, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 110 * u, color: p > 0.98 ? RED : '#fff', fontVariantNumeric: 'tabular-nums'}}>{k % 10}</div>
								))}
							</div>
							<div style={{position: 'absolute', left: 0, right: 0, top: '50%', height: 2 * u, background: 'rgba(0,0,0,.45)'}} />
						</div>
					))}
				</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 26 * u, letterSpacing: 8 * u, color: 'rgba(255,255,255,.75)', marginTop: 14 * u}}>{label}</div>
			</div>
		</AbsoluteFill>
	);
};

/** Tarjeta de embarque: tu experiencia viaja contigo (sello A BORDO). */
export const BoardingPass: React.FC<G & {y?: number; stampAt?: number; rows?: [string, string][]}> = ({dur, y = 0.72, stampAt = 40, rows = [['PASAJERO', 'TU EXPERIENCIA'], ['EQUIPAJE', '15 AÑOS DE OFICIO'], ['DESTINO', 'TU NUEVO MERCADO']]}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const sp = spring({frame: f - stampAt, fps, config: {stiffness: 260, damping: 12}});
	const ink = '#0a1440';
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, display: 'flex', borderRadius: 26 * u, overflow: 'hidden', boxShadow: `0 ${30 * u}px ${70 * u}px rgba(0,0,0,.5)`, opacity: v, transform: `translateY(${(1 - v) * 60 * u}px) rotate(${(1 - v) * -3}deg)`}}>
				<div style={{flex: 3, background: '#f4f6fc', padding: `${24 * u}px ${30 * u}px`, position: 'relative'}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 14 * u, marginBottom: 14 * u}}>
						<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: ink, letterSpacing: 2 * u}}>BOARDING PASS</span>
						<span style={{fontSize: 30 * u}}>✈</span>
					</div>
					{rows.map(([k, val], i) => (
						<div key={i} style={{display: 'flex', justifyContent: 'space-between', padding: `${6 * u}px 0`, borderTop: i ? `1px dashed ${hexA(ink, 0.2)}` : undefined}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, letterSpacing: 4 * u, color: hexA(ink, 0.55)}}>{k}</span>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: ink}}>{val}</span>
						</div>
					))}
					{f >= stampAt && (
						<div style={{position: 'absolute', right: 24 * u, top: 18 * u, transform: `rotate(-14deg) scale(${2 - sp})`, opacity: Math.min(1, sp * 1.5), border: `${5 * u}px solid #0b8a3a`, color: '#0b8a3a', borderRadius: 12 * u, padding: `${4 * u}px ${16 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, letterSpacing: 3 * u, mixBlendMode: 'multiply'}}>A BORDO ✓</div>
					)}
				</div>
				<div style={{flex: 1.1, background: `linear-gradient(180deg, ${GOLD}, #e09a00)`, borderLeft: `${4 * u}px dashed rgba(2,6,23,.35)`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 14 * u}}>
					<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 18 * u, letterSpacing: 4 * u, color: 'rgba(2,6,23,.6)'}}>PUERTA</div>
					<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 60 * u, color: '#020617'}}>A1</div>
					<div style={{display: 'flex', gap: 2 * u, marginTop: 8 * u}}>
						{Array.from({length: 18}).map((_, i) => <div key={i} style={{width: (random(`bc${i}`) > 0.5 ? 4 : 2) * u, height: 46 * u, background: '#020617'}} />)}
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Red de contactos que se construye: nodos que aparecen y líneas que los unen (panel inferior). */
export const NetworkMap: React.FC<G & {labels?: {text: string; at: number}[]; y?: number; h?: number}> = ({dur, labels = [], y = 0.56, h = 0.4}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width;
	const H = height * h;
	const N = 22;
	const nodes = Array.from({length: N}, (_, i) => ({x: 0.1 + 0.8 * random(`nx${i}`), y: 0.12 + 0.76 * random(`ny${i}`), at: 4 + i * 3.4}));
	const edges: [number, number][] = [];
	for (let i = 1; i < N; i++) edges.push([i, Math.floor(random(`e${i}`) * i)]);
	for (let i = 2; i < N; i += 3) edges.push([i, Math.floor(random(`e2${i}`) * i)]);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<svg width={W} height={H} style={{position: 'absolute', left: 0, top: y * height}}>
				{edges.map(([a, b], k) => {
					const t = Math.max(nodes[a].at, nodes[b].at);
					const p = interpolate(f, [t, t + 8], [0, 1], clamp);
					const A = nodes[a];
					const B = nodes[b];
					return <line key={k} x1={A.x * W} y1={A.y * H} x2={(A.x + (B.x - A.x) * p) * W} y2={(A.y + (B.y - A.y) * p) * H} stroke={hexA('#7da2ff', 0.55)} strokeWidth={2 * u} />;
				})}
				{nodes.map((n, i) => {
					const p = interpolate(f, [n.at, n.at + 6], [0, 1], {...clamp, easing: EASE.out});
					const big = i % 5 === 0;
					return <circle key={i} cx={n.x * W} cy={n.y * H} r={(big ? 13 : 7) * u * p} fill={big ? GOLD : '#9fb6ff'} style={{filter: big ? `drop-shadow(0 0 ${8 * u}px ${GOLD})` : undefined}} />;
				})}
			</svg>
			{labels.map((l, i) => {
				const p = spring({frame: f - l.at, fps: 30, config: {stiffness: 220, damping: 18}});
				return (
					<div key={i} style={{position: 'absolute', left: width * (0.08 + (i % 2) * 0.42), top: y * height + H * (0.1 + i * 0.3), ...glass(u, 0.85), borderRadius: 999, padding: `${12 * u}px ${28 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, color: '#fff', letterSpacing: 2 * u, opacity: p, transform: `scale(${0.85 + 0.15 * p})`, border: `${2 * u}px solid ${hexA(GOLD, 0.7)}`}}>{l.text}</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Línea de meses que se recorre (construir lleva tiempo). */
export const MonthTrack: React.FC<G & {months?: string[]; y?: number; label?: string}> = ({dur, months = ['MES 1', 'MES 2', 'MES 3', 'MES 4', 'MES 5', 'MES 6'], y = 0.8, label = 'ESO REQUIERE TIEMPO'}) => {
	const {f, v} = useIO(dur, 8, 8);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const p = interpolate(f, [4, dur - 4], [0, 1], {...clamp, easing: EASE.inOut});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 7 * u, color: GOLD, marginBottom: 18 * u}}>{label}</div>
				<div style={{position: 'relative', height: 8 * u, background: 'rgba(255,255,255,.12)', borderRadius: 4 * u}}>
					<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${p * 100}%`, background: GOLD, borderRadius: 4 * u, boxShadow: `0 0 ${14 * u}px ${GOLD}`}} />
					{months.map((m, i) => {
						const x = i / (months.length - 1);
						const on = p >= x - 0.01;
						return (
							<div key={i} style={{position: 'absolute', left: `${x * 100}%`, top: -10 * u, transform: 'translateX(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
								<div style={{width: 28 * u, height: 28 * u, borderRadius: '50%', background: on ? GOLD : '#0b1640', border: `${3 * u}px solid ${on ? GOLD : 'rgba(255,255,255,.3)'}`}} />
								<div style={{marginTop: 14 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 20 * u, color: on ? '#fff' : 'rgba(255,255,255,.4)', whiteSpace: 'nowrap'}}>{m}</div>
							</div>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Hoja de libreta con escritura a mano que se va trazando (fuente Caveat). */
export const HandNote: React.FC<G & {title?: string; lines: {text: string; at: number}[]; y?: number}> = ({dur, title = 'Problemas que sé resolver', lines, y = 0.57}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const W = width * 0.86;
	const sp = spring({frame: f, fps, config: {stiffness: 160, damping: 18}});
	const ink = '#13245f';
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 14 * u, background: '#fbf8ef', padding: `${30 * u}px ${36 * u}px ${30 * u}px ${80 * u}px`, boxShadow: `0 ${30 * u}px ${70 * u}px rgba(0,0,0,.5)`, transform: `translateY(${(1 - sp) * 120 * u}px) rotate(${-1.5 + (1 - sp) * -4}deg)`, backgroundImage: `repeating-linear-gradient(transparent, transparent ${74 * u}px, rgba(60,90,200,.18) ${74 * u}px, rgba(60,90,200,.18) ${76 * u}px)`, backgroundPositionY: `${58 * u}px`}}>
				<div style={{position: 'absolute', left: 54 * u, top: 0, bottom: 0, width: 3 * u, background: 'rgba(220,60,80,.45)'}} />
				<div style={{fontFamily: 'Caveat', fontWeight: 700, fontSize: 60 * u, color: ink, lineHeight: 1.2}}>{title}</div>
				{lines.map((l, i) => {
					const p = interpolate(f, [l.at, l.at + 22], [0, 1], clamp);
					return (
						<div key={i} style={{fontFamily: 'Caveat', fontWeight: 600, fontSize: 56 * u, color: ink, lineHeight: `${76 * u}px`, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}}>
							{i + 1}. {l.text}
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

/** Pestañas de carpeta (portafolio, muestra, proceso) que se van abriendo — evidencia. */
export const FolderTabs: React.FC<G & {tabs: {text: string; sub: string; at: number}[]; y?: number}> = ({dur, tabs, y = 0.74}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const cur = Math.max(0, tabs.filter((t) => f >= t.at).length - 1);
	const tw = W / tabs.length;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{display: 'flex'}}>
					{tabs.map((t, i) => {
						const on = i === cur && f >= t.at;
						return (
							<div key={i} style={{width: tw - 8 * u, marginRight: 8 * u, padding: `${14 * u}px 0`, textAlign: 'center', borderRadius: `${18 * u}px ${18 * u}px 0 0`, background: on ? GOLD : f >= t.at ? 'rgba(52,116,255,.55)' : 'rgba(255,255,255,.08)', fontFamily: fonts.heading, fontWeight: 900, fontSize: 26 * u, letterSpacing: 2 * u, color: on ? '#020617' : '#fff'}}>{t.text}</div>
						);
					})}
				</div>
				<div style={{borderRadius: `0 0 ${24 * u}px ${24 * u}px`, ...glass(u, 0.85), borderTop: `${4 * u}px solid ${GOLD}`, padding: `${26 * u}px ${30 * u}px`, minHeight: 110 * u}}>
					{tabs.map((t, i) => {
						const p = spring({frame: f - t.at, fps, config: {stiffness: 220, damping: 18}});
						return i === cur ? (
							<div key={i} style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 40 * u, color: '#fff', opacity: p, transform: `translateY(${(1 - p) * 20 * u}px)`}}>{t.sub}</div>
						) : null;
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Mensaje que se adapta: de GENÉRICO a ESPECÍFICO con un selector deslizante. */
export const MessageTuner: React.FC<G & {generic: string; specific: string; morphAt?: number; y?: number}> = ({dur, generic, specific, morphAt = 30, y = 0.58}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const p = interpolate(f, [morphAt, morphAt + 30], [0, 1], {...clamp, easing: EASE.inOut});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 7 * u, color: GOLD, marginBottom: 16 * u}}>TU MENSAJE</div>
				<div style={{position: 'relative', borderRadius: 28 * u, ...glass(u, 0.85), padding: `${30 * u}px ${32 * u}px`, minHeight: 190 * u}}>
					<div style={{position: 'absolute', inset: `${30 * u}px ${32 * u}px`, fontFamily: fonts.heading, fontWeight: 800, fontSize: 44 * u, color: 'rgba(255,255,255,.75)', opacity: 1 - p, filter: `blur(${p * 8}px)`}}>“{generic}”</div>
					<div style={{position: 'absolute', inset: `${30 * u}px ${32 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 44 * u, color: '#fff', opacity: p, filter: `blur(${(1 - p) * 8}px)`}}>“{specific}”</div>
				</div>
				<div style={{marginTop: 30 * u, display: 'flex', alignItems: 'center', gap: 20 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 4 * u, color: p < 0.5 ? '#fff' : 'rgba(255,255,255,.4)'}}>GENÉRICO</span>
					<div style={{flex: 1, height: 10 * u, borderRadius: 5 * u, background: 'rgba(255,255,255,.12)', position: 'relative'}}>
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${p * 100}%`, background: GOLD, borderRadius: 5 * u}} />
						<div style={{position: 'absolute', left: `${p * 100}%`, top: '50%', width: 40 * u, height: 40 * u, borderRadius: '50%', background: '#fff', border: `${5 * u}px solid ${GOLD}`, transform: 'translate(-50%,-50%)', boxShadow: `0 0 ${16 * u}px ${GOLD}`}} />
					</div>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 24 * u, letterSpacing: 4 * u, color: p > 0.5 ? GOLD : 'rgba(255,255,255,.4)'}}>ESPECÍFICO</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Sello circular de verificación que se estampa (EVIDENCIA · VERIFICADA). */
export const SealStamp: React.FC<G & {top?: string; bottom?: string; y?: number; x?: number; delay?: number}> = ({dur, top = 'EVIDENCIA', bottom = 'RESPALDA TU TRABAJO', y = 0.8, x = 0.5, delay = 4}) => {
	const {f, v} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const sp = spring({frame: f - delay, fps, config: {stiffness: 280, damping: 12}});
	const R = 130 * u;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: x * width - R, top: y * height - R, width: 2 * R, height: 2 * R, borderRadius: '50%', border: `${6 * u}px solid ${GOLD}`, boxShadow: `0 0 0 ${10 * u}px rgba(255,187,0,.15), 0 0 ${40 * u}px ${hexA(GOLD, 0.4)}`, background: 'rgba(2,6,23,.75)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${2.2 - sp * 1.2}) rotate(${(1 - sp) * -30 - 8}deg)`, opacity: Math.min(1, sp * 1.4)}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, letterSpacing: 4 * u, color: GOLD}}>{top}</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 80 * u, color: '#fff', lineHeight: 1}}>✓</div>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 15 * u, letterSpacing: 2 * u, color: 'rgba(255,255,255,.75)', textAlign: 'center', padding: `0 ${20 * u}px`}}>{bottom}</div>
			</div>
		</AbsoluteFill>
	);
};
