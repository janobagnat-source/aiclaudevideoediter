# AD10 — La esperanza de que más publicidad lo resuelva
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["preocupado", "ventas", "publicidad,", "cuentas", "rápida.", "acercaron.", "respondiste?", "propuesta?",
                           "resolver?", "diez", "detuvieron.", "ahí.", "gasto", "sígueme"])

# HOOK: el gasto en publicidad se dispara… las ventas siguen en $0
ad.hook_hit()
ad.g("CounterRace", 0.05, until={"cut": 1, "offset": -0.03}, y=0.82,
     a={"label": "GASTO EN PUBLICIDAD", "from": 200, "to": 4800, "prefix": "$"}, b={"label": "VENTAS", "from": 0, "to": 0, "prefix": "$"})
for k in range(16):
    ad.sfx("lib:bsb-2842", 0.15 + k * 0.2, 0.15)
ad.badge("megaphone-bold", {"word": "publicidad,", "offset": -0.3}, until={"cut": 1, "offset": -0.03}, label="MÁS PUBLICIDAD", side="right", y=0.44)
ad.sfx("synth:whoosh_fast", {"word": "publicidad,"}, 0.4, -0.3)
ad.sfx("synth:impact_punch", {"word": "mejorar”."}, 0.45)

# ENTIENDO ESA URGENCIA (3D)
ad.scene("tunnel", {"word": "esa", "offset": -0.06}, {"cut": 2, "offset": -0.02})
ad.g("Text3DTitle", {"word": "esa", "offset": -0.04}, until={"cut": 2, "offset": -0.02}, text="URGENCIA", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.5, depth=0.35)
ad.sfx("synth:impact_cinematic", {"word": "esa"}, 0.5, -0.05)
ad.sfx("synth:subdrop_short", {"word": "esa"}, 0.4, -0.05)

# CUENTAS POR PAGAR → facturas que caen (MG b-roll) → SOLUCIÓN RÁPIDA
ad.scene("glow", {"word": "cuentas", "offset": -0.1}, {"word": "queremos", "offset": -0.05}, word="CUENTAS")
ad.g("CostTags", {"word": "cuentas", "offset": -0.05}, until={"word": "queremos", "offset": -0.05}, y=0.32, tag="-$",
     items=["ALQUILER", "PROVEEDORES", "SUELDOS"], delays=[3, 13, 23])
for k in range(3):
    ad.sfx("lib:switch7", {"word": "cuentas"}, 0.3, 0.1 + k * 0.33)
ad.badge("lightning-bold", {"word": "solución"}, until={"cut": 3, "offset": -0.03}, label="SOLUCIÓN RÁPIDA", side="right", y=0.44)
ad.sfx("synth:whoosh_fast", {"word": "rápida."}, 0.35, -0.1)

# ANTES DE INVERTIR MÁS, MIRA A QUIENES YA SE ACERCARON
ad.badge("hand-palm-bold", {"word": "invertir"}, until={"cut": 4, "offset": -0.03}, label="ANTES DE INVERTIR", side="left", y=0.44)
ad.badge("users-three-bold", {"word": "personas"}, until={"cut": 4, "offset": -0.03}, label="YA SE ACERCARON", side="right", y=0.44)
ad.sfx("lib:maximize_006", {"word": "mira"}, 0.35)

# LAS 3 PREGUNTAS
ad.g("Checklist", {"cut": 4, "offset": -0.2}, until={"cut": 7, "offset": -0.03}, title="PREGÚNTATE",
     items=["¿LES RESPONDISTE?", "¿ENTENDIERON TU PROPUESTA?", "¿QUÉ DUDA QUEDÓ SIN RESOLVER?"], every=43, position=0.84, icon="?")
for c in (4, 5, 6):
    ad.sfx("lib:question_001", {"cut": c}, 0.32, 0.05)

# REVISA TUS ÚLTIMAS 10 CONVERSACIONES → ¿dónde se detuvo? (MG b-roll)
ad.scene("glow", {"word": "últimas", "offset": -0.1}, {"cut": 8, "offset": -0.02}, word="10 CHATS")
ad.g("ChatThread", {"word": "últimas", "offset": -0.05}, until={"cut": 8, "offset": -0.02}, y=0.27, title="Conversación 7 de 10",
     messages=[{"text": "Hola, ¿cuánto cuesta? 👀", "at": 4}, {"text": "Te paso la info 👇", "me": True, "at": 26}, {"text": "¿Y cuándo podríamos empezar?", "at": 52}])
ad.g("IconBadge", {"word": "detuvieron.", "offset": -0.1}, until={"cut": 8, "offset": -0.02}, icon=ad.icon("hand-palm-bold"), x=0.5, y=0.47,
     leader="none", size=0.85, label="AQUÍ SE DETUVO")
ad.sfx("lib:pluck_001", {"word": "últimas"}, 0.35, 0.1)
ad.sfx("lib:pluck_002", {"word": "conversaciones"}, 0.35, 0.3)
ad.sfx("synth:impact_soft", {"word": "detuvieron."}, 0.5)

# SIN RESPONDER / SIN SEGUIMIENTO → EMPIEZA POR AHÍ
ad.badge("chat-circle-dots-bold", {"word": "consultas"}, until={"cut": 9, "offset": -0.03}, label="SIN RESPONDER", side="left", y=0.44)
ad.badge("file-text-bold", {"word": "propuestas"}, until={"cut": 9, "offset": -0.03}, label="SIN SEGUIMIENTO", side="right", y=0.44)
ad.g("BlockTitle", {"word": "empieza", "offset": -0.1}, until={"cut": 9, "offset": -0.03}, y=0.81, width=0.6, stagger=6, enter="slam",
     lines=[{"text": "EMPIEZA", "weight": 900}, {"text": "POR AHÍ", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "empieza"}, 0.45)

# MÁS GENTE AL MISMO PROCESO → embudo con fugas, y el gasto vuelve a subir
ad.scene("glow", {"cut": 9, "offset": 0.0}, {"word": "aumentar", "offset": -0.05}, word="PROCESO")
ad.g("LeakyFunnel", {"cut": 9, "offset": 0.03}, until={"word": "aumentar", "offset": -0.05}, y=0.3,
     top="MÁS PERSONAS", bottom="VENTAS", leaks=["SIN RESPUESTA", "SIN SEGUIMIENTO"])
ad.sfx("lib:bsb-1111", {"cut": 9}, 0.22, 0.2)
ad.g("CounterRace", {"word": "aumentar", "offset": -0.03}, until={"cut": 10, "offset": -0.03}, y=0.82,
     a={"label": "TU GASTO", "from": 4800, "to": 9600, "prefix": "$"}, b={"label": "TUS VENTAS", "from": 0, "to": 0, "prefix": "$"})
ad.sfx("synth:whoosh_medium", {"word": "aumentar"}, 0.4, -0.1)
ad.sfx("synth:glitch_02", {"word": "frenando"}, 0.28)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-35df4743-377.mp3", drop=0)
ad.save(emphasis=["preocupado", "ventas", "publicidad,", "mejorar”.", "urgencia.", "cuentas", "rápida.", "invertir", "acercaron.",
                  "respondiste?", "propuesta?", "duda", "diez", "conversaciones", "detuvieron.", "consultas", "seguimiento,", "ahí.",
                  "gasto", "frenando", "sígueme", "escalar"],
        hide=[[6.9, 8.15]])
