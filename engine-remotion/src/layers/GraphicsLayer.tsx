import {Video} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Sequence, staticFile, useVideoConfig} from 'remotion';
import {BarChart, Checklist, Countdown, HookTitle, KineticText, LowerThird, OfferBadge, ProgressBar, SplitCompare, StatCounter, Testimonial} from '../graphics/text';
import {ArrowCallout, BrandBackground, CircleHighlight, CTAEndCard, Flash, FloatingCard, IconPop, LogoSting, Notification, ShapeBurst} from '../graphics/visual';
import {Logo3D, Model3D, Particles3D, Phone3D, Shapes3D, Text3DTitle} from '../three/scenes';
import type {Graphic} from '../types';

/** Video con alfa (p.ej. overlay renderizado con HyperFrames en WebM/ProRes 4444) o elemento de stock. props: src, blend, opacity, fit */
const OverlayVideo: React.FC<{dur: number; src: string; blend?: React.CSSProperties['mixBlendMode']; opacity?: number; fit?: 'cover' | 'contain'; volume?: number; trimBefore?: number}> = ({src, blend, opacity = 1, fit = 'cover', volume = 0, trimBefore = 0}) => {
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill style={{mixBlendMode: blend, opacity}}>
			<Video src={src.startsWith('http') ? src : staticFile(src)} objectFit={fit} muted={!volume} volume={volume} trimBefore={Math.round(trimBefore * fps)} style={{width: '100%', height: '100%'}} />
		</AbsoluteFill>
	);
};

// Registro: nombre en overlays.json -> componente. Para crear uno nuevo: añádelo en src/graphics y regístralo aquí.
export const REGISTRY: Record<string, React.FC<any>> = {
	HookTitle,
	KineticText,
	LowerThird,
	StatCounter,
	Checklist,
	OfferBadge,
	ProgressBar,
	Countdown,
	Testimonial,
	BarChart,
	SplitCompare,
	Flash,
	ShapeBurst,
	ArrowCallout,
	CircleHighlight,
	IconPop,
	BrandBackground,
	LogoSting,
	CTAEndCard,
	Notification,
	FloatingCard,
	OverlayVideo,
	Model3D,
	Logo3D,
	Text3DTitle,
	Particles3D,
	Shapes3D,
	Phone3D,
};

export const GraphicsLayer: React.FC<{items: Graphic[]; layer: 'under' | 'over' | 'top'}> = ({items, layer}) => {
	const {fps} = useVideoConfig();
	return (
		<>
			{items
				.filter((g) => (g.layer ?? 'over') === layer)
				.map((g, i) => {
					const C = REGISTRY[g.component];
					const dur = Math.max(1, Math.round(g.duration * fps));
					if (!C) {
						throw new Error(`Gráfico desconocido "${g.component}". Disponibles: ${Object.keys(REGISTRY).join(', ')}`);
					}
					return (
						<Sequence key={`${layer}${i}`} name={g.name ?? g.component} from={Math.round(g.start * fps)} durationInFrames={dur} premountFor={fps}>
							<C dur={dur} {...g.props} />
						</Sequence>
					);
				})}
		</>
	);
};
