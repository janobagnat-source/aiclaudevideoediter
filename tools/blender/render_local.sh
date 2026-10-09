#!/bin/bash
# Renderiza las escenas 3D de un proyecto con la placa de video de tu compu (Blender 4.2+ instalado).
# Uso: tools/blender/render_local.sh clientes/carlos-buelvas/proyectos/ad01 bars coins hourglass scale
set -e
P=$1; shift
for s in "$@"; do
  BLENDER_GPU=1 blender -b -P "$(dirname "$0")/$s.py" -- "$P/_work/blender/$s"
done
