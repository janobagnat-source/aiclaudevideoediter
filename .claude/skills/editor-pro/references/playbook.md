# Playbook creativo — ads y VSL de alto rendimiento

## Hook (0–3 s) — lo más importante del video
- **Frame 0 ya en movimiento**: nada de fade-in desde negro ni logo al inicio. El primer frame debe tener
  texto + imagen + movimiento (lo que se ve como miniatura en el feed).
- **Visual**: `HookTitle` (variant `slam` o `glitch`) con 2–3 líneas cortas y la palabra/número clave en
  `highlight`; `Flash` de 0.2 s en el frame 0; punch-in fuerte del A-roll (zoom 1.0→1.25 en 0.3 s,
  ease `punch`) o montaje rápido de 3–4 b-rolls de 0.4–0.6 s cortados en beat.
- **Sonoro**: `synth:impact_cinematic` + `synth:subdrop_01` en t=0 (vol 0.8–0.9); música arrancando en un
  punto de energía (`in` cerca de un beat fuerte) o un `riser_short` que remata en un `braam`/impacto al
  terminar el hook (~2.5–3 s).
- **Patrón de interrupción**: algo inesperado en los primeros 1.5 s (pregunta polémica, número enorme,
  objeto 3D entrando, imagen de contraste "antes/después").
- Captions ocultos durante el HookTitle (`captions.hideDuring`) para no duplicar texto.
- Variantes de hook = mayor palanca de testeo: ofrecé 2–3 hooks alternativos (mismo cuerpo).

## Ritmo
- **Ad 30 s**: cambio visual cada **1.5–2.5 s** (corte, cambio de nivel de zoom, b-roll, gráfico).
  Cortes de pausa agresivos (`--max-gap 0.3`). Cero aire muerto.
- **VSL 3 min**: cambio cada **3–5 s**, con "capítulos": KineticText/LowerThird de sección, ProgressBar,
  Checklist de recap, testimonios, StatCounters para pruebas. Respiraciones permitidas en momentos
  emocionales (dejá `keep-gap` mayor).
- Montajes de b-roll: cortá en beats (`./ve beats`), 0.4–0.8 s por plano, con whoosh en cada uno.
- Antes de un momento grande: 0.2–0.4 s de "vacío" (bajar música o cortar SFX) para que el golpe pegue.

## Zooms dinámicos (A-roll)
- El auto-zoom alterna planos 1.0 / 1.12 / 1.24 en cada corte (disimula jump cuts) + punch-in en palabras
  de `captions.emphasis` + drift lento. Ajustá `zoom.intensity` (0.6 sobrio – 1.4 agresivo).
- Límite de calidad: con fuente 1080p no pasar de **1.35** en 1080 de salida; con 4K hasta **1.8**.
- Momentos emocionales: push-in lento continuo (`[{t:0,s:1.0},{t:4,s:1.12,ease:"smooth"}]`).
- Impactos: `transition: "shake"` o `fx.shake` (cámara en mano) solo en golpes, nunca constante.
- 16:9 → 9:16: el `focus` (centro de la cara detectada) define el recorte; revisá en los stills que la
  cara no quede cortada; ajustá `focus` por corte si hace falta.

## Transiciones entre cortes (`cuts.<n>.transition`)
- `whip` (cambio de idea), `zoom-in` (profundizar), `flash` (revelación), `glitch` (tech/disrupción),
  `light-leak` (emocional/cinematográfico), `dip-black` (cambio de capítulo VSL), `shake` (impacto).
- No más de 1 transición "llamativa" cada ~4 s en ads; el resto cortes secos (jump cuts con zoom).
- Siempre con SFX acorde (whoosh/swipe para whip, glitch para glitch, impact suave para flash).

