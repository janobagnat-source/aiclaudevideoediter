# ./ve — comandos

```
PROYECTO
  ./ve new <cliente> <proyecto>          crea carpetas desde clientes/_PLANTILLA
  ./ve fetch <c>/<p>                     descarga los links de links.md (Drive, Dropbox, YouTube, URL)
  ./ve prep <c>/<p>                      analyze + guion + transcribe + align de una

ANÁLISIS Y CORTE
  ./ve analyze <c>/<p> [--fps 30]        inventario, mezzanines CFR, hojas de contacto, escenas, audio, caras
  ./ve brand <cliente>                   línea gráfica → marca/brand.json (+ descarga sus fuentes)
  ./ve guion <c>/<p> [--file x.docx]     guion → _work/guion.json
  ./ve transcribe <c>/<p> [--model ..]   Whisper large-v3-turbo palabra por palabra
  ./ve align <c>/<p> [--free] [--max-gap 0.38]   guion ↔ audio → mejor toma de cada frase → _work/EDL.md

ASSETS (todo registra licencia en credits.json)
  ./ve stock video|photo|music|sfx|3d|hdri|texture|icon "consulta" [-n 5] [-p <c>/<p>] [--orientation portrait]
  ./ve library build|index|search <q>|list   librería local de SFX/música
  ./ve beats <audio>                     tempo, beats, downbeats, drops
  ./ve font "Familia" [--3d]             fuente de Google Fonts local (+ versión 3D)
  ./ve sfx-synth                         regenera los SFX propios

MONTAJE Y RENDER
  ./ve cutout <c>/<p> <n_corte>          recorta al sujeto (alfa) para texto detrás de la persona
  ./ve build <c>/<p> [--overlays f.json] EDL + overlays + marca → _work/edit.json + TIMELINE.md
  ./ve render <c>/<p> --stills 0.5,3,8   fotogramas de revisión
  ./ve render <c>/<p> --draft            video 50 % para revisar ritmo + hoja de contacto
  ./ve render <c>/<p> [--lufs -14] [--name 16x9] [--version 2]   FINAL → entregables/
  ./ve studio <ruta/edit.json>           Remotion Studio (preview interactivo, puerto 3000)
  ./ve hf <args>                         CLI de HyperFrames (registry, remove-background, tts, render…)

ENTORNO
  ./ve setup [--full]                    instala/verifica todo (corre solo al iniciar sesión)
```
