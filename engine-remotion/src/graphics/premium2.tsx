// Motion graphics narrativos (tanda Carlos Buelvas ads 2–10). Marca vía useBrand(); animación solo con useCurrentFrame().
import {evolvePath} from '@remotion/paths';
import {noise2D} from '@remotion/noise';
import React from 'react';
import {Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';

type G = {dur: number};
const GOLD = '#FFBB00';
const BLUE = '#3474FF';
const DEEP = '#0034B7';
const src = (s?: string | null) => (!s ? undefined : s.startsWith('http') ? s : staticFile(s));
const useU = () => {
	const {width, height} = useVideoConfig();
	return Math.min(width, height) / 1080;
};
const useOut = (dur: number, n = 8) => interpolate(useCurrentFrame(), [dur - n, dur], [1, 0], {...clamp, easing: EASE.in});
const glass: React.CSSProperties = {background: 'linear-gradient(160deg, rgba(52,116,255,.28), rgba(4,12,48,.86))', border: '2px solid rgba(160,190,255,.4)', boxShadow: '0 30px 80px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.22)', backdropFilter: 'blur(14px)'};
const heading = (fonts: {heading: string}) => `${fonts.heading}, Montserrat, sans-serif`;

// ---------------------------------------------------------------------------------------------
/** Posteo de red social que se escribe solo y recibe un sello (p.ej. "ESE NO SOY YO").
 * props: text, avatar, handle, stamp, stampAt (frames), y, likes */
export const PostCard: React.FC<G & {text: string; avatar?: string; handle?: string; stamp?: string; stampAt?: number; y?: number; cps?: number}> = ({dur, text, avatar, handle = 'carlos.buelvas', stamp, stampAt = 40, y = 0.3, cps = 38}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 15, stiffness: 160}});
	const n = Math.floor(Math.max(0, frame - 6) * (cps / fps));
	const shown = text.slice(0, n);
	const st = spring({frame: frame - stampAt, fps, config: {damping: 9, stiffness: 260}});
	const W = width * 0.84;
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: `translateY(-50%) translateY(${(1 - s) * 70 * u}px) rotate(${(1 - s) * -4}deg)`, opacity: out * Math.min(1, s * 1.4)}}>
			<div style={{background: '#fff', borderRadius: 34 * u, padding: 30 * u, boxShadow: '0 40px 100px rgba(0,0,0,.5)', fontFamily: '-apple-system, Helvetica, sans-serif', color: '#111'}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 16 * u, marginBottom: 18 * u}}>
					<div style={{width: 72 * u, height: 72 * u, borderRadius: '50%', overflow: 'hidden', background: '#ccd'}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
					<div style={{fontWeight: 800, fontSize: 32 * u}}>{handle}</div>
					<div style={{marginLeft: 'auto', fontSize: 40 * u, color: '#999'}}>···</div>
				</div>
				<div style={{fontSize: 38 * u, lineHeight: 1.35, minHeight: 150 * u}}>
					{shown}
					<span style={{opacity: frame % 16 < 8 ? 1 : 0, color: BLUE}}>|</span>
				</div>
				<div style={{display: 'flex', gap: 26 * u, marginTop: 18 * u, fontSize: 40 * u, color: '#444'}}>♡ 💬 ↗</div>
			</div>
			{stamp && frame >= stampAt && (
				<div style={{position: 'absolute', right: -10 * u, top: '42%', transform: `rotate(-12deg) scale(${2.2 - 1.2 * st})`, opacity: Math.min(1, st * 2), border: `${7 * u}px solid ${GOLD}`, color: GOLD, fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 64 * u, padding: `${6 * u}px ${24 * u}px`, borderRadius: 14 * u, background: 'rgba(2,6,23,.85)', textTransform: 'uppercase', whiteSpace: 'nowrap', boxShadow: `0 0 ${30 * u}px ${hexA(GOLD, 0.6)}`}}>
					{stamp}
				</div>
			)}
		</div>
	);
};

