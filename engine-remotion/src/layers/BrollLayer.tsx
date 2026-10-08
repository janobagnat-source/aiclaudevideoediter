import {Video} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, EASE} from '../lib/anim';
import {useBrand} from '../lib/brand';
import type {Broll} from '../types';
import {GRADES} from './MainTrack';

const BrollItem: React.FC<{b: Broll; grade: string}> = ({b, grade}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const {colors} = useBrand();
	const dur = Math.max(1, Math.round(b.duration * fps));
	const p = frame / dur;
	const kb = b.kenburns ?? 'in';
	const kbScale = kb === 'in' ? 1.06 + p * 0.12 : kb === 'out' ? 1.18 - p * 0.12 : 1.12;
	const kbX = kb === 'left' ? (0.5 - p) * width * 0.06 : kb === 'right' ? (p - 0.5) * width * 0.06 : 0;
	const kbY = kb === 'up' ? (0.5 - p) * height * 0.05 : 0;
	const tr = b.transition ?? 'whip';
	const inN = Math.round(fps * 0.22);
	const outN = Math.round(fps * 0.18);
	const pin = interpolate(frame, [0, inN], [0, 1], {...clamp, easing: EASE.out});
	const pout = interpolate(frame, [dur - outN, dur], [0, 1], {...clamp, easing: EASE.in});
	let tx = 0;
	let ty = 0;
	let blur = 0;
	let op = 1;
	let sc = 1;
	if (tr === 'whip') {
		tx = (1 - pin) * width * 0.5 - pout * width * 0.5;
		blur = (1 - pin) * 30 + pout * 30;
	} else if (tr === 'whip-up') {
		ty = (1 - pin) * height * 0.5 - pout * height * 0.5;
		blur = (1 - pin) * 30 + pout * 30;
	} else if (tr === 'zoom-in') {
		sc = 1.4 - 0.4 * pin + pout * 0.5;
		blur = (1 - pin) * 18 + pout * 18;
		op = Math.min(pin * 2, 1 - pout);
	} else if (tr === 'cut') {
		op = 1;
	} else {
		op = Math.min(pin, 1 - pout);
	}
	const media = b.isImage ? (
		<Img src={staticFile(b.src)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: b.focus ? `${b.focus.x * 100}% ${b.focus.y * 100}%` : 'center'}} />
	) : (
		<Video src={staticFile(b.src)} trimBefore={Math.round(b.in * fps)} playbackRate={b.speed ?? 1} volume={b.volume ?? 0} muted={!b.volume} objectFit="cover" loop={(b.srcDuration ?? 99) < b.duration + b.in} style={{width: '100%', height: '100%', objectPosition: b.focus ? `${b.focus.x * 100}% ${b.focus.y * 100}%` : 'center'}} />
	);
	const inner = (
		<AbsoluteFill style={{transform: `translate(${kbX}px, ${kbY}px) scale(${kbScale})`, filter: GRADES[b.grade ?? grade] ?? undefined}}>{media}</AbsoluteFill>
	);
	const mode = b.mode ?? 'full';
	const wrapStyle: React.CSSProperties = {transform: `translate(${tx}px, ${ty}px) scale(${sc})`, filter: blur ? `blur(${blur}px)` : undefined, opacity: op};
	if (mode === 'full') {
		return <AbsoluteFill style={wrapStyle}>{inner}</AbsoluteFill>;
	}
	if (mode === 'split-top' || mode === 'split-bottom') {
		return (
			<AbsoluteFill style={wrapStyle}>
				<div style={{position: 'absolute', left: 0, right: 0, height: '50%', top: mode === 'split-top' ? 0 : '50%', overflow: 'hidden', borderBottom: mode === 'split-top' ? `6px solid ${colors.primary}` : undefined, borderTop: mode === 'split-bottom' ? `6px solid ${colors.primary}` : undefined}}>
					{inner}
				</div>
			</AbsoluteFill>
		);
	}
	// pip / card / circle
	const s = mode === 'circle' ? Math.min(width, height) * 0.46 : width * 0.62;
	const h = mode === 'circle' ? s : s * (b.isImage ? 1 : 0.75);
	const pop = interpolate(frame, [0, inN * 1.4], [0.6, 1], {...clamp, easing: EASE.punch});
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: Math.min(pin * 1.5, 1 - pout)}}>
			<div
				style={{
					width: s,
					height: h,
					borderRadius: mode === 'circle' ? '50%' : 36,
					overflow: 'hidden',
					transform: `translateY(${height * -0.12}px) scale(${pop * (1 - pout * 0.2)}) rotate(${(1 - pin) * -6}deg)`,
					boxShadow: `0 30px 80px rgba(0,0,0,.55), 0 0 0 6px ${colors.light}, 0 0 0 12px ${colors.primary}`,
					position: 'relative',
				}}
			>
				{inner}
			</div>
		</AbsoluteFill>
	);
};

export const BrollLayer: React.FC<{items: Broll[]; grade: string}> = ({items, grade}) => {
	const {fps} = useVideoConfig();
	return (
		<>
			{items.map((b, i) => (
				<Sequence key={i} name={`broll ${i}: ${b.src.split('/').pop()}`} from={Math.round(b.start * fps)} durationInFrames={Math.max(1, Math.round(b.duration * fps))} premountFor={fps}>
					<BrollItem b={b} grade={grade} />
				</Sequence>
			))}
		</>
	);
};
