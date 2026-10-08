import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile, useVideoConfig} from 'remotion';
import {clamp} from '../lib/anim';
import type {Music, Sfx} from '../types';

/** 1 = sin voz, 0 = voz activa (con ataque/release suaves) */
const voiceEnvelope = (t: number, speech: [number, number][], attack = 0.12, release = 0.4) => {
	let v = 0;
	for (const [a, b] of speech) {
		if (t < a - attack || t > b + release) continue;
		if (t < a) v = Math.max(v, (t - (a - attack)) / attack);
		else if (t <= b) v = 1;
		else v = Math.max(v, 1 - (t - b) / release);
	}
	return v;
};

export const AudioLayer: React.FC<{sfx: Sfx[]; music: Music[]; speech: [number, number][]}> = ({sfx, music, speech}) => {
	const {fps} = useVideoConfig();
	return (
		<>
			{music.map((m, i) => {
				const from = Math.round(m.start * fps);
				const dur = Math.max(1, Math.round(m.duration * fps));
				return (
					<Sequence key={`m${i}`} name={`música ${i}`} from={from} durationInFrames={dur} layout="none">
						<Audio
							src={staticFile(m.src)}
							trimBefore={Math.round(m.in * fps)}
							volume={(f) => {
								const t = m.start + f / fps;
								const fade = Math.min(interpolate(f, [0, Math.max(1, m.fadeIn * fps)], [0, 1], clamp), interpolate(f, [dur - Math.max(1, m.fadeOut * fps), dur], [1, 0], clamp));
								const duck = 1 - (1 - m.duck) * voiceEnvelope(t, speech);
								return m.volume * fade * duck;
							}}
						/>
					</Sequence>
				);
			})}
			{sfx.map((s, i) => (
				<Sequence key={`s${i}`} name={`sfx ${s.src.split('/').pop()}`} from={Math.round(s.start * fps)} layout="none">
					<Audio src={staticFile(s.src)} volume={(f) => s.volume * (1 - (1 - (s.duck ?? 1)) * voiceEnvelope(s.start + f / fps, speech, 0.05, 0.25))} trimBefore={s.trim ? Math.round(s.trim[0] * fps) : undefined} durationInFrames={s.trim ? Math.round((s.trim[1] - s.trim[0]) * fps) : undefined} />
				</Sequence>
			))}
		</>
	);
};