/** Conversación tipo chat: burbujas que entran en orden (con "escribiendo…"). props: messages [{text, me?, at (frames)}], y, title */
export const ChatThread: React.FC<G & {messages: {text: string; me?: boolean; at: number}[]; y?: number; title?: string; avatar?: string}> = ({dur, messages, y = 0.3, title = 'Cliente', avatar}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const out = useOut(dur);
	const W = width * 0.84;
	const s = spring({frame, fps, config: {damping: 16, stiffness: 150}});
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: `translateY(-50%) scale(${0.9 + 0.1 * s})`, opacity: out * s, borderRadius: 36 * u, overflow: 'hidden', ...glass}}>
			<div style={{display: 'flex', alignItems: 'center', gap: 16 * u, padding: `${18 * u}px ${24 * u}px`, background: 'rgba(0,10,40,.55)', borderBottom: '1px solid rgba(255,255,255,.12)'}}>
				<div style={{width: 60 * u, height: 60 * u, borderRadius: '50%', background: `linear-gradient(135deg, ${BLUE}, ${DEEP})`, overflow: 'hidden'}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
				<div style={{fontFamily: '-apple-system, Helvetica, sans-serif', fontWeight: 700, fontSize: 32 * u, color: '#fff'}}>{title}</div>
				<div style={{marginLeft: 'auto', width: 14 * u, height: 14 * u, borderRadius: '50%', background: '#00E051'}} />
			</div>
			<div style={{padding: 24 * u, display: 'flex', flexDirection: 'column', gap: 14 * u, minHeight: 200 * u}}>
				{messages.map((m, i) => {
					const f = frame - m.at;
					if (f < -14) return null;
					if (f < 0)
						return (
							<div key={i} style={{alignSelf: m.me ? 'flex-end' : 'flex-start', background: m.me ? BLUE : 'rgba(255,255,255,.92)', borderRadius: 26 * u, padding: `${14 * u}px ${22 * u}px`, fontSize: 40 * u, color: m.me ? '#fff' : '#333', letterSpacing: 4}}>
								{[0, 1, 2].map((d) => <span key={d} style={{opacity: 0.35 + 0.65 * Math.max(0, Math.sin((frame + d * 4) / 3))}}>●</span>)}
							</div>
						);
					const sp = spring({frame: f, fps, config: {damping: 13, stiffness: 240}});
					return (
						<div key={i} style={{alignSelf: m.me ? 'flex-end' : 'flex-start', maxWidth: '82%', background: m.me ? `linear-gradient(135deg, #5b8cff, ${BLUE})` : 'rgba(255,255,255,.95)', color: m.me ? '#fff' : '#111', borderRadius: 28 * u, borderBottomRightRadius: m.me ? 6 * u : 28 * u, borderBottomLeftRadius: m.me ? 28 * u : 6 * u, padding: `${16 * u}px ${24 * u}px`, fontFamily: '-apple-system, Helvetica, sans-serif', fontSize: 34 * u, lineHeight: 1.3, transform: `scale(${sp}) translateY(${(1 - sp) * 20}px)`, transformOrigin: m.me ? 'right bottom' : 'left bottom', boxShadow: '0 8px 24px rgba(0,0,0,.25)'}}>
							{m.text}
						</div>
					);
				})}
			</div>
		</div>
	);
};

/** Dos contadores en carrera (p.ej. SEGUIDORES sube vs VENTAS queda en 0). props: a {label,from,to}, b {label,from,to}, y */
export const CounterRace: React.FC<G & {a: {label: string; from: number; to: number; prefix?: string}; b: {label: string; from: number; to: number; prefix?: string}; y?: number}> = ({dur, a, b, y = 0.3}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const p = interpolate(frame, [4, Math.max(10, dur - 12)], [0, 1], {...clamp, easing: EASE.out});
	const box = (c: typeof a, gold: boolean, i: number) => {
		const s = spring({frame: frame - i * 5, fps, config: {damping: 14, stiffness: 160}});
		const v = c.from + (c.to - c.from) * p;
		const flat = c.to === c.from;
		return (
			<div style={{flex: 1, borderRadius: 30 * u, padding: `${26 * u}px ${18 * u}px`, textAlign: 'center', transform: `translateY(${(1 - s) * 60}px)`, opacity: s, ...glass, border: `2px solid ${gold ? hexA(GOLD, 0.7) : 'rgba(160,190,255,.4)'}`}}>
				<div style={{fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 76 * u, color: gold ? GOLD : '#fff', fontVariantNumeric: 'tabular-nums', transform: flat ? `translateX(${noise2D('cr', frame / 2, i) * 4 * u}px)` : undefined, textShadow: gold ? `0 0 ${24 * u}px ${hexA(GOLD, 0.5)}` : '0 6px 20px rgba(0,0,0,.5)'}}>
					{c.prefix ?? ''}
					{Math.round(v).toLocaleString('es-AR')}
				</div>
				<div style={{fontFamily: heading(fonts), fontWeight: 800, fontSize: 34 * u, color: '#cfe0ff', letterSpacing: 2, marginTop: 6 * u}}>{c.label}</div>
				<div style={{fontSize: 48 * u, marginTop: 6 * u, color: flat ? '#ff5a5a' : '#00E051'}}>{flat ? '▬' : '▲'}</div>
			</div>
		);
	};
	return (
		<div style={{position: 'absolute', left: width * 0.07, right: width * 0.07, top: y * height, transform: 'translateY(-50%)', display: 'flex', gap: 24 * u, opacity: out}}>
			{box(a, false, 0)}
			{box(b, true, 1)}
		</div>
	);
};

