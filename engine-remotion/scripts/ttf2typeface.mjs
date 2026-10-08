// Convierte una fuente TTF/OTF (p.ej. la tipografía de marca) a typeface.json para texto 3D extruido (Text3D).
// uso: node scripts/ttf2typeface.mjs <fuente.ttf> <salida.typeface.json>
import fs from 'node:fs';
import opentype from 'opentype.js';

const [, , input, output] = process.argv;
if (!input || !output) {
	console.error('uso: node scripts/ttf2typeface.mjs <fuente.ttf> <salida.json>');
	process.exit(1);
}
const font = opentype.loadSync(input);
const scale = (1000 * 100) / ((font.unitsPerEm || 2048) * 72);
const r = (n) => Math.round(n * scale);
const glyphs = {};
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚÜÑáéíóúüñ0123456789 .,;:!¡?¿%$€#@&+-=*/()[]"\'«»“”·–—_';
for (const ch of chars) {
	const g = font.charToGlyph(ch);
	if (!g) continue;
	let o = '';
	for (const c of g.path.commands) {
		if (c.type === 'M') o += `m ${r(c.x)} ${r(c.y)} `;
		else if (c.type === 'L') o += `l ${r(c.x)} ${r(c.y)} `;
		else if (c.type === 'Q') o += `q ${r(c.x)} ${r(c.y)} ${r(c.x1)} ${r(c.y1)} `;
		else if (c.type === 'C') o += `b ${r(c.x)} ${r(c.y)} ${r(c.x1)} ${r(c.y1)} ${r(c.x2)} ${r(c.y2)} `;
	}
	const bb = g.getBoundingBox();
	glyphs[ch] = {ha: r(g.advanceWidth), x_min: r(bb.x1), x_max: r(bb.x2), o};
}
const out = {
	glyphs,
	familyName: font.names.fontFamily?.en ?? 'Brand',
	ascender: r(font.ascender),
	descender: r(font.descender),
	underlinePosition: r(font.tables.post?.underlinePosition ?? -100),
	underlineThickness: r(font.tables.post?.underlineThickness ?? 50),
	boundingBox: {yMin: r(font.tables.head.yMin), xMin: r(font.tables.head.xMin), yMax: r(font.tables.head.yMax), xMax: r(font.tables.head.xMax)},
	resolution: 1000,
	original_font_information: {},
};
fs.writeFileSync(output, JSON.stringify(out));
console.log(output);
