# AD04 — Cuando “está caro” se siente personal
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["caro”…", "vale", "precio", "respira", "propuesta.", "confianza.", "preocupa.", "entregar.",
                           "descuento,", "decisión", "miedo", "sígueme"])

# HOOK: llega el mensaje del cliente “está caro” → ¿NO VALES SUFICIENTE?
ad.hook_hit()
ad.g("ChatThread", 0.05, until={"word": "vale", "offset": -0.08}, y=0.8, title="Cliente",
     messages=[{"text": "Vi tu propuesta 👀", "at": 2}, {"text": "Me interesa… pero está caro 😬", "at": 38}])
ad.sfx("lib:pluck_001", 0.12, 0.4)
ad.sfx("lib:pluck_002", {"word": "“está"}, 0.45, -0.15)
ad.sfx("synth:impact_punch", {"word": "caro”…"}, 0.5)
ad.sfx("synth:riser_short", {"word": "vale"}, 0.25, -1.2)
ad.g("BlockTitle", {"word": "vale", "offset": -0.05}, until={"cut": 2, "offset": -0.03}, y=0.82, width=0.82, stagger=6, enter="slam",
     lines=[{"text": "¿NO VALES", "weight": 900}, {"text": "SUFICIENTE?", "color": "gold"}])
ad.sfx("synth:subdrop_short", {"word": "vale"}, 0.45)
ad.sfx("synth:glitch_02", {"word": "suficiente"}, 0.3)

# INCOMODIDAD / DUDA → BAJAR EL PRECIO
ad.badge("smiley-nervous-bold", {"word": "incomodas,"}, until={"word": "bajar", "offset": -0.12}, label="INCOMODIDAD", side="left", y=0.44)
ad.badge("question-bold", {"word": "dudas"}, until={"word": "bajar", "offset": -0.12}, label="DUDA", side="right", y=0.44)
ad.scene("glow", {"word": "bajar", "offset": -0.1}, {"cut": 3, "offset": -0.02}, word="DESCUENTO")
ad.g("PriceDrop", {"word": "bajar", "offset": -0.05}, until={"cut": 3, "offset": -0.02}, y=0.3, **{"from": 1500}, to=990, label="TU PRECIO", dropAt=20)
ad.sfx("synth:whoosh_fast", {"word": "precio"}, 0.4, -0.05)
ad.sfx("lib:bsb-0307", {"word": "precio"}, 0.3, 0.1)

# RESPIRA ANTES DE RESPONDER → anillo de respiración (MG b-roll)
ad.scene("glow", {"word": "respira", "offset": -0.12}, {"cut": 4, "offset": -0.02})
ad.g("BreatheRing", {"word": "respira", "offset": -0.08}, until={"cut": 4, "offset": -0.02}, y=0.3, size=1.0, label1="RESPIRA", label2="Y RESPONDE")
ad.sfx("synth:riser_short", {"word": "respira"}, 0.18, 0.1)

# ESA PERSONA REACCIONA A UNA PROPUESTA (no a ti)
ad.badge("user-bold", {"word": "persona"}, until={"cut": 5, "offset": -0.03}, label="ESA PERSONA", side="left", y=0.44)
ad.badge("file-text-bold", {"word": "propuesta."}, until={"cut": 5, "offset": -0.03}, label="TU PROPUESTA", side="right", y=0.44)
ad.g("BlockTitle", {"word": "reaccionando", "offset": -0.05}, until={"cut": 5, "offset": -0.03}, y=0.82, width=0.8, stagger=8, enter="rise", sparkle=1,
     lines=[{"text": "NO ES", "weight": 900}, {"text": "PERSONAL", "color": "gold"}])
ad.sfx("lib:glass_002", {"word": "propuesta."}, 0.35)

