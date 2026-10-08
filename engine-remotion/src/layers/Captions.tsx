import {fitText} from '@remotion/layout-utils';
import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, hexA} from '../lib/anim';
import {useBrand} from '../lib/brand';
import type {Edit, Word} from '../types';

const normW = (s: string) =>
	s
		.toLowerCase()
		.normalize('NFD')
		.replace(/[̀-ͯ]/g, '')
		.replace(/[^a-z0-9ñ%]/g, '');

type Chunk = {words: Word[]; start: number; end: number};

export const chunkWords = (words: Word[], maxWords: number): Chunk[] => {
	const chunks: Chunk[] = [];
	let cur: Word[] = [];
	const flush = () => {
		if (cur.length) chunks.push({words: cur, start: cur[0].start, end: cur[cur.length - 1].end});
		cur = [];
	};
	words.forEach((w, i) => {
		const prev = words[i - 1];
		if (cur.length && (cur.length >= maxWords || (prev && w.start - prev.end > 0.35) || /[.!?…:]$/.test(prev?.text ?? ''))) flush();
		cur.push(w);
		if (w.text.length > 11 && cur.length >= 2) flush();
	});
	flush();
	// mantener cada chunk visible hasta que empiece el siguiente (si el hueco es corto)
	for (let i = 0; i < chunks.length - 1; i++) {
		const gap = chunks[i + 1].start - chunks[i].end;
		if (gap < 0.6) chunks[i].end = chunks[i + 1].start;
		else chunks[i].end += 0.25;
	}
	return chunks;
};

