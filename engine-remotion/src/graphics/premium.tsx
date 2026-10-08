// Motion graphics premium (estilo Carlos Buelvas / referencia): badges dorados, titulares en bloque,
// escenas de marca, perfil de Instagram, conceptos animados. Todo deriva de useCurrentFrame().
import {fitText} from '@remotion/layout-utils';
import {evolvePath} from '@remotion/paths';
import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';

type G = {dur: number};
const src = (s?: string | null) => (!s ? undefined : s.startsWith('http') ? s : staticFile(s));
const useU = () => {
	const {width, height} = useVideoConfig();
	return Math.min(width, height) / 1080;
};
const GOLD = '#FFBB00';
const gold = (c?: string) => c ?? GOLD;

/** Salida estándar suave (escala + blur) en los últimos `n` frames. */
const useOut = (dur: number, n = 8) => {
	const frame = useCurrentFrame();
	return interpolate(frame, [dur - n, dur], [1, 0], {...clamp, easing: EASE.in});
};

// ---------------------------------------------------------------------------------------------
/** Badge circular dorado de la referencia: anillo fino blanco + arco dorado + icono con glow + línea punteada.
 * props: icon (svg), x, y (centro 0-1), size, leader 'left'|'right'|'none', leaderLen (px), label */
export const IconBadge: React.FC<G & {icon: string; x?: number; y?: number; size?: number; leader?: 'left' | 'right' | 'none'; leaderLen?: number; label?: string; labelSide?: 'below' | 'left' | 'right'}> = ({
	dur,
	icon,
	x = 0.78,
	y = 0.55,
	size = 1,
	leader = 'left',
	leaderLen = 150,
	label,
	labelSide = 'below',
}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const S = 190 * u * size;
	const s = spring({frame, fps, config: {damping: 13, stiffness: 160, mass: 0.8}});
	const ring = interpolate(frame, [0, 16], [0, 1], {...clamp, easing: EASE.out});
	const arc = interpolate(frame, [6, 30], [0, 0.28], {...clamp, easing: EASE.out});
	const dash = interpolate(frame, [8, 22], [0, 1], {...clamp, easing: EASE.out});
	const out = useOut(dur, 9);
	const glow = 0.75 + 0.25 * Math.sin(frame / 6);
	const R = S / 2 - 4 * u;
	const C = 2 * Math.PI * R;
	const L = leaderLen * u;
	const cx = x * width;
	const cy = y * height;
	return (
		<div style={{position: 'absolute', left: cx - S / 2, top: cy - S / 2, width: S, height: S, opacity: out, transform: `scale(${(0.55 + 0.45 * s) * (0.9 + 0.1 * out)})`, filter: `blur(${(1 - out) * 6}px)`}}>
			{leader !== 'none' && (
				<div style={{position: 'absolute', top: S / 2 - 1.5 * u, [leader === 'left' ? 'right' : 'left']: S + 6 * u, width: L * dash, height: 3 * u, backgroundImage: `linear-gradient(90deg, rgba(255,255,255,.85) 50%, transparent 50%)`, backgroundSize: `${16 * u}px 100%`, transform: leader === 'left' ? 'scaleX(-1)' : undefined, transformOrigin: leader === 'left' ? 'right' : 'left'}} />
			)}
			<svg width={S} height={S} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<defs>
					<linearGradient id="bgArc" x1="0" y1="0" x2="1" y2="1">
						<stop offset="0" stopColor="#fff2b8" />
						<stop offset="1" stopColor={GOLD} />
					</linearGradient>
				</defs>
				<circle cx={S / 2} cy={S / 2} r={R} fill={hexA('#0a1230', 0.18)} stroke="rgba(255,255,255,.92)" strokeWidth={3.2 * u} strokeDasharray={C} strokeDashoffset={C * (1 - ring)} transform={`rotate(-90 ${S / 2} ${S / 2})`} />
				<circle cx={S / 2} cy={S / 2} r={R} fill="none" stroke="url(#bgArc)" strokeWidth={7 * u} strokeLinecap="round" strokeDasharray={`${C * arc} ${C}`} transform={`rotate(${90 + frame * 1.2} ${S / 2} ${S / 2})`} style={{filter: `drop-shadow(0 0 ${8 * u}px ${GOLD})`}} />
			</svg>
			<div
				style={{
					position: 'absolute',
					left: S * 0.27,
					top: S * 0.27,
					width: S * 0.46,
					height: S * 0.46,
					background: `linear-gradient(160deg, #ffffff 0%, #ffe9a6 35%, ${GOLD} 100%)`,
					WebkitMaskImage: `url(${src(icon)})`,
					WebkitMaskSize: 'contain',
					WebkitMaskRepeat: 'no-repeat',
					WebkitMaskPosition: 'center',
					filter: `drop-shadow(0 0 ${14 * u * glow}px ${hexA(GOLD, 0.9)}) drop-shadow(0 0 ${30 * u * glow}px ${hexA(GOLD, 0.45)})`,
					transform: `scale(${interpolate(frame, [4, 16], [0.4, 1], {...clamp, easing: EASE.punch})}) rotate(${interpolate(frame, [4, 16], [-25, 0], clamp)}deg)`,
				}}
			/>
			{label && (
				<div
					style={{
						position: 'absolute',
						...(labelSide === 'below' ? {top: S + 14 * u, left: '50%', transform: `translateX(-50%) translateY(${(1 - dash) * 16}px)`} : labelSide === 'left' ? {right: S + 18 * u, top: '50%', transform: 'translateY(-50%)'} : {left: S + 18 * u, top: '50%', transform: 'translateY(-50%)'}),
						opacity: dash,
						whiteSpace: 'nowrap',
						fontFamily: `${fonts.heading}, sans-serif`,
						fontWeight: 800,
						fontStyle: 'italic',
						fontSize: 34 * u * size,
						letterSpacing: 1,
						color: colors.light,
						textTransform: 'uppercase',
						textShadow: '0 4px 16px rgba(0,0,0,.7)',
					}}
				>
					{label}
				</div>
			)}
		</div>
	);
};