# PRESUPUESTO · CLARIDAD · CONFIANZA → 3 íconos en escena
ad.scene("pattern", {"word": "falta", "offset": -0.1}, {"cut": 6, "offset": -0.02}, word="ENTIENDE")
for x, ic, lab, w in [(0.22, "wallet-bold", "PRESUPUESTO", "presupuesto,"), (0.5, "lightbulb-bold", "CLARIDAD", "claridad"),
                      (0.78, "handshake-bold", "CONFIANZA", "confianza.")]:
    ad.g("IconBadge", {"word": w, "offset": -0.05}, until={"cut": 6, "offset": -0.02}, icon=ad.icon(ic), x=x, y=0.3, leader="none", size=1.0, label=lab)
    ad.sfx("synth:pop_01", {"word": w, "offset": -0.05}, 0.45)
ad.sfx("lib:confirmation_001", {"word": "confianza."}, 0.35, 0.1)

# PREGÚNTALE CON CALMA
ad.g("QuestionCard", {"cut": 6, "offset": 0.05}, until={"cut": 7, "offset": -0.03}, y=0.82, kicker="PREGÚNTALE CON CALMA",
     question="¿Qué es lo que más te preocupa?")
ad.sfx("lib:question_001", {"cut": 6, "offset": 0.05}, 0.4)

# RECUERDA LO QUE VAS A ENTREGAR
ad.g("Checklist", {"word": "tiempo,", "offset": -0.25}, until={"cut": 8, "offset": -0.03}, title="LO QUE ENTREGAS",
     items=["TU TIEMPO", "TU PREPARACIÓN", "TU TRABAJO"], every=30, position=0.84, icon="✓")
for w in ["tiempo,", "preparación", "trabajo"]:
    ad.sfx("synth:pop_01", {"word": w}, 0.4)
ad.badge("clock-bold", {"word": "tiempo,"}, until={"cut": 8, "offset": -0.03}, side="right", y=0.44)

# ANTES DEL DESCUENTO → ¿QUÉ ESTÁ COMPARANDO?
ad.badge("percent-bold", {"word": "descuento,"}, until={"word": "aclara", "offset": -0.1}, label="DESCUENTO", side="right", y=0.44)
ad.sfx("lib:switch7", {"word": "descuento,"}, 0.3)
ad.scene("glow", {"word": "aclara", "offset": -0.1}, {"cut": 9, "offset": -0.02}, word="COMPARA")
ad.g("CounterRace", {"word": "aclara", "offset": -0.05}, until={"cut": 9, "offset": -0.02}, y=0.3,
     a={"label": "TU PROPUESTA", "from": 1500, "to": 1500, "prefix": "$"}, b={"label": "LO QUE COMPARA", "from": 0, "to": 900, "prefix": "$"})
ad.sfx("lib:maximize_006", {"word": "aclara"}, 0.35)
for k in range(10):
    ad.sfx("lib:bsb-2842", {"word": "aclara"}, 0.14, 0.1 + k * 0.1)

# DECISIÓN DE NEGOCIO (3D) — NO POR MIEDO
ad.scene("tunnel", {"word": "decisión", "offset": -0.1}, {"word": "negocio,", "offset": 0.62})
ad.g("Text3DTitle", {"word": "decisión", "offset": -0.05}, until={"word": "negocio,", "offset": 0.62}, text="DECISIÓN\nDE NEGOCIO",
     font="Montserrat-Black", color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.sfx("synth:riser_short", {"word": "decisión"}, 0.28, -1.1)
ad.sfx("synth:impact_cinematic", {"word": "decisión"}, 0.5, -0.05)
ad.sfx("synth:subdrop_short", {"word": "decisión"}, 0.4, -0.05)
ad.g("BlockTitle", {"word": "miedo", "offset": -0.3}, until={"cut": 10, "offset": -0.03}, y=0.82, width=0.8, stagger=6, enter="slam",
     lines=[{"text": "NO POR", "weight": 900}, {"text": "MIEDO", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "miedo"}, 0.45)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-2d385c92-05f.mp3", drop=0)
ad.save(emphasis=["caro”…", "vale", "suficiente", "precio", "respira", "propuesta.", "presupuesto,", "claridad", "confianza.",
                  "preocupa.", "tiempo,", "preparación", "trabajo", "descuento,", "comparando.", "decisión", "negocio,", "miedo",
                  "sígueme", "escalar"],
        hide=[[32.45, 33.75]])
