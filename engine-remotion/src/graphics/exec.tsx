// Línea “ejecutiva / editorial” (Carlos vende a empresarios): tipografía limpia, paneles de vidrio, datos,
// nada de íconos sobre la cara. Todo deriva de useCurrentFrame() (render determinista).
import {fitText} from '@remotion/layout-utils';
import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';

type G = {dur: number};
const GOLD = '#FFBB00';
const RED = '#FF4D5E';
const GREEN = '#00E051';
const src = (s?: string | null) => (!s ? undefined : s.startsWith('http') ? s : staticFile(s));
const useU = () => {
	const {width} = useVideoConfig();
	return width / 1080;
};
const fmt = (n: number, dec = 0) => n.toLocaleString('es-AR', {minimumFractionDigits: dec, maximumFractionDigits: dec});
/** 0→1 entrada y 1→0 salida (frames) con curvas suaves */
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

// ---------------------------------------------------------------------------------------------
/** Título editorial sobre b-roll: kicker dorado con línea + líneas reveladas por máscara + valor opcional que cuenta.
 * props: kicker, lines [{text,color?,size?,weight?,italic?}], y (centro vertical 0-1), align, value {from,to,prefix,suffix,dec,color,at}
 */
export const KickerTitle: React.FC<G & {kicker?: string; lines?: {text: string; color?: string; size?: number; weight?: number; italic?: boolean}[]; y?: number; align?: 'left' | 'center'; x?: number; value?: {from: number; to: number; prefix?: string; suffix?: string; dec?: number; color?: string; at?: number; dur?: number; size?: number}; stagger?: number}> = ({
	dur,
	kicker,
	lines = [],
	y = 0.2,
	align = 'left',
	x = 0.08,
	value,
	stagger = 5,
}) => {
	const {f, o} = useIO(dur, 12, 9);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const lineW = interpolate(f, [0, 14], [0, 1], {...clamp, easing: EASE.out});
	const ta = align === 'center' ? 'center' : 'left';
	const left = align === 'center' ? 0 : x * width;
	const right = align === 'center' ? 0 : width * 0.06;
	let val: React.ReactNode = null;
	if (value) {
		const at = value.at ?? 6;
		const p = interpolate(f, [at, at + (value.dur ?? 26)], [0, 1], {...clamp, easing: EASE.out});
		const n = value.from + (value.to - value.from) * p;
		const sp = spring({frame: f - at, fps, config: {stiffness: 200, damping: 20}});
		val = (
			<div style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: (value.size ?? 200) * u, lineHeight: 0.95, color: value.color ?? '#fff', fontVariantNumeric: 'tabular-nums', letterSpacing: -4 * u, transform: `translateY(${(1 - sp) * 40 * u}px)`, opacity: sp, textShadow: `0 ${10 * u}px ${40 * u}px rgba(0,0,0,.5)`}}>
				{value.prefix ?? ''}
				{fmt(n, value.dec ?? 0)}
				{value.suffix ?? ''}
			</div>
		);
	}
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left, right, top: y * height, transform: 'translateY(-50%)', textAlign: ta, display: 'flex', flexDirection: 'column', alignItems: align === 'center' ? 'center' : 'flex-start', gap: 6 * u}}>
				{kicker && (
					<div style={{display: 'flex', alignItems: 'center', gap: 18 * u, marginBottom: 10 * u, flexDirection: align === 'center' ? 'column' : 'row'}}>
						<div style={{width: 64 * u * lineW, height: 3 * u, background: GOLD, boxShadow: `0 0 ${12 * u}px ${GOLD}`}} />
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 30 * u, letterSpacing: 9 * u, color: GOLD, opacity: lineW, transform: `translateX(${(1 - lineW) * -20 * u}px)`}}>{kicker}</div>
					</div>
				)}
				{val}
				{lines.map((l, i) => {
					const p = interpolate(f, [4 + i * stagger, 18 + i * stagger], [0, 1], {...clamp, easing: EASE.out});
					return (
						<div key={i} style={{overflow: 'hidden', paddingBottom: 6 * u}}>
							<div style={{fontFamily: fonts.heading, fontWeight: l.weight ?? 900, fontStyle: l.italic ? 'italic' : 'normal', fontSize: (l.size ?? 92) * u, lineHeight: 1.0, color: l.color ?? '#fff', letterSpacing: -1 * u, transform: `translateY(${(1 - p) * 110}%)`, textShadow: `0 ${8 * u}px ${30 * u}px rgba(0,0,0,.45)`}}>{l.text}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Cinta tipo bolsa (Bloomberg): ítems que corren; en flipAt (s) todo pasa a rojo ▼ con itemsAfter. */
export const TickerTape: React.FC<G & {items: string[]; itemsAfter?: string[]; flipAt?: number; y?: number; speed?: number; label?: string}> = ({dur, items, itemsAfter, flipAt, y = 0.8, speed = 7, label = 'MI NEGOCIO'}) => {
	const {f, v} = useIO(dur, 10, 8);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const flipped = flipAt != null && f >= flipAt * fps;
	const list = flipped && itemsAfter ? itemsAfter : items;
	const flash = flipAt != null ? interpolate(f - flipAt * fps, [0, 2, 10], [0, 1, 0], clamp) : 0;
	const h = 92 * u;
	const shift = -(f * speed * u) % (width * 1.2);
	const row = [...list, ...list, ...list];
	const col = flipped ? RED : GREEN;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height - h / 2, height: h, transform: `scaleY(${v})`, ...glass(u, 0.82), borderLeft: 'none', borderRight: 'none', overflow: 'hidden', display: 'flex', alignItems: 'center'}}>
				<div style={{position: 'absolute', inset: 0, background: RED, opacity: flash * 0.35}} />
				<div style={{zIndex: 2, height: '100%', display: 'flex', alignItems: 'center', padding: `0 ${26 * u}px`, background: flipped ? RED : GOLD, color: '#020617', fontFamily: fonts.heading, fontWeight: 900, fontSize: 28 * u, letterSpacing: 3 * u, whiteSpace: 'nowrap'}}>{label}</div>
				<div style={{display: 'flex', gap: 60 * u, whiteSpace: 'nowrap', transform: `translateX(${shift}px)`, paddingLeft: 40 * u}}>
					{row.map((it, i) => {
						const up = !flipped;
						return (
							<span key={i} style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 34 * u, color: '#fff', letterSpacing: 1 * u, fontVariantNumeric: 'tabular-nums'}}>
								{it.replace(/[▲▼]/g, '')} <span style={{color: col}}>{up ? '▲' : '▼'}</span>
							</span>
						);
					})}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Agenda semanal que se llena sola (para el panel inferior del split). */
export const CalendarWeek: React.FC<G & {y?: number; h?: number; fill?: number; title?: string; rows?: number}> = ({dur, y = 0.6, h = 0.34, fill = 2.6, title = 'AGENDA · ESTA SEMANA', rows = 7}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const days = ['LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB'];
	const W = width * 0.9;
	const H = height * h;
	const head = 70 * u;
	const colW = (W - 90 * u) / days.length;
	const rowH = (H - head - 24 * u) / rows;
	const cells: {d: number; r: number; k: number}[] = [];
	for (let d = 0; d < days.length; d++) for (let r = 0; r < rows; r++) cells.push({d, r, k: random(`c${d}-${r}`)});
	cells.sort((a, b) => a.k - b.k);
	const shown = Math.floor(interpolate(f, [8, 8 + fill * fps], [0, cells.length], {...clamp, easing: EASE.inOut}));
	const pct = Math.round((shown / cells.length) * 100);
	const hours = ['08', '10', '12', '14', '16', '18', '20'];
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, height: H, borderRadius: 34 * u, ...glass(u), opacity: v, transform: `translateY(${(1 - v) * 60 * u}px)`, overflow: 'hidden'}}>
				<div style={{height: head, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: `0 ${30 * u}px`, borderBottom: `1px solid rgba(255,255,255,.1)`}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, letterSpacing: 4 * u, color: '#fff'}}>{title}</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: pct >= 100 ? GOLD : '#9fb6ff', fontVariantNumeric: 'tabular-nums'}}>{pct}% OCUPADA</span>
				</div>
				<div style={{position: 'absolute', left: 90 * u, right: 0, top: head + 8 * u, display: 'flex'}}>
					{days.map((d) => (
						<div key={d} style={{width: colW, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 700, fontSize: 20 * u, color: 'rgba(255,255,255,.55)', letterSpacing: 2 * u}}>{d}</div>
					))}
				</div>
				{hours.slice(0, rows).map((hh, r) => (
					<div key={hh} style={{position: 'absolute', left: 22 * u, top: head + 40 * u + r * rowH, fontFamily: fonts.body, fontSize: 19 * u, color: 'rgba(255,255,255,.4)', fontVariantNumeric: 'tabular-nums'}}>{hh}:00</div>
				))}
				{cells.slice(0, shown).map((c, i) => {
					const age = i / Math.max(1, cells.length);
					const pop = interpolate(shown - i, [0, 3], [0.6, 1], clamp);
					const isGold = random(`g${c.d}${c.r}`) > 0.72;
					return (
						<div key={`${c.d}-${c.r}`} style={{position: 'absolute', left: 90 * u + c.d * colW + 5 * u, top: head + 36 * u + c.r * rowH + 4 * u, width: colW - 10 * u, height: rowH - 8 * u, borderRadius: 10 * u, background: isGold ? `linear-gradient(180deg, ${GOLD}, #e09a00)` : `linear-gradient(180deg, #3474FF, #1d4fd8)`, transform: `scale(${pop})`, opacity: pop, boxShadow: `0 ${4 * u}px ${12 * u}px rgba(0,0,0,.3)`, padding: 6 * u, overflow: 'hidden'}}>
							<div style={{height: 5 * u, width: '60%', borderRadius: 3 * u, background: isGold ? 'rgba(2,6,23,.45)' : 'rgba(255,255,255,.75)', opacity: age > -1 ? 1 : 0}} />
							<div style={{height: 4 * u, width: '38%', marginTop: 5 * u, borderRadius: 3 * u, background: isGold ? 'rgba(2,6,23,.3)' : 'rgba(255,255,255,.45)'}} />
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Libro contable del mes: ingreso arriba, deducciones que entran una a una, saldo que cae. */
export const Ledger: React.FC<G & {income: number; incomeLabel?: string; items: {label: string; amount: number; at: number}[]; resultLabel?: string; y?: number; prefix?: string}> = ({dur, income, incomeLabel = 'VENDISTE ESTE MES', items, resultLabel = 'TE QUEDA', y = 0.62, prefix = '$'}) => {
	const {f, v} = useIO(dur, 12, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	let bal = income;
	for (const it of items) {
		const p = interpolate(f, [it.at, it.at + 10], [0, 1], {...clamp, easing: EASE.out});
		bal -= it.amount * p;
	}
	const W = width * 0.86;
	const low = bal / income < 0.2;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: (width - W) / 2, top: y * height, width: W, borderRadius: 30 * u, ...glass(u, 0.66), padding: `${30 * u}px ${36 * u}px`, opacity: v, transform: `translateY(${(1 - v) * 50 * u}px)`}}>
				<Row u={u} fonts={fonts} label={incomeLabel} value={`${prefix} ${fmt(income)}`} color="#fff" strong />
				{items.map((it, i) => {
					const p = interpolate(f, [it.at, it.at + 8], [0, 1], {...clamp, easing: EASE.out});
					return (
						<div key={i} style={{opacity: p, transform: `translateX(${(1 - p) * 40 * u}px)`}}>
							<Row u={u} fonts={fonts} label={it.label} value={`− ${prefix} ${fmt(it.amount)}`} color={RED} />
						</div>
					);
				})}
				<div style={{height: 2 * u, background: 'rgba(255,255,255,.18)', margin: `${16 * u}px 0`}} />
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
					<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, letterSpacing: 4 * u, color: GOLD}}>{resultLabel}</span>
					<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 72 * u, color: low ? RED : '#fff', fontVariantNumeric: 'tabular-nums', letterSpacing: -2 * u}}>
						{prefix} {fmt(Math.max(0, bal))}
					</span>
				</div>
			</div>
		</AbsoluteFill>
	);
};
const Row: React.FC<{u: number; fonts: {heading: string; body: string}; label: string; value: string; color: string; strong?: boolean}> = ({u, fonts, label, value, color, strong}) => (
	<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', padding: `${8 * u}px 0`, borderBottom: '1px dashed rgba(255,255,255,.08)'}}>
		<span style={{fontFamily: fonts.heading, fontWeight: strong ? 800 : 600, fontSize: (strong ? 28 : 30) * u, letterSpacing: (strong ? 4 : 1) * u, color: strong ? 'rgba(255,255,255,.7)' : '#fff'}}>{label}</span>
		<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: (strong ? 44 : 36) * u, color, fontVariantNumeric: 'tabular-nums'}}>{value}</span>
	</div>
);

