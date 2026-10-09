# AD01 v3 — “Lo importante es lo que te queda”. Dirección: ejecutiva/editorial (Carlos le habla a empresarios).
# Nada sobre la cara: los gráficos viven en escenas 3D de Blender, en el panel del split o en la franja baja,
# y la tipografía grande va DETRÁS de Carlos (recorte). Sin letras 3D, sin íconos, cierre plano.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad01/_work/blender/"
ad.auto_zooms(punch_words=["dinero?", "agenda", "creciendo”.", "pagar", "muchísimo", "poco", "tiempo", "costo.", "ganancia",
                           "bienestar.", "sígueme"])

# ── HOOK ───────────────────────────────────────────────────────────────────────────────────────
# 0.0–1.0  Blender: barras de ventas de oro que se disparan + contador “+38 %”
ad.broll(BL + "bars/bars.mp4", 0, {"word": "al"}, speed=1.45, transition="cut", inn=0.2)
ad.g("KickerTitle", 0, until={"word": "al", "offset": -0.02}, kicker="VENTAS DEL MES", align="center", y=0.16,
     value={"from": 0, "to": 38, "prefix": "+", "suffix": "%", "at": 2, "dur": 22, "size": 210, "color": "#FFBB00"})
ad.sfx("synth:whoosh_heavy", 0, 0.45)
ad.sfx("synth:riser_short", 0, 0.3)
for k in range(5):
    ad.sfx("synth:pop_low", 0.12 + k * 0.13, 0.28)
ad.sfx("lib:bsb-1417", 0.78, 0.35)
# 1.04  corte duro a Carlos: “30” gigante DETRÁS de él (fin de mes), con barrido de luz
ad.g("LightSweep", {"word": "al", "offset": -0.08}, 0.45, layer="top")
ad.sfx("synth:impact_cinematic", {"word": "al"}, 0.55)
ad.sfx("synth:subdrop_01", {"word": "al"}, 0.45)
ad.cut_set(0, cutout="_work/cutouts/cut0.webm",
           behind=[{"component": "BehindTitle", "start": 1.0, "duration": 2.84,
                    "props": {"kicker": "FIN DE MES", "kickerY": 0.035, "lines": [{"text": "30", "gradient": True, "color": "#FFBB00", "size": 900}], "y": 0.3, "drift": 0.06}}],
           zoom=[{"t": 0, "s": 1.0}, {"t": 3.84, "s": 1.05, "ease": "linear"}])
ad.sfx("synth:heartbeat_01", {"word": "preocupado"}, 0.4, -0.1)

# ── AGENDA LLENA: split, Carlos arriba y la semana que se llena sola abajo ─────────────────────
ad.split({"cut": 1}, {"cut": 2}, bottom=0.5, caption=0.535)
ad.g("CalendarWeek", {"cut": 1, "offset": 0.15}, until={"cut": 2, "offset": -0.05}, y=0.575, h=0.385, fill=2.9)
for k in range(18):
    ad.sfx("lib:click_00" + str(1 + k % 5), {"cut": 1, "offset": 0.45 + k * 0.16}, 0.22)
ad.sfx("synth:tick_01", {"word": "día"}, 0.35)
ad.sfx("synth:ding_01", {"word": "día", "offset": 0.15}, 0.3)

# ── “AHORA SÍ, EL NEGOCIO ESTÁ CRECIENDO” → cinta de bolsa en verde… que se pone roja en el “Pero” ─
ad.g("TickerTape", {"word": "“Ahora", "offset": -0.1}, until={"word": "pagar", "offset": -0.12}, y=0.8, flipAt=2.5, speed=6,
     items=["VENTAS +24%", "CLIENTES +18%", "AGENDA 100%", "FACTURACIÓN +31%"],
     itemsAfter=["ALQUILER −$1.200", "SUELDOS −$3.400", "IMPUESTOS −$900", "PROVEEDORES −$2.100"])
ad.sfx("lib:card-slide-5", {"word": "“Ahora", "offset": -0.1}, 0.4)
ad.sfx("synth:ding_success", {"word": "creciendo”."}, 0.3)
ad.sfx("synth:tape_stop", {"word": "Pero"}, 0.45, -0.05)
ad.sfx("synth:glitch_02", {"word": "Pero"}, 0.3)

# ── PAGAR TODO: Blender, la torre de monedas se desarma; libro contable arriba ─────────────────
ad.broll(BL + "coins/coins.mp4", {"word": "pagar", "offset": -0.1}, {"cut": 5}, speed=0.67, transition="zoom-in")
ad.g("Ledger", {"word": "pagar", "offset": -0.05}, until={"cut": 5, "offset": -0.02}, y=0.07, income=12400,
     items=[{"label": "Alquiler", "amount": 1800, "at": 12}, {"label": "Sueldos", "amount": 5200, "at": 26},
            {"label": "Impuestos", "amount": 2300, "at": 40}, {"label": "Proveedores", "amount": 2460, "at": 54}])
ad.sfx("synth:whoosh_medium", {"word": "pagar", "offset": -0.1}, 0.45, -0.1)
for k, at in enumerate([12, 26, 40, 54]):
    ad.sfx("lib:bsb-0339", {"word": "pagar", "offset": -0.05 + at / 30}, 0.38)
    ad.sfx("lib:bsb-1417", {"word": "pagar", "offset": -0.02 + at / 30}, 0.18)
ad.sfx("synth:subdrop_short", {"word": "muchísimo"}, 0.4)

