#!/usr/bin/env bash
# Crea la estructura de carpetas de un cliente/proyecto:  ./ve new <cliente> <proyecto>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
C="${1:?uso: ve new <cliente> <proyecto>}"; P="${2:?uso: ve new <cliente> <proyecto>}"
CD="$ROOT/clientes/$C"; PD="$CD/proyectos/$P"
mkdir -p "$CD/marca" "$CD/broll" "$PD"/{crudo,broll,audio,referencias,entregables}
[ -f "$CD/marca/brand.md" ] || cp "$ROOT/clientes/_PLANTILLA/marca/brand.md" "$CD/marca/brand.md"
for f in brief.md guion.md links.md; do
  [ -f "$PD/$f" ] || cp "$ROOT/clientes/_PLANTILLA/proyectos/_PROYECTO/$f" "$PD/$f"
done
echo "$PD"