// ---------------------------------------------------------------------------------------------
/** Ticket térmico que se imprime: líneas con puntos guía, total y sello. */
export const Receipt: React.FC<G & {title?: string; items: {label: string; value: string; at: number}[]; total?: {label: string; value: string; at: number}; stamp?: string; stampAt?: number; y?: number; w?: number}> = ({dur, title = 'TU MES · DETALLE', items, total, stamp, stampAt = 9999, y = 0.575, w = 0.74}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const W = width * w;
	const lastAt = Math.max(...items.map((i) => i.at), total?.at ?? 0);
	// el papel “sale” de la ranura a medida que se imprimen las líneas
	const lineH = 64 * u;
	const fullH = 120 * u + items.length * lineH + (total ? 130 * u : 0) + 40 * u;
	const printed = interpolate(f, [0, 8, lastAt + 10], [0, 130 * u, fullH], {...clamp, easing: EASE.out});
	const slotY = y * height;
	const sp = spring({frame: f - stampAt, fps, config: {stiffness: 260, damping: 13}});
	const ink = '#1a1f2e';
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			{/* ranura de la impresora */}
			<div style={{position: 'absolute', left: (width - W * 1.12) / 2, top: slotY - 26 * u, width: W * 1.12, height: 34 * u, borderRadius: 17 * u, background: 'linear-gradient(180deg,#0b1438,#02061a)', boxShadow: `0 0 0 ${2 * u}px rgba(255,255,255,.1), 0 ${12 * u}px ${30 * u}px rgba(0,0,0,.6)`, zIndex: 3}} />
			<div style={{position: 'absolute', left: (width - W) / 2, top: slotY, width: W, height: printed, overflow: 'hidden', zIndex: 2}}>
				<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: fullH, background: '#f4f1ea', padding: `${30 * u}px ${36 * u}px`, boxSizing: 'border-box', boxShadow: `0 ${30 * u}px ${60 * u}px rgba(0,0,0,.45)`, }}>
					<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 28 * u, letterSpacing: 5 * u, color: ink, textAlign: 'center', paddingBottom: 18 * u, borderBottom: `${3 * u}px dashed ${hexA(ink, 0.35)}`}}>{title}</div>
					{items.map((it, i) => (
						<div key={i} style={{display: 'flex', alignItems: 'baseline', height: lineH, gap: 10 * u, opacity: f >= it.at ? 1 : 0}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 32 * u, color: ink, whiteSpace: 'nowrap'}}>{it.label}</span>
							<span style={{flex: 1, borderBottom: `${3 * u}px dotted ${hexA(ink, 0.35)}`, transform: `translateY(${-8 * u}px)`}} />
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 34 * u, color: '#c21f3a', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}}>{it.value}</span>
						</div>
					))}
					{total && (
						<div style={{marginTop: 14 * u, paddingTop: 18 * u, borderTop: `${4 * u}px solid ${ink}`, display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', opacity: f >= total.at ? 1 : 0}}>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 38 * u, color: ink, letterSpacing: 2 * u}}>{total.label}</span>
							<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 54 * u, color: '#c21f3a', fontVariantNumeric: 'tabular-nums'}}>{total.value}</span>
						</div>
					)}
					{stamp && f >= stampAt && (
						<div style={{position: 'absolute', right: 40 * u, bottom: 150 * u, transform: `rotate(-12deg) scale(${2.2 - sp * 1.2})`, opacity: Math.min(1, sp * 1.4), border: `${6 * u}px solid #c21f3a`, color: '#c21f3a', borderRadius: 14 * u, padding: `${8 * u}px ${22 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontSize: 46 * u, letterSpacing: 3 * u, mixBlendMode: 'multiply'}}>{stamp}</div>
					)}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Notificación de “nuevo cliente” con botones; el cursor va a EVALUAR y lo presiona. */
export const DecisionPrompt: React.FC<G & {title?: string; body?: string; app?: string; avatar?: string; accept?: string; review?: string; clickAt?: number; y?: number}> = ({dur, title = 'Nueva solicitud', body = 'Un cliente quiere empezar el lunes. ¿Aceptás el proyecto?', app = 'VENTAS', avatar, accept = 'Aceptar', review = 'Evaluar primero', clickAt = 40, y = 0.79}) => {
	const {f, o} = useIO(dur, 1, 10);
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const sp = spring({frame: f, fps, config: {stiffness: 170, damping: 18}});
	const W = width * 0.88;
	const cx = (width - W) / 2;
	const top = y * height;
	const cardH = 300 * u;
	// cursor: entra desde abajo a la derecha hacia el botón “evaluar”
	const btnX = cx + W * 0.73;
	const btnY = top + cardH - 70 * u;
	const cp = interpolate(f, [clickAt - 22, clickAt - 2], [0, 1], {...clamp, easing: EASE.inOut});
	const curX = interpolate(cp, [0, 1], [width * 0.95, btnX]);
	const curY = interpolate(cp, [0, 1], [height * 1.02, btnY]);
	const press = interpolate(f, [clickAt - 2, clickAt, clickAt + 5], [1, 0.92, 1], clamp);
	const on = f >= clickAt;
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: cx, top, width: W, height: cardH, borderRadius: 40 * u, ...glass(u, 0.8), transform: `translateY(${(1 - sp) * 260 * u}px)`, padding: 32 * u, boxSizing: 'border-box'}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 18 * u}}>
					<div style={{width: 64 * u, height: 64 * u, borderRadius: 16 * u, background: avatar ? undefined : `linear-gradient(135deg, ${GOLD}, #e08a00)`, overflow: 'hidden'}}>{avatar && <Img src={src(avatar)!} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
					<div style={{flex: 1}}>
						<div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 22 * u, letterSpacing: 3 * u, color: 'rgba(255,255,255,.55)'}}>{app} · AHORA</div>
						<div style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 36 * u, color: '#fff'}}>{title}</div>
					</div>
				</div>
				<div style={{fontFamily: fonts.body, fontWeight: 500, fontSize: 30 * u, color: 'rgba(255,255,255,.85)', marginTop: 16 * u, lineHeight: 1.25}}>{body}</div>
				<div style={{position: 'absolute', left: 32 * u, right: 32 * u, bottom: 30 * u, display: 'flex', gap: 18 * u}}>
					<div style={{flex: 1, height: 76 * u, borderRadius: 22 * u, background: 'rgba(255,255,255,.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 800, fontSize: 30 * u, color: 'rgba(255,255,255,.6)'}}>{accept}</div>
					<div style={{flex: 1.3, height: 76 * u, borderRadius: 22 * u, background: on ? GOLD : 'rgba(255,187,0,.16)', border: `${2 * u}px solid ${GOLD}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 900, fontSize: 30 * u, color: on ? '#020617' : GOLD, transform: `scale(${press})`, boxShadow: on ? `0 0 ${30 * u}px ${hexA(GOLD, 0.6)}` : undefined}}>{review}</div>
				</div>
			</div>
			{/* cursor */}
			<svg width={70 * u} height={70 * u} viewBox="0 0 24 24" style={{position: 'absolute', left: curX, top: curY, opacity: cp > 0 ? 1 : 0, transform: `scale(${press})`, filter: 'drop-shadow(0 4px 8px rgba(0,0,0,.5))'}}>
				<path d="M4 2l15 8.5-6.6 1.5 3.8 7.2-2.9 1.5-3.8-7.3L4 18z" fill="#fff" stroke="#020617" strokeWidth={1.2} />
			</svg>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Tipografía gigante DETRÁS del sujeto (usar en cuts[n].behind con cutout). Relleno u outline, deriva lenta. */
export const BehindTitle: React.FC<G & {lines: {text: string; outline?: boolean; color?: string; size?: number; tracking?: number; gradient?: boolean}[]; y?: number; drift?: number; kicker?: string; kickerY?: number}> = ({dur, lines, y = 0.36, drift = 0.06, kicker, kickerY}) => {
	const {f, o} = useIO(dur, 14, 10);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = f / Math.max(1, dur);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y * height, transform: `translateY(-50%) scale(${1 + drift * p})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
				{kicker && kickerY == null && <div style={{fontFamily: fonts.heading, fontWeight: 700, fontSize: 34 * u, letterSpacing: 14 * u, color: GOLD, marginBottom: 10 * u, opacity: interpolate(f, [6, 18], [0, 1], clamp)}}>{kicker}</div>}
				{lines.map((l, i) => {
					const fit = fitText({text: l.text, withinWidth: width * 0.94, fontFamily: fonts.heading, fontWeight: 900, letterSpacing: `${(l.tracking ?? 0) * u}px`}).fontSize;
					const size = Math.min((l.size ?? 400) * u, fit);
					const r = interpolate(f, [i * 4, 16 + i * 4], [0, 1], {...clamp, easing: EASE.out});
					return (
						<div key={i} style={{overflow: 'hidden', lineHeight: 0.86}}>
							<div
								style={{
									fontFamily: fonts.heading,
									fontWeight: 900,
									fontSize: size,
									letterSpacing: (l.tracking ?? 0) * u,
									color: l.outline ? 'transparent' : l.gradient ? 'transparent' : l.color ?? '#fff',
									backgroundImage: l.gradient ? `linear-gradient(180deg, ${l.color ?? GOLD} 0%, ${hexA(l.color ?? GOLD, 0.85)} 55%, ${hexA(l.color ?? GOLD, 0.15)} 100%)` : undefined,
									WebkitBackgroundClip: l.gradient ? 'text' : undefined,
									WebkitTextStroke: l.outline ? `${3 * u}px ${l.color ?? GOLD}` : undefined,
									transform: `translateY(${(1 - r) * 100}%)`,
									textShadow: l.outline ? undefined : `0 0 ${60 * u}px ${hexA(l.color ?? '#3474FF', 0.35)}`,
								}}
							>
								{l.text}
							</div>
						</div>
					);
				})}
			</div>
			{kicker && kickerY != null && (
				<div style={{position: 'absolute', left: 0, right: 0, top: kickerY * height, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 800, fontSize: 36 * u, letterSpacing: 16 * u, color: GOLD, opacity: interpolate(f, [6, 18], [0, 1], clamp), textShadow: `0 ${4 * u}px ${20 * u}px rgba(0,0,0,.6)`}}>{kicker}</div>
			)}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Chip de resultado (zona baja, lejos de la cara): etiqueta + número que cae con flecha. */
export const ResultChip: React.FC<G & {label: string; from: number; to: number; prefix?: string; y?: number; note?: string}> = ({dur, label, from, to, prefix = '$', y = 0.82, note}) => {
	const {f, v} = useIO(dur, 10, 9);
	const {width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const p = interpolate(f, [6, 30], [0, 1], {...clamp, easing: EASE.out});
	const n = from + (to - from) * p;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: '50%', top: y * height, transform: `translate(-50%,-50%) translateY(${(1 - v) * 40 * u}px)`, opacity: v, ...glass(u, 0.75), borderRadius: 999, padding: `${16 * u}px ${40 * u}px`, display: 'flex', alignItems: 'center', gap: 26 * u, whiteSpace: 'nowrap'}}>
				<span style={{fontFamily: fonts.heading, fontWeight: 800, fontSize: 26 * u, letterSpacing: 5 * u, color: 'rgba(255,255,255,.7)'}}>{label}</span>
				<span style={{fontFamily: fonts.heading, fontWeight: 900, fontSize: 64 * u, color: p > 0.95 ? RED : '#fff', fontVariantNumeric: 'tabular-nums'}}>
					{prefix} {fmt(n)}
				</span>
				<span style={{color: RED, fontSize: 40 * u, transform: `translateY(${Math.sin(f / 4) * 3 * u}px)`}}>▼</span>
				{note && <span style={{fontFamily: fonts.body, fontSize: 24 * u, color: 'rgba(255,255,255,.55)'}}>{note}</span>}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Cierre plano: fondo de marca con haces de luz lentos, logo dorado revelado por máscara + barrido de brillo,
 * filos dorados y CTA. Sin 3D. */
export const LogoReveal: React.FC<G & {logo: string; tagline?: string; cta?: string; ctaAt?: number}> = ({dur, logo, tagline = 'COACH · MENTOR DE VENTAS', cta = 'SÍGUEME', ctaAt = 16}) => {
	const f = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const {fonts} = useBrand();
	const u = useU();
	const bg = interpolate(f, [0, 8], [0, 1], {...clamp, easing: EASE.out});
	const wipe = interpolate(f, [4, 22], [0, 1], {...clamp, easing: EASE.inOut});
	const sweep = interpolate(f, [16, 40], [-0.4, 1.4], {...clamp, easing: EASE.inOut});
	const lines = interpolate(f, [14, 30], [0, 1], {...clamp, easing: EASE.out});
	const sc = interpolate(f, [0, dur], [1.04, 1.0]);
	const ctaS = spring({frame: f - ctaAt, fps, config: {stiffness: 220, damping: 16}});
	const L = src(logo)!;
	const LW = width * 0.62;
	const LH = LW * 0.62;
	const cy = height * 0.43;
	return (
		<AbsoluteFill style={{opacity: bg, background: `radial-gradient(90% 55% at 50% 42%, #0b2fa8 0%, #041350 45%, #020617 85%)`, overflow: 'hidden'}}>
			{/* haces de luz diagonales */}
			{[0, 1, 2].map((i) => (
				<div key={i} style={{position: 'absolute', left: '50%', top: '42%', width: width * 0.16, height: height * 1.6, transform: `translate(-50%,-50%) rotate(${-24 + i * 24 + Math.sin((f + i * 40) / 40) * 4}deg)`, background: `linear-gradient(90deg, transparent, rgba(80,130,255,${0.12 - i * 0.02}), transparent)`, filter: `blur(${20 * u}px)`}} />
			))}
			<div style={{position: 'absolute', left: (width - LW) / 2, top: cy - LH / 2, width: LW, height: LH, transform: `scale(${sc})`}}>
				<div style={{position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`}}>
					<Img src={L} style={{width: '100%', height: '100%', objectFit: 'contain', filter: `drop-shadow(0 0 ${30 * u}px rgba(255,187,0,.35))`}} />
				</div>
				{/* barrido de brillo recortado por la silueta del logo */}
				<div style={{position: 'absolute', inset: 0, WebkitMaskImage: `url(${L})`, WebkitMaskSize: 'contain', WebkitMaskRepeat: 'no-repeat', WebkitMaskPosition: 'center', background: `linear-gradient(105deg, transparent ${sweep * 100 - 12}%, rgba(255,255,255,.95) ${sweep * 100}%, transparent ${sweep * 100 + 12}%)`, mixBlendMode: 'screen'}} />
			</div>
			{/* filos dorados */}
			{[-1, 1].map((s) => (
				<div key={s} style={{position: 'absolute', top: cy + LH / 2 + 46 * u, left: '50%', width: width * 0.15 * lines, height: 2 * u, transform: `translateX(${s < 0 ? -100 : 0}%) translateX(${s * width * 0.31}px)`, background: `linear-gradient(${s < 0 ? 270 : 90}deg, ${GOLD}, transparent)`}} />
			))}
			<div style={{position: 'absolute', top: cy + LH / 2 + 30 * u, left: 0, right: 0, textAlign: 'center', fontFamily: fonts.heading, fontWeight: 700, fontSize: 26 * u, letterSpacing: 10 * u, color: 'rgba(255,255,255,.8)', opacity: lines}}>{tagline}</div>
			<div style={{position: 'absolute', top: height * 0.7, left: '50%', transform: `translate(-50%,-50%) scale(${ctaS})`, background: GOLD, color: '#020617', borderRadius: 999, padding: `${22 * u}px ${70 * u}px`, fontFamily: fonts.heading, fontWeight: 900, fontStyle: 'italic', fontSize: 52 * u, letterSpacing: 2 * u, boxShadow: `0 0 ${50 * u}px ${hexA(GOLD, 0.5)}`}}>
				{cta} ›
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------------------------
/** Viñeta de transición cinematográfica: barrido de luz azul/blanco que atraviesa la pantalla (entre escenas). */
export const LightSweep: React.FC<G & {color?: string; angle?: number}> = ({dur, color = '#9db8ff', angle = 70}) => {
	const f = useCurrentFrame();
	const {width} = useVideoConfig();
	const p = interpolate(f, [0, dur], [-0.6, 1.6], {...clamp, easing: EASE.inOut});
	return (
		<AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen', background: `linear-gradient(${angle}deg, transparent ${p * 100 - 30}%, ${hexA(color, 0.0)} ${p * 100 - 20}%, ${hexA(color, 0.85)} ${p * 100}%, ${hexA(color, 0)} ${p * 100 + 20}%, transparent ${p * 100 + 30}%)`, filter: `blur(${width * 0.01}px)`}} />
	);
};
