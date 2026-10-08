# Genera overlays.json del AD01 (decisiones creativas versionadas como código)
import json
from pathlib import Path
W = Path(__file__).parent
IC = "_work/assets/icons/"
A = "_work/assets/"
M = "clientes/carlos-buelvas/marca/"

def sfx(src, at, vol=0.5, off=0.0):
    return {"src": src, "at": at, "volume": vol, "offset": off}

def g(comp, at, dur=None, until=None, layer="over", **props):
    d = {"component": comp, "at": at, "layer": layer, "props": props}
    if until is not None: d["until"] = until
    else: d["duration"] = dur
    return d

CAM1 = {"x": 0.5, "y": 0.14}
CAM2 = {"x": 0.5, "y": 0.27}
cuts = {
 "0":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.34}, {"t": 0.5, "s": 1.12, "ease": "smooth"}, {"t": 3.30, "s": 1.15}, {"t": 3.52, "s": 1.25, "ease": "punch"}, {"t": 3.84, "s": 1.27}]},
 "1":  {"focus": CAM2, "zoom": [{"t": 0, "s": 1.04}, {"t": 3.9, "s": 1.12, "ease": "linear"}]},
 "2":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.06}, {"t": 2.4, "s": 1.12, "ease": "smooth"}, {"t": 2.55, "s": 1.2, "ease": "punch"}, {"t": 3.17, "s": 1.21}]},
 "3":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.0}, {"t": 2.3, "s": 1.05, "ease": "linear"}]},
 "4":  {"focus": CAM2, "zoom": [{"t": 0, "s": 1.10}, {"t": 2.0, "s": 1.18, "ease": "smooth"}], "fx": {"shake": 3}},
 "5":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.16}, {"t": 0.6, "s": 1.22, "ease": "punch"}]},
 "6":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.04}, {"t": 2.6, "s": 1.1, "ease": "linear"}]},
 "7":  {"focus": CAM2, "zoom": [{"t": 0, "s": 1.14}, {"t": 1.36, "s": 1.2, "ease": "smooth"}]},
 "8":  {"focus": CAM1, "zoom": [{"t": 0, "s": 1.08}]},
 "9":  {"focus": CAM2, "zoom": [{"t": 0, "s": 1.1}]},
 "10": {"focus": CAM2, "zoom": [{"t": 0, "s": 1.0}, {"t": 1.6, "s": 1.05, "ease": "smooth"}, {"t": 1.84, "s": 1.13, "ease": "punch"}, {"t": 2.58, "s": 1.14}]},
 "11": {"focus": CAM1, "zoom": [{"t": 0, "s": 1.1}, {"t": 1.2, "s": 1.15, "ease": "smooth"}, {"t": 2.7, "s": 1.16}, {"t": 2.85, "s": 1.24, "ease": "punch"}, {"t": 3.74, "s": 1.26}]},
 "12": {"focus": CAM2, "transition": {"type": "light-leak"}, "zoom": [{"t": 0, "s": 1.0}, {"t": 2.91, "s": 1.13, "ease": "smooth"}]},
 "13": {"focus": CAM1, "transition": {"type": "flash", "duration": 0.3}, "zoom": [{"t": 0, "s": 1.22}, {"t": 0.35, "s": 1.08, "ease": "smooth"}, {"t": 3.56, "s": 1.13, "ease": "linear"}]},
}

