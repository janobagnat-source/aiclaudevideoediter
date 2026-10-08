// Elementos 3D (React Three Fiber). Reglas Remotion: toda animación derivada de useCurrentFrame(), nunca useFrame().
import {Center, Environment, Lightformer, RoundedBox, useGLTF} from '@react-three/drei';
import {ThreeCanvas, useOffthreadVideoTexture} from '@remotion/three';
import React, {Suspense, useEffect, useMemo, useState} from 'react';
import {continueRender, delayRender, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {SVGLoader} from 'three/examples/jsm/loaders/SVGLoader.js';
import {FontLoader, type Font} from 'three/examples/jsm/loaders/FontLoader.js';
import {TextGeometry} from 'three/examples/jsm/geometries/TextGeometry.js';
import {clamp, EASE} from '../lib/anim';
import {useBrand} from '../lib/brand';
import type {GProps} from '../graphics/text';

const url = (s: string) => (s.startsWith('http') ? s : staticFile(s));

/** Iluminación de estudio procedural (sin descargar HDRIs): key, rim en color de marca y reflejos. */
const StudioLights: React.FC<{rim?: string; rim2?: string; intensity?: number}> = ({rim = '#ff3b30', rim2 = '#00e5ff', intensity = 1}) => (
	<>
		<ambientLight intensity={0.25 * intensity} />
		<directionalLight position={[4, 6, 6]} intensity={2.2 * intensity} />
		<pointLight position={[-6, 2, -3]} intensity={60 * intensity} color={rim} distance={30} />
		<pointLight position={[6, -2, -3]} intensity={50 * intensity} color={rim2} distance={30} />
		<Environment resolution={256} frames={1}>
			<Lightformer form="rect" intensity={3} position={[0, 5, -4]} scale={[10, 2, 1]} />
			<Lightformer form="rect" intensity={2} color={rim} position={[-5, 1, 2]} rotation-y={Math.PI / 2} scale={[6, 1, 1]} />
			<Lightformer form="rect" intensity={2} color={rim2} position={[5, 1, 2]} rotation-y={-Math.PI / 2} scale={[6, 1, 1]} />
			<Lightformer form="ring" intensity={1.5} position={[0, 0, 6]} scale={3} />
		</Environment>
	</>
);

const Canvas3D: React.FC<{children: React.ReactNode; fov?: number; z?: number; bg?: string}> = ({children, fov = 35, z = 8, bg}) => {
	const {width, height} = useVideoConfig();
	return (
		<ThreeCanvas width={width} height={height} camera={{fov, position: [0, 0, z]}} gl={{antialias: true, preserveDrawingBuffer: true, alpha: !bg}} style={{position: 'absolute', inset: 0, background: bg}}>
			<Suspense fallback={null}>{children}</Suspense>
		</ThreeCanvas>
	);
};

const useEntry = (dur: number) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame, fps, config: {damping: 14, stiffness: 90, mass: 1}});
	const out = interpolate(frame, [dur - 10, dur], [1, 0], {...clamp, easing: EASE.in});
	return {frame, s, out};
};

// ---------------------------------------------------------------- Modelo glTF (Poly Haven / Sketchfab / cliente)
const ModelInner: React.FC<{model: string; dur: number; scale: number; spin: number; y: number; tilt: number}> = ({model, dur, scale, spin, y, tilt}) => {
	const {scene} = useGLTF(url(model));
	const {frame, s, out} = useEntry(dur);
	const fitted = useMemo(() => {
		const c = scene.clone(true);
		const box = new THREE.Box3().setFromObject(c);
		const size = box.getSize(new THREE.Vector3()).length() || 1;
		const center = box.getCenter(new THREE.Vector3());
		c.position.sub(center);
		const g = new THREE.Group();
		g.add(c);
		g.scale.setScalar(4 / size);
		return g;
	}, [scene]);
	return (
		<group position={[0, y + Math.sin(frame / 25) * 0.08, 0]} scale={scale * s * out} rotation={[tilt, (1 - s) * -Math.PI + frame * spin, 0]}>
			<primitive object={fitted} />
		</group>
	);
};

