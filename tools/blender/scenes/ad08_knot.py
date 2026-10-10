"""AD08: un hilo dorado enredado (explicación de 10 minutos) que se ordena en una línea recta (mensaje claro)."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.backdrop(y=4, color="#1546d8", scale=(4.0, 3.2))
S.three_point(key=1200, rim=2600, fill=240)
gold = S.mat("hilo", (1.0, 0.66, 0.2), metal=1.0, rough=0.18)
cu = bpy.data.curves.new("hilo", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.035; cu.bevel_resolution = 4; cu.resolution_u = 24
sp = cu.splines.new("NURBS"); M = 40; sp.points.add(M - 1); sp.order_u = 4; sp.use_endpoint_u = True
random.seed(11)
knot = []
for i in range(M):
    t = i / (M - 1) * 6 * math.pi
    knot.append((0.9 * math.sin(t) + 0.5 * math.sin(3.1 * t) + random.uniform(-0.25, 0.25),
                 0.9 * math.cos(1.7 * t) + random.uniform(-0.25, 0.25),
                 2.2 + 0.9 * math.sin(2.3 * t) + random.uniform(-0.25, 0.25)))
line = [(-2.0 + 4.0 * i / (M - 1), 0, 2.2) for i in range(M)]
for i, p in enumerate(sp.points):
    for fr, src in [(1, knot), (int(N * 0.25), knot), (int(N * 0.8), line), (N, line)]:
        p.co = (*src[i], 1); p.keyframe_insert("co", frame=fr)
ob = bpy.data.objects.new("hilo", cu); bpy.context.collection.objects.link(ob); ob.data.materials.append(gold); ob.scale = (1.35, 1.35, 1.35); ob.location = (0, 0, -0.75)
S.kf(ob, 1, rotation_euler=(0, 0, 0)); S.kf(ob, int(N * 0.8), rotation_euler=(0, 0, math.radians(40))); S.kf(ob, N, rotation_euler=(0, 0, math.radians(40)))
cam = S.camera((0, -7.0, 2.4), (0, 0, 2.2), lens=42)
S.orbit(N, (0.6, -7.4, 2.8), (0.0, -6.6, 2.3), (0, 0, 2.2), (0, 0, 2.2))
cam.data.dof.aperture_fstop = 4
S.render("knot")
