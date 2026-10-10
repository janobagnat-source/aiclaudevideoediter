# AD05 v2 — “Emigrar no borra tu experiencia”. Viaje, red nueva, evidencia visible.
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
BL = "clientes/carlos-buelvas/proyectos/ad05/_work/blender/"
ad.set_cams({2: "cam1", 4: "cam1", 6: "cam1", 3: "cam2", 5: "cam2"})
ad.auto_zooms(punch_words=["cero.", "experiencia", "aeropuerto.", "tiempo.", "tres", "demostrarlo:", "proceso.", "necesidad", "borra", "evidencia", "sígueme"])

# ── HOOK: Blender, el globo y la ruta de vuelo; corte a Carlos con el contador que vuelve a 00 ──
ad.broll(BL + "ad05_globe2/globe.mp4", 0, {"word": "sentir", "offset": 0.05}, speed=1.0, transition="cut")
ad.cap_pos.append({"at": 0, "until": {"word": "sentir", "offset": 0.05}, "pos": 0.84})
ad.sfx("synth:whoosh_heavy", 0, 0.45); ad.sfx("lib:bsb-1111", 0.4, 0.15); ad.sfx("synth:riser_short", 0, 0.25)
ad.g("LightSweep", {"word": "sentir", "offset": -0.02}, 0.45, layer="top")
ad.sfx("synth:impact_cinematic", {"word": "sentir", "offset": 0.05}, 0.5)
ad.g("OdometerReset", {"word": "sentir", "offset": 0.1}, until={"cut": 1, "offset": -0.05}, **{"from": 15}, label="AÑOS DE EXPERIENCIA", y=0.79, delay=6)
for k in range(10):
    ad.sfx("synth:tick_01", {"word": "sentir", "offset": 0.3 + k * 0.08}, 0.2)
ad.sfx("synth:subdrop_short", {"word": "cero."}, 0.4)

# ── TU EXPERIENCIA NO SE QUEDÓ EN EL AEROPUERTO → tarjeta de embarque ───────────────────────────
ad.g("BoardingPass", {"word": "experiencia", "offset": -0.2}, until={"cut": 2, "offset": -0.05}, y=0.72, stampAt=56)
ad.sfx("lib:card-slide-1", {"word": "experiencia", "offset": -0.2}, 0.4); ad.sfx("synth:impact_punch", {"word": "aeropuerto."}, 0.45)

# ── MERCADO · CONTACTOS · NUEVAS FORMAS → split con la red que se construye ────────────────────
ad.split({"cut": 2}, {"cut": 3}, bottom=0.5, caption=0.535)
ad.g("NetworkMap", {"cut": 2}, until={"cut": 3, "offset": -0.05}, y=0.57, h=0.4,
     labels=[{"text": "OTRO MERCADO", "at": 64}, {"text": "CONTACTOS", "at": 100}, {"text": "NUEVAS FORMAS", "at": 144}])
for k in range(12):
    ad.sfx("synth:pop_low", {"cut": 2, "offset": 0.2 + k * 0.42}, 0.16)

# ── ESO REQUIERE TIEMPO → línea de meses ───────────────────────────────────────────────────────
ad.g("MonthTrack", {"cut": 3, "offset": 0.05}, until={"cut": 4, "offset": -0.05}, y=0.79)
ad.sfx("synth:tick_01", {"word": "tiempo."}, 0.35)

# ── ESCRIBE TRES PROBLEMAS → split con la libreta escrita a mano ───────────────────────────────
ad.split({"cut": 4}, {"cut": 5}, bottom=0.5, caption=0.535)
ad.g("HandNote", {"cut": 4, "offset": 0.05}, until={"cut": 5, "offset": -0.05}, y=0.585, title="Problemas que sé resolver",
     lines=[{"text": "Clientes que no cierran", "at": 46}, {"text": "Precios mal calculados", "at": 70}, {"text": "Procesos desordenados", "at": 94}])
for at in (46, 70, 94):
    ad.sfx("lib:bsb-2842", {"cut": 4, "offset": at / 30}, 0.18)

# ── TRABAJO ANTERIOR · MUESTRA · PROCESO → pestañas de evidencia ──────────────────────────────
ad.g("FolderTabs", {"cut": 5, "offset": 0.05}, until={"cut": 6, "offset": -0.05}, y=0.72,
     tabs=[{"text": "TRABAJO ANTERIOR", "sub": "Caso real: +32% en 3 meses", "at": 8}, {"text": "MUESTRA", "sub": "Una guía gratuita para probar", "at": 46},
           {"text": "PROCESO", "sub": "Mis 4 pasos, explicados", "at": 73}])
for at in (8, 46, 73):
    ad.sfx("lib:card-slide-7", {"cut": 5, "offset": at / 30}, 0.35)

# ── ADAPTA EL MENSAJE → split: de genérico a específico ────────────────────────────────────────
ad.split({"cut": 6}, {"cut": 7}, bottom=0.5, caption=0.535)
ad.g("MessageTuner", {"cut": 6, "offset": 0.05}, until={"cut": 7, "offset": -0.05}, y=0.585, morphAt=72,
     generic="Ayudo a negocios a crecer", specific="Ayudo a clínicas dentales de Madrid a llenar su agenda")
ad.sfx("synth:riser_short", {"cut": 6, "offset": 72 / 30 - 0.3}, 0.25); ad.sfx("synth:ding_success", {"cut": 6, "offset": 102 / 30}, 0.3)

# ── NO BORRA LO QUE SABES → texto detrás de Carlos ────────────────────────────────────────────
ad.cut_set(7, cutout="_work/cutouts/cut7.webm",
           behind=[{"component": "BehindTitle", "start": 1.2, "duration": 1.65,
                    "props": {"kicker": "NO SE BORRA", "kickerY": 0.035, "lines": [{"text": "LO QUE SABES", "gradient": True, "color": "#FFBB00", "size": 240}], "y": 0.27, "drift": 0.05}}])
ad.sfx("synth:impact_soft", {"word": "borra"}, 0.45)

# ── HAZLO VISIBLE → Blender: los focos revelan el trofeo; sello de evidencia ──────────────────
ad.broll(BL + "ad05_spot/spot.mp4", {"cut": 8, "offset": -0.03}, {"word": "evidencia", "offset": 0.55}, speed=0.5, transition="zoom-in")
ad.g("KickerTitle", {"cut": 8}, until={"word": "evidencia", "offset": 0.52}, kicker="HAZLO", align="center", y=0.1, lines=[{"text": "VISIBLE", "color": "#FFBB00", "size": 140}])
for k, f0 in enumerate((8, 18, 28)):
    ad.sfx("synth:impact_soft", {"cut": 8, "offset": f0 / 30 / 0.5}, 0.35)
ad.g("SealStamp", {"word": "evidencia", "offset": 0.55}, until={"cut": 9, "offset": -0.05}, y=0.78, top="EVIDENCIA", bottom="RESPALDA TU TRABAJO")
ad.sfx("synth:impact_punch", {"word": "evidencia", "offset": 0.6}, 0.45)

ad.cta()
ad.end_flat()
ad.cam_swipes()
ad.music("ov-8d613a13-4cc.mp3", drop=4)
ad.save(emphasis=["país", "cero.", "experiencia", "aeropuerto.", "mercado,", "contactos", "tiempo.", "tres", "problemas", "demostrarlo:",
                  "muestra", "proceso.", "necesidad", "cliente", "borra", "sabes.", "visible:", "evidencia", "sígueme", "escalar"])
