// AD03 (seguidores vs ventas) — interfaces propias de este ad.
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
const fmt = (n: number) => (n >= 1000 ? `${(n / 1000).toLocaleString('es-AR', {maximumFractionDigits: 1})} mil` : `${Math.round(n)}`);
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

/** Feed de otras cuentas que crecen (scroll infinito con likes disparándose) y al final tu tarjeta de ventas en 0. */
export const FeedScroll: React.FC<G & {y?: number; h?: number; youAt?: number}> = ({dur, y = 0.555, h = 0.42, youAt = 110}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const H = height * h;
	const W = width * 0.9;
	const cardH = 210 * u;
	const scroll = interpolate(f, [0, youAt], [0, cardH * 5.2], {...clamp, easing: EASE.inOut});
	const names = ['@marca.exitosa', '@coach.top', '@emprende.ya', '@negocio.viral', '@lider.digital', '@growth.pro', '@ventas.max'];
	const you = spring({frame: f - youAt, fps, config: {stiffness: 200, damping: 16}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, height: H, overflow: 'hidden', borderRadius: 30 * u, WebkitMaskImage: 'linear-gradient(transparent, black 12%, black 88%, transparent)'}}>
				<div style={{transform: `translateY(${-scroll}px)`}}>
					{names.map((n, i) => {
						const likes = 1200 * (i + 1) + f * (180 + i * 90);
						return (
							<div key={n} style={{height: cardH - 18 * u, marginBottom: 18 * u, borderRadius: 26 * u, ...glass(u, 0.6), display: 'flex', alignItems: 'center', gap: 22 * u, padding: `0 ${26 * u}px`}}>
								<div style={{width: 96 * u, height: 96 * u, borderRadius: '50%', background: `linear-gradient(135deg, hsl(${200 + i * 25},80%,60%), hsl(${260 + i * 20},70%,45%))`, border: `${3 * u}px solid rgba(255,255,255,.4)`}} />
								<div style={{flex: 1}}>
									<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: '#fff'}}>{n}</div>
									<div style={{display: 'flex', gap: 24 * u, marginTop: 8 * u, fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, color: 'rgba(255,255,255,.75)', fontVariantNumeric: 'tabular-nums'}}>
										<span>♥ {fmt(likes)}</span>
										<span style={{color: GREEN}}>▲ {fmt(likes * 3.1)} seguidores</span>
									</div>
								</div>
							</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 20 * u, height: cardH * 1.05, borderRadius: 26 * u, background: 'linear-gradient(160deg, rgba(40,10,20,.92), rgba(10,4,20,.95))', border: `${2.5 * u}px solid ${RED}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: `0 ${34 * u}px`, transform: `translateY(${(1 - you) * cardH * 1.4}px)`, opacity: you}}>
					<div>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 6 * u, color: 'rgba(255,255,255,.6)'}}>TU NEGOCIO · HOY</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 54 * u, color: '#fff'}}>VENTAS</div>
					</div>
					<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 120 * u, color: RED, fontVariantNumeric: 'tabular-nums'}}>0</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Comparación ELLOS vs TÚ en la franja baja: barras horizontales con el signo de pregunta. */
export const VersusBar: React.FC<G & {a?: string; b?: string; y?: number}> = ({dur, a = 'ELLOS', b = 'YO', y = 0.8}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.84;
	const pa = interpolate(f, [6, 34], [0, 1], {...clamp, easing: EASE.out});
	const pb = interpolate(f, [12, 40], [0, 0.18], {...clamp, easing: EASE.out});
	const q = spring({frame: f - 44, fps, config: {stiffness: 240, damping: 12}});
	const row = (label: string, p: number, col: string, n: string) => (
		<div style={{display: 'flex', alignItems: 'center', gap: 20 * u, marginBottom: 18 * u}}>
			<span style={{width: 130 * u, fontFamily: fonts.heading, fontWeight: 900, fontSize: 32 * u, letterSpacing: 3 * u, color: '#fff'}}>{label}</span>
			<div style={{flex: 1, height: 44 * u, borderRadius: 12 * u, background: 'rgba(255,255,255,.08)', overflow: 'hidden'}}>
				<div style={{height: '100%', width: `${p * 100}%`, background: col, borderRadius: 12 * u, boxShadow: `0 0 ${18 * u}px ${hexA(col, 0.6)}`}} />
			</div>
			<span style={{width: 120 * u, textAlign: 'right', fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, color: col, fontVariantNumeric: 'tabular-nums'}}>{n}</span>
		</div>
	);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, opacity: v, transform: `translateY(${(1 - v) * 40 * u}px)`}}>
				{row(a, pa, GREEN, `${Math.round(248 * pa)}K`)}
				{row(b, pb, '#9fb6ff', `${Math.round(45 * pb / 0.18)}`)}
			</div>
			<div style={{position: 'absolute', right: width * 0.05, top: y * height - 90 * u, fontFamily: fonts.heading, fontWeight: 900, fontSize: 130 * u, color: GOLD, transform: `scale(${q}) rotate(${(1 - q) * 30}deg)`, textShadow: `0 0 ${30 * u}px ${hexA(GOLD, 0.6)}`}}>?</div>
		</AbsoluteFill>
	);
};

/** Auditoría de tu contenido: grilla de 6 publicaciones; una línea de escaneo pasa y marca CLARO / CONFUSO. */
export const AuditGrid: React.FC<G & {y?: number; verdicts?: boolean[]; title?: string; scanAt?: number}> = ({dur, y = 0.575, verdicts = [false, true, false, false, true, false], title = 'REVISA TU CONTENIDO', scanAt = 20}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const cell = (W - 2 * 18 * u) / 3;
	const scanY = interpolate(f, [scanAt, scanAt + 50], [0, cell * 2 + 18 * u], {...clamp, easing: EASE.inOut});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 8 * u, color: GOLD, marginBottom: 16 * u}}>{title}</div>
				<div style={{position: 'relative', display: 'grid', gridTemplateColumns: `repeat(3, ${cell}px)`, gap: 18 * u}}>
					{verdicts.map((ok, i) => {
						const r = Math.floor(i / 3);
						const pin = spring({frame: f - i * 3, fps, config: {stiffness: 220, damping: 18}});
						const judged = scanY > r * (cell + 18 * u) + cell * 0.6;
						return (
							<div key={i} style={{width: cell, height: cell, borderRadius: 20 * u, overflow: 'hidden', position: 'relative', transform: `scale(${pin})`, background: `linear-gradient(${120 + i * 40}deg, hsl(${215 + i * 9},60%,${22 + (i % 3) * 6}%), hsl(${230 + i * 12},70%,12%))`, border: `${2 * u}px solid ${judged ? (ok ? GREEN : RED) : 'rgba(255,255,255,.12)'}`}}>
								<div style={{position: 'absolute', left: 18 * u, right: 18 * u, top: 20 * u, height: 12 * u, borderRadius: 6 * u, background: 'rgba(255,255,255,.35)'}} />
								<div style={{position: 'absolute', left: 18 * u, width: '55%', top: 44 * u, height: 10 * u, borderRadius: 6 * u, background: 'rgba(255,255,255,.2)'}} />
								{judged && (
									<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, padding: `${10 * u}px 0`, textAlign: 'center', background: ok ? hexA(GREEN, 0.9) : hexA(RED, 0.9), fontFamily: fonts.heading, fontWeight: 900, fontSize: 24 * u, letterSpacing: 3 * u, color: '#020617'}}>{ok ? '✓ CLARO' : '✗ CONFUSO'}</div>
								)}
							</div>
						);
					})}
					{f >= scanAt && f <= scanAt + 54 && <div style={{position: 'absolute', left: -10 * u, right: -10 * u, top: scanY, height: 4 * u, background: GOLD, boxShadow: `0 0 ${26 * u}px ${GOLD}, 0 0 ${60 * u}px ${hexA(GOLD, 0.6)}`}} />}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** Visor de cámara REC (esquinas, punto rojo, timecode) en los bordes — nunca sobre la cara. */
export const RecFrame: React.FC<G & {label?: string}> = ({dur, label = 'TU PRÓXIMO VIDEO'}) => {
	const {f, v} = useIO(dur, 8, 8);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const m = 46 * u;
	const L = 90 * u;
	const s = `${4 * u}px solid rgba(255,255,255,.9)`;
	const secs = Math.floor(f / fps);
	const corner = (st: React.CSSProperties) => <div style={{position: 'absolute', width: L, height: L, ...st}} />;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: v}}>
			{corner({left: m, top: m, borderLeft: s, borderTop: s})}
			{corner({right: m, top: m, borderRight: s, borderTop: s})}
			{corner({left: m, bottom: m + height * 0.25, borderLeft: s, borderBottom: s})}
			{corner({right: m, bottom: m + height * 0.25, borderRight: s, borderBottom: s})}
			<div style={{position: 'absolute', left: m + 26 * u, top: m + 24 * u, display: 'flex', alignItems: 'center', gap: 12 * u, fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: '#fff'}}>
				<div style={{width: 22 * u, height: 22 * u, borderRadius: '50%', background: RED, opacity: Math.floor(f / 12) % 2 ? 1 : 0.25}} />
				REC
			</div>
			<div style={{position: 'absolute', right: m + 26 * u, top: m + 26 * u, fontFamily: fonts.heading, fontWeight: 700, fontSize: 28 * u, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>00:00:{String(12 + secs).padStart(2, '0')}</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: m + 80 * u, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 10 * u, color: GOLD}}>{label}</div>
		</AbsoluteFill>
	);
};

/** Pregunta frecuente de un cliente (globo de comentario) en la franja baja. */
export const FAQBubble: React.FC<G & {question: string; who?: string; y?: number; tag?: string}> = ({dur, question, who = 'Cliente potencial', y = 0.8, tag = 'DUDA ANTES DE CONTRATARTE'}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.84;
	const p = spring({frame: f, fps, config: {stiffness: 190, damping: 17}});
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, opacity: v, transform: `translateY(${(1 - p) * 80 * u}px)`}}>
				<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 24 * u, letterSpacing: 6 * u, color: GOLD, marginBottom: 12 * u}}>{tag}</div>
				<div style={{position: 'relative', borderRadius: 30 * u, background: '#f5f7ff', padding: `${26 * u}px ${32 * u}px`, boxShadow: `0 ${24 * u}px ${60 * u}px rgba(0,0,0,.45)`}}>
					<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 22 * u, color: '#5a6690', marginBottom: 6 * u}}>{who}</div>
					<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 40 * u, color: '#0a1440', lineHeight: 1.15}}>{question}</div>
					<div style={{position: 'absolute', left: 50 * u, bottom: -22 * u, width: 0, height: 0, borderLeft: `${22 * u}px solid transparent`, borderRight: `${22 * u}px solid transparent`, borderTop: `${24 * u}px solid #f5f7ff`}} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** APLAUSOS vs UNA CONVERSACIÓN: lo que vale cada uno (panel inferior del split). */
export const ValueCompare: React.FC<G & {y?: number; dmAt?: number; compareAt?: number; avatar?: string}> = ({dur, y = 0.575, dmAt = 6, compareAt = 70, avatar}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * 0.88;
	const dm = spring({frame: f - dmAt, fps, config: {stiffness: 200, damping: 17}});
	const cp = interpolate(f, [compareAt, compareAt + 14], [0, 1], {...clamp, easing: EASE.out});
	const claps = Math.round(interpolate(f, [compareAt, compareAt + 30], [0, 1204], clamp));
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W}}>
				<div style={{borderRadius: 28 * u, ...glass(u, 0.8), padding: 26 * u, transform: `translateY(${(1 - dm) * 70 * u}px)`, opacity: dm}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 16 * u}}>
						<div style={{width: 64 * u, height: 64 * u, borderRadius: '50%', overflow: 'hidden', background: 'linear-gradient(135deg,#3474FF,#0034B7)'}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
						<div>
							<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, color: '#fff'}}>Nuevo mensaje</div>
							<div style={{fontFamily: fonts.body, fontSize: 28 * u, color: 'rgba(255,255,255,.85)'}}>“Vi tu video. ¿Podemos hablar de mi caso?”</div>
						</div>
					</div>
					<div style={{marginTop: 14 * u, display: 'inline-block', borderRadius: 999, background: hexA(GOLD, 0.18), border: `${2 * u}px solid ${GOLD}`, padding: `${6 * u}px ${18 * u}px`, fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: GOLD}}>CONVERSACIÓN COMERCIAL</div>
				</div>
				<div style={{display: 'flex', gap: 18 * u, marginTop: 22 * u, opacity: cp, transform: `translateY(${(1 - cp) * 30 * u}px)`}}>
					<div style={{flex: 1, borderRadius: 24 * u, ...glass(u, 0.6), padding: 24 * u}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: 'rgba(255,255,255,.6)'}}>APLAUSOS</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 56 * u, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>👏 {claps.toLocaleString('es-AR')}</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: RED}}>= $ 0</div>
					</div>
					<div style={{flex: 1, borderRadius: 24 * u, background: `linear-gradient(160deg, ${hexA(GOLD, 0.25)}, rgba(4,10,40,.85))`, border: `${2 * u}px solid ${GOLD}`, padding: 24 * u}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 22 * u, letterSpacing: 4 * u, color: GOLD}}>1 CONVERSACIÓN</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 56 * u, color: '#fff'}}>💬 1</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: GREEN}}>= un cliente</div>
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};