export const Captions: React.FC<{cfg: Edit['captions']}> = ({cfg}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const {colors, fonts} = useBrand();
	const chunks = useMemo(() => chunkWords(cfg.words, cfg.maxWords), [cfg.words, cfg.maxWords]);
	const emph = useMemo(() => new Set(cfg.emphasis.map(normW)), [cfg.emphasis]);
	const t = frame / fps;
	if (cfg.hideDuring.some(([a, b]) => t >= a && t < b)) return null;
	const ch = chunks.find((c) => t >= c.start - 0.02 && t < c.end);
	if (!ch) return null;
	const local = frame - Math.round(ch.start * fps);
	const enter = spring({frame: local, fps, config: {stiffness: 380, damping: 22, mass: 0.6}});
	const portrait = height > width;
	const base = (portrait ? width * 0.088 : height * 0.085) * (cfg.style === 'minimal' ? 0.72 : 1);
	const style = cfg.style;

	if (style === 'premium') {
		const GOLD = colors.gold ?? colors.secondary;
		const clean = (x: string) => x.replace(/[“”"«»]/g, '').replace(/[.,;:]+$/g, '').replace(/([?!])[.,;:]+$/g, '$1');
		const lineText = ch.words.map((w) => clean(cfg.uppercase ? w.text.toUpperCase() : w.text)).join(' ');
		const fit = fitText({text: lineText, withinWidth: width * 0.84, fontFamily: fonts.heading, fontWeight: 900, textTransform: 'uppercase', additionalStyles: {fontStyle: 'italic'}}).fontSize;
		const size = Math.min(base * 1.02, fit);
		return (
			<AbsoluteFill style={{pointerEvents: 'none'}}>
				<div style={{position: 'absolute', top: `${cfg.position * 100}%`, left: 0, right: 0, transform: 'translateY(-50%)', display: 'flex', justifyContent: 'center', flexWrap: 'nowrap', columnGap: size * 0.3}}>
					{ch.words.map((w, i) => {
						const said = t >= w.start - 0.06;
						const cf = frame - Math.round((ch.start - 0.04) * fps) - i * 1.5;
						const sp = spring({frame: cf, fps, config: {stiffness: 420, damping: 24, mass: 0.55}});
						const active = t >= w.start - 0.06 && t < (ch.words[i + 1]?.start ?? ch.end) - 0.04;
						const isEmph = emph.has(normW(w.text));
						const txt = clean(cfg.uppercase ? w.text.toUpperCase() : w.text);
						const color = isEmph ? GOLD : colors.light;
						const ul = active ? spring({frame: frame - Math.round((w.start - 0.06) * fps), fps, config: {damping: 200}, durationInFrames: 6}) : 0;
						return (
							<span key={i} style={{position: 'relative', display: 'inline-block', opacity: Math.min(1, sp * 1.6) * (said ? 1 : 0.42), transform: `translateY(${(1 - sp) * size * 0.45}px) scale(${active ? 1.03 : 1})`, filter: `blur(${(1 - sp) * 6}px)`}}>
								<span style={{filter: `drop-shadow(0 ${size * 0.05}px ${size * 0.06}px rgba(0,0,0,.85)) drop-shadow(0 ${size * 0.02}px ${size * 0.02}px rgba(0,0,0,.6))`, fontFamily: `${fonts.heading}, Montserrat, sans-serif`, fontWeight: 900, fontStyle: 'italic', fontSize: size, lineHeight: 1, letterSpacing: -0.5, color, textShadow: `0 ${size * 0.05}px ${size * 0.22}px rgba(0,4,30,.75), 0 0 ${size * 0.5}px rgba(0,20,80,.35)${isEmph ? `, 0 0 ${size * 0.4}px ${hexA(GOLD, 0.55)}` : ''}`, WebkitTextStroke: `${Math.max(1.5, size * 0.018)}px rgba(0,10,40,.55)`, paintOrder: 'stroke fill'}}>{txt}</span>
								<span style={{position: 'absolute', left: '4%', right: '4%', bottom: -size * 0.13, height: size * 0.075, borderRadius: size, background: isEmph ? colors.light : GOLD, transformOrigin: 'left', transform: `scaleX(${ul}) skewX(-12deg)`, boxShadow: `0 0 ${size * 0.25}px ${hexA(GOLD, 0.8)}`}} />
							</span>
						);
					})}
				</div>
			</AbsoluteFill>
		);
	}
	return (
		<AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', pointerEvents: 'none'}}>
			<div
				style={{
					position: 'absolute',
					top: `${cfg.position * 100}%`,
					transform: `translateY(-50%) translateY(${(1 - enter) * 26}px) scale(${0.86 + 0.14 * enter})`,
					width: '88%',
					display: 'flex',
					flexWrap: 'wrap',
					justifyContent: 'center',
					alignItems: 'center',
					gap: `${base * 0.12}px ${base * 0.24}px`,
					padding: style === 'boxed' ? `${base * 0.2}px ${base * 0.35}px` : 0,
					background: style === 'boxed' ? hexA(colors.dark, 0.82) : undefined,
					borderRadius: style === 'boxed' ? base * 0.3 : 0,
					opacity: interpolate(local, [0, 2], [0, 1], clamp),
				}}
			>
				{ch.words.map((w, i) => {
					const active = t >= w.start - 0.03 && t < (ch.words[i + 1]?.start ?? ch.end);
					const said = t >= w.start - 0.03;
					const isEmph = emph.has(normW(w.text));
					const wf = frame - Math.round(w.start * fps);
					const wpop = spring({frame: wf, fps, config: {stiffness: 500, damping: 18, mass: 0.5}});
					const txt = cfg.uppercase ? w.text.toUpperCase() : w.text;
					let color = colors.light;
					let bg: string | undefined;
					let scale = 1;
					let op = 1;
					if (style === 'bold-pop') {
						color = isEmph ? colors.secondary : active ? colors.light : colors.light;
						bg = active ? colors.primary : undefined;
						scale = active ? 1 + 0.1 * wpop : 1;
					} else if (style === 'karaoke') {
						op = said ? 1 : 0.35;
						color = active ? colors.primary : isEmph ? colors.secondary : colors.light;
						scale = active ? 1 + 0.08 * wpop : 1;
					} else if (style === 'neon') {
						color = isEmph || active ? colors.accent : colors.light;
					} else if (style === 'minimal' || style === 'serif-elegant') {
						op = said ? 1 : 0.5;
						color = isEmph ? colors.secondary : colors.light;
					} else if (style === 'boxed') {
						color = active ? colors.secondary : colors.light;
					}
					const size = base * (isEmph ? 1.22 : 1);
					return (
						<span
							key={i}
							style={{
								fontFamily: style === 'serif-elegant' && isEmph ? 'Playfair Display, serif' : `${fonts.heading}, Montserrat, Inter, sans-serif`,
								fontWeight: style === 'minimal' ? 700 : 900,
								fontStyle: style === 'serif-elegant' && isEmph ? 'italic' : 'normal',
								fontSize: size,
								lineHeight: 1.04,
								letterSpacing: style === 'minimal' ? 0 : -0.5,
								color,
								opacity: op,
								display: 'inline-block',
								transform: `scale(${scale}) rotate(${active && style === 'bold-pop' ? -2 : 0}deg)`,
								background: bg,
								padding: bg ? `${size * 0.02}px ${size * 0.14}px` : 0,
								borderRadius: bg ? size * 0.14 : 0,
								WebkitTextStroke: style === 'bold-pop' || style === 'karaoke' ? `${Math.max(2, size * 0.075)}px #000` : undefined,
								paintOrder: 'stroke fill',
								textShadow:
									style === 'neon'
										? `0 0 ${size * 0.25}px ${color}, 0 0 ${size * 0.6}px ${color}`
										: `0 ${size * 0.06}px ${size * 0.18}px rgba(0,0,0,.55)`,
							}}
						>
							{txt}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
