// Render headless del timeline: node scripts/render.mjs <edit.json> <out.mp4> [--still=seg] [--frames=a-b] [--scale=0.5]
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const [, , editPath, outPath, ...rest] = process.argv;
const opts = Object.fromEntries(rest.map((a) => a.replace(/^--/, '').split('=')));
if (!editPath || !outPath) {
	console.error('uso: node scripts/render.mjs <edit.json> <out.mp4> [--still=12.5] [--frames=0-90] [--scale=0.5] [--crf=16]');
	process.exit(1);
}
const edit = JSON.parse(fs.readFileSync(editPath, 'utf8'));
const chromiumOptions = {gl: process.env.REMOTION_GL || 'swangle', enableMultiProcessOnLinux: true};

const t0 = Date.now();
const serveUrl = await bundle({
	entryPoint: path.join(root, 'src/index.ts'),
	publicDir: path.join(root, 'public'),
	symlinkPublicDir: true,
	onProgress: () => undefined,
});
const composition = await selectComposition({serveUrl, id: 'Edit', inputProps: {edit}, chromiumOptions});
const scale = opts.scale ? Number(opts.scale) : 1;

if (opts.still !== undefined) {
	const stills = String(opts.still).split(',').map(Number);
	for (const s of stills) {
		const frame = Math.min(composition.durationInFrames - 1, Math.round(s * composition.fps));
		const out = stills.length > 1 ? outPath.replace(/(\.\w+)$/, `_${s.toFixed(2)}s$1`) : outPath;
		await renderStill({composition, serveUrl, output: out, frame, inputProps: {edit}, chromiumOptions, scale, imageFormat: 'jpeg', jpegQuality: 88});
		console.log(out);
	}
	process.exit(0);
}

if (opts.audio !== undefined) {
	await renderMedia({composition, serveUrl, codec: 'wav', outputLocation: outPath, inputProps: {edit}, chromiumOptions, concurrency: 3, timeoutInMilliseconds: 180000});
	console.log(outPath);
	process.exit(0);
}

let lastPct = -10;
await renderMedia({
	composition,
	serveUrl,
	codec: 'h264',
	outputLocation: outPath,
	inputProps: {edit},
	chromiumOptions,
	scale,
	crf: opts.crf ? Number(opts.crf) : 16,
	x264Preset: opts.preset || 'medium',
	pixelFormat: 'yuv420p',
	colorSpace: 'bt709',
	audioCodec: 'aac',
	audioBitrate: '320k',
	concurrency: opts.concurrency ? Number(opts.concurrency) : Math.max(1, os.cpus().length),
	frameRange: opts.frames ? opts.frames.split('-').map(Number) : null,
	offthreadVideoCacheSizeInBytes: 2 * 1024 * 1024 * 1024,
	timeoutInMilliseconds: 120000,
	onProgress: ({progress, renderedFrames, encodedFrames}) => {
		const pct = Math.floor(progress * 100);
		if (pct >= lastPct + 5) {
			lastPct = pct;
			console.error(`[render] ${pct}% (${renderedFrames} render / ${encodedFrames} enc) ${((Date.now() - t0) / 1000).toFixed(0)}s`);
		}
	},
});
console.log(outPath);
