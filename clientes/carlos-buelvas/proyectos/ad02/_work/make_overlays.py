# AD02 — Que tu contenido se sienta como tú
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["publicas", "soy", "diferentes.", "persona", "importa", "real", "palabras.", "confiar", "sígueme"])

# HOOK: posteo "perfecto" que se escribe solo → sello ESE NO SOY YO
ad.hook_hit()
ad.g("PostCard", 0.05, until={"cut": 1, "offset": -0.05}, y=0.80, avatar=M + "ig_perfil.jpg",
     text="✨ 5 claves infalibles para potenciar tu negocio y alcanzar el éxito 🚀💯 #emprendimiento", cps=30,
     stamp="ESE NO SOY YO", stampAt=150)
for k in range(22):
    ad.sfx("lib:bsb-2842", 0.2 + k * 0.11, 0.18)
ad.sfx("synth:impact_punch", {"cut": 1, "offset": -1.03}, 0.7)
ad.sfx("synth:glitch_02", {"cut": 1, "offset": -1.0}, 0.35)
ad.badge("pencil-simple-line-bold", {"word": "piensas:"}, until={"word": "pero"}, label="BIEN ESCRITO")

# IA / PLANTILLAS / FÓRMULAS → grilla de clones, uno se enciende (lo que nos hace diferentes)
ad.scene("pattern", {"cut": 1, "offset": 0.02}, {"cut": 2, "offset": -0.02}, word="COPIA")
ad.g("CloneGrid", {"cut": 1, "offset": 0.05}, until={"cut": 2, "offset": -0.02}, y=0.27, rows=3, w=0.72, avatar=M + "ig_perfil.jpg",
     highlightAt=170, label="TÚ", tags=["IA", "PLANTILLA", "FÓRMULA"])
for k in range(12):
    ad.sfx("lib:switch7", {"cut": 1}, 0.18, 0.1 + k * 0.05)
ad.sfx("synth:riser_short", {"word": "escondiendo"}, 0.3, -0.6)
ad.sfx("synth:impact_soft", {"word": "diferentes."}, 0.55)
ad.sfx("lib:glass_002", {"word": "diferentes."}, 0.4, 0.15)

# LA GENTE QUIERE RECONOCER A LA PERSONA → corchetes de enfoque sobre Carlos (sin tapar)
ad.g("FocusBrackets", {"word": "reconocer"}, until={"word": "cómo", "n": 1, "offset": -0.1}, x=0.5, y=0.135, w=0.46, h=0.19, label="LA PERSONA")
ad.sfx("lib:maximize_006", {"word": "reconocer"}, 0.4)
ad.sfx("lib:bsb-0307", {"word": "persona"}, 0.35)
ad.g("Checklist", {"word": "cómo", "n": 1, "offset": -0.15}, until={"cut": 3, "offset": -0.03}, title="", items=["CÓMO PIENSAS", "QUÉ TE IMPORTA", "CÓMO ENTIENDES SUS PROBLEMAS"], every=29, position=0.83, icon="✓")
for k, w in enumerate(["cómo", "qué", "entiendes"]):
    ad.sfx("synth:pop_01", {"word": w, "n": 1 if w != "cómo" else 1}, 0.4, 0.05 if k else 0.15)

# CONVERSACIÓN REAL CON UN CLIENTE → chat
ad.scene("glow", {"word": "recuerda", "offset": -0.1}, {"cut": 4, "offset": -0.02})
ad.g("ChatThread", {"word": "recuerda", "offset": -0.05}, until={"cut": 4, "offset": -0.02}, y=0.29, title="Cliente",
     messages=[{"text": "Carlos, trabajo un montón y no me queda nada 😩", "at": 4}, {"text": "Te entiendo. ¿Qué es lo que más te preocupa?", "me": True, "at": 40}, {"text": "Que no sé cuánto cobrar 🤔", "at": 72}])
ad.sfx("lib:bsb-1111", {"word": "recuerda"}, 0.25, 0.1)
ad.sfx("lib:pluck_002", {"word": "conversación"}, 0.35, 0.25)
ad.sfx("lib:pluck_001", {"word": "cliente."}, 0.35)
# las 3 preguntas
ad.badge("question-bold", {"cut": 4}, until={"cut": 5}, label="PREOCUPACIÓN", side="right")
ad.badge("chat-circle-text-bold", {"cut": 5}, until={"cut": 6}, label="EXPLICACIÓN", side="left")
ad.badge("hand-heart-bold", {"cut": 6}, until={"cut": 7}, label="AYUDA", side="right")
for c in (4, 5, 6):
    ad.sfx("lib:question_001" if c == 4 else "lib:confirmation_001", {"cut": c}, 0.35)

# CUENTA ESO CON TUS PALABRAS
ad.g("BlockTitle", {"cut": 7}, until={"cut": 8, "offset": -0.03}, y=0.80, width=0.84, stagger=10, enter="rise", sparkle=1,
     lines=[{"text": "CUENTA ESO", "weight": 900}, {"text": "CON TUS PALABRAS", "color": "gold"}])
ad.sfx("synth:whoosh_fast", {"cut": 7}, 0.45, -0.1)
ad.sfx("lib:glass_002", {"word": "palabras."}, 0.35)
ad.badge("microphone-stage-bold", {"cut": 7, "offset": 0.1}, until={"cut": 8, "offset": -0.03}, side="right", y=0.42)

# DIFICULTAD REAL → CONFIAR
ad.badge("puzzle-piece-bold", {"word": "resuelves"}, until={"cut": 9, "offset": -0.03}, label="DIFICULTAD REAL")
ad.scene("tunnel", {"word": "razón", "offset": -0.1}, {"cut": 10, "offset": -0.02})
ad.g("Text3DTitle", {"word": "razón", "offset": -0.05}, until={"cut": 10, "offset": -0.02}, text="CONFIAR\nEN TI", font="Montserrat-Black", color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.sfx("synth:riser_short", {"word": "razón"}, 0.28, -1.2)
ad.sfx("synth:impact_cinematic", {"word": "razón"}, 0.55, -0.05)
ad.sfx("synth:subdrop_short", {"word": "razón"}, 0.45, -0.05)
ad.g("ShapeBurst", {"word": "confiar"}, 0.6, x=0.5, y=0.27, radius=1.4)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-5f49e44a-f2b.mp3", drop=4)
ad.save(emphasis=["publicas", "escrito,", "diferentes.", "persona", "piensas,", "importa", "problemas.", "conversación", "real", "cliente.", "palabras.", "dificultad", "confiar", "sígueme", "escalar", "ventas."],
        hide=[[0.0, 0.0], [ad.edl["cuts"][7]["in"] * 0 + 28.66, 30.95]])
