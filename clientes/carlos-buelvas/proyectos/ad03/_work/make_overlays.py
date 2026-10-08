# AD03 — Muchos seguidores, pocas ventas
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["duele", "ventas", "ellos", "seguidores;", "negocio.", "comunidad", "vender.", "compararte,",
                           "confiar", "duda", "contratarte.", "conversación", "aplauso.", "sígueme"])

# HOOK: carrera de contadores — los seguidores de ELLOS se disparan, TUS VENTAS clavadas en 0
ad.hook_hit()
ad.g("CounterRace", 0.05, until={"word": "publicas,", "offset": -0.05}, y=0.82,
     a={"label": "SEGUIDORES DE ELLOS", "from": 1200, "to": 248000}, b={"label": "TUS VENTAS", "from": 0, "to": 0, "prefix": "$"})
for k in range(16):
    ad.sfx("lib:bsb-2842", 0.15 + k * 0.12, 0.16)
ad.sfx("synth:riser_short", {"word": "publicas,"}, 0.25, -1.0)
ad.badge("upload-simple-bold", {"word": "publicas,"}, until={"word": "ventas"}, label="PUBLICAS", side="left", y=0.44)
ad.badge("barbell-bold", {"word": "esfuerzas"}, until={"word": "ventas"}, label="TE ESFUERZAS", side="right", y=0.44)
ad.g("BlockTitle", {"word": "ventas"}, until={"cut": 1, "offset": -0.03}, y=0.82, width=0.8, stagger=6, enter="slam",
     lines=[{"text": "LAS VENTAS", "weight": 900}, {"text": "NO LLEGAN", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "ventas"}, 0.55)
ad.sfx("synth:glitch_02", {"word": "llegan."}, 0.3)

# ¿QUÉ TIENEN ELLOS QUE YO NO TENGO?
ad.g("QuestionCard", {"cut": 1, "offset": 0.05}, until={"cut": 2, "offset": -0.03}, y=0.82, kicker="Y TE PREGUNTAS",
     question="¿Qué tienen ellos que yo no tengo?")
ad.sfx("lib:question_001", {"cut": 1, "offset": 0.05}, 0.4)
ad.sfx("synth:whoosh_fast", {"cut": 1}, 0.4, -0.1)

# DESDE AFUERA SOLO VES SEGUIDORES → MG b-roll: lluvia de corazones (vanidad)
ad.scene("pattern", {"word": "ves"}, {"word": "sabes", "offset": -0.32}, word="SEGUIDORES")
ad.g("EmojiBurst", {"word": "ves"}, until={"word": "sabes", "offset": -0.32}, emoji="❤️", count=18, x=0.5, y=0.3, spread=1.2)
for k in range(6):
    ad.sfx("synth:pop_02", {"word": "ves"}, 0.22, 0.1 + k * 0.13)
# ... pero no sabes qué pasa DENTRO del negocio
ad.badge("eye-slash-bold", {"word": "sabes"}, until={"cut": 3, "offset": -0.03}, label="LO QUE NO VES", side="right", y=0.44)
ad.badge("storefront-bold", {"word": "negocio."}, until={"cut": 3, "offset": -0.03}, label="SU NEGOCIO", side="left", y=0.44)

# COMUNIDAD GRANDE Y SIN VENDER → embudo con fugas
ad.scene("glow", {"word": "comunidad", "offset": -0.1}, {"cut": 5, "offset": -0.02})
ad.g("LeakyFunnel", {"word": "comunidad", "offset": -0.05}, until={"cut": 5, "offset": -0.02}, y=0.3,
     top="COMUNIDAD GRANDE", bottom="VENTAS: 0", leaks=["SIN CLARIDAD", "SIN CONFIANZA"])
ad.sfx("lib:bsb-1111", {"word": "comunidad"}, 0.22, 0.2)
ad.sfx("synth:subdrop_short", {"word": "vender."}, 0.45)
ad.sfx("lib:glass_002", {"word": "vender."}, 0.3, 0.15)

# ANTES DE COMPARARTE, REVISA ALGO
ad.g("BlockTitle", {"cut": 5, "offset": 0.05}, until={"word": "ayuda", "offset": -0.25}, y=0.82, width=0.8, stagger=8, enter="rise", sparkle=1,
     lines=[{"text": "ANTES DE", "weight": 900}, {"text": "COMPARARTE", "color": "gold"}])
ad.badge("magnifying-glass-bold", {"word": "revisa"}, until={"word": "ayuda", "offset": -0.25}, label="REVISA", side="right", y=0.44)
ad.sfx("lib:maximize_006", {"word": "revisa"}, 0.35)
ad.g("Checklist", {"word": "ayuda", "offset": -0.2}, until={"cut": 7, "offset": -0.03}, title="¿TU CONTENIDO AYUDA A ENTENDER…",
     items=["QUÉ HACES", "POR QUÉ CONFIAR EN TI"], every=64, position=0.84, icon="✓")
ad.sfx("synth:pop_01", {"word": "ayuda", "offset": -0.2}, 0.4, 0.2)
ad.sfx("lib:confirmation_001", {"word": "confiar"}, 0.35)

# PRÓXIMO VIDEO: RESPONDE UNA DUDA → post que responde la duda
ad.badge("video-camera-bold", {"word": "video,"}, until={"word": "responde", "offset": -0.05}, label="PRÓXIMO VIDEO", side="right", y=0.44)
ad.scene("glow", {"word": "responde", "offset": -0.1}, {"cut": 8, "offset": -0.02})
ad.g("PostCard", {"word": "responde", "offset": -0.05}, until={"cut": 8, "offset": -0.02}, y=0.3, avatar=M + "ig_perfil.jpg", cps=34,
     text="❓ «¿Cuánto tarda en verse el resultado?» Te lo explico antes de que me contrates 👇", stamp="DUDA RESUELTA", stampAt=88)
for k in range(14):
    ad.sfx("lib:bsb-2842", {"word": "responde"}, 0.15, 0.1 + k * 0.1)
ad.sfx("synth:impact_soft", {"word": "contratarte."}, 0.5)

# CONVERSACIÓN COMERCIAL > APLAUSO
ad.scene("glow", {"word": "abrir", "offset": -0.1}, {"word": "mucho", "offset": -0.05})
ad.g("ChatThread", {"word": "abrir", "offset": -0.05}, until={"word": "mucho", "offset": -0.05}, y=0.29, title="Nuevo cliente",
     messages=[{"text": "Vi tu video y me quedó clarísimo 🙌", "at": 2}, {"text": "¿Cómo puedo trabajar contigo?", "at": 26}])
ad.sfx("lib:pluck_002", {"word": "abrir"}, 0.35, 0.1)
ad.sfx("lib:pluck_001", {"word": "conversación"}, 0.35, 0.3)
ad.scene("tunnel", {"word": "mucho", "offset": -0.05}, {"cut": 9, "offset": -0.02})
ad.g("Text3DTitle", {"word": "mucho"}, until={"cut": 9, "offset": -0.02}, text="MÁS QUE\nUN APLAUSO", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.sfx("synth:riser_short", {"word": "mucho"}, 0.28, -1.0)
ad.sfx("synth:impact_cinematic", {"word": "mucho"}, 0.5, -0.05)
ad.g("EmojiBurst", {"word": "aplauso.", "offset": -0.1}, until={"cut": 9, "offset": -0.02}, emoji="👏", count=12, x=0.5, y=0.62, spread=1.4)
ad.sfx("lib:bsb-0307", {"word": "aplauso."}, 0.3)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-1aab6084-889.mp3", drop=1)
ad.save(emphasis=["duele", "crecen", "publicas,", "ventas", "ellos", "seguidores;", "negocio.", "comunidad", "vender.", "compararte,",
                  "confiar", "duda", "contratarte.", "conversación", "comercial", "aplauso.", "sígueme", "escalar"],
        hide=[[32.15, 34.46]])
