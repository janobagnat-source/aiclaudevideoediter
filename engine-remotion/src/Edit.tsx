import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BrandProvider} from './lib/brand';
import {AudioLayer} from './layers/AudioLayer';
import {BrollLayer} from './layers/BrollLayer';
import {Captions} from './layers/Captions';
import {FilmGrain, Letterbox, LightLeaks, Vignette} from './layers/FxLayer';
import {GraphicsLayer} from './layers/GraphicsLayer';
import {MainTrack, TransitionOverlays} from './layers/MainTrack';
import type {Edit as EditT} from './types';
import {LayoutBackdrop, LayoutFrame} from './layers/Layout';

/**
 * Composición maestra. Orden de capas (abajo → arriba):
 * fondo · track principal · gráficos "under" · b-roll · gráficos "over" · captions · gráficos "top" · fx · overlays de transición
 */
export const Edit: React.FC<{edit: EditT}> = ({edit}) => {
	return (
		<BrandProvider brand={edit.brand}>
			<AbsoluteFill style={{background: edit.background}}>
				<LayoutBackdrop layouts={edit.layouts ?? []} />
				<LayoutFrame layouts={edit.layouts ?? []}>
					<MainTrack cuts={edit.cuts} grade={edit.fx.grade} />
				</LayoutFrame>
				<GraphicsLayer items={edit.graphics} layer="under" />
				<BrollLayer items={edit.broll} grade={edit.fx.grade} />
				<GraphicsLayer items={edit.graphics} layer="over" />
				{edit.captions.enabled && <Captions cfg={edit.captions} />}
				<GraphicsLayer items={edit.graphics} layer="top" />
				<Vignette amount={edit.fx.vignette} />
				<FilmGrain amount={edit.fx.grain} />
				<Letterbox ratio={edit.fx.letterbox} />
				<LightLeaks cuts={edit.cuts} hue={edit.fx.lightLeakHue ?? 0} />
				<TransitionOverlays cuts={edit.cuts} color={edit.brand.colors.primary} />
				<AudioLayer sfx={edit.sfx} music={edit.music} speech={edit.speech} />
			</AbsoluteFill>
		</BrandProvider>
	);
};
