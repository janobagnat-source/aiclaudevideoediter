import React from 'react';
import {Composition} from 'remotion';
import {Edit} from './Edit';
import {Gallery, GALLERY_DURATION} from './Gallery';
import type {Edit as EditT} from './types';

const EMPTY: EditT = {
	id: 'vacío',
	width: 1080,
	height: 1920,
	fps: 30,
	durationInFrames: 90,
	brand: {colors: {primary: '#ff3b30', secondary: '#ffd60a', accent: '#00e5ff', dark: '#0b0b0f', light: '#ffffff'}, fonts: {heading: 'Montserrat', body: 'Inter'}, fontFiles: [], logo: null},
	cuts: [],
	broll: [],
	graphics: [{component: 'HookTitle', start: 0, duration: 3, props: {lines: ['Pasa un', 'edit.json', 'con --props'], highlight: ['edit.json'], bg: 'brand'}}],
	sfx: [],
	music: [],
	speech: [],
	captions: {enabled: false, style: 'bold-pop', emphasis: [], position: 0.7, maxWords: 3, uppercase: true, hideDuring: [], words: []},
	fx: {grain: 0.04, vignette: 0.2, grade: 'punchy', chromatic: 0},
	background: '#0b0b0f',
};

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="Edit"
				component={Edit}
				defaultProps={{edit: EMPTY}}
				width={1080}
				height={1920}
				fps={30}
				durationInFrames={90}
				calculateMetadata={({props}) => ({
					width: props.edit.width,
					height: props.edit.height,
					fps: props.edit.fps,
					durationInFrames: props.edit.durationInFrames,
				})}
			/>
			<Composition id="Gallery" component={Gallery} width={1080} height={1920} fps={30} durationInFrames={GALLERY_DURATION} defaultProps={{}} />
			<Composition id="Gallery16x9" component={Gallery} width={1920} height={1080} fps={30} durationInFrames={GALLERY_DURATION} defaultProps={{}} />
		</>
	);
};
