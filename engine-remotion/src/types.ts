// Contrato del timeline que genera tools/build.py (_work/edit.json). Todos los tiempos en SEGUNDOS de timeline.

export type ZoomKey = {t: number; s: number; ease?: 'smooth' | 'punch' | 'linear' | 'snap'; x?: number; y?: number; r?: number};

export type TransitionName =
	| 'cut'
	| 'flash'
	| 'whip'
	| 'whip-up'
	| 'zoom-in'
	| 'zoom-out'
	| 'glitch'
	| 'shake'
	| 'blur'
	| 'dip-black'
	| 'light-leak'
	| 'rgb-split';

export type Cut = {
	i: number;
	sentence: number;
	source: string;
	src: string;
	in: number;
	out: number;
	speed: number;
	tl_start: number;
	tl_end: number;
	text: string;
	section?: string | null;
	words_tl: Word[];
	zoom?: ZoomKey[] | null;
	focus: {x: number; y: number};
	transition?: TransitionName | {type: TransitionName; duration?: number; color?: string} | null;
	fx?: {bw?: boolean; shake?: number; blur?: number; grade?: string; mirror?: boolean} | null;
	mirror?: boolean;
	volume?: number;
	/** Video con alfa del sujeto recortado (ve cutout) para poner gráficos DETRÁS de la persona */
	cutout?: string | null;
	/** Gráficos entre el fondo y el sujeto. start/duration en segundos relativos al corte */
	behind?: {component: string; start?: number; duration?: number; props: Record<string, unknown>}[];
};

export type Word = {text: string; start: number; end: number};

export type Broll = {
	src: string;
	start: number;
	duration: number;
	in: number;
	isImage: boolean;
	srcDuration?: number;
	mode?: 'full' | 'pip' | 'split-top' | 'split-bottom' | 'card' | 'circle';
	kenburns?: 'in' | 'out' | 'left' | 'right' | 'up' | 'none';
	transition?: TransitionName;
	speed?: number;
	volume?: number;
	grade?: string;
	focus?: {x: number; y: number};
	label?: string;
};

export type Graphic = {
	component: string;
	start: number;
	duration: number;
	props: Record<string, unknown>;
	layer?: 'under' | 'over' | 'top';
	name?: string;
};

export type Sfx = {src: string; start: number; volume: number; trim?: [number, number] | null; duck?: number};

export type Music = {
	src: string;
	start: number;
	in: number;
	duration: number;
	volume: number;
	duck: number;
	fadeIn: number;
	fadeOut: number;
};

export type BrandColors = {primary: string; secondary: string; accent: string; dark: string; light: string; [k: string]: string};

export type Edit = {
	id: string;
	width: number;
	height: number;
	fps: number;
	durationInFrames: number;
	brand: {colors: BrandColors; fonts: {heading: string; body: string}; fontFiles: string[]; logo: string | null};
	cuts: Cut[];
	broll: Broll[];
	graphics: Graphic[];
	sfx: Sfx[];
	music: Music[];
	speech: [number, number][];
	layouts?: Layout[];
	captions: {
		enabled: boolean;
		style: 'bold-pop' | 'karaoke' | 'minimal' | 'boxed' | 'neon' | 'serif-elegant' | 'premium';
		emphasis: string[];
		position: number;
		maxWords: number;
		uppercase: boolean;
		hideDuring: [number, number][];
		positionDuring?: [number, number, number][];
		words: Word[];
	};
	fx: {grain: number; vignette: number; grade: string; chromatic: number; letterbox?: number; lightLeaks?: boolean; lightLeakHue?: number};
	background: string;
};

/** Reacomodo del track principal. split: Carlos en una ventana superior (top..bottom, fracción de alto), gráficos abajo */
export type Layout = {start: number; duration: number; mode: 'split' | 'card'; bottom?: number; top?: number; radius?: number; border?: string; scale?: number; ease?: number};
