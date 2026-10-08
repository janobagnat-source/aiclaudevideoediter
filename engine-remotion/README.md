# engine-remotion

Motor de render del editor. No se edita a mano por video: cada proyecto genera `_work/edit.json`
(`./ve build`) y se renderiza con `scripts/render.mjs` (`./ve render`).

- `src/Edit.tsx` composición maestra (capas: track principal → gráficos → b-roll → captions → fx → audio)
- `src/layers/` MainTrack (zooms + transiciones + texto detrás del sujeto), Broll, Captions, Audio (ducking), Fx
- `src/graphics/` motion graphics 2D · `src/three/` 3D (R3F) · registro en `src/layers/GraphicsLayer.tsx`
- `src/Gallery.tsx` catálogo visual: `npx remotion still Gallery out.jpg --frame=40`
- `scripts/ttf2typeface.mjs` convierte fuentes de marca a JSON para texto 3D
- `public/clientes` y `public/library` son symlinks (los crea `./ve setup`)
