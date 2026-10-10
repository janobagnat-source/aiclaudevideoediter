# AD04 v2 — “Cuando ‘está caro’ se siente personal”. De la emoción a la decisión de negocio.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad04/_work/blender/"
ad.set_cams({0: "cam1", 5: "cam1", 7: "cam1", 6: "cam2", 8: "cam2"})
ad.auto_zooms(punch_words=["caro”…", "vale", "precio", "respira", "propuesta.", "confianza.", "preocupa.", "entregar.", "descuento,", "decisión", "miedo", "sígueme"])

# ── HOOK: split; llega la respuesta del cliente y aparece tu voz interna ────────────────────────
ad.g("Flash", 0, 0.25, layer="top", peak=0.8, color="#dbe7ff")
ad.sfx("synth:impact_cinematic", 0, 0.5); ad.sfx("synth:subdrop_01", 0, 0.4)
ad.split(0, {"cut": 1}, bottom=0.5, caption=0.535)
ad.g("ObjectionCard", 0.05, until={"cut": 1, "offset": -0.05}, y=0.585, hotAt=56, innerAt=110,
     msg="Gracias por la propuesta. La verdad… está caro.", hot="está caro", inner="¿Y si el problema soy yo?")
ad.sfx("lib:bsb-1111", 0.7, 0.3); ad.sfx("synth:glitch_02", {"word": "caro”…"}, 0.3); ad.sfx("synth:heartbeat_01", {"word": "sentir"}, 0.4)

# ── “…EL QUE NO VALE SUFICIENTE ERES TÚ” → la seguridad se drena ─────────────────────────────
ad.g("ValueDrain", {"cut": 1}, until={"word": "bajar", "offset": -0.12}, label="TU SEGURIDAD", **{"from": 100}, to=24, y=0.82)
ad.sfx("synth:riser_short", {"cut": 1}, 0.2)

# ── QUIERES BAJAR EL PRECIO → Blender: la etiqueta que se balancea + precio tachado ────────────
ad.broll(BL + "ad04_tag/tag.mp4", {"word": "bajar", "offset": -0.1}, {"cut": 3}, speed=0.67, transition="zoom-in")
ad.cap_pos.append({"at": {"word": "bajar", "offset": -0.1}, "until": {"cut": 3}, "pos": 0.9})
ad.g("PriceSlash", {"word": "precio", "offset": -0.1}, until={"cut": 3, "offset": -0.03}, **{"from": "$1.500"}, to="$990?", y=0.79, slashAt=10)
ad.sfx("synth:whoosh_medium", {"word": "bajar", "offset": -0.1}, 0.45, -0.1); ad.sfx("synth:impact_punch", {"word": "precio", "offset": 0.25}, 0.4)

# ── RESPIRA ANTES DE RESPONDER → guía de respiración ───────────────────────────────────────────
ad.g("BreathLine", {"word": "respira", "offset": -0.2}, until={"cut": 4, "offset": -0.03}, y=0.8, period=2.4)
ad.sfx("synth:reverse_swell_long", {"word": "respira"}, 0.25, -0.3)

# ── ESA PERSONA REACCIONA A UNA PROPUESTA → “PROPUESTA” detrás de Carlos ───────────────────────
ad.cut_set(4, cutout="_work/cutouts/cut4.webm",
           behind=[{"component": "BehindTitle", "start": 0.85, "duration": 1.75,
                    "props": {"kicker": "REACCIONA A UNA", "kickerY": 0.035, "lines": [{"text": "PROPUESTA", "gradient": True, "color": "#FFFFFF", "size": 300}], "y": 0.29, "drift": 0.05}}])
ad.sfx("synth:impact_soft", {"word": "propuesta."}, 0.45)

# ── PRESUPUESTO · CLARIDAD · CONFIANZA → split con diagnóstico ────────────────────────────────
ad.split({"cut": 5}, {"cut": 6}, bottom=0.5, caption=0.535)
ad.g("Diagnosis", {"cut": 5, "offset": 0.05}, until={"cut": 6, "offset": -0.05}, y=0.62, title="¿QUÉ LE FALTA?",
     items=[{"text": "PRESUPUESTO", "at": 54}, {"text": "CLARIDAD", "at": 73}, {"text": "CONFIANZA", "at": 94}])
for at in (54, 73, 94):
    ad.sfx("synth:click_ui", {"cut": 5, "offset": 0.05 + at / 30}, 0.35)

# ── PREGÚNTALE CON CALMA → tu mensaje ─────────────────────────────────────────────────────────
ad.g("AskBubble", {"cut": 6, "offset": 0.1}, until={"cut": 7, "offset": -0.05}, text="¿Qué es lo que más te preocupa?", y=0.77)
ad.sfx("lib:pluck_002", {"cut": 6, "offset": 0.2}, 0.35)

# ── TIEMPO, PREPARACIÓN, TRABAJO → split con la pila de valor que sostiene el precio ──────────
ad.split({"cut": 7}, {"cut": 8}, bottom=0.5, caption=0.535)
ad.g("ValueStack", {"cut": 7}, until={"cut": 8, "offset": -0.05}, y=0.56, priceAt=118,
     items=[{"text": "TIEMPO", "at": 32}, {"text": "PREPARACIÓN", "at": 56}, {"text": "TRABAJO", "at": 92}])
for at in (32, 56, 92):
    ad.sfx("synth:impact_soft", {"cut": 7, "offset": at / 30 + 0.2}, 0.3)
ad.sfx("synth:ding_success", {"cut": 7, "offset": 118 / 30}, 0.3)

# ── ANTES DEL DESCUENTO, ACLARA QUÉ ESTÁ COMPARANDO → tabla ───────────────────────────────────
ad.g("CompareTable", {"word": "aclara", "offset": -0.2}, until={"cut": 9, "offset": -0.05}, y=0.71,
     rows=[{"label": "Alcance completo", "a": True, "b": False}, {"label": "Acompañamiento", "a": True, "b": False}, {"label": "Garantía", "a": True, "b": False}])
ad.sfx("lib:card-slide-6", {"word": "aclara", "offset": -0.2}, 0.35)

# ── DECISIÓN DE NEGOCIO → Blender: el rey dorado mueve; luego “miedo” tachado ──────────────────
ad.broll(BL + "ad04_chess/chess.mp4", {"word": "decisión", "offset": -0.12}, {"word": "miedo", "offset": -0.15}, speed=0.95, transition="whip-up")
ad.g("KickerTitle", {"word": "decisión", "offset": -0.08}, until={"word": "miedo", "offset": -0.17}, kicker="UNA DECISIÓN", align="center", y=0.1,
     lines=[{"text": "DE NEGOCIO", "color": "#FFBB00", "size": 120}])
ad.sfx("synth:whoosh_heavy", {"word": "decisión", "offset": -0.12}, 0.45, -0.1); ad.sfx("synth:impact_cinematic", {"word": "negocio,"}, 0.45)
ad.g("TagRow", {"word": "miedo", "offset": -0.1}, until={"cut": 10, "offset": -0.05}, y=0.8, tags=[{"text": "MIEDO A PERDERLO", "at": 2}], strikeAt=30)
ad.sfx("synth:swipe_02", {"word": "miedo", "offset": 0.9}, 0.35)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-2d385c92-05f.mp3", drop=0)
ad.save(emphasis=["caro”…", "vale", "suficiente", "precio", "respira", "propuesta.", "presupuesto,", "claridad", "confianza.", "preocupa.",
                  "tiempo,", "preparación", "trabajo", "descuento,", "comparando.", "decisión", "negocio,", "miedo", "sígueme", "escalar"])
