# HyperFrames dentro del flujo

HyperFrames (`./ve hf <comando>`, versión fijada en `engine-hyperframes.version`) complementa a Remotion.
Sus skills están instaladas en `.claude/skills/` (router: `/hyperframes`). Usalo para:

## 1. Texto/gráficos detrás del sujeto (recorte con IA local)
```bash
./ve cutout <c>/<p> 0            # corta el corte 0 y genera _work/cutouts/cut0.webm (alfa)
```
En overlays: `"cuts": {"0": {"cutout": "_work/cutouts/cut0.webm", "zoom": [{"t":0,"s":1.05}], "behind": [...]}}`
El zoom/encuadre se aplica igual al fondo, a los gráficos "behind" y al sujeto.

## 2. Bloques y efectos del registry (~400 ítems: glitch, CRT, film burn, charts, mapas, confetti…)
```bash
./ve hf catalog                    # explorar   |  ./ve hf add <bloque>  (en un proyecto HF)
```
Flujo para usarlos en el ad:
1. `(cd clientes/<c>/proyectos/<p>/_work && ../../../../../ve hf init hf-overlay --non-interactive --resolution portrait)`
   (o `npx hyperframes@$(cat engine-hyperframes.version) init …` desde esa carpeta)
2. Construí la composición siguiendo `/hyperframes-core` + `/hyperframes-registry` (fondo transparente).
3. `./ve hf render --format webm -o ../assets/overlays/<nombre>.webm` (en la carpeta del proyecto HF).
4. En overlays.json: `{"component": "OverlayVideo", "at": …, "duration": …, "props": {"src": "_work/assets/overlays/<nombre>.webm"}}`
   (o `blend: "screen"` para overlays de luz sobre negro).

## 3. Escenas de motion graphics completas en HTML/GSAP
Para escenas tipo "explainer" o UI animada que sea más rápido escribir en HTML/CSS/GSAP:
seguí `/motion-graphics` o `/general-video`, renderizá a MP4/WebM y entralo como `broll` (mode full) u
`OverlayVideo`.

## 4. Otras utilidades
- `./ve hf tts "texto" -v ef_dora -o voz.wav` — voz en off temporal (Kokoro, español: `ef_dora`, `em_alex`).
- `./ve hf beats` — detección de beats alternativa (preferí `./ve beats`, que también da drops).
- `./ve hf transcribe` — alternativa a `./ve transcribe`.
- `./ve hf remove-background img.png -o out.png` — recortar fotos de producto/personas para MG.
