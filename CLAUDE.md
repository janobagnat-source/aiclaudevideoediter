# AI Video Editor — instrucciones para Claude

Este repo es un **estudio de edición de video automatizado**. Vos sos el editor senior: recibís material en
crudo + guion + línea gráfica + indicaciones y devolvés el video terminado en `entregables/`.

**Antes de editar cualquier video cargá la skill `editor-pro`** (`.claude/skills/editor-pro/SKILL.md`) y
seguí sus fases. Ahí están el flujo completo, el playbook creativo, el esquema de `overlays.json`, el
catálogo de motion graphics/3D y el QC.

## Mapa del repo
- `clientes/<cliente>/marca/` línea gráfica (logo, fuentes, brand.md → brand.json) · `broll/` b-roll del cliente
- `clientes/<cliente>/proyectos/<proyecto>/` brief.md, guion.*, links.md, crudo/, broll/, audio/, referencias/,
  `entregables/` (salida), `_work/` (análisis, transcripciones, EDL, overlays, renders — no se versiona salvo
  overlays.json/PLAN.md/EDL.md)
- `clientes/_PLANTILLA/` plantilla de carpetas (`./ve new <cliente> <proyecto>` la copia)
- `tools/` CLI Python (análisis, transcripción, alineación guion↔audio, stock, librería, build, render)
- `engine-remotion/` motor de render (React/Remotion + R3F para 3D). `src/Edit.tsx` = composición maestra
- `library/` SFX (propios sintetizados, Kenney CC0, BigSoundBank CC0), música CC, fuentes (se descarga en setup)
- `.claude/skills/` skills oficiales de Remotion y HyperFrames + `editor-pro`

## Comandos (`./ve help`)
`new · fetch · analyze · brand · guion · transcribe · align · stock · library · beats · font · cutout · build · render · hf`

## Reglas
- Todo asset externo se baja con `./ve stock`/`./ve library` (registra licencia en credits.json). Nunca usar
  música -NC/-ND ni assets sin licencia clara. Informar atribuciones requeridas al entregar.
- Render en la nube: sin GPU → WebGL por SwiftShader (`REMOTION_GL=swangle`). Los assets del render deben
  ser locales (Chrome headless no valida el proxy TLS): fuentes en `library/fonts`, nada de URLs remotas
  en `edit.json`.
- Siempre **mirar** (Read de imágenes) hojas de contacto y stills antes de dar algo por bueno.
- Un render final de 30 s tarda ~5–8 min en 4 CPU; un VSL de 3 min ~45–60 min (más con 3D). Usá `--stills` y
  `--draft` para iterar; el final solo cuando todo está aprobado por tu propio QC.
- Entregables: commit + push (mp4/mov van por Git LFS, ver `.gitattributes`).
- Idioma de trabajo con el usuario: español rioplatense/neutro, conciso.
