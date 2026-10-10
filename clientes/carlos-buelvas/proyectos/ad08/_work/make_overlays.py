# AD08 v2 — “Diez minutos para explicar lo que vendes”. Del enredo al mensaje claro.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad08/_work/blender/"
ad.set_cams({0: "cam1", 4: "cam1"})
ad.auto_zooms(punch_words=["diez", "perderse", "valor.", "frustra,", "ayudar.", "detalles", "necesita.", "realidad:", "prueba:", "entendió.", "mensaje", "clientes.", "sígueme"])

# ── HOOK: split; la presentación de 48 diapositivas, el reloj a 10:00 y la atención que se cae ─
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("SlideMarathon", 0.05, until={"cut": 1, "offset": -0.05}, y=0.565, endAt=165)
for k in range(24):
    ad.sfx("synth:click_ui", 0.3 + k * 0.22, 0.16)
ad.sfx("synth:tick_01", {"word": "perderse"}, 0.35); ad.sfx("synth:subdrop_short", {"word": "valor."}, 0.4)

# ── MÉTODOS, HERRAMIENTAS, DETALLES → Blender: el hilo enredado + nube de tecnicismos ─────────
ad.broll(BL + "ad08_knot/knot.mp4", {"word": "hablando", "offset": -0.1}, {"word": "persona", "offset": 0.05}, speed=0.14, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "hablando", "offset": -0.1}, "until": {"word": "persona", "offset": 0.05}, "pos": 0.88})
ad.g("JargonCloud", {"word": "hablando", "offset": 0.0}, until={"word": "persona", "offset": 0.02}, every=5)
for k in range(10):
    ad.sfx("synth:pop_02", {"word": "hablando", "offset": k * 5 / 30}, 0.22)
ad.sfx("synth:glitch_01", {"word": "detalles"}, 0.25)

# ── EMPIEZA POR SU REALIDAD → el hilo se ordena en una línea recta; luego split con su realidad ─
ad.broll(BL + "ad08_knot/knot.mp4", {"cut": 3}, {"word": "costando,", "offset": -0.15}, speed=0.74, transition="whip-up", inn=0.45)
ad.cap_pos.append({"at": {"cut": 3}, "until": {"word": "costando,", "offset": -0.15}, "pos": 0.88})
ad.g("KickerTitle", {"cut": 3, "offset": 0.05}, until={"word": "costando,", "offset": -0.17}, kicker="EMPIEZA POR", align="center", y=0.1, lines=[{"text": "SU REALIDAD", "color": "#FFBB00", "size": 120}])
ad.sfx("synth:whoosh_medium", {"cut": 3}, 0.4, -0.1); ad.sfx("synth:reverse_swell", {"cut": 3, "offset": 0.4}, 0.25)
ad.split({"word": "costando,", "offset": -0.2}, {"cut": 5}, bottom=0.5, caption=0.535)
ad.g("ClientReality", {"word": "costando,", "offset": -0.15}, until={"cut": 5, "offset": -0.05}, y=0.585,
     rows=[{"k": "LE ESTÁ COSTANDO", "v": "$3.000 al mes en clientes que no cierran", "at": 6, "color": "#FF4D5E"},
           {"k": "CÓMO LE AFECTA", "v": "Trabaja los fines de semana", "at": 42},
           {"k": "EN QUÉ AYUDAS", "v": "Un proceso de ventas simple", "at": 87, "color": "#00E051"}])
for at in (6, 42, 87):
    ad.sfx("lib:card-slide-5", {"word": "costando,", "offset": -0.15 + at / 30}, 0.3)

# ── HAZ UNA PRUEBA → medidor de comprensión; luego Blender: la lamparita se enciende ──────────
ad.g("ClarityGauge", {"word": "explícale", "offset": -0.1}, until={"word": "pídele", "offset": -0.15}, y=0.7, to=18)
ad.sfx("synth:riser_short", {"word": "explícale"}, 0.2); ad.sfx("lib:question_001", {"word": "profesión"}, 0.3)
ad.broll(BL + "ad08_bulb/bulb.mp4", {"word": "pídele", "offset": -0.1}, {"cut": 6}, speed=0.63, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "pídele", "offset": -0.1}, "until": {"cut": 6}, "pos": 0.88})
ad.g("KickerTitle", {"word": "pídele", "offset": -0.05}, until={"cut": 6, "offset": -0.03}, kicker="PÍDELE QUE TE DIGA", align="center", y=0.09, lines=[{"text": "¿QUÉ ENTENDIÓ?", "color": "#FFBB00", "size": 104}])
ad.sfx("synth:shutter_01", {"word": "pídele", "offset": -0.1 + 0.35 * 48 / 30 / 0.63}, 0.35); ad.sfx("synth:ding_01", {"word": "entendió."}, 0.3)

# ── TIENES UN MENSAJE QUE ACLARAR → texto detrás de Carlos ────────────────────────────────────
ad.cut_set(6, cutout="_work/cutouts/cut6.webm",
           behind=[{"component": "BehindTitle", "start": 1.9, "duration": 4.0,
                    "props": {"kicker": "ANTES DE BUSCAR MÁS CLIENTES", "kickerY": 0.035, "lines": [{"text": "ACLARA", "gradient": True, "color": "#FFBB00", "size": 330}, {"text": "TU MENSAJE", "gradient": True, "color": "#FFFFFF", "size": 200}], "y": 0.28, "drift": 0.05}}])
ad.sfx("synth:impact_soft", {"word": "mensaje"}, 0.45)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-4245acb6-208.mp3", drop=3)
ad.save(emphasis=["diez", "minutos", "vendes,", "perderse", "valor.", "frustra,", "ayudar.", "demostrar", "métodos,", "herramientas",
                  "detalles", "realidad:", "costando,", "afecta", "prueba:", "servicio", "entendió.", "ayudas,", "mensaje", "aclarar", "sígueme", "escalar"])
