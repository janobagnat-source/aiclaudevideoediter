// AD07 (miedo a dar seguimiento) — interfaces propias de este ad.
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
const Cursor: React.FC<{x: number; y: number; u: number; press?: number}> = ({x, y, u, press = 1}) => (
	<svg width={64 * u} height={64 * u} viewBox="0 0 24 24" style={{position: 'absolute', left: x, top: y, transform: `scale(${press})`, filter: 'drop-shadow(0 4px 8px rgba(0,0,0,.5))'}}>
		<path d="M4 2l15 8.5-6.6 1.5 3.8 7.2-2.9 1.5-3.8-7.3L4 18z" fill="#fff" stroke="#020617" strokeWidth={1.2} />
	</svg>
);

/** Borrador escrito que nunca se envía: el cursor se acerca al botón y se arrepiente. */
export const DraftUnsent: React.FC<G & {text: string; y?: number; days?: string}> = ({dur, text, y = 0.6, days = 'hace 3 días'}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const n = Math.floor(interpolate(f, [4, 40], [0, text.length], clamp));
	const top = y * height;
	const btnX = (width + W) / 2 - 110 * u;
	const btnY = top + 250 * u;
	// el cursor va y vuelve dos veces
	const c = (Math.sin(Math.max(0, f - 44) / 9) * 0.5 + 0.5) * (f > 44 ? 1 : 0);
	const cx = btnX + 90 * u - c * 60 * u;
	const cy = btnY + 120 * u - c * 90 * u;
	const near = c > 0.85;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top, width: W}}>
				<div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 12 * u}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 6 * u, color: 'rgba(255,255,255,.6)'}}>BORRADOR · SIN ENVIAR</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, color: RED}}>{days}</span>
				</div>
				<div style={{borderRadius: 30 * u, ...glass(u, 0.85), padding: `${26 * u}px ${30 * u}px`, display: 'flex', alignItems: 'flex-end', gap: 18 * u, minHeight: 220 * u}}>
					<div style={{flex: 1, fontFamily: fonts.body, fontSize: 38 * u, color: '#fff', lineHeight: 1.3}}>
						{text.slice(0, n)}
						{n < text.length && <span style={{color: GOLD}}>|</span>}
					</div>
					<div style={{width: 96 * u, height: 96 * u, borderRadius: '50%', background: near ? GOLD : 'rgba(255,187,0,.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 46 * u, color: '#020617', transform: `scale(${near ? 1.08 : 1})`, flexShrink: 0}}>➤</div>
				</div>
			</div>
			{f > 44 && <Cursor x={cx} y={cy} u={u} />}
		</AbsoluteFill>
	);
};

/** Pensamientos que flotan (nubes difusas) uno tras otro. */
export const ThoughtBubbles: React.FC<G & {items: {text: string; at: number}[]; y?: number}> = ({dur, items, y = 0.76}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{items.map((it, i) => {
				const p = spring({frame: f - it.at, fps, config: {stiffness: 120, damping: 16}});
				const drift = Math.sin((f + i * 30) / 22) * 8 * u;
				return (
					<div key={i} style={{position: 'absolute', left: i % 2 ? width * 0.2 : width * 0.06, right: i % 2 ? width * 0.06 : width * 0.2, top: y * height + i * 130 * u + drift, opacity: f >= it.at ? p : 0, transform: `scale(${0.8 + 0.2 * p})`, filter: `blur(${(1 - p) * 10}px)`}}>
						<div style={{borderRadius: 60 * u, background: 'rgba(225,232,255,.92)', padding: `${22 * u}px ${32 * u}px`, fontFamily: fonts.heading, fontWeight: 800, fontStyle: 'italic', fontSize: 40 * u, color: '#0a1440', boxShadow: `0 ${16 * u}px ${40 * u}px rgba(0,0,0,.35)`}}>{it.text}</div>
						<div style={{width: 30 * u, height: 30 * u, borderRadius: '50%', background: 'rgba(225,232,255,.9)', marginLeft: i % 2 ? 'auto' : 60 * u, marginRight: i % 2 ? 60 * u : undefined, marginTop: 8 * u}} />
						<div style={{width: 16 * u, height: 16 * u, borderRadius: '50%', background: 'rgba(225,232,255,.85)', marginLeft: i % 2 ? 'auto' : 40 * u, marginRight: i % 2 ? 40 * u : undefined, marginTop: 6 * u}} />
					</div>
				);
			})}
		</AbsoluteFill>
	);
};

