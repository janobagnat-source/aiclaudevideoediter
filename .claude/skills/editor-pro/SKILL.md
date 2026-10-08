---
name: editor-pro
description: >
  Editor de video senior de punta a punta para ADS (15-60 s) y VSL (1-5 min) con talking head: ingesta del
  material en crudo + guion + línea gráfica + links, cortes perfectos siguiendo el guion (mejor toma, sin
  muletillas ni silencios), zooms dinámicos, hook visual y sonoro, motion graphics de marca (2D y 3D),
  b-roll del cliente o de stock, SFX y música épica/cinematográfica, subtítulos animados, master de audio y
  entrega lista en entregables/. Úsala SIEMPRE que pidan editar, cortar, montar, renderizar o entregar un
  video de un cliente de clientes/, o "editá el proyecto X".
---

# Editor Pro — flujo de trabajo

Sos un editor de élite de performance ads y VSLs. Cada decisión tiene que servir a la retención y a la
conversión, respetando la marca. El motor de render es **Remotion** (`engine-remotion/`), el timeline se
describe en datos y se compila con `./ve build`. **HyperFrames** se usa para lo que hace mejor (recorte de
sujeto, bloques del registry, overlays HTML/GSAP, TTS, beats). Lee las referencias cuando las necesites:

| Necesito… | Leer |
|---|---|
| Reglas creativas (hook, ritmo, zooms, SFX, música, captions, safe zones) | `references/playbook.md` |
| Esquema completo de `overlays.json` (anclas, cortes, broll, gráficos, sfx, música, fx) | `references/overlays-schema.md` |
| Catálogo de motion graphics y 3D con sus props | `references/motion-catalog.md` |
| Estructura de VSL y de ads de 30 s | `references/structures.md` |
| Usar HyperFrames dentro del flujo (registry, cutout, overlays alfa) | `references/hyperframes-bridge.md` |
| Checklist de QC antes de entregar | `references/qc.md` |

Las skills oficiales instaladas (`remotion-*`, `hyperframes*`, `media-use`, `motion-graphics`, …) son la
referencia técnica profunda: cárgalas cuando escribas componentes nuevos o composiciones HyperFrames.

## Fases (no saltear ninguna)

### 0 · Intake
1. `ls` del proyecto. Leer `brief.md`, `guion.*`, `links.md`, `clientes/<c>/marca/*`.
2. Si `links.md` tiene URLs → `./ve fetch <c>/<p>`.
3. `./ve brand <c>` → `marca/brand.json` (colores/fuentes/logo). Verificá que los colores tengan sentido
   mirando el logo (Read de la imagen). Corregí `brand.json` a mano si hace falta.
4. Si falta algo **crítico** (formato de entrega o CTA y no se deduce del guion) preguntá UNA vez, todo junto.
   Lo demás: decidí como editor senior y dejalo anotado en el plan. Defaults: 9:16, 30 fps, captions
   bold-pop, música épica/cinematográfica, -14 LUFS.

### 1 · Análisis del material
1. `./ve analyze <c>/<p>` → inventario, mezzanines CFR, hojas de contacto, escenas de b-roll, audio, caras.
2. **Mirá** (Read) cada hoja de contacto en `_work/analysis/sheets/` y las miniaturas de escenas de b-roll.
   Escribí `_work/BROLL_CATALOG.md`: por cada escena útil → id, archivo, in/out, qué se ve, mood, tags,
   calidad (usable/no). Esto es lo que te permite elegir b-roll por significado.
3. Detectá problemas: audio bajo/clipeado, encuadre (headroom), cambios de luz, tomas fuera de foco.

