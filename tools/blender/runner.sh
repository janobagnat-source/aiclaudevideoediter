#!/bin/bash
# Cola dinámica de escenas: cada línea de /tmp/bl/q.txt = "<adXX> <escena>" (tools/blender/scenes/<escena>.py)
# Salida: clientes/carlos-buelvas/proyectos/<adXX>/_work/blender/<escena>/<nombre>.mp4 ; registro en /tmp/bl/q_done.txt
R=/home/user/aiclaudevideoediter; Q=/tmp/bl/q.txt; D=/tmp/bl/q_done.txt; touch $Q $D
idle=0
while [ $idle -lt 720 ]; do
  line=$(grep -vxFf $D $Q | head -1)
  if [ -z "$line" ]; then sleep 10; idle=$((idle+1)); continue; fi
  idle=0; set -- $line; ad=$1; sc=$2
  out=$R/clientes/carlos-buelvas/proyectos/$ad/_work/blender/$sc
  mkdir -p $out
  (cd /tmp && blender -b -P $R/tools/blender/scenes/$sc.py -- $out > /tmp/bl/run_$sc.log 2>&1)
  mp4=$(ls $out/*.mp4 2>/dev/null | head -1)
  if [ -z "$mp4" ]; then ffmpeg -v error -y -framerate 30 -i $out/f_%04d.png -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0" -c:v libx264 -crf 14 -pix_fmt yuv420p $out/$sc.mp4; fi
  echo "$line" >> $D
  echo "LISTO $line $(ls $out/f_*.png 2>/dev/null | wc -l) $(date +%H:%M)" >> /tmp/bl/q_log.txt
done
