#!/bin/bash
# Cola independiente: renderiza escenas faltantes (retoma frames hechos) y arma el mp4. Uso: queue.sh <proyecto> esc1 esc2 ...
P=$1; shift
B=/home/user/aiclaudevideoediter/tools/blender
for s in "$@"; do
  while pgrep -f "blender -b -P $B/$s.py" >/dev/null; do sleep 15; done
  N=$(grep -oP 'FRAMES", \K[0-9]+' $B/$s.py)
  have=$(ls $P/_work/blender/$s/f_*.png 2>/dev/null | wc -l)
  if [ "$have" -lt "$N" ]; then
    (cd /tmp && blender -b -P $B/$s.py -- $P/_work/blender/$s > /tmp/bl/$s.log 2>&1)
  fi
  ffmpeg -v error -y -framerate 30 -i $P/_work/blender/$s/f_%04d.png -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0" -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p $P/_work/blender/$s/$s.mp4
  echo "LISTO $s $(ls $P/_work/blender/$s/f_*.png | wc -l)" >> /tmp/bl/queue_done.txt
done
