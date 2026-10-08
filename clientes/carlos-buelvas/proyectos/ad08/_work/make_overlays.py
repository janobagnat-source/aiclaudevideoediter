# AD08 — Diez minutos para explicar lo que vendes
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["diez", "perderse", "valor.", "frustra,", "ayudar.", "detalles", "necesita.", "realidad:",
                           "prueba:", "entendió.", "mensaje", "clientes.", "sígueme"])

# HOOK: cronómetro corriendo a toda velocidad hasta 10:00 mientras explicás
ad.hook_hit()
ad.g("Stopwatch", 0.05, until={"word": "perderse", "offset": -0.1}, y=0.8, size=0.85, **{"from": 0}, to=600, label="EXPLICANDO…")
for k in range(14):
    ad.sfx("lib:bsb-2842", 0.2 + k * 0.24, 0.16)
ad.sfx("lib:glass_002", {"word": "perderse", "offset": -0.15}, 0.35)
ad.badge("question-bold", {"word": "perderse"}, until={"cut": 1, "offset": -0.03}, label="SE PIERDE", side="right", y=0.44)
ad.g("BlockTitle", {"word": "entender", "offset": -0.1}, until={"cut": 1, "offset": -0.03}, y=0.81, width=0.72, stagger=6, enter="slam",
     lines=[{"text": "ANTES DE VER", "weight": 900}, {"text": "TU VALOR", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "valor."}, 0.5)
ad.sfx("synth:subdrop_short", {"word": "valor."}, 0.4)

# FRUSTRA, PORQUE SABES CUÁNTO PUEDES AYUDAR
ad.badge("smiley-angry-bold", {"word": "frustra,"}, until={"cut": 2, "offset": -0.03}, label="FRUSTRA", side="left", y=0.44)
ad.badge("hand-heart-bold", {"word": "cuánto"}, until={"cut": 2, "offset": -0.03}, label="CUÁNTO PUEDES AYUDAR", side="right", y=0.44)
ad.sfx("synth:glitch_02", {"word": "frustra,"}, 0.25)

# MÉTODOS, HERRAMIENTAS, DETALLES… → pila de tecnicismos (MG b-roll)
ad.badge("graduation-cap-bold", {"word": "demostrar"}, until={"word": "hablando", "offset": -0.12}, label="TODO LO QUE SABES", side="right", y=0.44)
ad.scene("pattern", {"word": "hablando", "offset": -0.1}, {"word": "persona", "offset": -0.05}, word="DETALLES")
ad.g("TaskPile", {"word": "hablando", "offset": -0.05}, until={"word": "persona", "offset": -0.05}, y=0.32, every=10, title="LO QUE LE EXPLICAS",
     items=["MÉTODOS", "HERRAMIENTAS", "DETALLES", "TECNICISMOS", "MÁS DETALLES", "…"])
for k in range(6):
    ad.sfx("synth:pop_02", {"word": "hablando"}, 0.28, 0.1 + k * 0.33)
ad.badge("user-bold", {"word": "persona"}, until={"cut": 3, "offset": -0.03}, label="AÚN NO LO NECESITA", side="left", y=0.44)
ad.sfx("synth:impact_soft", {"word": "necesita."}, 0.45)

# EMPIEZA POR SU REALIDAD
ad.badge("target-bold", {"word": "realidad:", "offset": -0.3}, until={"cut": 5, "offset": -0.03}, label="SU REALIDAD", side="right", y=0.44)
ad.sfx("lib:maximize_006", {"word": "realidad:"}, 0.35, -0.3)
ad.g("Checklist", {"word": "costando,", "offset": -0.25}, until={"cut": 5, "offset": -0.03}, title="EMPIEZA POR",
     items=["QUÉ LE ESTÁ COSTANDO", "CÓMO LE AFECTA", "EN QUÉ PUEDES AYUDAR"], every=36, position=0.84, icon="✓")
for w in ["costando,", "afecta", "puedes"]:
    ad.sfx("synth:pop_01", {"word": w, "n": 2} if w == "puedes" else {"word": w}, 0.4)

# HAZ UNA PRUEBA → explicárselo a alguien de otro rubro (MG b-roll)
ad.badge("flask-bold", {"word": "prueba:", "offset": -0.25}, until={"word": "explícale", "offset": -0.12}, label="HAZ UNA PRUEBA", side="right", y=0.44)
ad.scene("glow", {"word": "explícale", "offset": -0.1}, {"word": "pídele", "offset": -0.05})
ad.g("ChatThread", {"word": "explícale", "offset": -0.05}, until={"word": "pídele", "offset": -0.05}, y=0.29, title="Amigo (otro rubro)",
     messages=[{"text": "Te cuento lo que hago: ayudo a negocios a vender más 🚀", "me": True, "at": 6},
               {"text": "¿Y cómo lo haces? 🤔", "at": 66}])
ad.sfx("lib:pluck_002", {"word": "explícale"}, 0.35, 0.15)
ad.sfx("lib:pluck_001", {"word": "profesión"}, 0.35)
ad.badge("lightbulb-filament-bold", {"word": "pídele"}, until={"cut": 6, "offset": -0.03}, label="¿QUÉ ENTENDIÓ?", side="right", y=0.44)
ad.sfx("lib:question_001", {"word": "entendió."}, 0.35)

# SI NO PUEDE EXPLICARLO → ACLARA TU MENSAJE (3D)
ad.g("QuestionCard", {"cut": 6, "offset": 0.05}, until={"word": "tienes", "offset": -0.05}, y=0.82, kicker="SI NO PUEDE EXPLICAR…",
     question="¿Cómo lo ayudas?")
ad.scene("tunnel", {"word": "mensaje", "offset": -0.08}, {"word": "buscar", "offset": -0.05})
ad.g("Text3DTitle", {"word": "mensaje", "offset": -0.05}, until={"word": "buscar", "offset": -0.05}, text="ACLARA\nTU MENSAJE", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.sfx("synth:riser_short", {"word": "mensaje"}, 0.28, -1.0)
ad.sfx("synth:impact_cinematic", {"word": "mensaje"}, 0.5, -0.05)
ad.badge("users-three-bold", {"word": "buscar"}, until={"cut": 7, "offset": -0.03}, label="MÁS CLIENTES", side="right", y=0.44)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-4245acb6-208.mp3", drop=3)
ad.save(emphasis=["diez", "minutos", "vendes,", "perderse", "valor.", "frustra,", "ayudar.", "demostrar", "métodos,", "herramientas",
                  "detalles", "realidad:", "costando,", "afecta", "prueba:", "servicio", "entendió.", "ayudas,", "mensaje", "aclarar",
                  "sígueme", "escalar"],
        hide=[[34.45, 36.06]])