/** Etiqueta de precio que baja por miedo (precio tachado → nuevo precio) y se "rompe". props: from, to, prefix, y, label */
export const PriceDrop: React.FC<G & {from: number; to: number; prefix?: string; y?: number; label?: string; dropAt?: number}> = ({dur, from, to, prefix = '$', y = 0.28, label = 'PRECIO', dropAt = 18}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 11, stiffness: 150}});
	const d = interpolate(frame, [dropAt, dropAt + 20], [0, 1], {...clamp, easing: EASE.smooth});
	const v = from + (to - from) * d;
	const strike = interpolate(frame, [dropAt - 6, dropAt], [0, 1], clamp);
	const swing = Math.sin(frame / 9) * 6 * (1 - d * 0.5);
	return (
		<div style={{position: 'absolute', left: width / 2, top: y * height, transform: `translate(-50%, -50%) scale(${s}) rotate(${swing}deg)`, transformOrigin: '50% -40%', opacity: out}}>
			<div style={{width: 6 * u, height: 90 * u, margin: '0 auto', background: 'rgba(255,255,255,.6)'}} />
			<div style={{position: 'relative', background: `linear-gradient(160deg, #ffe08a, ${GOLD})`, borderRadius: `${30 * u}px ${30 * u}px ${30 * u}px ${30 * u}px`, padding: `${30 * u}px ${56 * u}px`, boxShadow: `0 30px 70px rgba(0,0,0,.5), 0 0 ${40 * u}px ${hexA(GOLD, 0.5)}`, textAlign: 'center'}}>
				<div style={{position: 'absolute', top: 18 * u, left: '50%', width: 26 * u, height: 26 * u, marginLeft: -13 * u, borderRadius: '50%', background: '#0a1230'}} />
				<div style={{marginTop: 26 * u, fontFamily: heading(fonts), fontWeight: 800, fontSize: 34 * u, color: '#3a2a00', letterSpacing: 3}}>{label}</div>
				<div style={{position: 'relative', fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 110 * u, color: '#1a1100', fontVariantNumeric: 'tabular-nums'}}>
					{prefix}
					{Math.round(v).toLocaleString('es-AR')}
					<div style={{position: 'absolute', left: '-4%', top: '52%', height: 10 * u, width: `${108 * strike}%`, background: '#e0263a', transform: 'rotate(-8deg)', borderRadius: 6 * u, opacity: d < 0.98 ? 1 : 0}} />
				</div>
			</div>
			<div style={{textAlign: 'center', marginTop: 16 * u, fontSize: 70 * u, color: '#ff5a5a', opacity: d, transform: `translateY(${(1 - d) * -20}px)`}}>▼</div>
		</div>
	);
};