// ---------------------------------------------------------------------------------------------
type Line = {text: string; color?: 'white' | 'gold' | 'blue' | 'outline' | 'green' | 'purple'; weight?: number; italic?: boolean};

/** Titular de marca: bloque justificado (cada línea al mismo ancho), blanco/amarillo, opción delineado,
 * destello en una palabra. props: lines[{text,color,weight,italic}], width (0-1), y (centro 0-1), x (centro), sparkle (índice de línea), stagger, align */
export const BlockTitle: React.FC<G & {lines: Line[]; width?: number; y?: number; x?: number; sparkle?: number | null; stagger?: number; gap?: number; shadow?: boolean; enter?: 'rise' | 'slam' | 'wipe'}> = ({
	dur,
	lines,
	width: bw = 0.82,
	y = 0.2,
	x = 0.5,
	sparkle = null,
	stagger = 4,
	gap = 0.06,
	shadow = true,
	enter = 'rise',
}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const {colors, fonts} = useBrand();
	const W = bw * width;
	const out = useOut(dur, 8);
	const sizes = lines.map((l) =>
		fitText({text: l.text, withinWidth: W, fontFamily: fonts.heading, fontWeight: l.weight ?? 900, textTransform: 'uppercase', letterSpacing: '-1px', additionalStyles: {fontStyle: l.italic === false ? 'normal' : 'italic'}}).fontSize,
	);
	const total = sizes.reduce((a, s) => a + s * 0.92, 0) + gap * 100 * (lines.length - 1);
	let acc = 0;
	const colorOf = (c?: Line['color']) => (c === 'gold' ? gold(colors.gold) : c === 'blue' ? colors.blue ?? colors.primary : c === 'green' ? colors.green ?? '#00E051' : c === 'purple' ? colors.purple ?? '#5E318E' : colors.light);
	return (
		<div style={{position: 'absolute', left: x * width - W / 2, top: y * height - total / 2, width: W, opacity: out, filter: `blur(${(1 - out) * 8}px)`}}>
			{lines.map((l, i) => {
				const f = frame - i * stagger;
				const s = spring({frame: f, fps, config: {damping: 16, stiffness: 190, mass: 0.7}});
				const top = acc;
				acc += sizes[i] * 0.92 + gap * 100;
				const outline = l.color === 'outline';
				const ty = enter === 'rise' ? (1 - s) * sizes[i] * 0.9 : 0;
				const sc = enter === 'slam' ? interpolate(s, [0, 1], [1.9, 1]) : 1;
				const clip = enter === 'wipe' ? `inset(0 ${(1 - s) * 100}% 0 0)` : enter === 'rise' ? 'inset(-20% -5% -10% -5%)' : undefined;
				return (
					<div key={i} style={{position: 'absolute', top, left: 0, width: W, height: sizes[i] * 1.0, overflow: enter === 'rise' ? 'hidden' : 'visible', clipPath: clip}}>
						<div
							style={{
								transform: `translateY(${ty}px) scale(${sc})`,
								opacity: f < 0 ? 0 : Math.min(1, s * 1.4),
								filter: [enter === 'slam' ? `blur(${interpolate(f, [0, 5], [12, 0], clamp)}px)` : '', outline ? `drop-shadow(0 0 ${sizes[i] * 0.12}px rgba(0,8,40,.9))` : ''].filter(Boolean).join(' ') || undefined,
								fontFamily: `${fonts.heading}, sans-serif`,
								fontWeight: l.weight ?? 900,
								fontStyle: l.italic === false ? 'normal' : 'italic',
								fontSize: sizes[i],
								lineHeight: 1,
								letterSpacing: '-1px',
								textTransform: 'uppercase',
								whiteSpace: 'nowrap',
								textAlign: 'center',
								color: outline ? 'transparent' : colorOf(l.color),
								WebkitTextStroke: outline ? `${Math.max(3, sizes[i] * 0.04)}px ${colors.light}` : undefined,
								textShadow: shadow && !outline ? `0 ${sizes[i] * 0.06}px ${sizes[i] * 0.25}px rgba(0,0,10,.55)${l.color === 'gold' ? `, 0 0 ${sizes[i] * 0.35}px ${hexA(GOLD, 0.35)}` : ''}` : undefined,
							}}
						>
							{l.text}
						</div>
					</div>
				);
			})}
			{sparkle !== null && sparkle !== undefined && <Sparkle x={0.92} y={(() => {
				let a = 0;
				for (let k = 0; k < sparkle; k++) a += sizes[k] * 0.92 + gap * 100;
				return (a + sizes[sparkle] * 0.15) / total;
			})()} delay={sparkle * stagger + 10} boxW={W} boxH={total} />}
		</div>
	);
};

