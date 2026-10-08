import {lightLeak} from '@remotion/effects/light-leak';
import {noise2D} from '@remotion/noise';
import React from 'react';
import {AbsoluteFill, interpolate, random, Sequence, Solid, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp} from '../lib/anim';
import type {Cut} from '../types';

/** Grano de película: SVG feTurbulence con semilla por frame (determinista). */
export const FilmGrain: React.FC<{amount: number}> = ({amount}) => {
	const frame = useCurrentFrame();
	if (!amount) return null;
	const seed = Math.floor(frame % 97);
	return (
		<AbsoluteFill style={{mixBlendMode: 'overlay', opacity: amount * 4, pointerEvents: 'none'}}>
			<svg width="100%" height="100%">
				<filter id={`g${seed}`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} stitchTiles="stitch" />
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="100%" height="100%" filter={`url(#g${seed})`} />
			</svg>
		</AbsoluteFill>
	);
};

export const Vignette: React.FC<{amount: number}> = ({amount}) =>
	amount ? <AbsoluteFill style={{pointerEvents: 'none', background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,${amount}) 100%)`}} /> : null;

export const Letterbox: React.FC<{ratio?: number}> = ({ratio}) => {
	const {width, height} = useVideoConfig();
	if (!ratio) return null;
	const bar = Math.max(0, (height - width / ratio) / 2);
	return (
		<>
			<div style={{position: 'absolute', top: 0, left: 0, right: 0, height: bar, background: '#000'}} />
			<div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: bar, background: '#000'}} />
		</>
	);
};

const LeakInner: React.FC<{seed: number; hue: number}> = ({seed, hue}) => {
	const frame = useCurrentFrame();
	const {durationInFrames, width, height} = useVideoConfig();
	return (
		<Solid
			width={width}
			height={height}
			style={{mixBlendMode: 'screen'}}
			effects={[lightLeak({seed, hueShift: hue, progress: interpolate(frame, [0, durationInFrames - 1], [0, 1], clamp)})]}
		/>
	);
};

/** Light leaks en los cortes marcados con transition "light-leak". */
export const LightLeaks: React.FC<{cuts: Cut[]; hue?: number}> = ({cuts, hue = 0}) => {
	const {fps} = useVideoConfig();
	return (
		<>
			{cuts
				.filter((c) => (typeof c.transition === 'string' ? c.transition : c.transition?.type) === 'light-leak')
				.map((c) => {
					const d = Math.round(fps * 0.9);
					return (
						<Sequence key={c.i} from={Math.round(c.tl_start * fps) - Math.round(d / 2)} durationInFrames={d} name="light leak">
							<LeakInner seed={c.i} hue={hue} />
						</Sequence>
					);
				})}
		</>
	);
};

/** Flicker sutil de exposición (look de película), opcional. */
export const Flicker: React.FC<{amount: number}> = ({amount}) => {
	const frame = useCurrentFrame();
	if (!amount) return null;
	return <AbsoluteFill style={{background: '#000', opacity: Math.max(0, noise2D('fl', frame / 3, 0) * amount + random(frame) * amount * 0.3), pointerEvents: 'none'}} />;
};
