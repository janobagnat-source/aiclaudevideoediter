# AD02 v2 — “Que tu contenido se sienta como tú”. Línea ejecutiva: IA genérica vs. la persona real.
# Escenas 3D propias (bustos clonados, micrófono), split con cámara frontal, PERSONA detrás de Carlos, cierre plano.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad02/_work/blender/"
ad.set_cams({0: "cam1", 2: "cam1", 8: "cam1"})            # split → frontal
ad.auto_zooms(punch_words=["publicas", "yo”?", "diferentes.", "persona", "importa", "problemas.", "real", "palabras.", "confiar", "sígueme"])

# ── HOOK: split desde el primer frame; la IA escribe un post perfecto… que no suena a vos ─────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5)
ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("PromptBox", 0.1, until={"cut": 1, "offset": -0.05}, y=0.575, stampAt=150,
     prompt="Escribe un post inspirador para mi negocio",
     output="✨ ¡Hoy es el día perfecto para alcanzar tus metas! El éxito es un viaje, no un destino. Cree en ti 🚀 #emprendedor #motivación",
     stamp="ESE NO SOY YO")
for k in range(14):
    ad.sfx("lib:bsb-2842", 0.25 + k * 0.09, 0.14)
ad.sfx("synth:riser_short", {"word": "pero"}, 0.25, -0.8)
ad.sfx("synth:impact_punch", {"word": "no", "offset": -0.02}, 0.55)

# ── IA · PLANTILLAS · FÓRMULAS: chips en la franja baja; luego Blender: el busto que se vuelve oro ─
ad.g("TagRow", {"cut": 1, "offset": 0.05}, until={"word": "escondiendo", "offset": -0.4}, y=0.82,
     tags=[{"text": "IA", "at": 15}, {"text": "PLANTILLAS", "at": 55}, {"text": "FÓRMULAS", "at": 82}], strikeAt=96)
for at in (15, 55, 82):
    ad.sfx("lib:card-slide-3", {"cut": 1, "offset": 0.05 + at / 30}, 0.35)
ad.sfx("synth:swipe_02", {"cut": 1, "offset": 0.05 + 96 / 30}, 0.3)
ad.broll(BL + "ad02_busts/busts.mp4", {"word": "escondiendo", "offset": -0.45}, {"cut": 2}, speed=0.45, transition="zoom-in")
ad.g("KickerTitle", {"word": "nos", "offset": -0.1}, until={"cut": 2, "offset": -0.03}, kicker="LO QUE NOS HACE", align="center", y=0.1,
     lines=[{"text": "DIFERENTES", "color": "#FFBB00", "size": 120}])
ad.sfx("synth:whoosh_heavy", {"word": "escondiendo", "offset": -0.45}, 0.45, -0.1)
ad.sfx("synth:impact_soft", {"word": "diferentes."}, 0.5, -0.15)
ad.sfx("lib:glass_002", {"word": "diferentes."}, 0.35)

# ── LA GENTE QUIERE RECONOCER A LA PERSONA → “PERSONA” gigante detrás de Carlos ──────────────────
ad.cut_set(2, cutout="_work/cutouts/cut2.webm",
           behind=[{"component": "BehindTitle", "start": 1.05, "duration": 3.2,
                    "props": {"kicker": "QUIEREN RECONOCER A LA", "kickerY": 0.035, "lines": [{"text": "PERSONA", "gradient": True, "color": "#FFFFFF", "size": 330}], "y": 0.29, "drift": 0.06}}])
ad.sfx("synth:reverse_swell", {"word": "reconocer"}, 0.3, -0.4)
ad.sfx("synth:impact_soft", {"word": "persona"}, 0.4)
# … cómo piensas / qué te importa / cómo entiendes sus problemas → split con lista editorial
ad.split({"word": "cómo", "n": 1, "offset": -0.1}, {"cut": 3}, bottom=0.5, caption=0.535)
ad.g("NumberedList", {"word": "cómo", "n": 1, "offset": -0.05}, until={"cut": 3, "offset": -0.05}, y=0.585, title="TE QUIEREN CONOCER",
     items=[{"text": "CÓMO PIENSAS", "at": 4}, {"text": "QUÉ TE IMPORTA", "at": 28}, {"text": "CÓMO ENTIENDES SUS PROBLEMAS", "at": 64}])
for at in (4, 28, 64):
    ad.sfx("synth:pop_01", {"word": "cómo", "n": 1, "offset": -0.05 + at / 30}, 0.38)

# ── RECUERDA UNA CONVERSACIÓN REAL → nota de voz del cliente ──────────────────────────────────────
ad.g("VoiceNote", {"word": "recuerda", "offset": -0.1}, until={"cut": 4, "offset": -0.03}, y=0.8, caption="CONVERSACIÓN REAL · CLIENTE", secs=52)
ad.sfx("lib:bsb-1111", {"word": "recuerda"}, 0.25)

# ── LAS TRES PREGUNTAS (fila 1/3, 2/3, 3/3) ─────────────────────────────────────────────────────
ad.g("QuestionStack", {"cut": 4}, until={"cut": 7, "offset": -0.03}, y=0.74,
     items=[{"text": "¿Qué le preocupaba?", "at": 1}, {"text": "¿Qué le explicaste?", "at": 37}, {"text": "¿Cómo lo ayudaste?", "at": 71}])
for c in (4, 5, 6):
    ad.sfx("lib:question_001", {"cut": c}, 0.3)

# ── CUENTA ESO CON TUS PALABRAS → Blender: micrófono de estudio ─────────────────────────────────
ad.broll(BL + "ad02_mic/mic.mp4", {"cut": 7}, {"cut": 8}, speed=0.7, transition="whip-up")
ad.g("KickerTitle", {"cut": 7, "offset": 0.05}, until={"cut": 8, "offset": -0.03}, kicker="CUENTA ESO", align="center", y=0.1,
     lines=[{"text": "CON TUS PALABRAS", "color": "#FFBB00", "size": 92}])
ad.sfx("synth:whoosh_fast", {"cut": 7}, 0.45, -0.08)
ad.sfx("lib:glass_002", {"word": "palabras."}, 0.3)

# ── CÓMO RESUELVES UNA DIFICULTAD REAL → split con caso real ────────────────────────────────────
ad.split({"cut": 8}, {"cut": 9}, bottom=0.5, caption=0.535)
ad.g("CaseCard", {"cut": 8, "offset": 0.1}, until={"cut": 9, "offset": -0.05}, y=0.6, arrowAt=30,
     before="No sabía cuánto cobrar", after="Su tabla de precios en una sesión")
ad.sfx("synth:whoosh_fast", {"cut": 8, "offset": 1.0}, 0.35)
ad.sfx("synth:ding_01", {"cut": 8, "offset": 1.4}, 0.3)

# ── UNA RAZÓN CONCRETA PARA CONFIAR EN TI → medidor de confianza ────────────────────────────────
ad.g("MeterBar", {"word": "razón", "offset": -0.15}, until={"cut": 10, "offset": -0.05}, label="CONFIANZA", y=0.82, fillDur=42)
ad.sfx("synth:riser_short", {"word": "razón"}, 0.25, -0.1)
ad.sfx("synth:ding_success", {"word": "ti."}, 0.3)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-5f49e44a-f2b.mp3", drop=4)
ad.save(emphasis=["publicas", "escrito,", "yo”?", "diferentes.", "persona", "piensas,", "importa", "problemas.", "conversación", "real", "cliente.",
                  "palabras.", "dificultad", "confiar", "sígueme", "escalar", "ventas."],
        hide=[[24.98, 28.66], [28.7, 30.94]])