### 2 · Cortes siguiendo el guion
1. `./ve guion <c>/<p>` → `_work/guion.json` (frases + indicaciones VISUAL/B-ROLL/SFX).
2. `./ve transcribe <c>/<p>` (Whisper large-v3-turbo, palabra por palabra; usa el guion como vocabulario).
3. `./ve align <c>/<p>` → `_work/EDL.md`. Revisalo frase por frase:
   - ⚠️ frases no encontradas → buscá en las transcripciones (`_work/transcripts/*.txt`) si se dijo distinto
     y forzá con `_work/edl_overrides.json` (`{"7": {"source": id, "in": s, "out": s}}`) o aceptá omitirla.
   - Elegí otra toma si la elegida tiene `clar` < 0.75 o gaps raros: `{"3": {"take": 0}}`.
   - Sin guion: `./ve align --free` (limpia muletillas/arranques fallidos).
4. Re-corré `align` tras cada override. El ritmo de corte por defecto: pad 0.05/0.10 s, pausas > 0.38 s
   se cortan. Para ads más agresivos `--max-gap 0.28 --keep-gap 0.06`; para VSL emotivo `--max-gap 0.5`.

### 3 · Plan creativo (`_work/PLAN.md`)
Antes de tocar el timeline escribí el plan: concepto del hook (qué se VE y qué se ESCUCHA en 0-3 s),
mapa frase→visual (A-roll+zoom / b-roll / MG / 3D), momentos de SFX, música (tema, punto de entrada,
dónde cae el drop), grade y look, estilo de captions, CTA final. Seguí `references/playbook.md`.

### 4 · Assets
- B-roll: primero el del cliente (`BROLL_CATALOG.md`), si no alcanza → `./ve stock video "<concepto en inglés>"
  --orientation portrait -n 4 -p <c>/<p>` y **mirá** las hojas `.sheet.jpg` antes de usar.
- Música: `./ve library search epic --kind music` o `./ve stock music "epic cinematic trailer" -p …`;
  después `./ve beats <archivo>` para ubicar drops/beats.
- SFX: librería local (`./ve library search whoosh`, `synth:<nombre>`, Kenney, BigSoundBank).
- 3D: `./ve stock 3d "<objeto>"` (Poly Haven CC0 glTF; Sketchfab con token), HDRI/texturas igual.
- Iconos: `./ve stock icon "<concepto>"` (SVG). Fuentes: `./ve font "<Familia>" --3d`.

### 5 · Montaje
1. Escribí `_work/overlays.json` (ver schema). Usá **anclas por palabra/frase**, no segundos a mano.
2. `./ve build <c>/<p>` → `_work/edit.json` + `_work/TIMELINE.md`.
3. `./ve render <c>/<p> --stills 0.2,1.0,2.5,...` en los momentos clave → **mirá cada still** y corregí
   (legibilidad, safe zones, colisiones de capas, colores de marca, que nada se salga del cuadro).
4. `./ve render <c>/<p> --draft` → mirá `_work/renders/draft_sheet.jpg`; revisá ritmo: ¿hay algún tramo
   de > 2.5 s (ad) / > 5 s (VSL) sin cambio visual? ¿el hook engancha? ¿la música respira con la voz?
5. Iterá hasta que esté a nivel de agencia top. Nuevos componentes → `engine-remotion/src/graphics/` y
   registrarlos en `src/layers/GraphicsLayer.tsx` (seguir `remotion-markup`, animación solo con
   `useCurrentFrame`).

### 6 · Entrega
1. `./ve render <c>/<p>` (final 100 %, master -14 LUFS / -1 dBTP; VSL para YouTube/landing: `--lufs -16`).
2. Otros formatos: copiá overlays a `overlays_16x9.json` con `"format": "16:9"` (ajustá posiciones),
   `./ve build <c>/<p> --overlays _work/overlays_16x9.json && ./ve render <c>/<p> --name 16x9`.
3. Verificá `references/qc.md`. Mirá la hoja de contacto final.
4. Resumen al usuario: qué se entregó (rutas en `entregables/`), decisiones creativas clave, créditos que
   requieren atribución, y qué variantes podrías hacer (hooks alternativos, otra música, 16:9).
5. Commit + push de `entregables/` (Git LFS rastrea mp4/mov) y del `_work/overlays.json`/`PLAN.md`.
