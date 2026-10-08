# 🎬 AI Video Editor — Claude + Remotion + HyperFrames

Editor de video automático de nivel agencia para **ads de 30 s** y **VSL de 3 min**: subís el material en
crudo, el guion, la línea gráfica y las indicaciones; Claude analiza todo, corta siguiendo el guion
(eligiendo la mejor toma y eliminando muletillas/silencios), arma el hook visual y sonoro, zooms dinámicos,
motion graphics 2D/3D con los colores y tipografías de la marca, b-roll (del cliente o de bancos libres),
SFX y música épica/cinematográfica, subtítulos animados, masteriza el audio y deja el video listo en
`entregables/`.

## 1 · Dónde cargar el contenido

Cada cliente tiene su carpeta y cada video un proyecto:

```
clientes/
└── <cliente>/
    ├── marca/               ← LÍNEA GRÁFICA: logo (SVG + PNG), fuentes .ttf/.otf, brand.md, manual, refs
    ├── broll/               ← b-roll general del cliente (se reutiliza en todos sus videos)
    └── proyectos/
        └── <proyecto>/
            ├── brief.md       ← INDICACIONES: formato, duración, objetivo, CTA, tono, música…
            ├── guion.md       ← GUION (o guion.docx / guion.pdf / guion.txt)
            ├── links.md       ← LINKS: Drive/Dropbox/YouTube del crudo, b-roll, referencias
            ├── crudo/         ← VIDEO EN CRUDO (todas las tomas)
            ├── broll/         ← b-roll específico de este video
            ├── audio/         ← música o locución propia (opcional)
            ├── referencias/   ← videos/imágenes de estilo (opcional)
            └── entregables/   ← ✅ ACÁ APARECEN LOS VIDEOS TERMINADOS
```

Crear la estructura: pedile a Claude **`/nuevo-cliente acme ad-verano`** (o `./ve new acme ad-verano`).

**Cómo subir los archivos** (el entorno corre en la nube):
1. **Material pesado (crudo, b-roll) → links**: subilo a Google Drive (carpeta compartida "cualquiera con el
   link") o Dropbox y pegá el link en `links.md` bajo la sección correspondiente (`## crudo`, `## broll`…).
   Claude lo descarga solo (`./ve fetch`). También acepta YouTube/Vimeo/Loom y URLs directas.
2. **Archivos livianos (guion, brief, logo, fuentes)** → subilos al repo en GitHub (botón *Add file → Upload
   files* en la carpeta) o adjuntalos en el chat y pedile a Claude que los ubique.
3. **Desde tu compu con git**: `git lfs install` y luego `git add` normal — los .mp4/.mov van por Git LFS.

## 2 · Pedir la edición

En el chat de Claude Code:

```
/editar acme/ad-verano
/editar acme/vsl-lanzamiento "VSL 3 min 16:9 para landing, tono épico, CTA: Agendá tu llamada"
```
O simplemente: *"editá el proyecto acme/ad-verano, quiero 9:16 y 4:5, hook muy agresivo"*.

Claude trabaja en fases: análisis visual de todo el material → transcripción y alineación con el guion →
plan creativo (`_work/PLAN.md`) → búsqueda de assets → montaje → revisión de fotogramas y borrador →
render final → QC (loudness, negros, safe zones) → entrega + commit.

Indicaciones generales útiles en `brief.md`: formato(s), plataforma, duración, CTA exacto, tono de música,
estilo de subtítulos, cosas obligatorias/prohibidas, referencias.

## 3 · Qué recibís en `entregables/`
- `<cliente>_<proyecto>_9x16_v1.mp4` (H.264, 1080×1920, 30 fps, AAC 320k, -14 LUFS, -1 dBTP)
- `.srt` de subtítulos, miniatura `_thumb.jpg`, `_creditos.txt` (licencias y atribuciones requeridas)
- Versiones nuevas = `_v2`, `_v3`… Otros formatos: `_16x9`, `_4x5`, `_1x1`.

## 4 · Herramientas instaladas
| Capa | Herramientas |
|---|---|
| Motor de motion graphics | **Remotion 4** (React) + `@remotion/three` / React Three Fiber (3D), `@remotion/effects` (zoom blur, aberración cromática, light leaks…), transitions, captions, lottie, motion-blur, noise, paths, shapes |
| HyperFrames | CLI 0.8 + 21 skills oficiales: registry de ~400 bloques/efectos, recorte de sujeto con IA (texto detrás de la persona), TTS Kokoro, beats, overlays HTML/GSAP |
| Skills de Claude | `remotion-*` (oficiales), `hyperframes*`, `media-use`, `motion-graphics`… + **`editor-pro`** (flujo y playbook del editor) |
| Análisis | ffmpeg, faster-whisper large-v3-turbo (palabra por palabra), PySceneDetect, OpenCV YuNet (caras), librosa (beats/drops), EBU R128 |
| Bancos libres | Pexels, Pixabay, Unsplash, Openverse (imágenes y música CC), Jamendo, Freesound, BigSoundBank (CC0), Kenney (CC0), Poly Haven (3D/HDRI/texturas CC0), Sketchfab, Iconify, Google Fonts |
| SFX propios | 32 sonidos cinematográficos sintetizados (whooshes, risers, impacts, braams, sub drops, glitches, pops…) |

## 5 · API keys (opcionales, gratis — mejoran el b-roll y la música)
Sin keys ya funcionan: Openverse, BigSoundBank, Kenney, Poly Haven, Iconify, Jamendo vía Openverse.
Para b-roll de video de stock hace falta al menos Pexels o Pixabay. Agregalas como variables de entorno
del entorno de la nube (menú del entorno → *Edit* → variables/secrets) — nunca las pegues en el chat:

| Variable | Dónde se saca (gratis) | Para qué |
|---|---|---|
| `PEXELS_API_KEY` | pexels.com/api | video y fotos de stock HD/4K |
| `PIXABAY_API_KEY` | pixabay.com/api/docs | video y fotos |
| `UNSPLASH_ACCESS_KEY` | unsplash.com/developers | fotos premium |
| `FREESOUND_API_KEY` | freesound.org/apiv2/apply | SFX (si la CDN no bloquea la IP) |
| `JAMENDO_CLIENT_ID` | devportal.jamendo.com | más música CC |
| `SKETCHFAB_API_TOKEN` | sketchfab.com/settings/password | modelos 3D descargables |

## 6 · Tiempos de referencia (4 CPU, sin GPU)
Ad 30 s ≈ 5–8 min de render final · VSL 3 min ≈ 45–60 min · recorte de sujeto ≈ 0.5 s/frame ·
transcripción ≈ 0.4× tiempo real. El entorno se instala solo al iniciar cada sesión (`scripts/setup.sh`);
la primera vez la librería de sonidos y el modelo Whisper bajan en segundo plano (~3–5 min).

Comandos: [`docs/CLI.md`](docs/CLI.md) · Flujo del editor: [`.claude/skills/editor-pro`](.claude/skills/editor-pro/SKILL.md)
