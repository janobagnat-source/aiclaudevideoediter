import {loadFont as loadLocal} from '@remotion/fonts';
import React, {createContext, useContext, useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';
import type {Edit} from '../types';

export type Brand = Edit['brand'];

const DEFAULT: Brand = {
	colors: {primary: '#ff3b30', secondary: '#ffd60a', accent: '#00e5ff', dark: '#0b0b0f', light: '#ffffff'},
	fonts: {heading: 'Montserrat', body: 'Inter'},
	fontFiles: [],
	logo: null,
};

const Ctx = createContext<Brand>(DEFAULT);
export const useBrand = () => useContext(Ctx);

const loaded = new Set<string>();

type FontEntry = {weight: string; style: string; subset: string; file: string};
let manifestP: Promise<Record<string, FontEntry[]>> | null = null;
const manifest = () => {
	if (!manifestP) {
		manifestP = fetch(staticFile('library/fonts/manifest.json'))
			.then((r) => (r.ok ? r.json() : {}))
			.catch(() => ({}));
	}
	return manifestP;
};

/** Carga una familia desde library/fonts (descargada con `ve font`). Solo subset latin (cubre español). */
const loadLibraryFont = async (family: string) => {
	if (loaded.has(family)) return;
	loaded.add(family);
	const m = await manifest();
	const key = Object.keys(m).find((k) => k.toLowerCase() === family.toLowerCase());
	if (!key) {
		console.warn(`Fuente "${family}" no está en library/fonts — corre: ./ve font "${family}"`);
		return;
	}
	await Promise.all(
		m[key]
			.filter((f) => f.subset === 'latin')
			.map((f) => loadLocal({family: key, url: staticFile(`library/fonts/${f.file}`), weight: f.weight, style: f.style})),
	);
};

const loadFiles = async (files: string[]) => {
	for (const f of files) {
		const name = f.split('/').pop()!.replace(/\.(ttf|otf|woff2?)$/i, '');
		// "Marca-Bold" -> familia "Marca", peso por sufijo
		const [family, style = 'Regular'] = name.split(/[-_ ](?=[^-_ ]+$)/);
		const w = /black|heavy/i.test(style) ? '900' : /extrabold/i.test(style) ? '800' : /bold/i.test(style) ? '700' : /semi/i.test(style) ? '600' : /medium/i.test(style) ? '500' : /light/i.test(style) ? '300' : '400';
		if (loaded.has(name)) continue;
		loaded.add(name);
		await loadLocal({family, url: staticFile(f), weight: w, style: /italic/i.test(style) ? 'italic' : 'normal'});
	}
};

export const BrandProvider: React.FC<{brand?: Partial<Brand>; children: React.ReactNode}> = ({brand, children}) => {
	const b: Brand = {
		...DEFAULT,
		...brand,
		colors: {...DEFAULT.colors, ...(brand?.colors ?? {})},
		fonts: {...DEFAULT.fonts, ...(brand?.fonts ?? {})},
	};
	const [handle] = useState(() => delayRender('Cargando fuentes de marca'));
	const [ready, setReady] = useState(false);
	useEffect(() => {
		Promise.all([loadFiles(b.fontFiles ?? []), loadLibraryFont(b.fonts.heading), loadLibraryFont(b.fonts.body), loadLibraryFont('Inter'), loadLibraryFont('Anton'), loadLibraryFont('Playfair Display')])
			.catch((e) => console.warn('fuentes', e))
			.finally(() => {
				setReady(true);
				continueRender(handle);
			});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);
	// los hijos se montan con las fuentes ya cargadas (fitText/measureText miden con la fuente real)
	return <Ctx.Provider value={b}>{ready ? children : null}</Ctx.Provider>;
};
