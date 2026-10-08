// Demo de toda la librería de gráficos (sirve de catálogo visual y de test de render).
import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {BrandProvider} from './lib/brand';
import {REGISTRY} from './layers/GraphicsLayer';
import {FilmGrain, Vignette} from './layers/FxLayer';

const D = 75;
const DEMOS: [string, Record<string, unknown>][] = [
	['HookTitle', {lines: ['El error que', 'te cuesta', 'miles de $'], highlight: ['miles'], bg: 'brand', variant: 'slam'}],
	['KineticText', {text: 'Tu negocio merece crecer sin límites', emphasis: ['crecer'], position: 0.45}],
	['StatCounter', {value: 327, suffix: '%', label: 'más ventas'}],
	['Checklist', {title: 'Lo que incluye', items: ['Plan a medida', 'Soporte 24/7', 'Resultados en 30 días']}],
	['BarChart', {title: 'Ventas mensuales', bars: [{label: 'Ene', value: 20}, {label: 'Feb', value: 35}, {label: 'Mar', value: 50}, {label: 'Abr', value: 92, highlight: true}], unit: 'k'}],
	['Testimonial', {quote: 'En 2 meses tripliqué mi facturación. No lo podía creer.', author: 'Laura M.'}],
	['Text3DTitle', {text: 'ESCALÁ\nHOY', bg: '#0b0b0f'}],
	['Shapes3D', {bg: '#0b0b0f'}],
	['Particles3D', {mode: 'warp', speed: 1.2, bg: '#05050a'}],
	['CTAEndCard', {headline: 'Reservá tu llamada gratis', sub: 'Cupos limitados esta semana', button: 'Quiero mi lugar'}],
];
export const GALLERY_DURATION = DEMOS.length * D;

export const Gallery: React.FC = () => (
	<BrandProvider>
		<AbsoluteFill style={{background: 'linear-gradient(160deg,#1a1a2e,#0b0b0f)'}}>
			{DEMOS.map(([name, props], i) => {
				const C = REGISTRY[name];
				return (
					<Sequence key={name} name={name} from={i * D} durationInFrames={D}>
						{name === 'Testimonial' || name === 'Checklist' ? <REGISTRY.BrandBackground dur={D} variant="grid" /> : null}
						<C dur={D} {...props} />
						{name === 'StatCounter' ? <REGISTRY.OfferBadge dur={D} text="-50%" sub="hoy" /> : null}
						{name === 'KineticText' ? <REGISTRY.Notification dur={D} title="Nueva venta 🎉" body="Martín compró el plan Pro — $497" /> : null}
					</Sequence>
				);
			})}
			<Vignette amount={0.25} />
			<FilmGrain amount={0.04} />
		</AbsoluteFill>
	</BrandProvider>
);