/** Destello (máx. 2 por pieza según manual). Relativo al bloque padre. */
export const Sparkle: React.FC<{x: number; y: number; delay?: number; boxW: number; boxH: number; size?: number}> = ({x, y, delay = 0, boxW, boxH, size = 1}) => {
	const frame = useCurrentFrame();
	const u = useU();
	const f = frame - delay;
	const s = interpolate(f, [0, 6, 16], [0, 1.15, 0.85], {...clamp, easing: EASE.out});
	const S = 90 * u * size;
	return (
		<svg width={S} height={S} viewBox="-50 -50 100 100" style={{position: 'absolute', left: x * boxW - S / 2, top: y * boxH - S / 2, transform: `scale(${s}) rotate(${f * 1.5}deg)`, opacity: f < 0 ? 0 : 1, filter: `drop-shadow(0 0 ${10 * u}px #fff) drop-shadow(0 0 ${22 * u}px ${GOLD})`}}>
			<path d="M0,-50 C4,-8 8,-4 50,0 C8,4 4,8 0,50 C-4,8 -8,4 -50,0 C-8,-4 -4,-8 0,-50 Z" fill="#fff8e0" />
		</svg>
	);
};

// ---------------------------------------------------------------------------------------------
/** Fondo de escena de marca (para "b-roll" de motion graphics): degradado negro→azul, glow, túnel de luces,
 * patrón de palabra delineada, partículas y barrido de luz. props: variant 'glow'|'tunnel'|'pattern'|'image', image, word */
