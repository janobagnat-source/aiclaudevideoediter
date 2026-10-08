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