/** Anillo de respiración (inhalá/exhalá). props: label1, label2, y, size */
export const BreatheRing: React.FC<G & {label1?: string; label2?: string; y?: number; size?: number}> = ({dur, label1 = 'INHALA', label2 = 'EXHALA', y = 0.27, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur, 10);
	const inO = interpolate(frame, [0, 10], [0, 1], clamp);
	const cyc = (frame / fps) % 3;
	const br = cyc < 1.5 ? EASE.smooth(cyc / 1.5) : 1 - EASE.smooth((cyc - 1.5) / 1.5);
	const S = 300 * u * size;
	return (
		<div style={{position: 'absolute', left: width / 2 - S, top: y * height - S, width: S * 2, height: S * 2, opacity: out * inO, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
			{[1, 0.75, 0.5].map((k, i) => (
				<div key={i} style={{position: 'absolute', width: S * (0.9 + 0.6 * br) * k * 1.2, height: S * (0.9 + 0.6 * br) * k * 1.2, borderRadius: '50%', border: `${3 * u}px solid ${i === 0 ? hexA(GOLD, 0.8) : hexA(BLUE, 0.6 - i * 0.15)}`, background: i === 2 ? `radial-gradient(circle, ${hexA(BLUE, 0.55)}, ${hexA(DEEP, 0.2)})` : undefined, boxShadow: i === 0 ? `0 0 ${50 * u}px ${hexA(GOLD, 0.45)}` : undefined}} />
			))}
			<div style={{fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 66 * u, color: '#fff', letterSpacing: 4, textShadow: '0 6px 20px rgba(0,0,0,.6)'}}>{cyc < 1.5 ? label1 : label2}</div>
		</div>
	);
};

/** Bloc de notas que se escribe solo con ítems numerados. props: title, items[], every (frames), y */
export const NotepadList: React.FC<G & {title?: string; items: string[]; every?: number; y?: number; delays?: number[]}> = ({dur, title = 'MIS 3 PROBLEMAS', items, every = 16, y = 0.3, delays}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 15, stiffness: 140}});
	const W = width * 0.8;
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: `translateY(-50%) perspective(1500px) rotateX(${(1 - s) * 30}deg) rotate(${-2 * s}deg)`, opacity: out * s}}>
			<div style={{background: '#fffdf4', borderRadius: 26 * u, padding: `${34 * u}px ${36 * u}px ${30 * u}px ${70 * u}px`, boxShadow: '0 40px 100px rgba(0,0,0,.5)', backgroundImage: `repeating-linear-gradient(180deg, transparent 0 ${66 * u}px, rgba(52,116,255,.25) ${66 * u}px ${68 * u}px)`, position: 'relative'}}>
				<div style={{position: 'absolute', left: 46 * u, top: 0, bottom: 0, width: 3 * u, background: 'rgba(224,38,58,.5)'}} />
				<div style={{fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 50 * u, color: DEEP, marginBottom: 10 * u}}>{title}</div>
				{items.map((it, i) => {
					const st = delays?.[i] ?? 10 + i * every;
					const n = Math.floor(Math.max(0, frame - st) * 1.4);
					const txt = it.slice(0, n);
					const check = spring({frame: frame - st - it.length / 1.4, fps, config: {damping: 10, stiffness: 300}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 18 * u, height: 68 * u, fontFamily: '"Caveat", "Permanent Marker", cursive', fontSize: 52 * u, color: '#1b2a5a'}}>
							<span style={{fontFamily: heading(fonts), fontWeight: 900, color: GOLD, fontSize: 44 * u, textShadow: '0 1px 0 #7a5a00'}}>{i + 1}.</span>
							<span>{txt}</span>
							<span style={{marginLeft: 'auto', color: '#00b347', fontSize: 50 * u, transform: `scale(${frame - st > it.length / 1.4 ? check : 0})`}}>✔</span>
						</div>
					);
				})}
			</div>
		</div>
	);
};

