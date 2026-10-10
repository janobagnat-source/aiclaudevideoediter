# AD07 v2 — “El miedo a dar seguimiento”. Del borrador que no se envía al mensaje con una razón.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad07/_work/blender/"
ad.set_cams({0: "cam1", 1: "cam1", 2: "cam2", 3: "cam1", 5: "cam1", 6: "cam2", 7: "cam1", 8: "cam1"})
ad.auto_zooms(punch_words=["miedo", "molestarlo?", "envías.", "desesperado?", "no?”.", "pendiente.", "llamada:", "importaba:", "juntos?”.", "razón", "derecho", "sígueme"])

# ── HOOK: split; el borrador escrito… y el cursor que no se anima a enviar ─────────────────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 2}, bottom=0.5, caption=0.535)
ad.g("DraftUnsent", 0.05, until={"cut": 2, "offset": -0.05}, y=0.6, text="Hola Laura 👋 ¿Pudiste ver la propuesta?", days="escrito hace 3 días")
for k in range(10):
    ad.sfx("lib:bsb-2842", 0.2 + k * 0.11, 0.14)
ad.sfx("synth:heartbeat_01", {"word": "molestarlo?"}, 0.35); ad.sfx("synth:glitch_02", {"word": "envías."}, 0.3)

# ── ¿Y SI PAREZCO DESESPERADO? ¿Y SI ME DICE QUE NO? → pensamientos ────────────────────────────
ad.g("ThoughtBubbles", {"cut": 2, "offset": 0.05}, until={"cut": 4, "offset": -0.05}, y=0.72,
     items=[{"text": "¿Y si parezco desesperado?", "at": 14}, {"text": "¿Y si me dice que no?", "at": 70}])
ad.sfx("synth:reverse_swell", {"cut": 2}, 0.25); ad.sfx("synth:reverse_swell", {"cut": 3}, 0.25)

# ── UNA CONVERSACIÓN PENDIENTE → texto detrás de Carlos ───────────────────────────────────────
ad.cut_set(4, cutout="_work/cutouts/cut4.webm",
           behind=[{"component": "BehindTitle", "start": 1.0, "duration": 2.95,
                    "props": {"kicker": "UNA CONVERSACIÓN", "kickerY": 0.035, "lines": [{"text": "PENDIENTE", "gradient": True, "color": "#FFFFFF", "size": 300}], "y": 0.29, "drift": 0.05}}])
ad.sfx("synth:impact_soft", {"word": "pendiente."}, 0.45)

# ── DESDE LA PRIMERA LLAMADA: ACUERDEN CUÁNDO Y QUÉ → split con invitación de calendario ──────
ad.split({"word": "empieza", "offset": -0.15}, {"cut": 6}, bottom=0.5, caption=0.535)
ad.g("CalendarInvite", {"word": "empieza", "offset": -0.1}, until={"cut": 6, "offset": -0.05}, y=0.575, title="Seguimiento · Laura",
     when="Jueves 10:00 · 20 min", agenda="La propuesta y el presupuesto", whenAt=70, agendaAt=108, okAt=128)
ad.sfx("lib:card-slide-2", {"word": "cuándo"}, 0.35); ad.sfx("lib:bsb-2842", {"word": "revisarán."}, 0.2); ad.sfx("synth:ding_success", {"word": "revisarán.", "offset": 0.6}, 0.3)

# ── RETOMA ALGO QUE LE IMPORTABA → nota de la llamada con resaltador ──────────────────────────
ad.g("NoteRecall", {"cut": 6, "offset": 0.1}, until={"cut": 7, "offset": -0.05}, y=0.76, markAt=22,
     note="Le preocupa no tener tiempo para implementar todo.", mark="no tener tiempo para implementar")
ad.sfx("synth:swipe_01", {"cut": 6, "offset": 0.85}, 0.3)

# ── EL MENSAJE CORRECTO → split: se escribe, se envía, responde ───────────────────────────────
ad.split({"cut": 7}, {"cut": 9}, bottom=0.5, caption=0.535)
ad.g("SendFlow", {"cut": 7}, until={"cut": 9, "offset": -0.05}, y=0.6, sendAt=140, replyAt=150, reply="¡Sí! Me vendría genial 🙌",
     lines=[{"text": "Me comentaste que tenías esta duda.", "at": 4}, {"text": "¿Te ayudaría que la revisemos juntos?", "at": 73}])
for k in range(12):
    ad.sfx("lib:bsb-2842", {"cut": 7, "offset": 0.15 + k * 0.1}, 0.12)
ad.sfx("synth:whoosh_fast", {"cut": 7, "offset": 140 / 30}, 0.35); ad.sfx("lib:pluck_001", {"cut": 7, "offset": 150 / 30}, 0.35)

# ── UNA RAZÓN PARA RESPONDER → Blender: el avión de papel despega ─────────────────────────────
ad.broll(BL + "ad07_plane/plane.mp4", {"cut": 9}, {"cut": 10}, speed=0.52, transition="whip-up")
ad.cap_pos.append({"at": {"cut": 9}, "until": {"cut": 10}, "pos": 0.88})
ad.g("KickerTitle", {"cut": 9, "offset": 0.05}, until={"cut": 10, "offset": -0.03}, kicker="LE DAS UNA RAZÓN", align="center", y=0.09, lines=[{"text": "PARA RESPONDER", "color": "#FFBB00", "size": 96}])
ad.sfx("synth:whoosh_heavy", {"cut": 9, "offset": 16 / 30 / 0.52}, 0.4)

# ── SU DERECHO A DECIR QUE NO → Blender: la puerta queda abierta ──────────────────────────────
ad.broll(BL + "ad07_door/door.mp4", {"word": "derecho", "offset": -0.1}, {"cut": 11}, speed=0.69, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "derecho", "offset": -0.1}, "until": {"cut": 11}, "pos": 0.88})
ad.g("KickerTitle", {"word": "derecho", "offset": -0.05}, until={"cut": 11, "offset": -0.03}, kicker="SU DERECHO", align="center", y=0.09, lines=[{"text": "A DECIR QUE NO", "color": "#FFBB00", "size": 96}])
ad.sfx("synth:reverse_swell_long", {"word": "derecho"}, 0.3, -0.3)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-c37c19bc-ebb.mp3", drop=2)
ad.save(emphasis=["miedo", "seguimiento", "molestarlo?", "escrito,", "envías.", "desesperado?", "no?”.", "incómoda,", "pendiente.",
                  "seguro,", "llamada:", "retoma", "importaba:", "duda.", "juntos?”.", "escribes", "razón", "derecho", "sígueme", "escalar"])
