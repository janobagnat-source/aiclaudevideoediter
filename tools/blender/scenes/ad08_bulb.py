"""AD08: lamparita de vidrio con filamento dorado que se enciende — la prueba: ¿qué entendió?"""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 48))
S = Studio(frames=N)
S.sc.cycles.transmission_bounces = 8
S.backdrop(y=5, color="#123cc8", scale=(4.2, 3.2), strength=0.8)
S.three_point(key=800, rim=2200, fill=200)
gold = S.gold(0.15)
glass = S.glass()
bulb = []
for i in range(31):
    t = i / 30; z = 1.0 + 2.0 * t
    r = 0.32 + 0.62 * math.sin(min(1, (t * 1.25)) * math.pi * 0.62) if t < 0.95 else 0.2
    bulb.append((max(0.0, r * (1 - max(0, t - 0.8) * 4.2)), z))
bulb[-1] = (0.0, 3.0)
g = S.lathe("bulbo", bulb, glass, solid=0.012)
base = [(0, 0.35), (0.34, 0.35), (0.36, 0.45), (0.33, 0.55), (0.36, 0.65), (0.33, 0.75), (0.36, 0.85), (0.33, 1.0), (0.0, 1.0)]
S.lathe("rosca", base, gold)
fil = S.mat("filamento", (1, 0.6, 0.15), emit=(1.0, 0.55, 0.12), emit_strength=0.2)
cu = bpy.data.curves.new("fil", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.012
sp = cu.splines.new("NURBS"); pts = [(0.12 * math.cos(a * 0.6), 0.12 * math.sin(a * 0.6), 1.6 + a * 0.035) for a in range(0, 30)]
pts = [(-0.08, 0, 1.15), (-0.08, 0, 1.55)] + pts + [(0.08, 0, 1.55), (0.08, 0, 1.15)]
sp.points.add(len(pts) - 1)
for p, c in zip(sp.points, pts):
    p.co = (*c, 1)
f = bpy.data.objects.new("fil", cu); bpy.context.collection.objects.link(f); f.data.materials.append(fil)
em = fil.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
em.default_value = 0.2; em.keyframe_insert("default_value", frame=int(N * 0.35))
em.default_value = 60; em.keyframe_insert("default_value", frame=int(N * 0.45))
bpy.ops.object.light_add(type="POINT", location=(0, 0, 2.1)); pl = bpy.context.object; pl.data.color = (1, 0.72, 0.35); pl.data.shadow_soft_size = 0.3
pl.data.energy = 0; pl.data.keyframe_insert("energy", frame=int(N * 0.35))
pl.data.energy = 700; pl.data.keyframe_insert("energy", frame=int(N * 0.45))
cam = S.camera((0, -5.0, 2.0), (0, 0, 2.0), lens=50)
S.orbit(N, (-0.8, -5.4, 1.7), (0.6, -4.5, 2.2), (0, 0, 1.9), (0, 0, 2.1))
cam.data.dof.aperture_fstop = 3.2
S.render("bulb")