/** Ruta de avión entre dos puntos (emigrar): arco punteado, avión que lo recorre, pines de origen/destino. props: from, to (labels), y */
export const FlightPath: React.FC<G & {from?: string; to?: string; y?: number}> = ({dur, from = 'ORIGEN', to = 'NUEVO PAÍS', y = 0.3}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const X0 = width * 0.16;
	const X1 = width * 0.84;
	const Y = y * height + 90 * u;
	const d = `M ${X0} ${Y} Q ${width / 2} ${Y - 380 * u} ${X1} ${Y}`;
	const p = interpolate(frame, [6, Math.min(dur - 10, 50)], [0, 1], {...clamp, easing: EASE.smooth});
	const ev = evolvePath(p, d);
	const t = p;
	const bx = (1 - t) * (1 - t) * X0 + 2 * (1 - t) * t * (width / 2) + t * t * X1;
	const by = (1 - t) * (1 - t) * Y + 2 * (1 - t) * t * (Y - 380 * u) + t * t * Y;
	const dx = 2 * (1 - t) * (width / 2 - X0) + 2 * t * (X1 - width / 2);
	const dy = 2 * (1 - t) * (-380 * u) + 2 * t * (380 * u);
	const ang = (Math.atan2(dy, dx) * 180) / Math.PI;
	const pin = (x: number, label: string, on: number, gold: boolean) => (
		<div style={{position: 'absolute', left: x, top: Y, transform: `translate(-50%, -100%) scale(${on})`, textAlign: 'center'}}>
			<div style={{fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 38 * u, color: gold ? GOLD : '#fff', whiteSpace: 'nowrap', marginBottom: 10 * u, textShadow: '0 4px 14px rgba(0,0,0,.6)'}}>{label}</div>
			<div style={{width: 34 * u, height: 34 * u, margin: '0 auto', borderRadius: '50% 50% 50% 0', transform: 'rotate(-45deg)', background: gold ? GOLD : BLUE, boxShadow: `0 0 ${20 * u}px ${gold ? GOLD : BLUE}`}} />
		</div>
	);
	return (
		<div style={{position: 'absolute', inset: 0, opacity: out}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
				<path d={d} fill="none" stroke="rgba(255,255,255,.25)" strokeWidth={4 * u} strokeDasharray={`${14 * u} ${14 * u}`} />
				<path d={d} fill="none" stroke={GOLD} strokeWidth={6 * u} strokeLinecap="round" {...ev} style={{filter: `drop-shadow(0 0 ${10 * u}px ${GOLD})`}} />
			</svg>
			{pin(X0, from, interpolate(frame, [0, 8], [0, 1], clamp), false)}
			{pin(X1, to, interpolate(frame, [Math.min(dur - 10, 50) - 6, Math.min(dur - 10, 50) + 2], [0, 1], clamp), true)}
			<div style={{position: 'absolute', left: bx, top: by, fontSize: 80 * u, transform: `translate(-50%, -50%) rotate(${ang + 45}deg)`, filter: `drop-shadow(0 6px 12px rgba(0,0,0,.5))`}}>✈️</div>
		</div>
	);
};

/** Batería que se agota (cansancio). props: label, y, from, to */
export const BatteryDrain: React.FC<G & {label?: string; y?: number; from?: number; to?: number; x?: number; size?: number}> = ({dur, label = 'ENERGÍA', y = 0.3, from = 100, to = 8, x = 0.5, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 13, stiffness: 150}});
	const p = interpolate(frame, [6, Math.max(12, dur - 12)], [from, to], {...clamp, easing: EASE.smooth});
	const col = p > 50 ? '#00E051' : p > 20 ? GOLD : '#ff3b30';
	const W = 420 * u * size;
	const H = 200 * u * size;
	const blink = p < 20 ? (Math.floor(frame / 5) % 2 ? 0.45 : 1) : 1;
	return (
		<div style={{position: 'absolute', left: x * width - W / 2, top: y * height - H / 2, transform: `scale(${s})`, opacity: out}}>
			<div style={{display: 'flex', alignItems: 'center'}}>
				<div style={{width: W, height: H, borderRadius: 30 * u, border: `${9 * u}px solid #fff`, padding: 12 * u, boxShadow: '0 20px 60px rgba(0,0,0,.5)'}}>
					<div style={{width: `${p}%`, height: '100%', borderRadius: 16 * u, background: col, opacity: blink, boxShadow: `0 0 ${30 * u}px ${col}`}} />
				</div>
				<div style={{width: 22 * u, height: H * 0.4, background: '#fff', borderRadius: `0 ${10 * u}px ${10 * u}px 0`}} />
			</div>
			<div style={{textAlign: 'center', marginTop: 16 * u, fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 60 * u, color: '#fff', textShadow: '0 6px 20px rgba(0,0,0,.6)'}}>
				{label} <span style={{color: col}}>{Math.round(p)}%</span>
			</div>
		</div>
	);
};

/** Embudo que pierde gente por agujeros (publicidad que no convierte). props: top, bottom, y, leaks[] */
export const LeakyFunnel: React.FC<G & {top?: string; bottom?: string; y?: number; leaks?: string[]}> = ({dur, top = 'MÁS PUBLICIDAD', bottom = 'VENTAS', y = 0.3, leaks = ['SIN RESPUESTA', 'SIN SEGUIMIENTO']}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 15, stiffness: 130}});
	const W = width * 0.7;
	const H = 520 * u;
	const cx = width / 2;
	const y0 = y * height - H / 2;
	const dots = Array.from({length: 46}, (_, i) => {
		const t = ((frame - random(`d${i}`) * 50) / 50) % 1;
		if (frame - random(`d${i}`) * 50 < 0) return null;
		const leak = i % 3 !== 0; // 2 de cada 3 se escapan
		const yy = y0 + t * H;
		const half = (W / 2) * (1 - (t * 0.78));
		let xx = cx + (random(`x${i}`) - 0.5) * half * 1.6;
		if (leak && t > 0.45) xx = cx + (i % 2 ? 1 : -1) * (half + (t - 0.45) * 500 * u);
		return <div key={i} style={{position: 'absolute', left: xx - 9 * u, top: yy, width: 18 * u, height: 18 * u, borderRadius: '50%', background: leak && t > 0.45 ? '#ff5a5a' : GOLD, opacity: 1 - (leak && t > 0.45 ? (t - 0.45) * 1.8 : 0), boxShadow: `0 0 ${10 * u}px ${leak && t > 0.45 ? '#ff5a5a' : GOLD}`}} />;
	});
	return (
		<div style={{position: 'absolute', inset: 0, opacity: out * s}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
				<path d={`M ${cx - W / 2} ${y0} L ${cx + W / 2} ${y0} L ${cx + W * 0.11} ${y0 + H} L ${cx - W * 0.11} ${y0 + H} Z`} fill={hexA(BLUE, 0.25)} stroke="#9fc0ff" strokeWidth={4 * u} />
				{[0.52, 0.66].map((k, i) => (
					<g key={i}>
						<circle cx={cx + (i ? 1 : -1) * (W / 2) * (1 - k * 0.78)} cy={y0 + k * H} r={16 * u} fill="#01030c" stroke="#ff5a5a" strokeWidth={4 * u} />
					</g>
				))}
			</svg>
			{dots}
			<div style={{position: 'absolute', left: 0, right: 0, top: y0 - 70 * u, textAlign: 'center', fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 52 * u, color: '#fff'}}>{top}</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: y0 + H + 14 * u, textAlign: 'center', fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 52 * u, color: GOLD}}>{bottom}</div>
			{leaks.map((l, i) => (
				<div key={i} style={{position: 'absolute', top: y0 + [0.52, 0.66][i % 2] * H - 22 * u, [i % 2 ? 'right' : 'left']: 20 * u, fontFamily: heading(fonts), fontWeight: 800, fontSize: 28 * u, color: '#ff8080', background: 'rgba(40,0,0,.6)', borderRadius: 12 * u, padding: `${6 * u}px ${12 * u}px`, opacity: interpolate(frame, [18 + i * 8, 26 + i * 8], [0, 1], clamp)}}>{l}</div>
			))}
		</div>
	);
};

