"""Base común para b-rolls 3D en Blender (estética ejecutiva de la marca: azul profundo + dorado, estudio oscuro).

Uso dentro de un script de escena (ejecutado con `blender -b -P escena.py -- <out_dir> [--preview]`):
    import sys; sys.path.insert(0, "<repo>/tools/blender")
    from studio import *
    S = Studio(frames=72)            # limpia la escena, 1080x1920 30 fps, Cycles CPU
    gold = S.gold(); ...
    S.render()                       # PNG por frame en out_dir + mp4 al final (ffmpeg)
"""
from __future__ import annotations

import math
import os
import subprocess
import sys

import bpy
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else "/tmp/blender_out"
PREVIEW = "--preview" in ARGS
STILL = next((int(a.split("=")[1]) for a in ARGS if a.startswith("--still=")), None)
FONTS = os.path.join(os.path.dirname(__file__), "..", "..", "library", "fonts")

NAVY = (0.0, 0.034, 0.24)        # #0034B7 aprox lineal
BLUE = (0.033, 0.18, 1.0)        # #3474FF
GOLD = (1.0, 0.50, 0.0)          # #FFBB00 lineal
DARK = (0.0006, 0.0012, 0.006)   # #020617


def hexlin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


class Studio:
    def __init__(self, frames=72, fps=30, samples=None, res=(1080, 1920)):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        self.sc = sc
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        # BLENDER_GPU=1 → usa la placa de video si existe (OPTIX/CUDA en NVIDIA, HIP en AMD, METAL en Mac)
        if os.environ.get("BLENDER_GPU"):
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for backend in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = backend
                    prefs.get_devices()
                    gpus = [d for d in prefs.devices if d.type != "CPU"]
                    if gpus:
                        for d in prefs.devices:
                            d.use = d.type != "CPU"
                        sc.cycles.device = "GPU"
                        print("GPU:", backend, [d.name for d in gpus])
                        break
                except Exception:
                    continue
        sc.cycles.samples = samples or (10 if PREVIEW else (64 if os.environ.get("BLENDER_GPU") else 14))
        sc.cycles.adaptive_threshold = 0.04
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
        sc.cycles.max_bounces = 5
        sc.cycles.diffuse_bounces = 2
        sc.cycles.glossy_bounces = 3
        sc.cycles.transmission_bounces = 6
        sc.cycles.use_adaptive_sampling = True
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 40 if PREVIEW else (100 if os.environ.get("BLENDER_GPU") else min(62, int(os.environ.get("RES", 54))))   # se reescala a 1080x1920 con lanczos al codificar
        sc.render.use_persistent_data = True
        sc.render.fps = fps
        sc.frame_start, sc.frame_end = 1, frames
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Punchy"
        sc.render.image_settings.file_format = "PNG"
        sc.render.film_transparent = False
        sc.render.use_overwrite = False      # si se reinicia, retoma desde el último frame hecho
        sc.render.use_motion_blur = True
        sc.render.motion_blur_shutter = 0.35
        self.frames = frames
        # mundo: degradado azul profundo casi negro
        w = bpy.data.worlds.new("w")
        sc.world = w
        w.use_nodes = True
        bg = w.node_tree.nodes["Background"]
        bg.inputs[0].default_value = (*hexlin("#06134a"), 1)
        bg.inputs[1].default_value = 0.6
        self._glare()

    # ---------------- materiales
    def mat(self, name, color, metal=0.0, rough=0.4, emit=None, emit_strength=0.0, transmission=0.0, ior=1.45, alpha=1.0, coat=0.0):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (*color, 1)
        p.inputs["Metallic"].default_value = metal
        p.inputs["Roughness"].default_value = rough
        p.inputs["Transmission Weight"].default_value = transmission
        p.inputs["IOR"].default_value = ior
        p.inputs["Alpha"].default_value = alpha
        p.inputs["Coat Weight"].default_value = coat
        if emit:
            p.inputs["Emission Color"].default_value = (*emit, 1)
            p.inputs["Emission Strength"].default_value = emit_strength
        return m

    def gold(self, rough=0.16):
        return self.mat("oro", (1.0, 0.66, 0.2), metal=1.0, rough=rough)

    def glass(self):
        return self.mat("vidrio", (0.9, 0.95, 1.0), rough=0.02, transmission=1.0, ior=1.5)

    def floor(self, color="#030b2e", rough=0.18, size=60):
        bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
        f = bpy.context.object
        f.data.materials.append(self.mat("piso", hexlin(color), metal=0.0, rough=rough, coat=0.6))
        return f

    # ---------------- luces y cámara
    def area(self, loc, rot, energy, color=(1, 1, 1), size=4.0, name="luz"):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot)
        l = bpy.context.object
        l.name = name
        l.data.energy = energy
        l.data.color = color
        l.data.size = size
        return l

    def three_point(self, key=900, rim=1400, fill=180):
        self.area((4, -5, 6), (math.radians(55), 0, math.radians(38)), key, (1.0, 0.86, 0.66), 5, "key")
        self.area((-5, 4, 4), (math.radians(-60), 0, math.radians(-140)), rim, hexlin("#3474FF"), 6, "rim")
        self.area((-4, -6, 2), (math.radians(80), 0, math.radians(-35)), fill, hexlin("#6f8cff"), 8, "fill")
        self.softboxes()

    def softboxes(self):
        """Paneles emisivos invisibles a cámara: solo aparecen en los reflejos (el metal necesita algo que reflejar)."""
        import bpy as _b
        for loc, rot, sz, col, st in [((0, -14, 6), (math.radians(70), 0, 0), (16, 3), (1.0, 0.9, 0.75), 6.0),
                                      ((-9, -4, 5), (math.radians(80), 0, math.radians(-70)), (3, 10), hexlin("#3474FF"), 9.0),
                                      ((9, -4, 5), (math.radians(80), 0, math.radians(70)), (3, 10), (1.0, 0.85, 0.6), 5.0),
                                      ((0, 0, 14), (0, 0, 0), (14, 14), (0.75, 0.82, 1.0), 1.2)]:
            _b.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
            p = _b.context.object
            p.scale = (sz[0], sz[1], 1)
            m = self.mat("softbox", col, emit=col, emit_strength=st)
            p.data.materials.append(m)
            p.visible_camera = False
            p.visible_shadow = False

    def camera(self, loc, look_at, lens=50):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.object
        cam.data.lens = lens
        cam.data.dof.use_dof = True
        cam.data.dof.aperture_fstop = 2.8
        self.sc.camera = cam
        tgt = bpy.data.objects.new("cam_target", None)
        bpy.context.collection.objects.link(tgt)
        tgt.location = look_at
        c = cam.constraints.new("TRACK_TO")
        c.target = tgt
        c.track_axis = "TRACK_NEGATIVE_Z"
        c.up_axis = "UP_Y"
        cam.data.dof.focus_object = tgt
        self.cam, self.tgt = cam, tgt
        return cam

    def text(self, body, size=1.0, font="Montserrat/Montserrat-Black.ttf", extrude=0.0, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), align="CENTER"):
        bpy.ops.object.text_add(location=loc, rotation=rot)
        t = bpy.context.object
        t.data.body = body
        t.data.size = size
        t.data.extrude = extrude
        t.data.align_x = align
        t.data.align_y = "CENTER"
        fp = os.path.join(FONTS, font)
        if os.path.exists(fp):
            t.data.font = bpy.data.fonts.load(fp)
        if mat:
            t.data.materials.append(mat)
        return t

    @staticmethod
    def key(obj, path, frame, value, interp="BEZIER", ease="AUTO"):
        setattr(obj, path, value) if not isinstance(value, (tuple, list)) else setattr(obj, path, Vector(value) if len(value) == 3 else value)
        obj.keyframe_insert(data_path=path, frame=frame)
        if obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == path:
                    for kp in fc.keyframe_points:
                        if int(kp.co[0]) == frame:
                            kp.interpolation = interp
                            kp.easing = ease

    def _glare(self):
        sc = self.sc
        sc.use_nodes = True
        nt = sc.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        rl = nt.nodes.new("CompositorNodeRLayers")
        gl = nt.nodes.new("CompositorNodeGlare")
        gl.glare_type = "FOG_GLOW"
        gl.quality = "HIGH"
        gl.threshold = 0.9
        gl.mix = -0.75
        gl.size = 8
        comp = nt.nodes.new("CompositorNodeComposite")
        nt.links.new(rl.outputs["Image"], gl.inputs["Image"])
        nt.links.new(gl.outputs["Image"], comp.inputs["Image"])

    # ---------------- utilidades de escena
    def backdrop(self, y=6.0, color="#123cc8", scale=(4.3, 3.3), strength=1.0, loc=(0, -0.1)):
        """Pared con glow radial azul de marca (degradado negro→azul) detrás de la escena."""
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 4), rotation=(math.radians(90), 0, 0))
        wall = bpy.context.object; wall.scale = (40, 30, 1)
        mw = bpy.data.materials.new("pared"); mw.use_nodes = True; nt = mw.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
        grad = nt.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
        mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*hexlin("#020617"), 1); ramp.color_ramp.elements[1].color = (*hexlin(color), 1)
        ramp.color_ramp.elements[0].position = 0.05; ramp.color_ramp.elements[1].position = 0.9
        mapn.inputs["Location"].default_value = (loc[0], loc[1], 0); mapn.inputs["Scale"].default_value = (scale[0], scale[1], 1)
        nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
        nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
        em.inputs["Strength"].default_value = strength; nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        wall.data.materials.append(mw)
        return wall

    def lathe(self, name, prof, mat, seg=96, solid=0.0):
        """Sólido de revolución a partir de un perfil [(radio, z), ...]."""
        import bmesh
        me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
        bm = bmesh.new()
        verts = [bm.verts.new((r, 0, z)) for r, z in prof]
        for a, b in zip(verts[:-1], verts[1:]):
            bm.edges.new((a, b))
        bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=math.radians(360), steps=seg)
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
        bm.to_mesh(me); bm.free()
        ob.data.materials.append(mat)
        for p in ob.data.polygons:
            p.use_smooth = True
        if solid:
            m = ob.modifiers.new("solid", "SOLIDIFY"); m.thickness = solid
        return ob

    @staticmethod
    def smooth(o):
        for p in o.data.polygons:
            p.use_smooth = True
        return o

    @staticmethod
    def kf(obj, frame, **vals):
        """Keyframe rápido: kf(obj, 10, location=(..), rotation_euler=(..), scale=(..))"""
        for k, v in vals.items():
            setattr(obj, k, v)
            obj.keyframe_insert(k, frame=frame)

    def orbit(self, frames, start, end, tgt_start=None, tgt_end=None):
        self.cam.location = start; self.cam.keyframe_insert("location", frame=1)
        self.cam.location = end; self.cam.keyframe_insert("location", frame=frames)
        if tgt_start is not None:
            self.tgt.location = tgt_start; self.tgt.keyframe_insert("location", frame=1)
            self.tgt.location = tgt_end; self.tgt.keyframe_insert("location", frame=frames)

    # ---------------- render
    def render(self, name="clip"):
        sc = self.sc
        os.makedirs(OUT, exist_ok=True)
        if STILL is not None:
            sc.frame_set(STILL)
            sc.render.filepath = os.path.join(OUT, f"{name}_still_{STILL:03d}.png")
            bpy.ops.render.render(write_still=True)
            return
        sc.render.filepath = os.path.join(OUT, "f_")
        bpy.ops.render.render(animation=True)
        mp4 = os.path.join(OUT, f"{name}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(sc.render.fps), "-i", os.path.join(OUT, "f_%04d.png"),
                        "-vf", "scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", mp4], check=True)
        print("OK", mp4)
