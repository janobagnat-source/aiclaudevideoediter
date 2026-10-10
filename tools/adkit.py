"""Kit para escribir overlays.json de ads de Carlos Buelvas (o cualquier talking head multicámara) con el mismo estándar.

Uso en _work/make_overlays.py:
    import sys; sys.path.insert(0, "<repo>/tools")
    from adkit import Ad
    ad = Ad(__file__)                 # lee edl.json + cams.json del proyecto
    ad.hook_hit()                      # flash + impacto + sub en t=0
    ad.g("BlockTitle", {"word": "x"}, 2.0, lines=[...])
    ad.sfx("synth:whoosh_fast", {"cut": 3}, 0.5, -0.1)
    ad.scene("glow", {"word": "agenda"}, {"cut": 2})   # fondo de marca a pantalla completa (capa under)
    ad.cta(); ad.end_card()
    ad.music("ov-5f49e44a-f2b.mp3", drop=4)
    ad.save(emphasis=[...], hide=[[a, b]])
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = "clientes/carlos-buelvas/marca/"
IC_DIR = ROOT / "clientes/carlos-buelvas/proyectos/ad01/_work/assets/icons"


class Ad:
    def __init__(self, file: str):
        self.w = Path(file).resolve().parent
        self.proj = self.w.parent
        self.edl = json.loads((self.w / "edl.json").read_text())
        cams_p = self.w / "src" / "cams.json"
        self.cams = json.loads(cams_p.read_text()) if cams_p.exists() else {}
        self.G: list[dict] = []
        self.S: list[dict] = []
        self.cut_over: dict = {}
        self.music_cfg: list = []
        self.B: list[dict] = []          # b-roll (p.ej. clips de Blender)
        self.layouts: list[dict] = []    # reacomodos del track principal (split)
        self.cap_pos: list[dict] = []    # posición de subtítulos por tramos
        self.n = len(self.edl["cuts"])

    # ---------------- helpers
    @staticmethod
    def icon(name: str) -> str:
        p = IC_DIR / f"{name}.svg"
        if not p.exists():
            import requests
            IC_DIR.mkdir(parents=True, exist_ok=True)
            r = requests.get(f"https://api.iconify.design/ph/{name}.svg", params={"color": "#ffffff"}, timeout=30)
            if r.status_code != 200 or "<svg" not in r.text:
                raise SystemExit(f"icono ph:{name} no existe")
            p.write_text(r.text)
        return str(p.relative_to(ROOT))

    def g(self, comp, at, dur=None, until=None, layer="over", **props):
        d = {"component": comp, "at": at, "layer": layer, "props": props}
        if until is not None:
            d["until"] = until
        else:
            d["duration"] = dur
        self.G.append(d)
        return d

    def broll(self, src, at, until, mode="full", transition="cut", speed=1.0, inn=0.0, kenburns="none", **kw):
        self.B.append({"src": src, "at": at, "until": until, "mode": mode, "transition": transition, "speed": speed,
                       "in": inn, "kenburns": kenburns, **kw})

    def split(self, at, until, bottom=0.5, caption=0.535, **kw):
        """Carlos arriba en una ventana flotante, panel de marca abajo para gráficos; los subtítulos suben al borde."""
        self.layouts.append({"at": at, "until": until, "mode": "split", "bottom": bottom, **kw})
        self.cap_pos.append({"at": at, "until": until, "pos": caption})
        self.sfx("lib:card-slide-2", at, 0.45, -0.05)

    def force_cam(self, cut, cam):
        """Cambia la cámara de un corte en edl.json (p.ej. frontal en los split). Llamar ANTES de auto_zooms."""
        c = self.edl["cuts"][cut]
        if c["source"] != cam:
            if c.get("src"):
                c["src"] = c["src"].replace(f'{c["source"]}_9x16', f"{cam}_9x16")
            c["source"] = cam
            (self.w / "edl.json").write_text(json.dumps(self.edl, ensure_ascii=False, indent=1))

    def set_cams(self, mapping):
        for k, v in mapping.items():
            self.force_cam(int(k), v)

    def cut_set(self, cut, **kw):
        self.cut_over.setdefault(str(cut), {}).update(kw)

    def sfx(self, src, at, vol=0.5, off=0.0, **kw):
        self.S.append({"src": src, "at": at, "volume": vol, "offset": off, **kw})

    def scene(self, variant, at, until, **kw):
        self.g("BrandScene", at, until=until, layer="under", variant=variant, **kw)
        self.sfx("synth:whoosh_medium", at, 0.55, -0.15)

    def badge(self, icon, at, until=None, dur=None, label=None, side="right", y=0.45, size=0.9):
        x = 0.83 if side == "right" else 0.17
        self.g("IconBadge", at, dur=dur, until=until, icon=self.icon(icon), x=x, y=y, leader="left" if side == "right" else "right",
               size=size, **({"label": label} if label else {}))
        self.sfx("lib:pluck_00" + str(1 + len(self.S) % 2), at, 0.32, 0.05)

    def focus_of(self, cam):
        fy = (self.cams.get(cam) or {}).get("face_y", 0.2)
        return {"x": 0.5, "y": round(max(0.1, fy - 0.02), 3)}

    # ---------------- zooms profesionales automáticos (alternancia + empujes suaves + punch en énfasis)
    def auto_zooms(self, punch_words=(), overrides=None):
        overrides = overrides or {}
        pw = {p.lower().strip("¿?¡!.,:;“”\"") for p in punch_words}
        for i, c in enumerate(self.edl["cuts"]):
            if str(i) in overrides:
                self.cut_over[str(i)] = {"focus": self.focus_of(c["source"]), **overrides[str(i)]}
                continue
            dur = c["out"] - c["in"]
            base = [1.02, 1.12, 1.06][i % 3]
            keys = [{"t": 0, "s": base}]
            level = base
            last_step = 0.0
            for w in c["words"]:
                rel = w["start"] - c["in"]
                clean = w["text"].lower().strip("¿?¡!.,:;“”\"")
                if clean in pw and rel > 0.2:
                    keys += [{"t": round(rel - 0.03, 3), "s": round(level, 3)}, {"t": round(rel + 0.14, 3), "s": round(level + 0.08, 3), "ease": "punch"}]
                    level += 0.08
                    last_step = rel
                elif rel - last_step > 2.4 and rel < dur - 0.6:
                    keys += [{"t": round(rel - 0.02, 3), "s": round(level, 3)}, {"t": round(rel + 0.5, 3), "s": round(level + 0.05 if level < 1.2 else level - 0.1, 3), "ease": "smooth"}]
                    level = keys[-1]["s"]
                    last_step = rel
            keys.append({"t": round(dur, 3), "s": round(level + 0.02, 3), "ease": "linear"})
            self.cut_over[str(i)] = {"focus": self.focus_of(c["source"]), "zoom": keys}

    def transition(self, cut, kind, duration=0.3):
        self.cut_over.setdefault(str(cut), {})["transition"] = {"type": kind, "duration": duration}

    # ---------------- bloques estándar
    def hook_hit(self):
        self.g("Flash", 0, 0.28, layer="top", peak=0.9, color="#dbe7ff")
        self.sfx("synth:impact_cinematic", 0, 0.6)
        self.sfx("synth:subdrop_01", 0, 0.5)
        self.sfx("lib:bsb-1796", 0, 0.4)

    def cta(self, start_anchor=None):
        last = self.n - 1
        at = start_anchor or {"cut": last, "offset": 0.55}
        self.transition(last, "flash", 0.3)
        self.g("InstagramFollow", at, until={"end": True, "offset": -1.75}, y=0.80, avatar=M + "ig_perfil.jpg",
               name="Carlos Buelvas | Coach Mentor de Ventas", bio="CEO Business Sales Academy · 🌎 Speaker",
               tagline="🚀 Acelero tus Ventas sin estrategias de marketing complicadas", verified=True,
               followers="85,1 mil", posts="3.508", following="3.615")
        self.sfx("synth:braam_01", {"cut": last}, 0.5)
        self.sfx("synth:impact_cinematic", {"cut": last}, 0.5)
        self.sfx("synth:whoosh_medium", at, 0.5)
        self.sfx("lib:click1", at, 0.6, 0.9)
        self.sfx("lib:confirmation_002", at, 0.45, 0.95)
        for k in range(4):
            self.sfx("synth:pop_02", at, 0.25, 1.0 + k * 0.12)

    def end_card(self, logo_scale=0.42):
        self.g("BrandScene", {"end": True, "offset": -1.85}, until={"end": True}, layer="top", variant="tunnel")
        self.g("Logo3D", {"end": True, "offset": -1.8}, until={"end": True}, layer="top", svg=M + "logo.svg", depth=60, metal=0.9, color="#FFBB00", scale=logo_scale)
        self.g("CTAPill", {"end": True, "offset": -1.3}, until={"end": True}, layer="top", text="SÍGUEME", x=0.5, y=0.78, size=1.1)
        self.sfx("synth:whoosh_heavy", {"end": True, "offset": -1.85}, 0.55, -0.1)
        self.sfx("synth:impact_cinematic", {"end": True, "offset": -1.75}, 0.55)
        self.sfx("lib:glass_002", {"end": True, "offset": -1.0}, 0.4)

    def end_flat(self, logo=M + "logo_dorado.png", tagline="COACH · MENTOR DE VENTAS"):
        """Cierre plano (sin 3D): logo dorado con revelado por máscara y barrido de brillo + CTA."""
        self.g("LogoReveal", {"end": True, "offset": -1.85}, until={"end": True}, layer="top", logo=logo, tagline=tagline)
        self.sfx("synth:whoosh_reverse", {"end": True, "offset": -1.85}, 0.45, -0.2)
        self.sfx("synth:impact_soft", {"end": True, "offset": -1.7}, 0.5)
        self.sfx("lib:glass_002", {"end": True, "offset": -1.15}, 0.35)
        self.sfx("synth:pop_02", {"end": True, "offset": -1.3}, 0.3)

    def cam_swipes(self, vol=0.16):
        for i in range(1, self.n):
            if self.edl["cuts"][i]["source"] != self.edl["cuts"][i - 1]["source"]:
                self.sfx("synth:swipe_02", {"cut": i}, vol, -0.06)

    def music(self, file, drop=None, inn=None, volume=0.3, duck=0.32, at_cut=None):
        path = next(iter(glob.glob(str(ROOT / "library/music/_dl") + "/**/" + file, recursive=True)))
        lic = {x.get("local", "").split("/")[-1]: x.get("license", "") for x in json.loads((ROOT / "library/credits.json").read_text()) if isinstance(x, dict)}
        if lic.get(file, "") not in ("by", "cc0", "pdm"):
            raise SystemExit(f"música {file}: licencia «{lic.get(file)}» no permitida (solo CC BY / CC0)")
        m = {"src": str(Path(path).relative_to(ROOT)), "at": 0, "volume": volume, "duck": duck, "fadeIn": 0.15, "fadeOut": 1.4}
        if inn is not None:
            m["in"] = inn
        else:
            m["dropAt"] = {"cut": at_cut if at_cut is not None else self.n - 1}
            m["drop"] = drop or 0
        self.music_cfg.append(m)

    def save(self, emphasis=(), hide=(), tail=1.9):
        ov = {"format": "9:16", "fps": 30, "tail": tail, "background": "#01030c", "logo": M + "logo_blanco.png",
              "zoom": {"auto": False}, "cuts": self.cut_over,
              "captions": {"enabled": True, "style": "premium", "position": 0.605, "maxWords": 3, "uppercase": True,
                           "emphasis": list(emphasis), "hideDuring": [list(h) for h in hide] + [[999, 9999]],
                           "positionDuring": self.cap_pos},
              "graphics": self.G, "sfx": self.S, "music": self.music_cfg, "broll": self.B, "layouts": self.layouts,
              "mix": {"sfxTarget": -20.0, "sfxDuck": 0.5},
              "fx": {"grade": "cinematic", "grain": 0.035, "vignette": 0.28, "lightLeakHue": 185}}
        (self.w / "overlays.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1))
        print(len(self.G), "gráficos", len(self.S), "sfx")