/** Cronómetro digital (p.ej. "10 minutos explicando"). props: from (seg), to (seg), label, y */
export const Stopwatch: React.FC<G & {from?: number; to?: number; label?: string; y?: number; size?: number}> = ({dur, from = 0, to = 600, label = 'EXPLICANDO…', y = 0.28, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 12, stiffness: 160}});
	const v = from + (to - from) * interpolate(frame, [4, Math.max(8, dur - 10)], [0, 1], {...clamp, easing: EASE.in});
	const mm = String(Math.floor(v / 60)).padStart(2, '0');
	const ss = String(Math.floor(v % 60)).padStart(2, '0');
	const S = 360 * u * size;
	const R = S / 2 - 16 * u;
	const C = 2 * Math.PI * R;
	return (
		<div style={{position: 'absolute', left: width / 2 - S / 2, top: y * height - S / 2, width: S, height: S, transform: `scale(${s})`, opacity: out}}>
			<div style={{position: 'absolute', left: S / 2 - 28 * u, top: -44 * u, width: 56 * u, height: 40 * u, borderRadius: 10 * u, background: '#fff'}} />
			<svg width={S} height={S} style={{position: 'absolute', inset: 0, transform: 'rotate(-90deg)'}}>
				<circle cx={S / 2} cy={S / 2} r={R} fill="rgba(6,14,44,.9)" stroke="rgba(255,255,255,.85)" strokeWidth={6 * u} />
				<circle cx={S / 2} cy={S / 2} r={R} fill="none" stroke={v > to * 0.7 ? '#ff3b30' : GOLD} strokeWidth={14 * u} strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - ((v - from) / (to - from || 1)))} style={{filter: `drop-shadow(0 0 ${14 * u}px ${GOLD})`}} />
			</svg>
			<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
				<div style={{fontFamily: heading(fonts), fontWeight: 900, fontSize: 96 * u, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>
					{mm}:{ss}
				</div>
				<div style={{fontFamily: heading(fonts), fontWeight: 800, fontStyle: 'italic', fontSize: 30 * u, color: '#9fb6ff', letterSpacing: 2}}>{label}</div>
			</div>
		</div>
	);
};