/** props: model (ruta .gltf/.glb), scale, spin (rad/frame), y, tilt, x (0-1 pos pantalla) */
export const Model3D: React.FC<GProps & {model: string; scale?: number; spin?: number; y?: number; tilt?: number; bg?: string}> = ({dur, model, scale = 1, spin = 0.012, y = 0, tilt = 0.15, bg}) => {
	const {colors} = useBrand();
	return (
		<Canvas3D bg={bg}>
			<StudioLights rim={colors.primary} rim2={colors.accent} />
			<ModelInner model={model} dur={dur} scale={scale} spin={spin} y={y} tilt={tilt} />
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Logo SVG extruido
const useSvgShapes = (svgUrl: string | null) => {
	const [data, setData] = useState<{shapes: THREE.Shape[]; color: string}[] | null>(null);
	const [handle] = useState(() => delayRender('Cargando SVG para Logo3D'));
	useEffect(() => {
		if (!svgUrl) {
			continueRender(handle);
			return;
		}
		fetch(svgUrl)
			.then((r) => r.text())
			.then((txt) => {
				const parsed = new SVGLoader().parse(txt);
				setData(parsed.paths.map((p) => ({shapes: SVGLoader.createShapes(p), color: (p.color as THREE.Color)?.getStyle?.() ?? '#ffffff'})));
			})
			.catch((e) => console.warn(e))
			.finally(() => continueRender(handle));
	}, [svgUrl, handle]);
	return data;
};

/** Logo de marca en 3D desde SVG. props: svg (ruta .svg), depth, metal (0-1), color ('brand'|'original'|hex), spin */
export const Logo3D: React.FC<GProps & {svg: string; depth?: number; metal?: number; color?: string; spin?: number; scale?: number; bg?: string}> = ({dur, svg, depth = 40, metal = 0.6, color = 'original', spin = 0.004, scale = 1, bg}) => {
	const {colors} = useBrand();
	const paths = useSvgShapes(svg ? url(svg) : null);
	const {frame, s, out} = useEntry(dur);
	const geo = useMemo(() => {
		if (!paths) return null;
		return paths.map((p) => ({
			geom: new THREE.ExtrudeGeometry(p.shapes, {depth, bevelEnabled: true, bevelThickness: depth * 0.18, bevelSize: depth * 0.08, bevelSegments: 6, curveSegments: 24}),
			color: color === 'original' ? p.color : color === 'brand' ? colors.primary : color,
		}));
	}, [paths, depth, color, colors.primary]);
	const bbox = useMemo(() => {
		if (!geo) return null;
		const b = new THREE.Box3();
		geo.forEach((g) => {
			g.geom.computeBoundingBox();
			b.union(g.geom.boundingBox!);
		});
		return b;
	}, [geo]);
	if (!geo || !bbox) return null;
	const size = bbox.getSize(new THREE.Vector3());
	const k = (5 / Math.max(size.x, size.y)) * scale;
	const c = bbox.getCenter(new THREE.Vector3());
	return (
		<Canvas3D bg={bg}>
			<StudioLights rim={colors.primary} rim2={colors.accent} intensity={1.2} />
			<group scale={k * s * out} rotation={[(1 - s) * 0.8 + Math.sin(frame / 40) * 0.08, (1 - s) * Math.PI * 1.5 + Math.sin(frame * spin * 6) * 0.35, 0]}>
				<group scale={[1, -1, 1]} position={[-c.x * 1, c.y * 1, -depth / 2]}>
					{geo.map((g, i) => (
						<mesh key={i} geometry={g.geom}>
							<meshPhysicalMaterial color={g.color} metalness={metal} roughness={0.22} clearcoat={1} clearcoatRoughness={0.1} />
						</mesh>
					))}
				</group>
			</group>
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Texto 3D extruido
const useFont3D = (fontUrl: string) => {
	const [font, setFont] = useState<Font | null>(null);
	const [h] = useState(() => delayRender('Cargando fuente 3D'));
	useEffect(() => {
		fetch(fontUrl)
			.then((r) => r.json())
			.then((j) => setFont(new FontLoader().parse(j)))
			.catch((e) => console.warn('fuente 3D', e))
			.finally(() => continueRender(h));
	}, [fontUrl, h]);
	return font;
};

/** props: text (\n = salto), font ('Montserrat-Black'|'Anton'|ruta typeface.json — `ve font X --3d`), color, metal, size, y, depth */
export const Text3DTitle: React.FC<GProps & {text: string; font?: string; color?: string; metal?: number; size?: number; y?: number; bg?: string; depth?: number}> = ({dur, text, font = 'Montserrat-Black', color, metal = 0.4, size = 1, y = 0, bg, depth = 0.35}) => {
	const {colors} = useBrand();
	const {frame, s, out} = useEntry(dur);
	const fontUrl = font.endsWith('.json') ? url(font) : staticFile(`fonts3d/${font}.typeface.json`);
	const f = useFont3D(fontUrl);
	const lines = text.toUpperCase().split('\n');
	const geos = useMemo(
		() => (f ? lines.map((ln) => new TextGeometry(ln, {font: f, size, depth, curveSegments: 10, bevelEnabled: true, bevelThickness: 0.04, bevelSize: 0.025, bevelSegments: 4})) : []),
		// eslint-disable-next-line react-hooks/exhaustive-deps
		[f, text, size, depth],
	);
	const {width, height} = useVideoConfig();
	const visW = 2 * Math.tan((35 / 2) * (Math.PI / 180)) * 10 * (width / height);
	const maxW = Math.max(
		0.001,
		...geos.map((g) => {
			g.computeBoundingBox();
			return g.boundingBox!.max.x - g.boundingBox!.min.x;
		}),
	);
	const fit = Math.min(1, (0.84 * visW) / maxW);
	return (
		<Canvas3D bg={bg} z={10}>
			<StudioLights rim={colors.primary} rim2={colors.accent} intensity={1.1} />
			<group position={[0, y, 0]} rotation={[(1 - s) * -1.2 + Math.sin(frame / 50) * 0.06, Math.sin(frame / 45) * 0.18, 0]} scale={s * out * fit}>
				{geos.map((g, i) => (
					<Center key={i} position={[0, (lines.length / 2 - i - 0.5) * 1.3 * size, 0]}>
						<mesh geometry={g}>
							<meshPhysicalMaterial color={color ?? colors.light} metalness={metal} roughness={0.25} clearcoat={1} />
						</mesh>
					</Center>
				))}
			</group>
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Partículas / hiperespacio
/** Campo de partículas con dolly de cámara. props: count, speed, mode 'float'|'warp', bg */
export const Particles3D: React.FC<GProps & {count?: number; speed?: number; mode?: 'float' | 'warp'; bg?: string}> = ({dur, count = 600, speed = 1, mode = 'float', bg}) => {
	const {colors} = useBrand();
	const frame = useCurrentFrame();
	const out = interpolate(frame, [dur - 10, dur], [1, 0], clamp);
	const pts = useMemo(
		() =>
			Array.from({length: count}, (_, i) => ({
				x: (random(`x${i}`) - 0.5) * 24,
				y: (random(`y${i}`) - 0.5) * 24,
				z: -random(`z${i}`) * 60,
				s: 0.02 + random(`s${i}`) * 0.07,
				c: [colors.primary, colors.secondary, colors.accent, colors.light][i % 4],
			})),
		[count, colors.primary, colors.secondary, colors.accent, colors.light],
	);
	const travel = frame * (mode === 'warp' ? 0.9 : 0.06) * speed;
	return (
		<Canvas3D bg={bg} fov={60} z={6}>
			<ambientLight intensity={1} />
			{pts.map((p, i) => {
				const z = ((p.z + travel + 60) % 60) - 55;
				const stretch = mode === 'warp' ? 1 + speed * 25 * (1 - Math.abs(z) / 60) : 1;
				return (
					<mesh key={i} position={[p.x, p.y + (mode === 'float' ? Math.sin(frame / 30 + i) * 0.2 : 0), z]} scale={[p.s, p.s, p.s * stretch]}>
						<sphereGeometry args={[1, 8, 8]} />
						<meshBasicMaterial color={p.c} transparent opacity={out * Math.min(1, (z + 55) / 15)} />
					</mesh>
				);
			})}
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Formas premium flotantes (fondo de escenas MG)
/** props: count, bg, variant 'glossy'|'glass'|'metal' */
export const Shapes3D: React.FC<GProps & {count?: number; bg?: string; variant?: 'glossy' | 'glass' | 'metal'}> = ({dur, count = 7, bg, variant = 'glossy'}) => {
	const {colors} = useBrand();
	const {frame, s, out} = useEntry(dur);
	const kinds = ['torus', 'ico', 'sphere', 'box', 'torusKnot', 'cone', 'capsule'];
	return (
		<Canvas3D bg={bg} z={12}>
			<StudioLights rim={colors.primary} rim2={colors.accent} />
			{Array.from({length: count}, (_, i) => {
				const k = kinds[i % kinds.length];
				const px = (random(`px${i}`) - 0.5) * 9;
				const py = (random(`py${i}`) - 0.5) * 12;
				const pz = -random(`pz${i}`) * 6;
				const rs = 0.5 + random(`r${i}`) * 0.9;
				const c = [colors.primary, colors.secondary, colors.accent, colors.light][i % 4];
				const ent = interpolate(s, [0, 1], [0, 1]);
				return (
					<mesh key={i} position={[px, py + Math.sin(frame / 35 + i) * 0.4, pz]} rotation={[frame * 0.01 * (i % 2 ? 1 : -1), frame * 0.013, i]} scale={rs * ent * out}>
						{k === 'torus' && <torusGeometry args={[0.8, 0.32, 48, 96]} />}
						{k === 'ico' && <icosahedronGeometry args={[1, 0]} />}
						{k === 'sphere' && <sphereGeometry args={[0.9, 64, 64]} />}
						{k === 'box' && <boxGeometry args={[1.3, 1.3, 1.3]} />}
						{k === 'torusKnot' && <torusKnotGeometry args={[0.6, 0.22, 160, 24]} />}
						{k === 'cone' && <coneGeometry args={[0.8, 1.6, 48]} />}
						{k === 'capsule' && <capsuleGeometry args={[0.5, 1, 16, 32]} />}
						<meshPhysicalMaterial color={c} metalness={variant === 'metal' ? 1 : 0.1} roughness={variant === 'glass' ? 0.05 : 0.2} clearcoat={1} transmission={variant === 'glass' ? 0.9 : 0} thickness={1} ior={1.4} />
					</mesh>
				);
			})}
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Teléfono 3D con pantalla (imagen o video)
const PhoneScreenVideo: React.FC<{src: string}> = ({src}) => {
	const tex = useOffthreadVideoTexture({src: url(src)});
	return <meshBasicMaterial map={tex} toneMapped={false} />;
};
const PhoneScreenImage: React.FC<{src: string}> = ({src}) => {
	const [tex, setTex] = useState<THREE.Texture | null>(null);
	const [h] = useState(() => delayRender('textura teléfono'));
	useEffect(() => {
		new THREE.TextureLoader().load(
			url(src),
			(t) => {
				t.colorSpace = THREE.SRGBColorSpace;
				setTex(t);
				continueRender(h);
			},
			undefined,
			() => continueRender(h),
		);
	}, [src, h]);
	return <meshBasicMaterial map={tex} toneMapped={false} />;
};

/** Mockup de celular 3D que entra girando. props: screen (img o video), x, rotate, scale, body color */
export const Phone3D: React.FC<GProps & {screen: string; x?: number; scale?: number; body?: string; turn?: number; bg?: string}> = ({dur, screen, x = 0, scale = 1, body = '#111214', turn = 0.35, bg}) => {
	const {colors} = useBrand();
	const {frame, s, out} = useEntry(dur);
	const isVideo = /\.(mp4|mov|webm)$/i.test(screen);
	const W = 2.2;
	const H = 4.6;
	return (
		<Canvas3D bg={bg} z={9}>
			<StudioLights rim={colors.primary} rim2={colors.accent} />
			<group position={[x, (1 - s) * -6, 0]} rotation={[0.08 + Math.sin(frame / 40) * 0.04, (1 - s) * Math.PI * 1.2 + Math.sin(frame / 50) * turn, (1 - s) * 0.3]} scale={scale * out}>
				<RoundedBox args={[W + 0.16, H + 0.16, 0.28]} radius={0.3} smoothness={8}>
					<meshPhysicalMaterial color={body} metalness={0.8} roughness={0.25} clearcoat={1} />
				</RoundedBox>
				<mesh position={[0, 0, 0.145]}>
					<planeGeometry args={[W, H]} />
					{isVideo ? <PhoneScreenVideo src={screen} /> : <PhoneScreenImage src={screen} />}
				</mesh>
			</group>
		</Canvas3D>
	);
};

// ---------------------------------------------------------------- Monedas doradas 3D
/** Monedas de oro 3D. mode: 'rain' (caen de arriba), 'fountain' (saltan desde abajo y caen), 'drain' (caen y se van).
 * props: count, mode, xMin/xMax (0-1, zona horizontal permitida — evitar la cara), yMin (0-1 límite superior de aparición), size */
export const Coins3D: React.FC<GProps & {count?: number; mode?: 'rain' | 'fountain' | 'drain'; xMin?: number; xMax?: number; avoid?: [number, number]; yTop?: number; size?: number}> = ({dur, count = 26, mode = 'rain', xMin = 0, xMax = 1, avoid, yTop = 0, size = 1}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const aspect = width / height;
	const z = 10;
	const visH = 2 * Math.tan((35 / 2) * (Math.PI / 180)) * z;
	const visW = visH * aspect;
	const coins = useMemo(
		() =>
			Array.from({length: count}, (_, i) => {
				let xr = xMin + random(`cx${i}`) * (xMax - xMin);
				if (avoid && xr > avoid[0] && xr < avoid[1]) xr = random(`cs${i}`) > 0.5 ? avoid[0] - random(`ca${i}`) * 0.15 : avoid[1] + random(`cb${i}`) * 0.15;
				return {x: (xr - 0.5) * visW, delay: random(`cd${i}`) * (mode === 'fountain' ? 10 : 22), vx: (random(`vx${i}`) - 0.5) * 2, vy: 9 + random(`vy${i}`) * 6, spin: 4 + random(`sp${i}`) * 8, ax: random(`ax${i}`) * Math.PI, s: (0.32 + random(`ss${i}`) * 0.22) * size, zz: -random(`zz${i}`) * 4};
			}),
		[count, xMin, xMax, avoid, visW, mode, size],
	);
	const out = interpolate(frame, [dur - 8, dur], [1, 0], clamp);
	return (
		<Canvas3D z={z}>
			<ambientLight intensity={0.5} />
			<directionalLight position={[3, 5, 6]} intensity={3} />
			<pointLight position={[-4, 2, 4]} intensity={40} color="#ffd36b" />
			<Environment resolution={128} frames={1}>
				<Lightformer form="rect" intensity={4} position={[0, 5, -3]} scale={[10, 2, 1]} />
				<Lightformer form="rect" intensity={2} color="#3474FF" position={[-5, 0, 2]} rotation-y={Math.PI / 2} scale={[6, 2, 1]} />
				<Lightformer form="ring" intensity={2} position={[0, 0, 6]} scale={4} />
			</Environment>
			{coins.map((c, i) => {
				const t = Math.max(0, (frame - c.delay) / fps);
				if (frame < c.delay) return null;
				let y: number;
				let x = c.x;
				if (mode === 'fountain') {
					y = -visH / 2 - 1 + c.vy * t - 0.5 * 18 * t * t;
					x = c.x + c.vx * t;
				} else {
					const top = visH / 2 - yTop * visH + 1.2;
					y = top - 0.5 * 14 * t * t - 1.5 * t;
					if (mode === 'drain') x = c.x * (1 - t * 0.3);
				}
				return (
					<group key={i} position={[x, y, c.zz]} rotation={[c.ax + t * c.spin, t * c.spin * 0.7, t * 1.3]} scale={c.s * out}>
						<mesh rotation={[Math.PI / 2, 0, 0]}>
							<cylinderGeometry args={[1, 1, 0.16, 48]} />
							<meshPhysicalMaterial color="#ffc42e" metalness={0.85} roughness={0.28} clearcoat={1} emissive="#6b4700" emissiveIntensity={0.35} envMapIntensity={1.6} />
						</mesh>
						<mesh position={[0, 0, 0.085]}>
							<torusGeometry args={[0.78, 0.05, 12, 48]} />
							<meshPhysicalMaterial color="#fff0b0" metalness={1} roughness={0.15} />
						</mesh>
						<mesh position={[0, 0, -0.085]}>
							<torusGeometry args={[0.78, 0.05, 12, 48]} />
							<meshPhysicalMaterial color="#fff0b0" metalness={1} roughness={0.15} />
						</mesh>
					</group>
				);
			})}
		</Canvas3D>
	);
};
