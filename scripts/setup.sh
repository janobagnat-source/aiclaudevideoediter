#!/usr/bin/env bash
# Instalación idempotente de TODO el entorno del editor (se ejecuta sola al iniciar cada sesión en la nube).
#   ./ve setup            instalación completa (rápida si ya está todo)
#   ./ve setup --full     además descarga la librería completa de SFX/música y precarga Whisper (en primer plano)
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
LOG="$ROOT/.setup.log"
FULL="${1:-}"
say() { printf '\033[1;36m[setup]\033[0m %s\n' "$*"; }
mkdir -p clientes library

# 1) Python (uv) -------------------------------------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
  say "instalando uv"; pip3 install -q uv >>"$LOG" 2>&1 || true
fi
if [ ! -x .venv/bin/python ]; then
  say "creando .venv (Python 3.12)"; uv venv .venv --python 3.12 >>"$LOG" 2>&1 || python3 -m venv .venv
fi
if ! .venv/bin/python -c "import faster_whisper, librosa, cv2, scenedetect, rapidfuzz" >/dev/null 2>&1; then
  say "instalando dependencias Python"; VIRTUAL_ENV="$ROOT/.venv" uv pip install -q -r requirements.txt >>"$LOG" 2>&1 \
    || .venv/bin/pip install -q -r requirements.txt >>"$LOG" 2>&1
fi

# 2) Node: Remotion + 3D -------------------------------------------------------------------------
if [ ! -d engine-remotion/node_modules/remotion ]; then
  say "instalando Remotion (npm ci)"; (cd engine-remotion && npm ci --no-audit --no-fund >>"$LOG" 2>&1)
fi
mkdir -p engine-remotion/public
[ -L engine-remotion/public/clientes ] || ln -sfn ../../clientes engine-remotion/public/clientes
[ -L engine-remotion/public/library ] || ln -sfn ../../library engine-remotion/public/library

# 3) Navegadores headless para render (Remotion + HyperFrames) ----------------------------------
(cd engine-remotion && npx --yes remotion browser ensure >>"$LOG" 2>&1) || say "⚠️ remotion browser ensure falló (ver .setup.log)"
HFV="$(cat engine-hyperframes.version)"
npx --yes "hyperframes@$HFV" browser ensure >>"$LOG" 2>&1 || say "⚠️ hyperframes browser ensure falló"

# 4) Librería base offline: SFX sintetizados + fuentes ------------------------------------------
[ -f library/sfx/synth/impact_cinematic.wav ] || { say "generando SFX propios"; .venv/bin/python tools/sfx_synth.py >>"$LOG" 2>&1; }
[ -f library/fonts/manifest.json ] || { say "descargando fuentes"; .venv/bin/python tools/fonts.py --defaults >>"$LOG" 2>&1; }
[ -f library/index.json ] || .venv/bin/python tools/library.py index >>"$LOG" 2>&1

# 5) Librería completa (Kenney CC0, BigSoundBank CC0, música CC) + modelo Whisper -----------------
heavy() {
  [ -d library/sfx/kenney/impact-sounds ] && [ -d library/music/_dl/epic ] || .venv/bin/python tools/library.py build --sfx 3 --music 3
  .venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')"
}
if [ "$FULL" = "--full" ]; then
  say "librería completa + Whisper (primer plano)"; heavy >>"$LOG" 2>&1
else
  ( heavy >>"$LOG" 2>&1 & ) ; say "librería completa y Whisper descargando en segundo plano (log: .setup.log)"
fi
say "listo ✔  — './ve help' para ver los comandos"
