# `_work/overlays.json` — esquema

Es el único archivo creativo que escribís a mano. `./ve build` lo combina con `edl.json` (cortes) y
`brand.json` y genera `edit.json` (lo que renderiza Remotion). Todos los tiempos son del **timeline final**.

## Anclas (`at`, `until`)
```jsonc
2.5                                   // segundos absolutos
{"word": "gratis", "n": 1}            // n-ésima aparición de la palabra (tolera tildes/mayúsculas)
{"word": "gratis", "end": true}       // al final de la palabra
{"sentence": 4, "offset": -0.2}       // inicio de la frase 4 del guion (end:true = final)
{"cut": 7}                            // inicio del corte 7 de EDL.md
{"end": true, "offset": -3}           // 3 s antes del final (incluye "tail")
```
Duración: `"duration": 2.0` o `"until": <ancla>`.

## Raíz
```jsonc
{
  "format": "9:16",            // 9:16 | 16:9 | 1:1 | 4:5 | 9:16-4k | 16:9-4k
  "fps": 30,
  "tail": 1.5,                 // segundos extra al final (end card sobre fondo)
  "background": "#0b0b0f",
  "colors": {"primary": "#..."},  // override puntual de brand.json
  "fonts": {"heading": "Anton"},  // override (la fuente debe estar en library/fonts: ./ve font "Anton")
  "logo": "clientes/x/marca/logo.png",
  "zoom": {"auto": true, "intensity": 1.0},
  "captions": {
    "enabled": true, "style": "bold-pop",   // bold-pop | karaoke | boxed | minimal | neon | serif-elegant
    "emphasis": ["gratis", "90%"], "position": 0.72, "maxWords": 3, "uppercase": true,
    "hideDuring": [[0, 2.8]]                 // tramos sin subtítulos (segundos)
  },
  "cuts": { "<n>": { /* ver abajo */ } },
  "broll": [ ... ], "graphics": [ ... ], "sfx": [ ... ], "music": [ ... ],
  "fx": {"grade": "punchy", "grain": 0.04, "vignette": 0.22, "letterbox": 0}
}
```

## `cuts.<n>` (n = índice del corte en EDL.md / TIMELINE.md)
```jsonc
{
  "skip": true,                          // quitar el corte
  "in": 12.30, "out": 15.10,             // re-trim fino (segundos de la fuente)
  "speed": 1.1,                          // acelerar (pitch preservado)
  "zoom": [{"t": 0, "s": 1.0}, {"t": 0.3, "s": 1.25, "ease": "punch"}, {"t": 2, "s": 1.3, "x": 0.02, "y": -0.01, "r": 0}],
  "focus": {"x": 0.52, "y": 0.38},       // centro de zoom/recorte (0-1). Default: cara detectada
  "transition": "whip",                  // o {"type": "flash", "duration": 0.3}
  "fx": {"grade": "bw", "shake": 6, "blur": 0},
  "mirror": false, "volume": 1.0,
  "cutout": "_work/cutouts/cut0.webm",   // sujeto recortado (ve cutout) → permite "behind"
  "behind": [{"component": "HookTitle", "start": 0, "duration": 2.4, "props": {"lines": ["NO"], "bg": "none"}}]
}
```
`ease`: `smooth` | `punch` (overshoot) | `snap` | `linear`. `t` en segundos desde el inicio del corte.

## `broll[]`
```jsonc
{"src": "clientes/x/broll/fabrica.mp4" | "_work/assets/video/<q>/pexels-123.mp4" | "foto.jpg",
 "at": {"sentence": 3}, "duration": 2.2, "in": 4.0,          // in = segundo de la fuente
 "mode": "full",          // full | pip | card | circle | split-top | split-bottom
 "kenburns": "in",        // in | out | left | right | up | none
 "transition": "whip",    // whip | whip-up | zoom-in | fade | cut
 "speed": 1.0, "volume": 0, "grade": "cinematic", "focus": {"x": 0.5, "y": 0.5}}
```
La voz del A-roll sigue sonando debajo (es un "cutaway").

## `graphics[]`
```jsonc
{"component": "StatCounter", "at": {"word": "300"}, "duration": 2.0,
 "layer": "over",          // under (debajo del b-roll) | over (default) | top (encima de captions)
 "props": {"value": 300, "suffix": "%", "label": "más ventas"}}
```
Props con rutas (`src`, `logo`, `model`, `svg`, `screen`, `image`) se resuelven solas (relativas al proyecto,
al cliente o al repo). Catálogo completo en `motion-catalog.md`.

## `sfx[]`
```jsonc
{"src": "synth:impact_cinematic" | "lib:whoosh" | "library/sfx/kenney/impact-sounds/impactMetal_heavy_000.ogg",
 "at": {"word": "gratis"}, "offset": -0.1, "volume": 0.7, "trim": [0, 1.2]}
```

## `music[]`
```jsonc
{"src": "_work/assets/music/epic/ov-xxx.mp3", "at": 0, "in": 12.5, "until": {"end": true},
 "volume": 0.24, "duck": 0.4, "fadeIn": 0.3, "fadeOut": 1.2,
 "dropAt": {"sentence": 9}, "drop": 0}   // alinea el drop nº `drop` (de ve beats) con el ancla; calcula `in`
```