## SFX — dónde y cuánto
| Momento | SFX | Vol | Offset |
|---|---|---|---|
| Entrada de b-roll / gráfico grande | `synth:whoosh_fast` / `whoosh_medium` / BigSoundBank whoosh | 0.4–0.6 | -0.15 s |
| Ítems de lista, iconos, badges | `synth:pop_01`, `click_ui`, Kenney interface | 0.3–0.5 | 0 |
| Hook, revelación, número clave | `impact_cinematic` + `subdrop_01` | 0.7–0.9 | 0 |
| Antes de CTA / gran reveal | `riser_medium` (2–3 s) → `braam_01` | 0.35 / 0.6 | riser termina en el hit |
| Dinero, venta, éxito | `cash_01`, `ding_success` | 0.4–0.5 | 0 |
| Glitch / tech | `glitch_01..03`, Kenney digital/sci-fi | 0.4 | -0.05 |
| Texto que se escribe | Kenney typing / `tick_01` en loop | 0.25 | — |
| Cambio de capítulo (VSL) | `reverse_swell` → corte | 0.5 | termina en el corte |
- Máximo 2–3 SFX simultáneos. La voz siempre manda: SFX nunca tapan palabras clave.
- Variá los sonidos (no el mismo whoosh 10 veces): alterná synth / Kenney / BigSoundBank.

## Música
- Tono por defecto: **épico / cinematográfico** (trailer, orchestral hybrid). Alternativas según brief:
  motivational, tech, hip-hop/trap para público joven, dark/tension para problemas.
- Volumen de cama 0.18–0.28 con `duck` 0.35–0.5 (baja bajo la voz con ataque/release suaves).
- `dropAt`: alineá el drop (de `./ve beats`) con el CTA o con la revelación principal.
- Fade out 1–1.5 s, terminando con el último hit/logo. Sin silencios incómodos al final.
- VSL largo: cambiar de tema o de sección musical por capítulos (varios items en `music`).
- Licencias: preferí CC0/CC-BY. Jamendo CC-BY exige atribución (queda en `_creditos.txt`). Nunca -ND/-NC.

## Motion graphics
- **Solo colores y fuentes de marca** (brand.json). Fondo de escenas MG: `BrandBackground` (mesh/grid/rays).
- Densidad ad: 1–2 MG cada 10 s, cada uno ≤ 2.5 s. VSL: MG en cada dato/prueba/paso.
- Números → `StatCounter`; pasos/beneficios → `Checklist`; comparaciones → `SplitCompare`/`BarChart`;
  prueba social → `Testimonial`/`Notification`; oferta → `OfferBadge`/`Countdown`; señalar → `ArrowCallout`
  / `CircleHighlight`; nombre/autoridad → `LowerThird`; cierre → `CTAEndCard` (+`LogoSting`).
- 3D para momentos héroe: `Text3DTitle` (título de impacto), `Logo3D` (SVG del cliente), `Model3D`
  (producto/objeto de Poly Haven), `Phone3D` (app/web del cliente en pantalla), `Shapes3D`/`Particles3D`
  (fondos premium). 1–3 momentos 3D por ad; no abusar.
- Efectos con nombre (CRT, film burn, glitch avanzado, mapas, charts complejos): buscá primero en el
  registry de HyperFrames (ver `hyperframes-bridge.md`).
- **Texto detrás del sujeto** (efecto premium para hook/títulos): `./ve cutout` + `cuts.<n>.behind`.

## Subtítulos
- Ads: `bold-pop`, 2–3 palabras, MAYÚSCULAS, palabra activa resaltada con color primario.
- VSL: `karaoke` o `boxed`, 3–4 palabras; `minimal` para marcas premium/lujo; `serif-elegant` para
  marcas femeninas/editoriales; `neon` para tech/gaming.
- `emphasis`: números, dinero, beneficios, dolores, la oferta. Ortografía = la del guion (align la aplica).
- Safe zones 9:16: captions entre y=0.62 y 0.75 (Reels/TikTok tapan abajo ~18 % y a la derecha ~12 %).
  Nada importante en el 10 % superior. 16:9: captions y=0.82.

## Color y textura
- `fx.grade`: `punchy` (ads), `cinematic` (épico), `warm` (cercano), `moody` (dolor/problema), `clean`.
- Grano 0.03–0.05 y viñeta 0.2–0.3 dan look cinematográfico; letterbox (`fx.letterbox: 2.39`) solo 16:9.
- Mismo grade en todos los cortes de una escena; b-roll de stock con `grade` para igualarlo.

## CTA
- Últimos 3–5 s: `CTAEndCard` con el texto exacto del brief, botón con pulso, logo, flecha.
- Voz del CTA siempre audible (no tapar con gráfico el rostro si es el momento de confianza: usá
  `layer: "over"` y `bg: "none"` si querés mantener a la persona).
- Hit final (braam/impact) sincronizado con la aparición del botón.