G = []
S = []
# ---------------- HOOK 0–3.84
G += [
 g("Flash", 0, 0.28, layer="top", peak=0.9, color="#dbe7ff"),
 g("BlockTitle", 0.02, until={"word": "al"}, y=0.71, width=0.84, stagger=13, enter="slam",
   lines=[{"text": "¿DE QUÉ SIRVE"}, {"text": "VENDER MÁS", "color": "gold"}]),
 g("IconBadge", {"word": "vender"}, 1.7, icon=IC + "trend-up-bold.svg", x=0.83, y=0.43, leader="left", leaderLen=120, size=0.95),
 g("BlockTitle", {"word": "al"}, until={"cut": 1, "offset": -0.02}, y=0.72, width=0.86, stagger=9, enter="rise",
   lines=[{"text": "AL FINAL DEL MES", "color": "outline", "weight": 800}, {"text": "SI SIGUES PREOCUPADO", "weight": 900}, {"text": "POR EL DINERO?", "color": "gold"}]),
 g("Coins3D", {"word": "dinero?", "offset": -0.3}, until={"cut": 1, "offset": -0.02}, layer="over", mode="rain", count=24, avoid=[0.26, 0.74], size=0.95),
 g("Flash", {"word": "dinero?"}, 0.18, layer="top", peak=0.45, color="#FFBB00"),
]
S += [sfx("synth:impact_cinematic", 0, 0.85), sfx("synth:subdrop_01", 0, 0.7), sfx("lib:bsb-1796", 0, 0.45),
      sfx("synth:swipe_01", {"word": "vender"}, 0.45, -0.05), sfx("lib:confirmation_001", {"word": "vender"}, 0.35, 0.1),
      sfx("synth:riser_short", 1.15, 0.32), sfx("synth:whoosh_fast", {"word": "al"}, 0.5, -0.1),
      sfx("lib:pluck_002", {"word": "sigues"}, 0.3), sfx("lib:pluck_001", {"word": "por"}, 0.3),
      sfx("synth:impact_punch", {"word": "dinero?"}, 0.8), sfx("lib:bsb-1417", {"word": "dinero?"}, 0.4, 0.05),
      sfx("lib:chips-collide-2", {"word": "dinero?"}, 0.55, 0.2), sfx("lib:chips-stack-3", {"word": "dinero?"}, 0.45, 0.55)]

# ---------------- AGENDA LLENA (escena)
G += [
 g("BrandScene", {"word": "agenda", "offset": -0.25}, until={"word": "todo", "offset": -0.1}, layer="under", variant="glow"),
 g("AgendaFill", {"word": "agenda", "offset": -0.2}, until={"word": "todo", "offset": -0.1}, title="AGENDA LLENA", y=0.29, rows=6),
 g("IconBadge", {"word": "atendemos"}, until={"word": "todo", "offset": -0.1}, icon=IC + "users-three-bold.svg", x=0.5, y=0.80, leader="none", label="CLIENTES TODO EL DÍA", size=0.9),
]
S += [sfx("synth:whoosh_medium", {"word": "agenda", "offset": -0.25}, 0.55, -0.12), sfx("lib:switch7", {"word": "agenda"}, 0.35)]
for k in range(12):
    S.append(sfx("lib:tick_00" + str(1 + k % 2), {"word": "agenda"}, 0.28, 0.2 + k * 0.09))
S += [sfx("synth:pop_01", {"word": "atendemos"}, 0.45), sfx("synth:swipe_02", {"word": "todo", "offset": -0.1}, 0.4)]
G += [g("IconBadge", {"word": "todo"}, until={"cut": 2}, icon=IC + "hourglass-high-bold.svg", x=0.83, y=0.47, leader="left", size=0.85)]
S += [sfx("lib:pluck_001", {"word": "todo"}, 0.3, 0.05)]

# ---------------- CRECIENDO (sobre video)
G += [
 g("IconBadge", {"word": "“Ahora"}, until={"cut": 3, "offset": -0.05}, icon=IC + "rocket-launch-bold.svg", x=0.83, y=0.44, leader="left", size=0.95, label="CRECIENDO"),
 g("GrowthLine", {"word": "negocio"}, until={"cut": 3, "offset": -0.05}, y=0.83, h=0.13),
]
S += [sfx("lib:confirmation_002", {"word": "“Ahora"}, 0.35), sfx("lib:phaserUp3", {"word": "negocio"}, 0.3), sfx("synth:ding_success", {"word": "creciendo”."}, 0.3)]

