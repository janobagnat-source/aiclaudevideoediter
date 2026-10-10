# AD10 v2 — “La esperanza de que más publicidad lo resuelva”. Antes de pagar más, mira tu proceso.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad10/_work/blender/"
ad.set_cams({0: "cam1", 3: "cam1", 4: "cam1", 5: "cam1", 6: "cam1", 8: "cam2"})
ad.auto_zooms(punch_words=["preocupado", "ventas", "publicidad,", "cuentas", "rápida.", "acercaron.", "respondiste?", "propuesta?", "resolver?", "diez", "detuvieron.", "ahí.", "gasto", "sígueme"])

# ── HOOK: split; el panel de anuncios: subís el presupuesto, el gasto se dispara, ventas = 0 ───
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("AdsDashboard", 0.05, until={"cut": 1, "offset": -0.05}, y=0.57, boostAt=100)
ad.sfx("synth:riser_short", {"word": "pago"}, 0.3, -0.3); ad.sfx("lib:bsb-1417", {"word": "publicidad,"}, 0.3)
for k in range(8):
    ad.sfx("synth:tick_01", {"word": "publicidad,", "offset": 0.1 + k * 0.15}, 0.16)

# ── CUENTAS POR PAGAR → facturas vencidas + el botón de la solución rápida ───────────────────
ad.g("BillsStack", {"word": "cuentas", "offset": -0.2}, until={"cut": 3, "offset": -0.05}, y=0.7, quickAt=int((11.02 - 8.5) * 30))
for k in range(3):
    ad.sfx("lib:card-slide-" + str(3 + k), {"word": "cuentas", "offset": -0.2 + k * 0.3}, 0.3)
ad.sfx("synth:ding_01", {"word": "solución"}, 0.3)

# ── MIRA A LOS QUE YA SE ACERCARON + LAS 3 PREGUNTAS → split con la lista y su auditoría ──────
ad.split({"cut": 3}, {"cut": 7}, bottom=0.5, caption=0.535)
ad.g("LeadsList", {"cut": 3}, until={"cut": 7, "offset": -0.05}, y=0.575,
     audit=[int((16.40 - 12.28) * 30) + 4, int((17.84 - 12.28) * 30) + 4, int((19.34 - 12.28) * 30) + 4])
for k in range(5):
    ad.sfx("synth:pop_low", {"cut": 3, "offset": 0.15 + k * 0.17}, 0.2)
for c in (4, 5, 6):
    ad.sfx("synth:click_ui", {"cut": c, "offset": 0.15}, 0.4)

# ── REVISA TUS ÚLTIMAS 10 CONVERSACIONES → Blender: la luz se detiene en la que quedó colgada ──
ad.broll(BL + "ad10_inbox2/inbox.mp4", {"word": "últimas", "offset": -0.2}, {"cut": 8}, speed=0.5, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "últimas", "offset": -0.2}, "until": {"cut": 8}, "pos": 0.88})
ad.g("KickerTitle", {"word": "últimas", "offset": -0.15}, until={"cut": 8, "offset": -0.03}, kicker="REVISA TUS ÚLTIMAS", align="center", y=0.09, lines=[{"text": "10 CONVERSACIONES", "color": "#FFBB00", "size": 88}])
ad.sfx("synth:whoosh_medium", {"word": "últimas", "offset": -0.2}, 0.4, -0.1); ad.sfx("synth:impact_soft", {"word": "detuvieron."}, 0.45)

# ── CONSULTAS SIN RESPONDER / PROPUESTAS SIN SEGUIMIENTO → pendientes; EMPIEZA POR AHÍ ───────
ad.g("BacklogBadges", {"word": "consultas", "offset": -0.2}, until={"cut": 9, "offset": -0.05}, y=0.72, hereAt=int((29.36 - 26.44) * 30),
     items=[{"text": "Consultas sin responder", "n": 7, "at": 4}, {"text": "Propuestas sin seguimiento", "n": 4, "at": int((28.09 - 26.44) * 30)}])
ad.sfx("synth:pop_01", {"word": "consultas"}, 0.35); ad.sfx("synth:pop_01", {"word": "propuestas"}, 0.35); ad.sfx("synth:impact_punch", {"word": "empieza"}, 0.4)

# ── MÁS GENTE AL MISMO PROCESO → Blender: monedas que se escapan del embudo; gasto vs ventas ─
ad.broll(BL + "ad10_leak/leak.mp4", {"cut": 9}, {"word": "aumentar", "offset": -0.1}, speed=0.74, transition="whip-up")
ad.cap_pos.append({"at": {"cut": 9}, "until": {"word": "aumentar", "offset": -0.1}, "pos": 0.88})
ad.g("KickerTitle", {"cut": 9, "offset": 0.05}, until={"word": "aumentar", "offset": -0.12}, kicker="MÁS GENTE AL", align="center", y=0.09, lines=[{"text": "MISMO PROCESO", "color": "#FFBB00", "size": 104}])
for k in range(8):
    ad.sfx("lib:bsb-0339", {"cut": 9, "offset": 0.2 + k * 0.28}, 0.18)
ad.g("TwinLines", {"word": "aumentar", "offset": -0.05}, until={"cut": 10, "offset": -0.05}, y=0.72)
ad.sfx("synth:glitch_02", {"word": "frenando"}, 0.3)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-35df4743-377.mp3", drop=0)
ad.save(emphasis=["preocupado", "ventas", "publicidad,", "mejorar”.", "urgencia.", "cuentas", "rápida.", "invertir", "acercaron.",
                  "respondiste?", "propuesta?", "duda", "diez", "conversaciones", "detuvieron.", "consultas", "seguimiento,", "ahí.", "gasto", "frenando", "sígueme", "escalar"])