export const BrandScene: React.FC<G & {variant?: 'glow' | 'tunnel' | 'pattern' | 'image'; image?: string; word?: string; intensity?: number}> = ({dur, variant = 'glow', image, word = 'VENTAS', intensity = 1}) => {
	const frame = useCurrentFrame();
	const {width, height, fps} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const inO = interpolate(frame, [0, 6], [0, 1], clamp);
	const out = interpolate(frame, [dur - 6, dur], [1, 0], clamp);
	const deep = colors.blueDeep ?? '#0034B7';
	const blue = colors.blue ?? '#3474FF';
	const zoom = 1.05 + (frame / Math.max(dur, 1)) * 0.08;
	return (
		<AbsoluteFill style={{opacity: Math.min(inO, out), overflow: 'hidden', background: '#01030c'}}>
			{variant === 'image' && image ? (
				<Img src={src(image)!} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
			) : (
				<AbsoluteFill style={{background: `radial-gradient(ellipse 90% 60% at 50% ${42 + Math.sin(frame / 40) * 4}%, ${hexA(blue, 0.85 * intensity)} 0%, ${hexA(deep, 0.75)} 35%, #01040f 75%)`, transform: `scale(${zoom})`}} />
			)}
			{variant === 'tunnel' && (
				<svg width={width} height={height} style={{position: 'absolute', inset: 0, mixBlendMode: 'screen'}}>
					{Array.from({length: 26}, (_, i) => {
						const a = (i / 26) * Math.PI * 2 + frame * 0.004;
						const r0 = 40 * u;
						const r1 = Math.max(width, height) * 0.9;
						const ph = ((frame * 0.025 + random(`t${i}`)) % 1);
						const rA = r0 + (r1 - r0) * ph;
						const rB = rA + 260 * u * (0.4 + ph);
						return <line key={i} x1={width / 2 + Math.cos(a) * rA} y1={height * 0.45 + Math.sin(a) * rA} x2={width / 2 + Math.cos(a) * rB} y2={height * 0.45 + Math.sin(a) * rB} stroke={i % 3 ? blue : '#9fc0ff'} strokeWidth={(2 + 5 * ph) * u} strokeLinecap="round" opacity={0.25 + 0.6 * ph} style={{filter: `drop-shadow(0 0 ${8 * u}px ${blue})`}} />;
					})}
				</svg>
			)}
			{variant === 'pattern' && (
				<div style={{position: 'absolute', inset: '-10%', display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10 * u, transform: `rotate(-8deg) translateY(${(-frame * 1.2) % (160 * u)}px)`, opacity: 0.16}}>
					{Array.from({length: 18}, (_, i) => (
						<div key={i} style={{whiteSpace: 'nowrap', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: 150 * u, lineHeight: 1, color: 'transparent', WebkitTextStroke: `${2 * u}px #9fc0ff`, transform: `translateX(${(i % 2 ? -1 : 1) * ((frame * 2) % 400) * u}px)`}}>
							{`${word} ${word} ${word} ${word}`}
						</div>
					))}
				</div>
			)}
			{/* partículas/polvo de luz */}
			{Array.from({length: 40}, (_, i) => {
				const px = random(`px${i}`) * width;
				const py = ((random(`py${i}`) * height - frame * (0.6 + random(`v${i}`) * 1.6) * u) % height + height) % height;
				const r = (1 + random(`r${i}`) * 3) * u;
				return <div key={i} style={{position: 'absolute', left: px, top: py, width: r * 2, height: r * 2, borderRadius: '50%', background: i % 5 === 0 ? GOLD : '#bcd3ff', opacity: 0.3 + 0.5 * Math.abs(noise2D(`p${i}`, frame / 30, 0)), boxShadow: `0 0 ${r * 4}px ${i % 5 === 0 ? GOLD : blue}`}} />;
			})}
			{/* barrido de luz */}
			<AbsoluteFill style={{background: `linear-gradient(115deg, transparent ${interpolate(frame, [0, fps * 1.4], [-40, 140])}%, rgba(160,195,255,.16) ${interpolate(frame, [0, fps * 1.4], [-30, 150])}%, transparent ${interpolate(frame, [0, fps * 1.4], [-20, 160])}%)`}} />
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.6) 100%)'}} />
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** "Vendés más pero te queda poco": barras VENTAS (crece) vs LO QUE TE QUEDA (mínima) + contadores.
 * props: salesLabel, keepLabel, sales (valor), keep (valor), prefix, y, h */
export const ProfitGap: React.FC<G & {salesLabel?: string; keepLabel?: string; sales?: number; keep?: number; prefix?: string; y?: number; h?: number}> = ({dur, salesLabel = 'VENTAS', keepLabel = 'TE QUEDA', sales = 12000, keep = 900, prefix = '$', y = 0.52, h = 0.42}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const out = useOut(dur);
	const g1 = spring({frame: frame - 4, fps, config: {damping: 15, stiffness: 70}});
	const g2 = spring({frame: frame - 16, fps, config: {damping: 9, stiffness: 120}});
	const H = h * height;
	const bw = width * 0.26;
	const fmt = (v: number) => prefix + Math.round(v).toLocaleString('en-US');
	const shake = frame > 16 && frame < 30 ? noise2D('pg', frame, 0) * 6 * u : 0;
	const bar = (label: string, val: number, p: number, color: string, glow: string, xx: number) => (
		<div style={{position: 'absolute', left: xx - bw / 2, top: y * height + H / 2, width: bw, transform: 'translateY(-100%)'}}>
			<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: 64 * u, color: colors.light, textAlign: 'center', marginBottom: 12 * u, textShadow: '0 6px 20px rgba(0,0,0,.6)', fontVariantNumeric: 'tabular-nums'}}>{fmt(val * Math.min(1, p))}</div>
			<div style={{height: Math.max(6 * u, H * 0.78 * p * (val / sales)), borderRadius: `${22 * u}px ${22 * u}px ${6 * u}px ${6 * u}px`, background: color, boxShadow: `0 0 ${50 * u}px ${glow}, inset 0 ${3 * u}px 0 rgba(255,255,255,.35)`}} />
			<div style={{marginTop: 16 * u, fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontStyle: 'italic', fontSize: 38 * u, color: colors.light, textAlign: 'center', letterSpacing: 1}}>{label}</div>
		</div>
	);
	return (
		<AbsoluteFill style={{opacity: out, transform: `translateX(${shake}px)`}}>
			{bar(salesLabel, sales, g1, `linear-gradient(180deg, #7ea6ff, ${colors.blue ?? '#3474FF'} 40%, ${colors.blueDeep ?? '#0034B7'})`, hexA(colors.blue ?? '#3474FF', 0.7), width * 0.32)}
			{bar(keepLabel, keep, g2, `linear-gradient(180deg, #ffe08a, ${GOLD})`, hexA(GOLD, 0.8), width * 0.68)}
			<div style={{position: 'absolute', left: width * 0.1, right: width * 0.1, top: y * height + H / 2 + 2 * u, height: 3 * u, background: 'rgba(255,255,255,.35)'}} />
		</AbsoluteFill>
	);
};

