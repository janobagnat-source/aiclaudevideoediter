"""AD10: monedas (publicidad) que caen en un embudo de vidrio y se escapan por los costados; abajo llega casi nada."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 60))
S = Studio(frames=N)
S.sc.cycles.transmission_bounces = 8
S.floor(color="#020a26", rough=0.12)
S.backdrop(y=6, color="#123cc8")
S.three_point(key=1200, rim=2600, fill=220)
glass = S.glass(); gold = S.gold(0.14)
fun = S.lathe("embudo", [(1.5, 3.4), (1.45, 3.2), (0.25, 1.6), (0.14, 1.2), (0.14, 0.8)], glass, solid=0.03); fun.location = (0, 0, 0.6)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.2, depth=0.04); base = bpy.context.object; base.data.materials.append(gold); S.smooth(base); base.hide_render = True
random.seed(5)
for i in range(26):
    c = base.copy(); c.data = base.data; bpy.context.collection.objects.link(c); c.hide_render = False
    f0 = 2 + int(i * (N - 22) / 26)
    a = random.uniform(0, 6.283); r = random.uniform(0.2, 1.1)
    start = (r * math.cos(a), r * math.sin(a), 6.5); rim = (0.8 * math.cos(a), 0.8 * math.sin(a), 3.1)
    S.kf(c, 1, location=start, rotation_euler=(random.uniform(0, 3), random.uniform(0, 3), 0))
    S.kf(c, f0, location=start)
    S.kf(c, f0 + 7, location=rim, rotation_euler=(random.uniform(2, 6), random.uniform(2, 6), 0))
    if i % 9 == 0:   # pocas llegan abajo
        S.kf(c, f0 + 14, location=(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), 0.03 + (i // 9) * 0.045), rotation_euler=(0, 0, 0))
    else:            # el resto se escapa por los costados
        out = (3.6 * math.cos(a), 3.6 * math.sin(a) - 1.0, random.uniform(0.0, 1.6))
        S.kf(c, f0 + 16, location=out, rotation_euler=(random.uniform(4, 9), random.uniform(4, 9), 0))
cam = S.camera((2.4, -9.6, 3.2), (0, 0, 2.2), lens=34)
S.orbit(N, (2.8, -10.0, 3.6), (1.2, -8.2, 2.6), (0, 0, 2.6), (0, 0, 1.8))
cam.data.dof.aperture_fstop = 4
S.render("leak")