# ── “PARA LO POCO QUE NOS QUEDÓ”: plano frío y el resultado del mes abajo ───────────────────────
ad.cut_set(5, fx={"grade": "moody"})
ad.g("ResultChip", {"cut": 5, "offset": 0.1}, until={"cut": 6, "offset": -0.05}, label="TE QUEDÓ", **{"from": 2400}, to=640, y=0.82, note="de $ 12.400")
ad.sfx("synth:impact_soft", {"word": "poco"}, 0.45)

# ── “TU TIEMPO TAMBIÉN CUENTA”: Blender, reloj de arena de oro ──────────────────────────────────
ad.broll(BL + "hourglass/hourglass.mp4", {"word": "servicio,", "offset": -0.05}, {"cut": 7}, speed=0.76, transition="whip-up")
ad.g("KickerTitle", {"word": "servicio,", "offset": 0.0}, until={"cut": 7, "offset": -0.03}, kicker="SI VENDES UN SERVICIO", y=0.085,
     lines=[{"text": "TU TIEMPO", "size": 104}, {"text": "TAMBIÉN CUENTA", "color": "#FFBB00", "size": 84}])
ad.sfx("synth:whoosh_fast", {"word": "servicio,", "offset": -0.05}, 0.45, -0.08)
for k in range(8):
    ad.sfx("synth:tick_01", {"word": "servicio,", "offset": 0.2 + k * 0.25}, 0.22)

# ── HORAS EXTRA / CAMBIOS / DESCUENTOS: split con un ticket que se imprime ──────────────────────
ad.split({"cut": 7}, {"cut": 10}, bottom=0.5, caption=0.535)
ad.g("Receipt", {"cut": 7, "offset": 0.0}, until={"cut": 10, "offset": -0.05}, y=0.585,
     items=[{"label": "HORAS EXTRA", "value": "+12 h", "at": 8}, {"label": "CAMBIOS REGALADOS", "value": "4", "at": 50},
            {"label": "DESCUENTOS", "value": "−15%", "at": 90}],
     total={"label": "COSTO REAL", "value": "$ 2.180", "at": 120}, stamp="NO COBRADO", stampAt=128)
for at in (8, 50, 90, 120):
    for k in range(6):
        ad.sfx("lib:bsb-2842", {"cut": 7, "offset": at / 30 - 0.15 + k * 0.045}, 0.16)
ad.sfx("synth:impact_punch", {"cut": 7, "offset": 128 / 30}, 0.5)

# ── “ANTES DE ACEPTAR OTRO CLIENTE, PREGÚNTATE” → solicitud entrante, el cursor elige EVALUAR ───
ad.g("DecisionPrompt", {"cut": 10, "offset": 0.1}, until={"cut": 11, "offset": -0.03}, y=0.775, clickAt=52, avatar=M + "ig_perfil.jpg",
     title="Nuevo cliente", body="Quiere empezar el lunes y necesita cambios urgentes. ¿Aceptas el proyecto?", app="SOLICITUD")
ad.sfx("lib:bsb-1111", {"cut": 10, "offset": 0.1}, 0.3)
ad.sfx("lib:bsb-1742", {"cut": 10, "offset": 0.1 + 52 / 30}, 0.55)

# ── LA PREGUNTA: Blender, balanza TIEMPO vs GANANCIA que se equilibra ───────────────────────────
ad.broll(BL + "scale/scale.mp4", {"word": "trabajo", "offset": -0.1}, {"cut": 12}, speed=0.59, transition="zoom-in")
ad.g("KickerTitle", {"word": "trabajo", "offset": -0.05}, until={"cut": 12, "offset": -0.03}, kicker="PREGÚNTATE", y=0.12, align="center",
     lines=[{"text": "¿ME DEJA UNA", "size": 78}, {"text": "GANANCIA QUE LO JUSTIFIQUE?", "color": "#FFBB00", "size": 60}])
ad.cap_pos.append({"at": {"word": "trabajo", "offset": -0.1}, "until": {"cut": 12}, "pos": 0.87})
ad.sfx("synth:whoosh_medium", {"word": "trabajo", "offset": -0.1}, 0.45, -0.1)
for i in range(6):
    ad.sfx("lib:bsb-0339", {"word": "trabajo", "offset": -0.1 + (10 + i * 6) / 30 / 0.59}, 0.28)
ad.sfx("synth:impact_soft", {"word": "justifica"}, 0.45)

# ── “TU ESFUERZO MERECE CONVERTIRSE EN BIENESTAR” → BIENESTAR gigante detrás de Carlos ─────────
ad.cut_set(12, fx={"grade": "warm"})
ad.split({"cut": 12}, {"cut": 13}, bottom=0.5, caption=0.535)
ad.g("KickerTitle", {"cut": 12, "offset": 0.2}, until={"cut": 13, "offset": -0.05}, kicker="TU ESFUERZO MERECE", align="center", y=0.76,
     lines=[{"text": "BIENESTAR", "color": "#FFBB00", "size": 150}], stagger=4)
ad.g("LightSweep", {"cut": 12, "offset": -0.1}, 0.5, layer="top", color="#ffd98a")
ad.sfx("synth:reverse_swell", {"cut": 12}, 0.35, -0.6)
ad.sfx("lib:glass_002", {"word": "bienestar."}, 0.35)

# ── CTA y cierre plano ─────────────────────────────────────────────────────────────────────────
ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-1a767512-5d6.mp3", drop=1, at_cut=13)
ad.save(emphasis=["dinero?", "agenda", "llena,", "creciendo”.", "pagar", "muchísimo", "poco", "tiempo", "extra,", "regalas", "descuentos",
                  "costo.", "ganancia", "justifica", "bienestar.", "sígueme", "escalar", "ventas."],
        hide=[[18.45, 19.95]])