# ---------------- PAGAR TODO (escena túnel + monedas)
G += [
 g("BrandScene", {"word": "el", "n": 4, "offset": -0.1}, until={"cut": 4, "offset": -0.02}, layer="under", variant="tunnel"),
 g("BlockTitle", {"word": "momento", "offset": -0.15}, until={"cut": 4, "offset": -0.02}, y=0.27, width=0.84, stagger=7, enter="rise",
   lines=[{"text": "LLEGA EL MOMENTO", "weight": 800}, {"text": "DE PAGAR", "color": "outline"}, {"text": "TODO", "color": "gold"}]),
 g("Coins3D", {"word": "pagar"}, until={"cut": 4, "offset": -0.02}, mode="drain", count=18, yTop=0.66, size=0.85),
]
S += [sfx("synth:whoosh_heavy", {"word": "el", "n": 4, "offset": -0.1}, 0.55, -0.15), sfx("synth:braam_02", {"word": "momento"}, 0.45, -0.1),
      sfx("lib:chips-stack-3", {"word": "pagar"}, 0.5, 0.05), sfx("lib:bsb-0339", {"word": "todo", "n": 2}, 0.45), sfx("synth:swipe_01", {"cut": 4}, 0.35, -0.05)]

# ---------------- TRABAJAMOS MUCHÍSIMO (sobre lateral)
G += [g("IconBadge", {"word": "trabajamos"}, until={"cut": 5, "offset": -0.05}, icon=IC + "briefcase-bold.svg", x=0.83, y=0.46, leader="left", size=0.9, label="MUCHÍSIMO")]
S += [sfx("lib:pluck_002", {"word": "trabajamos"}, 0.32), sfx("synth:heartbeat_01", {"word": "muchísimo"}, 0.35)]

# ---------------- LO POCO QUE NOS QUEDÓ (escena ProfitGap)
G += [
 g("BrandScene", {"word": "lo", "n": 1, "offset": -0.12}, until={"cut": 6, "offset": -0.02}, layer="under", variant="glow"),
 g("ProfitGap", {"word": "lo", "n": 1, "offset": -0.1}, until={"cut": 6, "offset": -0.02}, y=0.27, h=0.34, salesLabel="VENDES", keepLabel="TE QUEDA", sales=12000, keep=850),
]
S += [sfx("synth:whoosh_medium", {"word": "lo", "n": 1}, 0.5, -0.2), sfx("lib:phaserUp3", {"word": "lo", "n": 1}, 0.3, 0.05),
      sfx("synth:tape_stop", {"word": "poco"}, 0.35, 0.15), sfx("synth:impact_soft", {"word": "quedó."}, 0.55)]

# ---------------- TU TIEMPO TAMBIÉN CUENTA
G += [
 g("IconBadge", {"word": "servicio,"}, until={"word": "tu", "offset": -0.1}, icon=IC + "tag-bold.svg", x=0.83, y=0.44, leader="left", size=0.9, label="SERVICIO"),
 g("BrandScene", {"word": "tu", "offset": -0.08}, until={"cut": 7, "offset": -0.02}, layer="under", variant="pattern", word="TIEMPO"),
 g("TimeIsMoney", {"word": "tu", "offset": -0.05}, until={"cut": 7, "offset": -0.02}, x=0.5, y=0.26, size=0.95, label="TU TIEMPO TAMBIÉN CUENTA"),
]
S += [sfx("lib:pluck_001", {"word": "servicio,"}, 0.32), sfx("synth:whoosh_medium", {"word": "tu"}, 0.5, -0.18), sfx("synth:cash_01", {"word": "también"}, 0.4)]
for k in range(10):
    S.append(sfx("lib:tick_002", {"word": "tu"}, 0.3, 0.05 + k * 0.14))

# ---------------- HORAS EXTRA (lateral)
G += [g("IconBadge", {"word": "Las"}, until={"cut": 8, "offset": -0.02}, icon=IC + "clock-countdown-bold.svg", x=0.83, y=0.46, leader="left", size=0.9, label="HORAS EXTRA")]
S += [sfx("synth:swipe_02", {"cut": 7}, 0.3), sfx("lib:confirmation_001", {"word": "horas"}, 0.35)]

