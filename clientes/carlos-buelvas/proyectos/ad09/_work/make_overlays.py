# AD09 v2 — “Prometer lo que no puedes sostener”. Lo que comprás con cada “sí”.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad09/_work/blender/"
ad.set_cams({0: "cam1", 2: "cam2", 3: "cam1", 4: "cam1", 5: "cam1"})
ad.auto_zooms(punch_words=["prometer", "problema.", "sí", "hora.", "cansancio,", "alguien.", "comprometerte,", "calidad", "escrito", "cambios.", "límite", "pagando.", "sígueme"])

# ── HOOK: split; un carrito lleno de promesas “gratis”… total: 1 PROBLEMA ─────────────────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("ShoppingCart", 0.05, until={"cut": 1, "offset": -0.05}, y=0.575, totalAt=118,
     items=[{"text": "Entrega en 24 h", "at": 40}, {"text": "Todo incluido", "at": 55}, {"text": "Disponible 24/7", "at": 70}])
for at in (40, 55, 70):
    ad.sfx("synth:pop_01", at / 30, 0.38)
ad.sfx("lib:bsb-1417", 118 / 30, 0.35); ad.sfx("synth:impact_punch", {"word": "problema."}, 0.5)

# ── LOS PEDIDOS DEL CLIENTE → notificaciones apiladas ────────────────────────────────────────
ad.g("RequestToasts", {"word": "necesitamos", "offset": -0.2}, until={"word": "sí", "n": 2, "offset": -0.12}, y=0.74,
     items=[{"text": "¿Me lo puedes tener para mañana?", "at": 4}, {"text": "¿Puedes sumar una cosita más?", "at": 34}, {"text": "¿Hablamos el domingo?", "at": 64}])
for at in (4, 34, 64):
    ad.sfx("lib:bsb-1111", {"word": "necesitamos", "offset": -0.2 + at / 30}, 0.2)

# ── SÍ A TODO → Blender: la torre que se carga hasta inclinarse + sellos “SÍ” ─────────────────
ad.broll(BL + "ad09_tower/tower.mp4", {"word": "sí", "n": 2, "offset": -0.12}, {"cut": 2}, speed=0.38, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "sí", "n": 2, "offset": -0.12}, "until": {"cut": 2}, "pos": 0.88})
ad.g("YesStamps", {"word": "sí", "n": 2, "offset": -0.12}, until={"cut": 2, "offset": -0.03}, y=0.62,
     items=[{"text": "ENTREGAR ANTES", "at": 40}, {"text": "INCLUIR MÁS COSAS", "at": 71}, {"text": "DISPONIBLE 24/7", "at": 116}])
for at in (40, 71, 116):
    ad.sfx("synth:impact_punch", {"word": "sí", "n": 2, "offset": -0.12 + at / 30}, 0.35)
ad.sfx("synth:tape_stop", {"cut": 2, "offset": -0.4}, 0.3)

# ── CANSANCIO · INCOMODIDAD · FALLARLE A ALGUIEN → electrocardiograma que se apaga ────────────
ad.g("EnergyEKG", {"word": "cansancio,", "offset": -0.3}, until={"cut": 3, "offset": -0.05}, y=0.73,
     labels=[{"text": "CANSANCIO", "at": 9}, {"text": "INCOMODIDAD", "at": 38}, {"text": "FALLARLE A ALGUIEN", "at": 119}])
ad.sfx("synth:heartbeat_01", {"word": "cansancio,"}, 0.3); ad.sfx("synth:subdrop_short", {"word": "fallándole"}, 0.35)

# ── PREGÚNTATE → split con la pregunta en tipografía serif y marco dorado ────────────────────
ad.split({"cut": 3}, {"cut": 6}, bottom=0.5, caption=0.535)
ad.g("SpotlightQuestion", {"cut": 4, "offset": 0.0}, until={"cut": 6, "offset": -0.05}, y=0.6, kicker="ANTES DE COMPROMETERTE",
     question="¿Puedo cumplir esto con la calidad que quiero dar?")
ad.sfx("synth:reverse_swell", {"cut": 4}, 0.3, -0.3); ad.sfx("lib:glass_002", {"word": "calidad"}, 0.3)

# ── DÉJALO POR ESCRITO → Blender: la lapicera firma; cláusulas que se tildan ──────────────────
ad.broll(BL + "ad09_pen/pen.mp4", {"word": "escrito", "offset": -0.25}, {"cut": 7}, speed=0.34, transition="whip-up")
ad.cap_pos.append({"at": {"word": "escrito", "offset": -0.25}, "until": {"cut": 7}, "pos": 0.9})
ad.g("ClauseTicks", {"word": "escrito", "offset": -0.2}, until={"cut": 7, "offset": -0.03}, y=0.06, title="DÉJALO POR ESCRITO",
     items=[{"text": "QUÉ INCLUYE", "at": 26}, {"text": "CUÁNDO SE ENTREGA", "at": 59}, {"text": "CÓMO SE ATIENDEN LOS CAMBIOS", "at": 105}])
for at in (26, 59, 105):
    ad.sfx("synth:click_ui", {"word": "escrito", "offset": -0.2 + at / 30}, 0.4)
ad.sfx("lib:bsb-2842", {"word": "escrito", "offset": 0.4}, 0.18)

# ── CADA LÍMITE QUE CALLAS → “LÍMITE” detrás de Carlos ───────────────────────────────────────
ad.cut_set(7, cutout="_work/cutouts/cut7.webm",
           behind=[{"component": "BehindTitle", "start": 0.3, "duration": 4.45,
                    "props": {"kicker": "CADA LÍMITE QUE CALLAS", "kickerY": 0.035, "lines": [{"text": "LÍMITE", "gradient": True, "color": "#FFBB00", "size": 360}], "y": 0.28, "drift": 0.06}}])
ad.sfx("synth:impact_soft", {"word": "límite"}, 0.45)

# ── TRABAJO QUE NADIE TE ESTÁ PAGANDO → planilla de horas impaga ─────────────────────────────
ad.g("TimesheetUnpaid", {"cut": 8, "offset": 0.05}, until={"cut": 9, "offset": -0.05}, y=0.69, stampAt=48,
     rows=[["Cambio extra del sábado", "3 h"], ["Reunión no pactada", "2 h"], ["Ajustes “rápidos”", "5 h"]])
ad.sfx("synth:impact_punch", {"cut": 8, "offset": 0.05 + 48 / 30}, 0.45)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-82f05f97-07e.mp3", drop=4)
ad.save(emphasis=["prometer", "sostener,", "problema.", "sí", "todo:", "antes,", "disponibles", "cansancio,", "incomodidad", "fallándole",
                  "comprometerte,", "calidad", "escrito", "incluye", "cambios.", "límite", "callas", "nadie", "pagando.", "sígueme", "escalar"],
        hide=[[23.75, 26.28]])