/** Agenda que se llena de citas (agenda llena). props: title, cols, rows, y */
export const AgendaFill: React.FC<G & {title?: string; y?: number; rows?: number}> = ({dur, title = 'AGENDA LLENA', y = 0.5, rows = 7}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 16, stiffness: 140}});
	const W = width * 0.8;
	const days = ['L', 'M', 'M', 'J', 'V', 'S'];
	const cw = W / days.length;
	const ch = 70 * u;
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, transform: `translateY(-50%) perspective(1400px) rotateX(${(1 - s) * 40}deg) scale(${0.85 + 0.15 * s})`, opacity: out, width: W}}>
			<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: 66 * u, color: colors.light, marginBottom: 18 * u, textAlign: 'center'}}>{title}</div>
			<div style={{background: 'rgba(8,18,52,.72)', border: `${2 * u}px solid rgba(120,160,255,.35)`, borderRadius: 30 * u, padding: 18 * u, boxShadow: `0 30px 90px rgba(0,0,0,.5), 0 0 60px ${hexA(colors.blue ?? '#3474FF', 0.3)}`, backdropFilter: 'blur(12px)'}}>
				<div style={{display: 'flex'}}>
					{days.map((d, i) => (
						<div key={i} style={{width: cw - 4 * u, textAlign: 'center', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontSize: 30 * u, color: '#9fb6ff', marginBottom: 10 * u}}>{d}</div>
					))}
				</div>
				{Array.from({length: rows}, (_, r) => (
					<div key={r} style={{display: 'flex', gap: 0}}>
						{days.map((_, c) => {
							const k = r * days.length + c;
							const order = random(`ag${k}`) * 26 + k * 0.6;
							const on = interpolate(frame, [6 + order, 10 + order], [0, 1], clamp);
							const isGold = random(`gd${k}`) > 0.82;
							return (
								<div key={c} style={{width: cw - 8 * u, height: ch - 10 * u, margin: 4 * u, borderRadius: 12 * u, background: 'rgba(255,255,255,.05)', overflow: 'hidden'}}>
									<div style={{width: '100%', height: '100%', borderRadius: 12 * u, background: isGold ? `linear-gradient(135deg, #ffe08a, ${GOLD})` : `linear-gradient(135deg, #6f98ff, ${colors.blue ?? '#3474FF'})`, transform: `scale(${on})`, opacity: on}} />
								</div>
							);
						})}
					</div>
				))}
			</div>
		</div>
	);
};