/** Documento / contrato que se completa con checks (dejar por escrito). props: title, items[], y, sign */
export const ContractDoc: React.FC<G & {title?: string; items: string[]; y?: number; every?: number; sign?: boolean; delays?: number[]}> = ({dur, title = 'ACUERDO DE SERVICIO', items, y = 0.3, every = 14, sign = true, delays}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 15, stiffness: 140}});
	const W = width * 0.74;
	const last = (delays?.[items.length - 1] ?? 8 + (items.length - 1) * every) + 14;
	const sigD = `M ${30 * u} ${50 * u} C ${70 * u} ${0} ${90 * u} ${90 * u} ${130 * u} ${40 * u} S ${200 * u} ${20 * u} ${230 * u} ${55 * u} S ${300 * u} ${30 * u} ${330 * u} ${45 * u}`;
	const sp = interpolate(frame, [last, last + 18], [0, 1], clamp);
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: `translateY(-50%) translateY(${(1 - s) * 120 * u}px) rotate(${(1 - s) * 6 + 1.5}deg)`, opacity: out * s}}>
			<div style={{background: '#fff', borderRadius: 18 * u, padding: `${36 * u}px ${40 * u}px`, boxShadow: '0 40px 100px rgba(0,0,0,.55)'}}>
				<div style={{fontFamily: heading(fonts), fontWeight: 900, fontSize: 40 * u, color: DEEP, letterSpacing: 2, borderBottom: `${4 * u}px solid ${GOLD}`, paddingBottom: 12 * u, marginBottom: 18 * u}}>{title}</div>
				{items.map((it, i) => {
					const st = delays?.[i] ?? 8 + i * every;
					const c = spring({frame: frame - st, fps, config: {damping: 10, stiffness: 280}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 18 * u, margin: `${14 * u}px 0`, opacity: interpolate(frame, [st - 4, st + 2], [0.25, 1], clamp)}}>
							<div style={{width: 46 * u, height: 46 * u, borderRadius: 10 * u, border: `${4 * u}px solid ${DEEP}`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00b347', fontSize: 40 * u, fontWeight: 900}}>
								<span style={{transform: `scale(${c})`}}>✓</span>
							</div>
							<div style={{fontFamily: heading(fonts), fontWeight: 700, fontSize: 38 * u, color: '#1a2340'}}>{it}</div>
						</div>
					);
				})}
				{sign && (
					<svg width={360 * u} height={90 * u} style={{marginTop: 10 * u}}>
						<path d={sigD} fill="none" stroke={DEEP} strokeWidth={5 * u} strokeLinecap="round" {...evolvePath(sp, sigD)} />
					</svg>
				)}
			</div>
		</div>
	);
};

/** Pila de tareas que se duplica (contratar no resuelve). props: items[], y, every */
export const TaskPile: React.FC<G & {items: string[]; y?: number; every?: number; title?: string}> = ({dur, items, y = 0.3, every = 6, title}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const W = width * 0.7;
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: 'translateY(-50%)', opacity: out}}>
			{title && <div style={{fontFamily: heading(fonts), fontWeight: 900, fontStyle: 'italic', fontSize: 56 * u, color: '#fff', textAlign: 'center', marginBottom: 16 * u}}>{title}</div>}
			<div style={{position: 'relative', height: 120 * u + items.length * 34 * u}}>
				{items.map((it, i) => {
					const s = spring({frame: frame - i * every, fps, config: {damping: 11, stiffness: 200}});
					const yy = (items.length - 1 - i) * 34 * u;
					return (
						<div key={i} style={{position: 'absolute', left: 0, right: 0, top: yy, transform: `translateY(${(1 - s) * -500 * u}px) rotate(${(random(`tp${i}`) - 0.5) * 7}deg)`, background: i % 2 ? '#fff7d6' : '#ffffff', borderRadius: 16 * u, padding: `${18 * u}px ${24 * u}px`, boxShadow: '0 12px 30px rgba(0,0,0,.35)', display: 'flex', alignItems: 'center', gap: 16 * u, fontFamily: heading(fonts), fontWeight: 800, fontSize: 34 * u, color: '#1a2340'}}>
							<span style={{width: 34 * u, height: 34 * u, borderRadius: 8 * u, border: `${4 * u}px solid ${DEEP}`}} />
							{it}
						</div>
					);
				})}
			</div>
		</div>
	);
};