# ---------------- COSTOS (escena que cubre los cortes 8 y 9)
G += [
 g("BrandScene", {"cut": 8, "offset": -0.02}, until={"cut": 10, "offset": -0.02}, layer="under", variant="glow"),
 g("CostTags", {"cut": 8, "offset": -0.02}, until={"cut": 10, "offset": -0.02}, y=0.28, items=["HORAS EXTRA", "CAMBIOS QUE REGALAS", "DESCUENTOS"], delays=[0, 12, 48], tag="COSTO"),
 g("Flash", {"word": "costo."}, 0.2, layer="top", peak=0.35, color="#FFBB00"),
]
S += [sfx("synth:whoosh_medium", {"cut": 8}, 0.5, -0.2), sfx("lib:card-slide-1", {"cut": 8}, 0.5, 0.05), sfx("lib:card-slide-3", {"word": "cambios"}, 0.5),
      sfx("lib:card-slide-5", {"word": "descuentos"}, 0.5), sfx("lib:impactPunch_medium_000", {"word": "descuentos"}, 0.35, 0.25),
      sfx("synth:impact_soft", {"word": "costo."}, 0.6), sfx("lib:bsb-1417", {"word": "costo."}, 0.35, 0.05), sfx("lib:bsb-1795", {"cut": 10}, 0.4, -0.15)]

# ---------------- OTRO CLIENTE / PREGÚNTATE
G += [
 g("IconBadge", {"word": "otro"}, until={"word": "pregúntate:", "offset": -0.05}, icon=IC + "user-plus-bold.svg", x=0.83, y=0.46, leader="left", size=0.9, label="OTRO CLIENTE"),
 g("IconBadge", {"word": "pregúntate:"}, until={"cut": 11, "offset": -0.02}, icon=IC + "question-bold.svg", x=0.83, y=0.46, leader="left", size=0.95),
]
S += [sfx("lib:pluck_002", {"word": "otro"}, 0.32), sfx("lib:question_001", {"word": "pregúntate:"}, 0.4), sfx("synth:swipe_01", {"cut": 11}, 0.3, -0.05)]

# ---------------- GANANCIA (3D héroe)
G += [
 g("IconBadge", {"word": "trabajo"}, until={"word": "ganancia", "offset": -0.15}, icon=IC + "scales-bold.svg", x=0.83, y=0.44, leader="left", size=0.9),
 g("BrandScene", {"word": "ganancia", "offset": -0.12}, until={"word": "lo", "n": 2, "offset": -0.05}, layer="under", variant="tunnel"),
 g("Text3DTitle", {"word": "ganancia", "offset": -0.1}, until={"word": "lo", "n": 2, "offset": -0.05}, text="GANANCIA", font="Montserrat-Black", color="#FFBB00", metal=0.85, size=1.0, y=1.55, depth=0.4),
 g("IconBadge", {"word": "voy"}, until={"cut": 12, "offset": -0.05}, icon=IC + "coins-bold.svg", x=0.83, y=0.44, leader="left", size=0.9),
]
S += [sfx("lib:pluck_001", {"word": "trabajo"}, 0.3), sfx("synth:riser_short", {"word": "trabajo"}, 0.28, -0.3),
      sfx("synth:impact_cinematic", {"word": "ganancia"}, 0.7, -0.08), sfx("synth:subdrop_short", {"word": "ganancia"}, 0.55, -0.08),
      sfx("lib:glass_002", {"word": "ganancia"}, 0.35, 0.4), sfx("synth:whoosh_fast", {"word": "lo", "n": 2}, 0.45, -0.12), sfx("lib:pluck_002", {"word": "voy"}, 0.3)]

