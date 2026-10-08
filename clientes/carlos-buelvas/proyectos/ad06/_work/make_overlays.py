# AD06 — Contrataste para tener menos trabajo
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["contrataste", "tuyo", "persona.", "frustrante,", "respirar.", "equipo", "liderar.", "yo”,",
                           "proceso?", "decidir?”.", "tarea", "límite:", "tiempo.", "sígueme"])

# HOOK: el contrato “para tener menos trabajo” se firma… y la pila de tareas crece
ad.hook_hit()
ad.g("BrandScene", 0, until={"word": "ahora", "offset": -0.1}, layer="under", variant="glow", word="CONTRATO")
ad.g("ContractDoc", 0.05, until={"word": "ahora", "offset": -0.1}, y=0.3, title="NUEVA CONTRATACIÓN",
     items=["Puesto: ASISTENTE", "Objetivo: MENOS TRABAJO 😌"], every=14, sign=True)
ad.sfx("lib:pluck_001", 0.3, 0.35)
ad.sfx("lib:pluck_002", 0.75, 0.35)
ad.sfx("lib:bsb-2842", 1.4, 0.3)
ad.sfx("synth:whoosh_medium", {"word": "ahora", "offset": -0.1}, 0.45, -0.1)
ad.g("TaskPile", {"word": "ahora"}, until={"cut": 1, "offset": -0.03}, y=0.82, every=9, title="TU DÍA AHORA",
     items=["LO TUYO", "REVISAR LO SUYO", "CORREGIR", "REHACER", "VOLVER A REVISAR"])
for k in range(5):
    ad.sfx("synth:pop_02", {"word": "ahora"}, 0.3, 0.1 + k * 0.3)
ad.sfx("synth:impact_punch", {"word": "persona."}, 0.45)

# FRUSTRANTE… IBAS A RESPIRAR → batería que se vacía
ad.badge("smiley-angry-bold", {"cut": 1, "offset": 0.05}, until={"cut": 3, "offset": -0.03}, label="FRUSTRANTE", side="left", y=0.44)
ad.g("BatteryDrain", {"cut": 1, "offset": 0.1}, until={"cut": 3, "offset": -0.03}, x=0.83, y=0.42, size=0.6, label="TU ENERGÍA", **{"from": 70}, to=6)
ad.sfx("synth:glitch_02", {"word": "frustrante,"}, 0.25)
ad.sfx("lib:bsb-0307", {"word": "respirar."}, 0.3)

# QUEREMOS CRECER CON EQUIPO → curva de crecimiento (MG b-roll)
ad.scene("glow", {"word": "crecer", "n": 1, "offset": -0.1}, {"cut": 4, "offset": -0.02}, word="CRECER")
ad.g("GrowthLine", {"word": "crecer", "n": 1, "offset": -0.05}, until={"cut": 4, "offset": -0.02}, y=0.33, h=0.3)
ad.g("IconBadge", {"word": "equipo"}, until={"cut": 4, "offset": -0.02}, icon=ad.icon("users-three-bold"), x=0.5, y=0.12, leader="none", size=0.9, label="EQUIPO")
ad.sfx("synth:riser_short", {"word": "crecer", "n": 1}, 0.25, 0.1)
ad.sfx("synth:pop_01", {"word": "equipo"}, 0.45)
ad.sfx("lib:glass_002", {"word": "todo."}, 0.3)

# CRECER EXIGE APRENDER A LIDERAR
ad.badge("crown-simple-bold", {"word": "liderar.", "offset": -0.3}, until={"cut": 5, "offset": -0.03}, label="LIDERAR", side="right", y=0.44)
ad.g("BlockTitle", {"word": "aprender", "offset": -0.1}, until={"cut": 5, "offset": -0.03}, y=0.81, width=0.66, stagger=6, enter="slam",
     lines=[{"text": "APRENDER", "weight": 900}, {"text": "A LIDERAR", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "liderar."}, 0.45)

# “NADIE HACE LAS COSAS COMO YO” → PREGÚNTATE (3 preguntas)
ad.g("QuestionCard", {"word": "“nadie", "offset": -0.1}, until={"word": "“¿Expliqué", "offset": -0.3}, y=0.82, kicker="ANTES DE DECIR",
     question="“Nadie hace las cosas como yo”")
ad.sfx("lib:switch7", {"word": "“nadie"}, 0.3, -0.1)
ad.g("Checklist", {"word": "“¿Expliqué", "offset": -0.25}, until={"cut": 8, "offset": -0.03}, title="PREGÚNTATE",
     items=["¿EXPLIQUÉ LO QUE ESPERABA?", "¿LE DI UN PROCESO?", "¿LE ENSEÑÉ CÓMO DECIDIR?"], every=57, position=0.84, icon="?")
for w in ["“¿Expliqué", "di", "enseñé"]:
    ad.sfx("lib:question_001", {"word": w}, 0.32)
ad.badge("chalkboard-teacher-bold", {"word": "enseñé"}, until={"cut": 8, "offset": -0.03}, side="right", y=0.42)

# ELIGE UNA TAREA Y DEFINE CÓMO SE ENTREGA BIEN → libreta (MG b-roll)
ad.scene("glow", {"cut": 8, "offset": 0.0}, {"cut": 9, "offset": -0.02}, word="PROCESO")
ad.g("NotepadList", {"cut": 8, "offset": 0.05}, until={"cut": 9, "offset": -0.02}, y=0.3, title="1 TAREA = 1 PROCESO",
     items=["Qué se entrega", "Cómo se entrega bien", "Cuándo está lista"], delays=[10, 40, 70])
for k, d in enumerate([10, 40, 70]):
    ad.sfx("lib:pluck_00" + str(1 + k % 2), {"cut": 8}, 0.3, d / 30)

# TODO PASA POR TI → EL LÍMITE: TU TIEMPO (3D)
ad.g("FocusBrackets", {"word": "pasando"}, until={"word": "creció,", "offset": 0.3}, x=0.5, y=0.2, w=0.5, h=0.24, label="TODO PASA POR TI")
ad.sfx("lib:maximize_006", {"word": "pasando"}, 0.35)
ad.badge("users-three-bold", {"word": "equipo", "n": 2}, until={"word": "límite:", "offset": -0.1}, label="EQUIPO MÁS GRANDE", side="left", y=0.44)
ad.badge("lock-simple-bold", {"word": "mismo"}, until={"word": "límite:", "offset": -0.1}, label="MISMO LÍMITE", side="right", y=0.44)
ad.scene("tunnel", {"word": "límite:", "offset": -0.05}, {"cut": 11, "offset": -0.02})
ad.g("Text3DTitle", {"word": "límite:"}, until={"cut": 11, "offset": -0.02}, text="TU TIEMPO", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.5, depth=0.35)
ad.sfx("synth:riser_short", {"word": "límite:"}, 0.28, -1.0)
ad.sfx("synth:impact_cinematic", {"word": "límite:"}, 0.5, -0.05)
ad.sfx("lib:bsb-1111", {"word": "tiempo."}, 0.25)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-cafeace9-eb9.mp3", drop=1)
ad.save(emphasis=["contrataste", "menos", "trabajo…", "tuyo", "revisar", "frustrante,", "respirar.", "crecer", "equipo", "liderar.",
                  "nadie", "yo”,", "esperaba?", "proceso?", "decidir?”.", "tarea", "bien.", "decisión", "límite:", "tiempo.",
                  "sígueme", "escalar"],
        hide=[[38.18, 39.59]])
