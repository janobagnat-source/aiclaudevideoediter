# Catálogo de motion graphics (engine-remotion/src)

Todos toman colores/fuentes de `brand.json` automáticamente. Posiciones `x`, `y`, `position` en 0–1 del
cuadro. Escalan solos según la resolución (9:16, 16:9, 4K). Demo visual: `npx remotion still Gallery` o
`npx remotion render Gallery` en `engine-remotion/`.

## Texto y datos (`src/graphics/text.tsx`)
| Componente | Uso | Props |
|---|---|---|
| `HookTitle` | Titular de impacto del hook / reveals | `lines[]`, `highlight[]`, `variant` slam\|stack\|glitch\|split, `position`, `bg` none\|dim\|brand\|blur, `size`, `stagger` (frames entre líneas). Auto-ajusta al ancho |
| `KineticText` | Frase palabra por palabra con máscara | `text`, `emphasis[]`, `position`, `size`, `align` center\|left, `perWord` (frames), `box`, `uppercase` |
| `LowerThird` | Nombre + cargo / autoridad | `name`, `title`, `position`, `side` left\|right |
| `StatCounter` | Número que cuenta con anillo | `value`, `from`, `prefix`, `suffix`, `label`, `decimals`, `position`, `ring`, `countFrames` |
| `Checklist` | Pasos/beneficios que aparecen | `items[]`, `title`, `every` (frames entre ítems), `position`, `icon` ✓\|→\|n, `bad` (✕ rojo para "errores") |
| `OfferBadge` | Starburst de oferta | `text` ("-50%"), `sub`, `x`, `y`, `size` |
| `ProgressBar` | Barra de progreso (VSL) | `thickness`, `top` |
| `Countdown` | Urgencia | `from` "23:59:59", `label`, `position` |
| `Testimonial` | Reseña con estrellas | `quote`, `author`, `stars`, `position` |
| `BarChart` | Barras animadas | `bars[{label,value,highlight}]`, `title`, `unit`, `position` |
| `SplitCompare` | Antes/Después | `left`, `right`, `vertical` |

## Visuales (`src/graphics/visual.tsx`)
| Componente | Uso | Props |
|---|---|---|
| `Flash` | Destello de impacto (0.15–0.3 s) | `color`, `peak` |
| `ShapeBurst` | Explosión de líneas en un beat | `x`, `y`, `color`, `count`, `radius` |
| `ArrowCallout` | Flecha dibujada que señala | `x`, `y` (punta), `from{x,y}`, `label`, `color` |
| `CircleHighlight` | Marcador a mano alrededor de algo | `x`, `y`, `w`, `h`, `color` |
| `IconPop` | Icono SVG (iconify) o emoji con pop | `src` \| `emoji`, `x`, `y`, `size`, `label`, `tint` |
| `BrandBackground` | Fondo animado para escenas MG | `variant` mesh\|grid\|rays\|dark |
| `LogoSting` | Reveal de logo con barrido de luz | `logo`, `tagline`, `bg`, `size` |
| `CTAEndCard` | Cierre con botón | `headline`, `button`, `sub`, `logo`, `bg` mesh\|grid\|rays\|dark\|none, `arrow`, `position` |
| `Notification` | Notificación tipo iPhone (ventas/prueba social) | `title`, `body`, `app`, `y`, `icon` |
| `FloatingCard` | Captura/imagen flotante con perspectiva | `src`, `x`, `y`, `w`, `rotate`, `radius` |
| `OverlayVideo` | Video con alfa (HyperFrames WebM/MOV) o elemento de stock | `src`, `blend` (screen, multiply…), `opacity`, `fit`, `volume`, `trimBefore` |

## 3D (`src/three/scenes.tsx`, React Three Fiber, render por SwiftShader en la nube)
| Componente | Uso | Props |
|---|---|---|
| `Text3DTitle` | Título extruido con bevel y luces de marca | `text` (`\n` = salto), `font` Montserrat-Black\|Anton\|`<Fam>-900` (`ve font X --3d`)\|ruta .json, `color`, `metal`, `size`, `y`, `depth`, `bg` |
| `Logo3D` | Logo del cliente extruido desde SVG | `svg`, `depth`, `metal`, `color` original\|brand\|#hex, `spin`, `scale`, `bg` |
| `Model3D` | Modelo glTF/GLB (Poly Haven, Sketchfab, cliente) | `model`, `scale`, `spin`, `y`, `tilt`, `bg` |
| `Phone3D` | Celular 3D con imagen/video en pantalla | `screen`, `x`, `scale`, `body`, `turn`, `bg` |
| `Shapes3D` | Formas premium flotantes (fondo) | `count`, `variant` glossy\|glass\|metal, `bg` |
| `Particles3D` | Partículas / hiperespacio | `count`, `speed`, `mode` float\|warp, `bg` |
Sin `bg` el canvas 3D es transparente → se compone sobre el video (p.ej. logo 3D sobre el A-roll).
Render 3D en CPU es más lento (~0.5–1.5 s/frame): úsalo en momentos puntuales.

## Crear un componente nuevo
1. Archivo en `src/graphics/` con firma `React.FC<{dur: number} & Props>`; animá SOLO con
   `useCurrentFrame()` (+ `spring`/`interpolate`, helpers en `src/lib/anim.ts`), colores con `useBrand()`.
2. Registrar en `REGISTRY` de `src/layers/GraphicsLayer.tsx`.
3. `npx tsc --noEmit` y `./ve render <p> --stills …` para verlo.
Consultá `remotion-markup` (timing, text, transitions, 3d, lottie, light-leaks, effects) antes de escribirlo.
