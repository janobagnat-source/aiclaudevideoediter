# AD09 — Prometer lo que no puedes sostener
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["prometer", "problema.", "sí", "hora.", "cansancio,", "alguien.", "comprometerte,", "calidad",
                           "escrito", "cambios.", "límite", "pagando.", "sígueme"])

# HOOK: la propuesta llena de promesas imposibles → ESTÁS COMPRANDO UN PROBLEMA
ad.hook_hit()
ad.scene("glow", {"word": "prometer", "offset": -0.1}, {"word": "estás", "offset": -0.05}, word="PROMESAS")
ad.g("ContractDoc", {"word": "prometer", "offset": -0.05}, until={"word": "estás", "offset": -0.05}, y=0.3, title="TU PROPUESTA",
     items=["✅ Entrega en 24 h", "✅ Todo incluido", "✅ Disponible 24/7"], every=12, sign=True)
for k in range(3):
    ad.sfx("synth:pop_01", {"word": "prometer"}, 0.35, 0.2 + k * 0.4)
ad.g("BlockTitle", {"word": "estás"}, until={"cut": 1, "offset": -0.03}, y=0.81, width=0.8, stagger=6, enter="slam",
     lines=[{"text": "ESTÁS COMPRANDO", "weight": 900}, {"text": "UN PROBLEMA", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "estás"}, 0.5)
ad.sfx("synth:glitch_02", {"word": "problema."}, 0.3)
ad.sfx("synth:subdrop_short", {"word": "problema."}, 0.4)

# DECIMOS QUE SÍ A TODO (3D) → la lista de “sí”
ad.badge("user-bold", {"word": "cliente"}, until={"word": "sí", "n": 2, "offset": -0.1}, label="NECESITAMOS ESE CLIENTE", side="right", y=0.44)
ad.scene("tunnel", {"word": "sí", "n": 2, "offset": -0.08}, {"word": "entregar", "offset": -0.06})
ad.g("Text3DTitle", {"word": "sí", "n": 2, "offset": -0.05}, until={"word": "entregar", "offset": -0.06}, text="SÍ A TODO", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.5, depth=0.35)
ad.sfx("synth:impact_cinematic", {"word": "sí", "n": 2}, 0.5, -0.05)
ad.sfx("synth:riser_short", {"word": "sí", "n": 2}, 0.22, -0.9)
ad.g("CostTags", {"word": "entregar", "offset": -0.2}, until={"cut": 2, "offset": -0.03}, y=0.8, tag="SÍ",
     items=["ENTREGAR ANTES", "INCLUIR MÁS COSAS", "DISPONIBLE A CUALQUIER HORA"], delays=[6, 37, 76])
for w in ["entregar", "incluir", "disponibles"]:
    ad.sfx("lib:switch7", {"word": w}, 0.3)

# CANSANCIO · INCOMODIDAD · FALLARLE A ALGUIEN
ad.g("BatteryDrain", {"word": "cansancio,", "offset": -0.1}, until={"cut": 3, "offset": -0.03}, x=0.83, y=0.42, size=0.6, label="ENERGÍA", **{"from": 80}, to=5)
ad.badge("smiley-nervous-bold", {"word": "incomodidad"}, until={"word": "esa", "offset": -0.05}, label="INCOMODIDAD", side="left", y=0.44)
ad.badge("heart-break-bold", {"word": "fallándole"}, until={"cut": 3, "offset": -0.03}, label="FALLARLE A ALGUIEN", side="left", y=0.44)
ad.sfx("lib:bsb-0307", {"word": "cansancio,"}, 0.3)
ad.sfx("synth:impact_soft", {"word": "fallándole"}, 0.45)

# ANTES DE COMPROMETERTE, PREGÚNTATE
ad.g("QuestionCard", {"word": "pregúntate:", "offset": -0.05}, until={"cut": 6, "offset": -0.03}, y=0.82, kicker="ANTES DE COMPROMETERTE",
     question="¿Puedo cumplir esto con la calidad que quiero dar?")
ad.sfx("lib:question_001", {"word": "pregúntate:"}, 0.4)
ad.badge("seal-check-bold", {"word": "calidad"}, until={"cut": 6, "offset": -0.03}, label="CALIDAD", side="right", y=0.44)
ad.sfx("lib:glass_002", {"word": "calidad"}, 0.3)

# DÉJALO POR ESCRITO → acuerdo de servicio que se firma (MG b-roll)
ad.scene("glow", {"word": "escrito", "offset": -0.12}, {"cut": 7, "offset": -0.02}, word="ACUERDO")
ad.g("ContractDoc", {"word": "escrito", "offset": -0.08}, until={"cut": 7, "offset": -0.02}, y=0.3, title="ACUERDO DE SERVICIO",
     items=["Qué incluye", "Cuándo se entrega", "Cómo se atienden los cambios"], delays=[15, 56, 101], sign=True)
for w in ["incluye", "cuándo", "atenderás"]:
    ad.sfx("synth:pop_01", {"word": w}, 0.4)
ad.sfx("lib:bsb-2842", {"word": "cambios."}, 0.3, 0.2)

# CADA LÍMITE QUE CALLAS → TRABAJO QUE NADIE TE PAGA ($0)
ad.badge("lock-simple-bold", {"word": "límite"}, until={"word": "trabajo", "offset": -0.1}, label="EL LÍMITE QUE CALLAS", side="right", y=0.44)
ad.sfx("lib:maximize_006", {"word": "límite"}, 0.35)
ad.scene("glow", {"word": "trabajo", "offset": -0.1}, {"cut": 9, "offset": -0.02}, word="GRATIS")
ad.g("PriceDrop", {"word": "trabajo", "offset": -0.05}, until={"cut": 9, "offset": -0.02}, y=0.3, **{"from": 1500}, to=0, label="TE PAGAN", dropAt=24)
ad.sfx("synth:whoosh_fast", {"word": "nadie"}, 0.4)
ad.sfx("synth:impact_punch", {"word": "pagando."}, 0.45)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-82f05f97-07e.mp3", drop=4)
ad.save(emphasis=["prometer", "sostener,", "problema.", "sí", "todo:", "antes,", "disponibles", "cansancio,", "incomodidad", "fallándole",
                  "comprometerte,", "calidad", "escrito", "incluye", "cambios.", "límite", "callas", "nadie", "pagando.", "sígueme", "escalar"],
        hide=[[9.0, 10.22]])