/** Corchetes de enfoque alrededor de una zona (p.ej. el rostro) SIN taparla. props: x, y, w, h, label */
export const FocusBrackets: React.FC<G & {x?: number; y?: number; w?: number; h?: number; label?: string}> = ({dur, x = 0.5, y = 0.2, w = 0.5, h = 0.26, label}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const p = interpolate(frame, [0, 12], [1.25, 1], {...clamp, easing: EASE.out});
	const W = w * width * p;
	const H = h * height * p;
	const L = 70 * u;
	const corner = (r: number) => {
		const cx = x * width + (r % 2 ? 1 : -1) * W / 2;
		const cy = y * height + (r > 1 ? 1 : -1) * H / 2;
		const sx = r % 2 ? -1 : 1;
		const sy = r > 1 ? -1 : 1;
		return <path key={r} d={`M ${cx} ${cy + sy * L} L ${cx} ${cy} L ${cx + sx * L} ${cy}`} fill="none" stroke={GOLD} strokeWidth={7 * u} strokeLinecap="round" style={{filter: `drop-shadow(0 0 ${8 * u}px ${GOLD})`}} />;
	};
	const scan = ((frame * 2.2) % 100) / 100;
	return (
		<div style={{position: 'absolute', inset: 0, opacity: out * interpolate(frame, [0, 6], [0, 1], clamp)}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
				{[0, 1, 2, 3].map(corner)}
				<line x1={x * width - W / 2 + 10 * u} x2={x * width + W / 2 - 10 * u} y1={y * height - H / 2 + H * scan} y2={y * height - H / 2 + H * scan} stroke={hexA(GOLD, 0.35)} strokeWidth={2 * u} />
			</svg>
			{label && <div style={{position: 'absolute', left: x * width - W / 2, top: y * height + H / 2 + 12 * u, fontFamily: heading(fonts), fontWeight: 800, fontStyle: 'italic', fontSize: 32 * u, color: '#1a1100', background: GOLD, padding: `${4 * u}px ${16 * u}px`, borderRadius: 8 * u}}>{label}</div>}
		</div>
	);
};

/** Explosión de emojis/íconos (aplausos, corazones, likes). props: emoji, count, x, y */
export const EmojiBurst: React.FC<G & {emoji?: string; count?: number; x?: number; y?: number; spread?: number}> = ({dur, emoji = '👏', count = 14, x = 0.5, y = 0.35, spread = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	return (
		<>
			{Array.from({length: count}, (_, i) => {
				const t = (frame - i * 1.5) / fps;
				if (t < 0) return null;
				const a = random(`ea${i}`) * Math.PI * 2;
				const v = (300 + random(`ev${i}`) * 500) * u * spread;
				const xx = x * width + Math.cos(a) * v * t;
				const yy = y * height + Math.sin(a) * v * t * 0.7 + 600 * u * t * t;
				const o = interpolate(t, [0, 0.1, dur / fps - 0.3, dur / fps], [0, 1, 1, 0], clamp);
				return <div key={i} style={{position: 'absolute', left: xx, top: yy, fontSize: (50 + random(`es${i}`) * 40) * u, transform: `translate(-50%,-50%) rotate(${t * 200 * (i % 2 ? 1 : -1)}deg)`, opacity: o}}>{emoji}</div>;
			})}
		</>
	);
};

/** Grilla de posteos clonados (IA/plantillas) donde uno se distingue en dorado con la foto real. props: avatar, highlightAt, cols, rows, y, label */
export const CloneGrid: React.FC<G & {avatar?: string; highlightAt?: number; cols?: number; rows?: number; y?: number; label?: string; tags?: string[]; w?: number}> = ({dur, avatar, highlightAt = 40, cols = 3, rows = 3, y = 0.27, label = 'TÚ', tags = ['IA', 'PLANTILLA', 'FÓRMULA'], w = 0.72}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur);
	const W = width * w;
	const cw = W / cols;
	const ch = cw * 1.12;
	const H = ch * rows;
	const hiIdx = Math.floor(cols * rows / 2) + (cols % 2 ? 0 : -1);
	const hs = spring({frame: frame - highlightAt, fps, config: {damping: 12, stiffness: 170}});
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height - H / 2, width: W, height: H, opacity: out}}>
			{Array.from({length: cols * rows}, (_, i) => {
				const r = Math.floor(i / cols);
				const c = i % cols;
				const s = spring({frame: frame - (r * cols + c) * 1.6, fps, config: {damping: 14, stiffness: 200}});
				const hi = i === hiIdx;
				const dim = frame >= highlightAt && !hi ? 1 - 0.55 * hs : 1;
				return (
					<div key={i} style={{position: 'absolute', left: c * cw + 8 * u, top: r * ch + 8 * u, width: cw - 16 * u, height: ch - 16 * u, borderRadius: 20 * u, overflow: 'hidden', transform: `scale(${s * (hi ? 1 + 0.18 * hs : 1)})`, zIndex: hi ? 2 : 1, opacity: dim, background: hi && frame >= highlightAt ? `linear-gradient(160deg, #ffe08a, ${GOLD})` : 'rgba(225,232,255,.92)', boxShadow: hi && frame >= highlightAt ? `0 0 ${50 * u * hs}px ${hexA(GOLD, 0.8)}` : '0 10px 24px rgba(0,0,0,.3)'}}>
						{hi && frame >= highlightAt && avatar ? (
							<Img src={src(avatar)!} style={{width: '100%', height: '78%', objectFit: 'cover', opacity: hs}} />
						) : (
							<div style={{margin: 14 * u, height: '52%', borderRadius: 12 * u, background: 'rgba(110,130,180,.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 50 * u, color: 'rgba(60,80,140,.6)'}}>🤖</div>
						)}
						<div style={{margin: `${8 * u}px ${14 * u}px`, fontFamily: heading(fonts), fontWeight: 900, fontSize: 24 * u, color: hi && frame >= highlightAt ? '#1a1100' : '#4a5b8a', textAlign: 'center'}}>{hi && frame >= highlightAt ? label : tags[i % tags.length]}</div>
					</div>
				);
			})}
		</div>
	);
};