/** Invitación de calendario que se completa campo a campo y se acepta. */
export const CalendarInvite: React.FC<G & {title: string; when: string; agenda: string; whenAt?: number; agendaAt?: number; okAt?: number; y?: number}> = ({dur, title, when, agenda, whenAt = 30, agendaAt = 60, okAt = 90, y = 0.58}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const sp = spring({frame: f, fps, config: {stiffness: 170, damping: 18}});
	const field = (k: string, v: string, at: number) => {
		const p = interpolate(f, [at, at + 12], [0, 1], clamp);
		return (
			<div style={{display: 'flex', gap: 18 * u, padding: `${14 * u}px 0`, borderTop: '1px solid rgba(10,20,64,.08)'}}>
				<span style={{width: 150 * u, fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 3 * u, color: '#5a6690'}}>{k}</span>
				<span style={{flex: 1, fontFamily: fonts.heading, fontWeight: 800, fontSize: 32 * u, color: '#0a1440', clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}}>{v}</span>
			</div>
		);
	};
	const ok = spring({frame: f - okAt, fps, config: {stiffness: 260, damping: 14}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 28 * u, background: '#f6f7fb', overflow: 'hidden', boxShadow: `0 ${30 * u}px ${70 * u}px rgba(0,0,0,.5)`, transform: `translateY(${(1 - sp) * 100 * u}px)`}}>
				<div style={{background: 'linear-gradient(90deg,#0034B7,#3474FF)', padding: `${20 * u}px ${28 * u}px`, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 26 * u, letterSpacing: 4 * u, color: '#fff'}}>📅 INVITACIÓN</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 22 * u, color: 'rgba(255,255,255,.8)'}}>ACORDADO EN LA LLAMADA</span>
				</div>
				<div style={{padding: `${18 * u}px ${28 * u}px ${24 * u}px`}}>
					<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 40 * u, color: '#0a1440', marginBottom: 6 * u}}>{title}</div>
					{field('CUÁNDO', when, whenAt)}
					{field('REVISAREMOS', agenda, agendaAt)}
					<div style={{display: 'inline-block', marginTop: 12 * u, borderRadius: 999, background: hexA('#0b8a3a', 0.12), border: `${2 * u}px solid #0b8a3a`, padding: `${8 * u}px ${20 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 26 * u, color: '#0b6a2e', transform: `scale(${ok})`, opacity: f >= okAt ? 1 : 0}}>✓ ACEPTADO POR AMBOS</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Nota de la llamada (CRM) con un resaltador que marca lo que le importaba. */
export const NoteRecall: React.FC<G & {note: string; mark: string; y?: number; markAt?: number}> = ({dur, note, mark, y = 0.76, markAt = 20}) => {
	const {f, v} = useIO(dur, 10, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.86;
	const p = interpolate(f, [markAt, markAt + 14], [0, 1], {...clamp, easing: EASE.out});
	const i = note.indexOf(mark);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 24 * u, background: '#fff8dc', padding: `${22 * u}px ${28 * u}px`, boxShadow: `0 ${22 * u}px ${50 * u}px rgba(0,0,0,.45)`, transform: `rotate(-1deg) translateY(${(1 - v) * 40 * u}px)`}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 20 * u, letterSpacing: 5 * u, color: '#8a6d1a'}}>NOTAS DE LA LLAMADA</div>
				<div style={{fontFamily: fonts.body, fontWeight: 600, fontSize: 34 * u, color: '#2a2210', lineHeight: 1.35, marginTop: 8 * u}}>
					{i >= 0 ? note.slice(0, i) : note}
					{i >= 0 && (
						<span style={{backgroundImage: `linear-gradient(90deg, ${hexA(GOLD, 0.85)} 0%, ${hexA(GOLD, 0.85)} 100%)`, backgroundSize: `${p * 100}% 70%`, backgroundRepeat: 'no-repeat', backgroundPosition: '0 85%', fontWeight: 800}}>{mark}</span>
					)}
					{i >= 0 ? note.slice(i + mark.length) : ''}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** El mensaje correcto: se escribe, se envía (✓✓) y el cliente empieza a responder. */
export const SendFlow: React.FC<G & {lines: {text: string; at: number}[]; sendAt?: number; replyAt?: number; reply?: string; y?: number}> = ({dur, lines, sendAt = 120, replyAt = 140, reply = '¡Sí! Me sirve mucho 🙌', y = 0.58}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const sent = f >= sendAt;
	const fly = spring({frame: f - sendAt, fps, config: {stiffness: 200, damping: 18}});
	const rp = spring({frame: f - replyAt, fps, config: {stiffness: 200, damping: 17}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, display: 'flex', flexDirection: 'column', gap: 14 * u}}>
				<div style={{alignSelf: 'flex-end', maxWidth: W * 0.88, borderRadius: `${30 * u}px ${30 * u}px ${8 * u}px ${30 * u}px`, background: sent ? `linear-gradient(135deg, ${GOLD}, #f0a400)` : 'rgba(255,255,255,.1)', border: sent ? 'none' : `${2 * u}px dashed rgba(255,255,255,.35)`, padding: `${22 * u}px ${28 * u}px`, transform: `translateY(${sent ? (1 - fly) * 30 * u : 0}px)`}}>
					{lines.map((l, i) => {
						const n = Math.floor(interpolate(f, [l.at, l.at + l.text.length * 0.9], [0, l.text.length], clamp));
						return <div key={i} style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 36 * u, color: sent ? '#020617' : '#fff', lineHeight: 1.3}}>{l.text.slice(0, n)}</div>;
					})}
					{sent && <div style={{textAlign: 'right', fontFamily: fonts.body, fontSize: 22 * u, color: '#0b3bd6'}}>Enviado ✓✓</div>}
				</div>
				<div style={{alignSelf: 'flex-start', borderRadius: `${30 * u}px ${30 * u}px ${30 * u}px ${8 * u}px`, background: '#eef1fb', padding: `${20 * u}px ${28 * u}px`, opacity: f >= replyAt ? rp : 0, transform: `scale(${0.9 + 0.1 * rp})`, transformOrigin: 'left bottom'}}>
					<div style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 34 * u, color: '#0a1440'}}>{reply}</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};