/** Reloj/tiempo = dinero. props: label, y, x, size */
export const TimeIsMoney: React.FC<G & {label?: string; x?: number; y?: number; size?: number}> = ({dur, label = 'TU TIEMPO CUENTA', x = 0.5, y = 0.4, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
	const S = 360 * u * size;
	const ticks = Array.from({length: 60}, (_, i) => i);
	const minute = frame * 18;
	const hour = frame * 1.5;
	const coinT = interpolate(frame, [18, 30], [0, 1], {...clamp, easing: EASE.punch});
	return (
		<div style={{position: 'absolute', left: x * width - S / 2, top: y * height - S / 2, width: S, height: S + 120 * u, opacity: out, transform: `scale(${s})`}}>
			<svg width={S} height={S} viewBox="-100 -100 200 200" style={{filter: `drop-shadow(0 0 ${30 * u}px ${hexA(colors.blue ?? '#3474FF', 0.8)})`}}>
				<circle r="92" fill="rgba(6,14,44,.85)" stroke="rgba(255,255,255,.9)" strokeWidth="3" />
				<circle r="92" fill="none" stroke={GOLD} strokeWidth="6" strokeLinecap="round" strokeDasharray={`${578 * interpolate(frame, [0, dur], [0, 1], clamp)} 578`} transform="rotate(-90)" />
				{ticks.map((i) => (
					<line key={i} x1={0} y1={-84} x2={0} y2={i % 5 ? -80 : -72} stroke={i % 5 ? 'rgba(255,255,255,.4)' : '#fff'} strokeWidth={i % 5 ? 1 : 2.5} transform={`rotate(${i * 6})`} />
				))}
				<line x1={0} y1={8} x2={0} y2={-46} stroke="#fff" strokeWidth="6" strokeLinecap="round" transform={`rotate(${hour})`} />
				<line x1={0} y1={12} x2={0} y2={-70} stroke={GOLD} strokeWidth="3.5" strokeLinecap="round" transform={`rotate(${minute})`} />
				<circle r="6" fill={GOLD} />
			</svg>
			<div style={{position: 'absolute', right: -S * 0.08, top: -S * 0.06, width: S * 0.38, height: S * 0.38, borderRadius: '50%', background: `radial-gradient(circle at 35% 30%, #fff3c4, ${GOLD} 55%, #b07800)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: S * 0.22, color: '#5a3d00', transform: `scale(${coinT}) rotate(${(1 - coinT) * 180}deg)`, boxShadow: `0 0 ${40 * u}px ${hexA(GOLD, 0.8)}`}}>$</div>
			{label && <div style={{position: 'absolute', top: S + 24 * u, left: S / 2 - width / 2, width, textAlign: 'center', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: 58 * u, color: colors.light, whiteSpace: 'nowrap', opacity: interpolate(frame, [10, 20], [0, 1], clamp)}}>{label}</div>}
		</div>
	);
};

/** Etiquetas de costo que caen y se apilan ("tienen un costo"). props: items[], y */
export const CostTags: React.FC<G & {items: string[]; y?: number; every?: number; tag?: string; delays?: number[]}> = ({dur, items, y = 0.46, every = 9, tag = '-$', delays}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const out = useOut(dur);
	return (
		<div style={{position: 'absolute', left: width * 0.1, right: width * 0.1, top: y * height, transform: 'translateY(-50%)', display: 'flex', flexDirection: 'column', gap: 26 * u, opacity: out}}>
			{items.map((it, i) => {
				const d0 = delays?.[i] ?? i * every;
				const s = spring({frame: frame - d0, fps, config: {damping: 11, stiffness: 170}});
				const rot = (i % 2 ? 1 : -1) * 2.5;
				const stamp = spring({frame: frame - d0 - 6, fps, config: {damping: 9, stiffness: 300}});
				return (
					<div key={i} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'linear-gradient(135deg, rgba(14,30,90,.92), rgba(4,10,40,.92))', border: `${2 * u}px solid rgba(130,170,255,.4)`, borderRadius: 26 * u, padding: `${22 * u}px ${30 * u}px`, transform: `translateX(${(1 - s) * (i % 2 ? 1 : -1) * width * 0.6}px) rotate(${rot * s}deg)`, boxShadow: '0 20px 50px rgba(0,0,0,.5)'}}>
						<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: 52 * u, color: colors.light, textTransform: 'uppercase'}}>{it}</div>
						<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 900, fontSize: 50 * u, color: '#1a1100', background: GOLD, borderRadius: 14 * u, padding: `${4 * u}px ${18 * u}px`, transform: `scale(${stamp}) rotate(${-8 * stamp}deg)`, boxShadow: `0 0 ${24 * u}px ${hexA(GOLD, 0.7)}`}}>{tag}</div>
					</div>
				);
			})}
		</div>
	);
};

/** Tarjeta de pregunta en vidrio con balanza (¿me deja ganancia?). props: question, y, icon */
export const QuestionCard: React.FC<G & {question: string; kicker?: string; y?: number}> = ({dur, question, kicker = 'PREGÚNTATE', y = 0.2}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {colors, fonts} = useBrand();
	const out = useOut(dur);
	const s = spring({frame, fps, config: {damping: 15, stiffness: 150}});
	const words = question.split(' ');
	return (
		<div style={{position: 'absolute', left: width * 0.06, right: width * 0.06, top: y * height, transform: `translateY(-50%) translateY(${(1 - s) * -60 * u}px)`, opacity: out * s, background: 'linear-gradient(160deg, rgba(52,116,255,.30), rgba(4,12,48,.82))', border: `${2 * u}px solid rgba(160,190,255,.45)`, borderRadius: 34 * u, padding: `${30 * u}px ${36 * u}px`, boxShadow: `0 30px 80px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.25)`, backdropFilter: 'blur(14px)'}}>
			<div style={{display: 'inline-block', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontStyle: 'italic', fontSize: 30 * u, letterSpacing: 3, color: '#1a1100', background: GOLD, borderRadius: 999, padding: `${6 * u}px ${20 * u}px`, marginBottom: 14 * u}}>{kicker}</div>
			<div style={{fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontStyle: 'italic', fontSize: 50 * u, lineHeight: 1.12, color: colors.light}}>
				{words.map((w, i) => {
					const o = interpolate(frame, [6 + i * 1.6, 10 + i * 1.6], [0, 1], clamp);
					return (
						<span key={i} style={{opacity: o, display: 'inline-block', transform: `translateY(${(1 - o) * 14}px)`, marginRight: '0.26em', color: /ganancia|justifica/i.test(w) ? GOLD : undefined}}>
							{w}
						</span>
					);
				})}
			</div>
		</div>
	);
};

/** Perfil de Instagram + botón Seguir con tap de cursor + corazones (CTA "Sígueme").
 * props: handle, name, bio, avatar (imagen), y, followers, logo */
export const InstagramFollow: React.FC<G & {handle?: string; name?: string; bio?: string; avatar?: string; y?: number; followers?: string; posts?: string; following?: string; verified?: boolean; tagline?: string}> = ({
	dur,
	handle = 'carlos.buelvas',
	name = 'Carlos Buelvas',
	bio = 'Coach & Mentor de Ventas',
	avatar,
	y = 0.24,
	followers,
	posts,
	following,
	verified = false,
	tagline = 'Te ayudo a escalar tu negocio acelerando tus ventas 🚀',
}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const out = useOut(dur, 10);
	const s = spring({frame, fps, config: {damping: 14, stiffness: 150}});
	const tapAt = Math.round(fps * 0.9);
	const tap = frame - tapAt;
	const pressed = tap >= 0;
	const press = tap >= 0 && tap < 5 ? interpolate(tap, [0, 2, 5], [1, 0.9, 1]) : 1;
	const cursorP = interpolate(frame, [tapAt - 14, tapAt], [0, 1], {...clamp, easing: EASE.smooth});
	const W = width * 0.86;
	const ff = `${fonts.body}, -apple-system, Helvetica, sans-serif`;
	return (
		<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, transform: `translateY(-50%) translateY(${(1 - s) * 80 * u}px) scale(${0.9 + 0.1 * s})`, opacity: out * Math.min(1, s * 1.5)}}>
			<div style={{background: 'rgba(250,250,252,.97)', borderRadius: 40 * u, padding: `${30 * u}px ${32 * u}px`, boxShadow: `0 40px 100px rgba(0,0,0,.5), 0 0 0 ${3 * u}px rgba(255,187,0,.0)`, fontFamily: ff, color: '#0b0b0b'}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 28 * u}}>
					<div style={{width: 150 * u, height: 150 * u, borderRadius: '50%', padding: 6 * u, background: 'conic-gradient(from 200deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5, #feda75)', flex: 'none'}}>
						<div style={{width: '100%', height: '100%', borderRadius: '50%', border: `${5 * u}px solid #fff`, overflow: 'hidden', background: '#223'}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
					</div>
					<div style={{flex: 1}}>
						<div style={{display: 'flex', alignItems: 'center', gap: 10 * u, fontWeight: 800, fontSize: 40 * u}}>
							{handle}
							{verified && <svg width={34 * u} height={34 * u} viewBox="0 0 24 24"><path fill="#0095f6" d="M12 1l2.6 2.2 3.4-.4 1 3.3 3 1.7-1 3.2 1 3.2-3 1.7-1 3.3-3.4-.4L12 23l-2.6-2.2-3.4.4-1-3.3-3-1.7 1-3.2-1-3.2 3-1.7 1-3.3 3.4.4z" /><path fill="#fff" d="M10.4 15.6l-3-3 1.4-1.4 1.6 1.6 4.6-4.6 1.4 1.4z" /></svg>}
						</div>
						{followers && posts && following && <div style={{display: 'flex', gap: 30 * u, marginTop: 10 * u, fontSize: 28 * u}}>
							{[
								[posts, 'publicaciones'],
								[followers, 'seguidores'],
								[following, 'seguidos'],
							].map(([a, b]) => (
								<div key={b}>
									<div style={{fontWeight: 800, fontSize: 32 * u}}>{a}</div>
									<div style={{color: '#555'}}>{b}</div>
								</div>
							))}
						</div>}
						<div style={{fontSize: 30 * u, color: '#444', marginTop: 6 * u}}>{name}</div>
					</div>
				</div>
				<div style={{marginTop: 18 * u, fontWeight: 700, fontSize: 32 * u}}>{bio}</div>
				<div style={{fontSize: 28 * u, color: '#333', whiteSpace: 'pre-line', lineHeight: 1.3}}>{tagline}</div>
				<div style={{display: 'flex', gap: 14 * u, marginTop: 22 * u}}>
					<div style={{flex: 1, textAlign: 'center', borderRadius: 18 * u, padding: `${18 * u}px 0`, fontWeight: 800, fontSize: 34 * u, background: pressed ? '#efefef' : '#0095f6', color: pressed ? '#111' : '#fff', transform: `scale(${press})`}}>{pressed ? 'Siguiendo ✓' : 'Seguir'}</div>
					<div style={{flex: 1, textAlign: 'center', borderRadius: 18 * u, padding: `${18 * u}px 0`, fontWeight: 800, fontSize: 34 * u, background: '#efefef'}}>Mensaje</div>
				</div>
			</div>
			{/* cursor/mano */}
			<svg width={110 * u} height={110 * u} viewBox="0 0 24 24" style={{position: 'absolute', left: W * 0.27 + (1 - cursorP) * W * 0.5, top: 420 * u + (1 - cursorP) * 260 * u, transform: `scale(${tap >= 0 && tap < 6 ? 0.85 : 1})`, filter: 'drop-shadow(0 6px 10px rgba(0,0,0,.5))', opacity: interpolate(frame, [tapAt - 16, tapAt - 10, tapAt + 16, tapAt + 22], [0, 1, 1, 0], clamp)}}>
				<path fill="#fff" stroke="#111" strokeWidth="1" d="M9 11V5.5a1.5 1.5 0 0 1 3 0V10l.5-.1a1.5 1.5 0 0 1 2 .9l.1.4.4-.1a1.5 1.5 0 0 1 1.9 1l.1.3.3-.1a1.5 1.5 0 0 1 1.9 1.3V17c0 3-2.5 5.5-5.5 5.5h-1c-2 0-3.4-.9-4.5-2.4L5 16.6a1.5 1.5 0 0 1 2.3-1.9L9 16z" />
			</svg>
			{/* corazones */}
			{pressed &&
				Array.from({length: 9}, (_, i) => {
					const t = (tap - i * 2) / fps;
					if (t < 0 || t > 1.2) return null;
					const x0 = W * 0.27 + (random(`hx${i}`) - 0.5) * 140 * u;
					return (
						<div key={i} style={{position: 'absolute', left: x0, top: 470 * u - t * 520 * u, fontSize: (40 + random(`hs${i}`) * 30) * u, opacity: 1 - t / 1.2, transform: `rotate(${(random(`hr${i}`) - 0.5) * 40}deg) scale(${Math.min(1, t * 6)})`, color: i % 3 === 0 ? GOLD : '#ff3b5c'}}>
							♥
						</div>
					);
				})}
		</div>
	);
};

/** Pastilla CTA amarilla del manual (con brillo y flecha). props: text, x, y, size, pulse */
export const CTAPill: React.FC<G & {text: string; x?: number; y?: number; size?: number}> = ({dur, text, x = 0.5, y = 0.85, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const u = useU();
	const {fonts} = useBrand();
	const s = spring({frame, fps, config: {damping: 10, stiffness: 200}});
	const out = useOut(dur);
	const pulse = 1 + 0.035 * Math.max(0, Math.sin(frame / 5));
	const sweep = ((frame * 4) % 260) - 80;
	return (
		<div style={{position: 'absolute', left: x * width, top: y * height, transform: `translate(-50%, -50%) scale(${s * pulse * out})`}}>
			<div style={{position: 'relative', overflow: 'hidden', whiteSpace: 'nowrap', fontFamily: `${fonts.heading}, sans-serif`, fontWeight: 800, fontStyle: 'italic', fontSize: 44 * u * size, letterSpacing: 2, color: '#fff', background: `linear-gradient(180deg, #ffcf3d, ${GOLD} 60%, #e0a000)`, borderRadius: 999, padding: `${20 * u * size}px ${54 * u * size}px`, boxShadow: `0 0 ${36 * u}px ${hexA(GOLD, 0.75)}, inset 0 ${2 * u}px 0 rgba(255,255,255,.55)`, textShadow: '0 2px 6px rgba(120,70,0,.45)', textTransform: 'uppercase'}}>
				{text} ›
				<div style={{position: 'absolute', inset: 0, background: `linear-gradient(100deg, transparent ${sweep}%, rgba(255,255,255,.6) ${sweep + 12}%, transparent ${sweep + 24}%)`}} />
			</div>
		</div>
	);
};

/** Flecha / trazo de crecimiento (escalar): línea que sube en zigzag con punta y glow. props: y, label */
export const GrowthLine: React.FC<G & {y?: number; h?: number; color?: string}> = ({dur, y = 0.45, h = 0.3, color}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const u = useU();
	const out = useOut(dur);
	const c = color ?? GOLD;
	const x0 = width * 0.1;
	const x1 = width * 0.9;
	const yb = (y + h / 2) * height;
	const yt = (y - h / 2) * height;
	const pts = [0, 0.18, 0.32, 0.46, 0.6, 0.74, 1].map((t, i) => [x0 + (x1 - x0) * t, yb - (yb - yt) * [0, 0.25, 0.15, 0.48, 0.38, 0.72, 1][i]]);
	const d = 'M ' + pts.map((p) => p.join(' ')).join(' L ');
	const p = interpolate(frame, [0, 22], [0, 1], {...clamp, easing: EASE.out});
	const ev = evolvePath(p, d);
	const tip = pts[pts.length - 1];
	return (
		<svg width={width} height={height} style={{position: 'absolute', inset: 0, opacity: out}}>
			<path d={d} fill="none" stroke={c} strokeWidth={14 * u} strokeLinejoin="round" strokeLinecap="round" {...ev} style={{filter: `drop-shadow(0 0 ${16 * u}px ${c})`}} />
			{p > 0.97 && <path d={`M ${tip[0] - 60 * u} ${tip[1] + 6 * u} L ${tip[0]} ${tip[1]} L ${tip[0] - 10 * u} ${tip[1] + 60 * u}`} fill="none" stroke={c} strokeWidth={14 * u} strokeLinecap="round" strokeLinejoin="round" />}
		</svg>
	);
};