# ---------------- BIENESTAR (emocional, lateral)
G += [g("BlockTitle", {"word": "tu", "n": 2, "offset": -0.03}, until={"cut": 13, "offset": -0.03}, y=0.78, width=0.84, stagger=16, enter="rise", sparkle=2,
        lines=[{"text": "TU ESFUERZO", "weight": 900}, {"text": "MERECE CONVERTIRSE", "weight": 700}, {"text": "EN BIENESTAR", "color": "gold"}])]
S += [sfx("synth:reverse_swell", {"cut": 12}, 0.45, -1.5), sfx("lib:pluck_001", {"word": "esfuerzo"}, 0.3), sfx("lib:pluck_002", {"word": "merece"}, 0.3),
      sfx("lib:glass_002", {"word": "bienestar."}, 0.4, 0.2), sfx("synth:riser_short", {"word": "convertirse"}, 0.28, -0.6)]

# ---------------- CTA
G += [g("InstagramFollow", {"word": "para", "n": 2, "offset": 0.1}, until={"end": True, "offset": -1.75}, layer="over", y=0.80, avatar=A + "avatar.jpg")]
S += [sfx("synth:braam_01", {"cut": 13}, 0.55), sfx("synth:impact_cinematic", {"cut": 13}, 0.55), sfx("synth:whoosh_medium", {"word": "para", "n": 2}, 0.5),
      sfx("lib:click1", {"word": "para", "n": 2}, 0.6, 1.0), sfx("lib:confirmation_002", {"word": "para", "n": 2}, 0.45, 1.05)]
for k in range(4):
    S.append(sfx("synth:pop_02", {"word": "para", "n": 2}, 0.25, 1.1 + k * 0.12))

# ---------------- CIERRE DE MARCA (cola)
G += [
 g("BrandScene", {"end": True, "offset": -1.85}, until={"end": True}, layer="top", variant="tunnel"),
 g("Logo3D", {"end": True, "offset": -1.8}, until={"end": True}, layer="top", svg=M + "logo.svg", depth=60, metal=0.9, color="#FFBB00", scale=0.42),
 g("CTAPill", {"end": True, "offset": -1.3}, until={"end": True}, layer="top", text="SÍGUEME", x=0.5, y=0.78, size=1.1),
]
S += [sfx("synth:whoosh_heavy", {"end": True, "offset": -1.85}, 0.55, -0.1), sfx("synth:impact_cinematic", {"end": True, "offset": -1.75}, 0.6),
      sfx("lib:glass_002", {"end": True, "offset": -1.0}, 0.4), sfx("lib:confirmation_002", {"end": True, "offset": -1.3}, 0.35)]

# cambios de cámara sutiles
for c in (1, 2, 5, 9, 10, 13):
    S.append(sfx("synth:swipe_02", {"cut": c}, 0.18, -0.06))

ov = {
 "format": "9:16", "fps": 30, "tail": 1.9, "background": "#01030c",
 "logo": M + "logo_blanco.png",
 "zoom": {"auto": False},
 "cuts": cuts,
 "captions": {"enabled": True, "style": "premium", "position": 0.605, "maxWords": 3, "uppercase": True,
              "emphasis": ["dinero?", "agenda", "llena,", "creciendo”.", "pagar", "muchísimo", "poco", "tiempo", "extra,", "regalas", "descuentos", "costo.", "ganancia", "justifica", "bienestar.", "sígueme", "escalar", "ventas."],
              "hideDuring": [[0, 3.84], [30.55, 33.9], [37.4, 99]]},
 "graphics": G, "sfx": S,
 "music": [{"src": "library/music/_dl/epic/music/epic-cinematic/ov-1a767512-5d6.mp3", "at": 0, "volume": 0.3, "duck": 0.42,
            "dropAt": {"cut": 13}, "drop": 1, "fadeIn": 0.15, "fadeOut": 1.4}],
 "fx": {"grade": "cinematic", "grain": 0.035, "vignette": 0.28, "lightLeakHue": 185},
}
(W / "overlays.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1))
print(len(G), "gráficos", len(S), "sfx")
