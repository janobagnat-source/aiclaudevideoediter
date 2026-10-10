# AD03 v2 — “Muchos seguidores, pocas ventas”. Lo que se ve desde afuera vs. lo que vende.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad03/_work/blender/"
ad.set_cams({0: "cam1", 6: "cam1", 8: "cam1", 7: "cam2"})          # split → frontal; fuera del split → costado
ad.auto_zooms(punch_words=["duele", "ventas", "ellos", "seguidores;", "negocio.", "comunidad", "vender.", "compararte,", "confiar", "duda", "aplauso.", "sígueme"])

# ── HOOK: split; el feed de otros explota en likes… y tu tarjeta de ventas cae en 0 ─────────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("FeedScroll", 0.05, until={"cut": 1, "offset": -0.05}, y=0.565, h=0.41, youAt=115)
for k in range(10):
    ad.sfx("synth:pop_low", 0.2 + k * 0.3, 0.2)
ad.sfx("synth:glitch_02", {"word": "ventas"}, 0.3)
ad.sfx("synth:impact_punch", {"word": "llegan."}, 0.5)

# ── ¿QUÉ TIENEN ELLOS QUE YO NO TENGO? → comparación en la franja baja ──────────────────────────
ad.g("VersusBar", {"cut": 1, "offset": 0.1}, until={"cut": 2, "offset": -0.05}, y=0.8)
ad.sfx("lib:card-slide-4", {"cut": 1, "offset": 0.1}, 0.35); ad.sfx("lib:question_001", {"word": "tengo?”."}, 0.35)

# ── DESDE AFUERA VES SEGUIDORES → Blender: iceberg ─────────────────────────────────────────────
ad.broll(BL + "ad03_iceberg/iceberg.mp4", {"word": "desde", "offset": -0.08}, {"cut": 3}, speed=0.4, transition="whip-up")
ad.cap_pos.append({"at": {"word": "desde", "offset": -0.08}, "until": {"cut": 3}, "pos": 0.88})
ad.g("KickerTitle", {"word": "ves"}, until={"cut": 3, "offset": -0.03}, kicker="LO QUE VES", y=0.15, x=0.08, lines=[{"text": "SEGUIDORES", "size": 74}])
ad.g("KickerTitle", {"word": "sabes", "offset": -0.1}, until={"cut": 3, "offset": -0.03}, kicker="LO QUE NO VES", y=0.6, x=0.08, lines=[{"text": "SU NEGOCIO", "color": "#FFBB00", "size": 74}])
ad.sfx("synth:whoosh_heavy", {"word": "desde", "offset": -0.08}, 0.45, -0.1)
ad.sfx("synth:reverse_swell", {"word": "sabes"}, 0.3, -0.5)
ad.sfx("synth:subdrop_short", {"word": "negocio."}, 0.4)

# ── COMUNIDAD GRANDE Y SIN VENDER → Blender: embudo lleno, salen dos monedas ────────────────────
ad.broll(BL + "ad03_funnel/funnel.mp4", {"cut": 4}, {"cut": 5}, speed=0.58, transition="zoom-in")
ad.cap_pos.append({"at": {"cut": 4}, "until": {"cut": 5}, "pos": 0.88})
ad.g("KickerTitle", {"cut": 4, "offset": 0.05}, until={"cut": 5, "offset": -0.03}, kicker="UNA COMUNIDAD GRANDE", align="center", y=0.09,
     lines=[{"text": "SIN VENDER", "color": "#FFBB00", "size": 110}])
for k in range(6):
    ad.sfx("synth:pop_02", {"cut": 4, "offset": 0.2 + k * 0.18}, 0.2)
ad.sfx("lib:bsb-0339", {"cut": 4, "offset": 0.35 * 54 / 30 / 0.58}, 0.4); ad.sfx("lib:bsb-0339", {"cut": 4, "offset": 0.62 * 54 / 30 / 0.58}, 0.4)

# ── REVISA ALGO: ¿tu contenido explica qué haces y por qué confiar? → split con auditoría ───────
ad.split({"word": "revisa", "offset": -0.1}, {"cut": 7}, bottom=0.5, caption=0.535)
ad.g("AuditGrid", {"word": "revisa", "offset": -0.05}, until={"cut": 7, "offset": -0.05}, y=0.575, scanAt=34, title="REVISA TU CONTENIDO")
ad.sfx("lib:maximize_006", {"word": "revisa"}, 0.35)
ad.sfx("synth:riser_short", {"word": "revisa", "offset": 34 / 30}, 0.22)
for k in range(6):
    ad.sfx("synth:click_ui", {"word": "revisa", "offset": (34 + 8 + k * 7) / 30}, 0.25)

# ── EN TU PRÓXIMO VIDEO, RESPONDE UNA DUDA → visor REC + la duda del cliente ────────────────────
ad.g("RecFrame", {"cut": 7}, until={"cut": 8, "offset": -0.03}, label="TU PRÓXIMO VIDEO")
ad.sfx("synth:shutter_01", {"cut": 7}, 0.35); ad.sfx("synth:ding_01", {"cut": 7, "offset": 0.1}, 0.2)
ad.g("FAQBubble", {"word": "duda", "offset": -0.1}, until={"cut": 8, "offset": -0.05}, y=0.79, question="¿En cuánto tiempo voy a ver resultados?")
ad.sfx("lib:bsb-1111", {"word": "duda"}, 0.25)

# ── UNA CONVERSACIÓN COMERCIAL > UN APLAUSO → split ────────────────────────────────────────────
ad.split({"cut": 8}, {"cut": 9}, bottom=0.5, caption=0.535)
ad.g("ValueCompare", {"cut": 8}, until={"cut": 9, "offset": -0.05}, y=0.575, dmAt=38, compareAt=101)
ad.sfx("lib:pluck_002", {"cut": 8, "offset": 38 / 30}, 0.4)
ad.sfx("lib:bsb-0307", {"cut": 8, "offset": 101 / 30}, 0.3); ad.sfx("synth:ding_success", {"word": "aplauso."}, 0.3)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-1aab6084-889.mp3", drop=1)
ad.save(emphasis=["duele", "crecen", "publicas,", "ventas", "ellos", "seguidores;", "negocio.", "comunidad", "vender.", "compararte,",
                  "confiar", "duda", "contratarte.", "conversación", "comercial", "aplauso.", "sígueme", "escalar"])
