# QC antes de entregar (todo debe estar en ✔)

**Corte**
- [ ] Todas las frases del guion están (EDL sin ⚠️, o la omisión está justificada en el resumen).
- [ ] Ningún corte a mitad de palabra; sin muletillas ni respiraciones feas; sin repeticiones.
- [ ] Ritmo: ningún tramo sin cambio visual > 2.5 s (ad) / > 5 s (VSL).

**Imagen**
- [ ] Frame 0 fuerte (sirve de miniatura). Hook legible en < 1 s.
- [ ] Ningún texto fuera de safe zone ni cortado; nada tapa la cara en momentos clave.
- [ ] Colores y tipografías de marca en todos los MG; logo correcto y nítido.
- [ ] Zoom sin pixelado visible (≤1.35 con fuente 1080p); la cara bien encuadrada en 9:16.
- [ ] Grade consistente; b-roll de stock igualado.
- [ ] `blackdetect` sin segmentos negros no intencionales (QC json).

**Sonido**
- [ ] -14 LUFS (redes) / -16 (YouTube/landing) ±0.5; true peak ≤ -1 dBTP (QC json).
- [ ] Voz siempre inteligible sobre música (duck) y SFX.
- [ ] Drop/hit musical alineado con el momento clave; final sin corte brusco.
- [ ] SFX variados, sin saturar.

**Texto**
- [ ] Subtítulos sincronizados y con la ortografía del guion (marcas, precios, tildes).
- [ ] CTA con el texto exacto del brief.

**Entrega**
- [ ] `entregables/<cliente>_<proyecto>_<formato>_vN.mp4` + `.srt` + `_thumb.jpg` + `_creditos.txt`.
- [ ] Créditos con atribución requerida informados al usuario.
- [ ] Commit + push.
