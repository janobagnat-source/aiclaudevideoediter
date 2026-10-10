# AD06 v2 — “Contrataste para tener menos trabajo”. Delegar sin liderar = el mismo límite.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad06/_work/blender/"
ad.set_cams({0: "cam1", 3: "cam1", 5: "cam1", 7: "cam1", 8: "cam2"})
ad.auto_zooms(punch_words=["contrataste", "tuyo", "persona.", "frustrante,", "respirar.", "equipo", "liderar.", "yo”,", "proceso?", "decidir?”.", "tarea", "límite:", "tiempo.", "sígueme"])

# ── HOOK: split; “nuevo asistente contratado ✓”… y el tablero se desborda ─────────────────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("KanbanFlood", 0.05, until={"cut": 1, "offset": -0.05}, y=0.565, hireAt=8, floodAt=92)
ad.sfx("synth:ding_success", 0.35, 0.35)
for k in range(10):
    ad.sfx("lib:card-slide-" + str(1 + k % 8), 3.1 + k * 0.22, 0.25)

# ── IBAS A RESPIRAR → respuesta automática que se cancela ─────────────────────────────────────
ad.g("OOOToggle", {"word": "pensabas", "offset": -0.2}, until={"cut": 3, "offset": -0.05}, y=0.78, onAt=8, offAt=58)
ad.sfx("synth:click_ui", {"word": "pensabas", "offset": 0.1}, 0.4); ad.sfx("synth:glitch_02", {"word": "pensabas", "offset": -0.2 + 58 / 30}, 0.35)

# ── CREER QUE EL EQUIPO RESOLVERÁ TODO → split con organigrama ────────────────────────────────
ad.split({"cut": 3}, {"cut": 4}, bottom=0.5, caption=0.535)
ad.g("OrgChartGrow", {"cut": 3}, until={"cut": 4, "offset": -0.05}, y=0.565, levels=[3, 6])
for k in range(9):
    ad.sfx("synth:pop_02", {"cut": 3, "offset": (12 + k * 6) / 30}, 0.22)

# ── APRENDER A LIDERAR → “LIDERAR” detrás de Carlos ───────────────────────────────────────────
ad.cut_set(4, cutout="_work/cutouts/cut4.webm",
           behind=[{"component": "BehindTitle", "start": 1.6, "duration": 1.55,
                    "props": {"kicker": "CRECER EXIGE", "kickerY": 0.035, "lines": [{"text": "LIDERAR", "gradient": True, "color": "#FFBB00", "size": 330}], "y": 0.28, "drift": 0.05}}])
ad.sfx("synth:impact_soft", {"word": "liderar."}, 0.45)

# ── “NADIE HACE LAS COSAS COMO YO” → se tacha; luego las 3 preguntas sin tildar ───────────────
ad.g("QuoteStrike", {"word": "“nadie", "offset": -0.2}, until={"word": "“¿Expliqué", "offset": -0.25}, quote="Nadie hace las cosas como yo", strikeAt=40, y=0.78)
ad.sfx("synth:swipe_02", {"word": "“nadie", "offset": -0.2 + 40 / 30}, 0.35)
ad.split({"word": "“¿Expliqué", "offset": -0.2}, {"cut": 8}, bottom=0.5, caption=0.535)
ad.g("SelfCheck", {"word": "“¿Expliqué", "offset": -0.15}, until={"cut": 8, "offset": -0.05}, y=0.585,
     items=[{"text": "¿Expliqué lo que esperaba?", "at": 2}, {"text": "¿Le di un proceso?", "at": 50}, {"text": "¿Le enseñé cómo decidir?", "at": 98}])
for at in (2, 50, 98):
    ad.sfx("lib:question_001", {"word": "“¿Expliqué", "offset": -0.15 + at / 30}, 0.3)

# ── ELIGE UNA TAREA Y DEFINE CÓMO SE ENTREGA BIEN → procedimiento ─────────────────────────────
ad.g("SOPCard", {"word": "tarea", "offset": -0.2}, until={"cut": 9, "offset": -0.05}, y=0.66, every=12,
     task="Responder consultas de clientes", steps=["Responder en menos de 2 h", "Usar la guía de precios", "Agendar llamada si hay interés"], done="la consulta queda agendada")
ad.sfx("lib:bsb-2842", {"word": "define"}, 0.2)

# ── TODO PASA POR TI → Blender: engranajes que se traban; el límite es tu tiempo ──────────────
ad.broll(BL + "ad06_gears/gears.mp4", {"word": "pasando", "offset": -0.15}, {"cut": 10}, speed=0.4, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "pasando", "offset": -0.15}, "until": {"cut": 10}, "pos": 0.88})
ad.g("KickerTitle", {"word": "pasando", "offset": -0.1}, until={"word": "límite:", "offset": -0.1}, kicker="SI TODO", align="center", y=0.09, lines=[{"text": "PASA POR TI", "color": "#FFBB00", "size": 110}])
ad.g("KickerTitle", {"word": "límite:", "offset": -0.08}, until={"cut": 10, "offset": -0.03}, kicker="EL MISMO", align="center", y=0.09, lines=[{"text": "LÍMITE", "color": "#FF4D5E", "size": 140}])
ad.sfx("synth:whoosh_heavy", {"word": "pasando", "offset": -0.15}, 0.45, -0.1)
ad.sfx("synth:tape_stop", {"word": "límite:"}, 0.45, -0.1); ad.sfx("synth:impact_cinematic", {"word": "límite:"}, 0.45)
ad.g("KickerTitle", {"cut": 10, "offset": 0.02}, until={"cut": 11, "offset": -0.03}, align="center", y=0.8, lines=[{"text": "TU TIEMPO", "color": "#FFBB00", "size": 120}])
ad.sfx("synth:tick_01", {"word": "tiempo."}, 0.4)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-cafeace9-eb9.mp3", drop=1)
ad.save(emphasis=["contrataste", "menos", "trabajo…", "tuyo", "revisar", "frustrante,", "respirar.", "crecer", "equipo", "liderar.",
                  "nadie", "yo”,", "esperaba?", "proceso?", "decidir?”.", "tarea", "bien.", "decisión", "límite:", "tiempo.", "sígueme", "escalar"],
        hide=[[38.76, 39.6]])
