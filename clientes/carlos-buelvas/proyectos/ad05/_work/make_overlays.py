# AD05 — Emigrar no borra tu experiencia
import sys; sys.path.insert(0, "/home/user/aiclaudevideoediter/tools")
from adkit import Ad, M
ad = Ad(__file__)
ad.auto_zooms(punch_words=["país", "cero.", "experiencia", "aeropuerto.", "tiempo.", "tres", "demostrarlo:", "proceso.",
                           "necesidad", "borra", "visible:", "evidencia", "sígueme"])

# HOOK: vuelo de TU PAÍS → NUEVO PAÍS (MG b-roll) y golpe en “DE CERO”
ad.hook_hit()
ad.g("BrandScene", 0, until={"word": "sentir", "offset": -0.05}, layer="under", variant="glow", word="NUEVO PAÍS")
ad.g("FlightPath", 0.05, until={"word": "sentir", "offset": -0.05}, y=0.3, **{"from": "TU PAÍS"}, to="NUEVO PAÍS")
ad.sfx("synth:whoosh_heavy", 0.25, 0.4)
ad.sfx("lib:bsb-1111", 0.6, 0.2)
ad.sfx("synth:whoosh_medium", {"word": "sentir", "offset": -0.05}, 0.45, -0.1)
ad.g("BlockTitle", {"word": "empezaste", "offset": -0.05}, until={"cut": 1, "offset": -0.03}, y=0.81, width=0.62, stagger=6, enter="slam",
     lines=[{"text": "EMPEZAR", "weight": 900}, {"text": "DE CERO", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "cero."}, 0.55)
ad.sfx("synth:subdrop_short", {"word": "cero."}, 0.4)

# PERO TU EXPERIENCIA NO SE QUEDÓ EN EL AEROPUERTO
ad.badge("suitcase-rolling-bold", {"word": "experiencia"}, until={"cut": 2, "offset": -0.03}, label="TU EXPERIENCIA", side="right", y=0.44)
ad.badge("airplane-takeoff-bold", {"word": "quedó"}, until={"cut": 2, "offset": -0.03}, label="AEROPUERTO", side="left", y=0.44)
ad.g("BlockTitle", {"word": "aeropuerto.", "offset": -0.1}, until={"cut": 2, "offset": -0.03}, y=0.81, width=0.6, stagger=8, enter="rise", sparkle=1,
     lines=[{"text": "VIAJA", "weight": 900}, {"text": "CONTIGO", "color": "gold"}])
ad.sfx("lib:glass_002", {"word": "aeropuerto."}, 0.35)

# LO QUE TAL VEZ NECESITAS
ad.g("Checklist", {"word": "otro", "offset": -0.2}, until={"cut": 3, "offset": -0.03}, title="TAL VEZ NECESITAS",
     items=["CONOCER OTRO MERCADO", "CONSTRUIR CONTACTOS", "NUEVAS FORMAS DE TRABAJAR"], every=45, position=0.84, icon="✓")
for w in ["mercado,", "contactos", "aprender"]:
    ad.sfx("synth:pop_01", {"word": w}, 0.4)
ad.badge("globe-hemisphere-west-bold", {"word": "mercado,"}, until={"cut": 3, "offset": -0.03}, side="right", y=0.42)
# ESO REQUIERE TIEMPO
ad.badge("hourglass-medium-bold", {"cut": 3, "offset": 0.05}, until={"cut": 4, "offset": -0.03}, label="REQUIERE TIEMPO", side="right", y=0.44)
ad.sfx("lib:bsb-0307", {"word": "tiempo."}, 0.3)

# ESCRIBE TRES PROBLEMAS → libreta (MG b-roll)
ad.scene("glow", {"word": "escribe", "offset": -0.1}, {"cut": 5, "offset": -0.02}, word="ESCRIBE")
ad.g("NotepadList", {"word": "escribe", "offset": -0.05}, until={"cut": 5, "offset": -0.02}, y=0.3, title="3 PROBLEMAS QUE RESUELVO",
     items=["Problema #1", "Problema #2", "Problema #3"], every=14)
for k in range(3):
    ad.sfx("lib:pluck_00" + str(1 + k % 2), {"word": "tres"}, 0.3, 0.1 + k * 0.47)
ad.sfx("lib:bsb-2842", {"word": "demostrarlo:"}, 0.2)
# CÓMO DEMOSTRARLO
ad.g("Checklist", {"word": "trabajo", "offset": -0.25}, until={"cut": 6, "offset": -0.03}, title="CÓMO DEMOSTRARLO",
     items=["UN TRABAJO ANTERIOR", "UNA MUESTRA", "TU PROCESO"], every=38, position=0.84, icon="✓")
for w in ["trabajo", "muestra", "explicación"]:
    ad.sfx("lib:confirmation_001" if w == "explicación" else "synth:pop_01", {"word": w}, 0.38)
ad.badge("briefcase-bold", {"word": "trabajo"}, until={"cut": 6, "offset": -0.03}, side="right", y=0.42)

# ADAPTA EL MENSAJE AL CLIENTE DE HOY → post adaptado
ad.scene("glow", {"word": "adapta", "offset": -0.1}, {"cut": 7, "offset": -0.02})
ad.g("PostCard", {"word": "adapta", "offset": -0.05}, until={"cut": 7, "offset": -0.02}, y=0.3, avatar=M + "ig_perfil.jpg", cps=34,
     text="🎯 ¿Tienes un negocio y no sabes cómo vender en este nuevo mercado? Esto es para ti 👇", stamp="MENSAJE ADAPTADO", stampAt=96)
for k in range(14):
    ad.sfx("lib:bsb-2842", {"word": "adapta"}, 0.15, 0.1 + k * 0.1)
ad.sfx("synth:impact_soft", {"word": "hoy."}, 0.5)

# LLEGAR A UN LUGAR NUEVO NO BORRA LO QUE SABES
ad.badge("map-pin-bold", {"word": "lugar"}, until={"cut": 8, "offset": -0.03}, label="LUGAR NUEVO", side="right", y=0.44)
ad.g("BlockTitle", {"word": "borra", "offset": -0.1}, until={"cut": 8, "offset": -0.03}, y=0.81, width=0.72, stagger=6, enter="slam",
     lines=[{"text": "NO BORRA", "weight": 900}, {"text": "LO QUE SABES", "color": "gold"}])
ad.sfx("synth:impact_punch", {"word": "borra"}, 0.45)

# HAZLO VISIBLE (3D) → EVIDENCIA
ad.scene("tunnel", {"cut": 8, "offset": 0.0}, {"word": "problema", "offset": -0.05})
ad.g("Text3DTitle", {"cut": 8, "offset": 0.02}, until={"word": "problema", "offset": -0.05}, text="HAZLO\nVISIBLE", font="Montserrat-Black",
     color="#FFBB00", metal=0.85, size=0.9, y=1.1, depth=0.35)
ad.transition(8, "flash", 0.25)
ad.sfx("synth:impact_cinematic", {"cut": 8}, 0.5)
ad.sfx("synth:subdrop_short", {"cut": 8}, 0.4)
ad.badge("magnifying-glass-bold", {"word": "problema"}, until={"cut": 9, "offset": -0.03}, label="UN PROBLEMA", side="left", y=0.44)
ad.badge("seal-check-bold", {"word": "evidencia"}, until={"cut": 9, "offset": -0.03}, label="EVIDENCIA", side="right", y=0.44)
ad.g("ShapeBurst", {"word": "evidencia"}, 0.6, x=0.83, y=0.44, radius=0.8)
ad.sfx("lib:glass_002", {"word": "evidencia"}, 0.35, 0.1)

ad.cta()
ad.end_card()
ad.cam_swipes()
ad.music("ov-8d613a13-4cc.mp3", drop=4)
ad.save(emphasis=["país", "cero.", "experiencia", "aeropuerto.", "mercado,", "contactos", "tiempo.", "tres", "problemas", "demostrarlo:",
                  "muestra", "proceso.", "necesidad", "cliente", "borra", "sabes.", "visible:", "evidencia", "sígueme", "escalar"],
        hide=[[32.94, 34.40]])
