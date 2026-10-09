# AD07 — El miedo a dar seguimiento
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["miedo", "molestarlo?", "envías.", "desesperado?", "no?”.", "pendiente.", "llamada:", "importaba:",
                           "juntos?”.", "razón", "derecho", "sígueme"])

# HOOK: el mensaje de seguimiento escrito… que nunca se envía
ad.hook_hit()
ad.g("ChatThread", 0.05, until={"word": "pero", "offset": -0.05}, y=0.82, title="Cliente",
     messages=[{"text": "Hola 👋 ¿pudiste revisar la propuesta?", "me": True, "at": 22}])
for k in range(9):
    ad.sfx("lib:bsb-2842", 0.25 + k * 0.1, 0.16)
ad.badge("smiley-nervous-bold", {"word": "molestarlo?", "offset": -0.1}, until={"cut": 1, "offset": -0.03}, label="¿MOLESTAR?", side="right", y=0.44)
ad.sfx("lib:question_001", {"word": "molestarlo?"}, 0.35)
ad.g("BlockTitle", {"word": "pero"}, until={"cut": 2, "offset": -0.03}, y=0.81, width=0.68, stagger=6, enter="slam",
     lines=[{"text": "ESCRITO…", "weight": 900}, {"text": "SIN ENVIAR", "color": "gold"}])
ad.badge("paper-plane-tilt-bold", {"word": "envías."}, until={"cut": 2, "offset": -0.03}, label="NO LO ENVÍAS", side="left", y=0.44)
ad.sfx("synth:glitch_02", {"word": "envías."}, 0.3)
ad.sfx("synth:impact_punch", {"word": "envías."}, 0.4)

# ¿Y SI…? → los dos miedos (MG b-roll)
ad.scene("pattern", {"word": "“¿Y", "offset": -0.1}, {"cut": 4, "offset": -0.02}, word="¿Y SI…?")
ad.g("IconBadge", {"word": "desesperado?", "offset": -0.2}, until={"cut": 4, "offset": -0.02}, icon=ad.icon("smiley-sad-bold"), x=0.3, y=0.3,
     leader="none", size=1.05, label="¿DESESPERADO?")
ad.g("IconBadge", {"word": "dice"}, until={"cut": 4, "offset": -0.02}, icon=ad.icon("x-circle-bold"), x=0.7, y=0.3, leader="none", size=1.05, label="¿UN NO?")
ad.sfx("synth:pop_01", {"word": "desesperado?", "offset": -0.2}, 0.45)
ad.sfx("synth:pop_01", {"word": "dice"}, 0.45)
ad.sfx("lib:bsb-1111", {"word": "“¿Y"}, 0.2, 0.1)

# CONVERSACIÓN PENDIENTE
ad.badge("hourglass-medium-bold", {"word": "incómoda,"}, until={"cut": 5, "offset": -0.03}, label="RESPUESTA INCÓMODA", side="right", y=0.44)
ad.g("BlockTitle", {"word": "conversación", "offset": -0.15}, until={"cut": 5, "offset": -0.03}, y=0.81, width=0.8, stagger=8, enter="rise", sparkle=1,
     lines=[{"text": "CONVERSACIÓN", "weight": 900}, {"text": "PENDIENTE", "color": "gold"}])
ad.sfx("synth:subdrop_short", {"word": "pendiente."}, 0.4)

# DESDE LA PRIMERA LLAMADA: ACUERDEN… → acta de la llamada (MG b-roll)
ad.badge("phone-call-bold", {"word": "llamada:", "offset": -0.25}, until={"word": "acuerden", "offset": -0.1}, label="PRIMERA LLAMADA", side="right", y=0.44)
ad.sfx("lib:pluck_001", {"word": "llamada:"}, 0.35, -0.2)
ad.scene("glow", {"word": "acuerden", "offset": -0.1}, {"cut": 6, "offset": -0.02}, word="ACUERDO")
ad.g("ContractDoc", {"word": "acuerden", "offset": -0.05}, until={"cut": 6, "offset": -0.02}, y=0.3, title="ACUERDO DE LA LLAMADA",
     items=["📅 Cuándo volvemos a hablar", "📋 Qué vamos a revisar"], delays=[20, 58], sign=False)
ad.sfx("synth:pop_01", {"word": "cuándo"}, 0.4)
ad.sfx("synth:pop_01", {"word": "revisarán."}, 0.4, -0.2)

# RETOMA ALGO QUE LE IMPORTABA
ad.badge("arrow-u-up-left-bold", {"word": "retoma"}, until={"cut": 7, "offset": -0.03}, label="RETOMA", side="left", y=0.44)
ad.badge("heart-bold", {"word": "importaba:", "offset": -0.15}, until={"cut": 7, "offset": -0.03}, label="LO QUE LE IMPORTA", side="right", y=0.44)
# el mensaje correcto → y el cliente responde
ad.scene("glow", {"cut": 7, "offset": 0.0}, {"cut": 9, "offset": -0.02})
ad.g("ChatThread", {"cut": 7, "offset": 0.02}, until={"cut": 9, "offset": -0.02}, y=0.29, title="Cliente",
     messages=[{"text": "Me comentaste que tenías esta duda 🤔", "me": True, "at": 6},
               {"text": "¿Te ayudaría que la revisemos juntos?", "me": True, "at": 80},
               {"text": "¡Sí, me encantaría! 🙌", "at": 146}])
ad.sfx("lib:pluck_002", {"cut": 7}, 0.35, 0.2)
ad.sfx("lib:pluck_002", {"word": "ayudaría"}, 0.35)
ad.sfx("lib:confirmation_002", {"word": "juntos?”."}, 0.4, 0.4)

# POR QUÉ ESCRIBES · UNA RAZÓN · SU DERECHO A DECIR NO
ad.g("Checklist", {"word": "sabes", "offset": -0.2}, until={"word": "derecho", "offset": -0.1}, title="ASÍ…",
     items=["SABES POR QUÉ ESCRIBES", "LE DAS UNA RAZÓN", "RESPETAS SU DECISIÓN"], every=57, position=0.84, icon="✓")
for w in ["escribes", "razón", "respetando"]:
    ad.sfx("synth:pop_01", {"word": w}, 0.4)
ad.scene("tunnel", {"word": "derecho", "offset": -0.08}, {"cut": 11, "offset": -0.02})
ad.g("Text3DTitle", {"word": "derecho", "offset": -0.05}, until={"cut": 11, "offset": -0.02}, text="SU DERECHO\nA DECIR NO", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.sfx("synth:riser_short", {"word": "derecho"}, 0.28, -1.0)
ad.sfx("synth:impact_cinematic", {"word": "derecho"}, 0.5, -0.05)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-c37c19bc-ebb.mp3", drop=2)
ad.save(emphasis=["miedo", "seguimiento", "molestarlo?", "escrito,", "envías.", "desesperado?", "no?”.", "incómoda,", "pendiente.",
                  "seguro,", "llamada:", "retoma", "importaba:", "duda.", "juntos?”.", "escribes", "razón", "derecho", "sígueme", "escalar"],
        hide=[[33.03, 35.5]])
