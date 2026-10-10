"""AD09: una lapicera dorada firma un acuerdo con condiciones claras — dejarlo por escrito."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.2)
S.backdrop(y=6, color="#123cc8", strength=0.9)
S.three_point(key=1200, rim=2200, fill=260)
gold = S.gold(0.12); paper = S.mat("papel", (0.95, 0.94, 0.9), rough=0.7)
ink = S.mat("tinta", hexlin("#0a1a5c"), rough=0.4); lines = S.mat("lineas", hexlin("#9aa3b8"), rough=0.6)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.01)); sh = bpy.context.object; sh.scale = (2.1, 2.9, 0.01); sh.data.materials.append(paper)
for i in range(9):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.1 if i % 3 else -0.3, 1.1 - i * 0.24, 0.022)); l = bpy.context.object
    l.scale = (1.4 if i % 3 else 1.0, 0.025, 0.002); l.data.materials.append(lines)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.25, -1.05, 0.022)); l = bpy.context.object; l.scale = (1.2, 0.012, 0.002); l.data.materials.append(ink)
# firma: curva que se dibuja
cu = bpy.data.curves.new("firma", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.01
sp = cu.splines.new("NURBS"); pts = []
for i in range(24):
    t = i / 23
    pts.append((-0.3 + 1.1 * t, -0.95 + 0.12 * math.sin(t * 9) + 0.05 * math.sin(t * 23), 0.03))
sp.points.add(len(pts) - 1)
for p, c in zip(sp.points, pts):
    p.co = (*c, 1)
sp.order_u = 3; sp.use_endpoint_u = True
sg = bpy.data.objects.new("firma", cu); bpy.context.collection.objects.link(sg); sg.data.materials.append(ink)
cu.bevel_factor_end = 0.0; cu.keyframe_insert("bevel_factor_end", frame=12)
cu.bevel_factor_end = 1.0; cu.keyframe_insert("bevel_factor_end", frame=40)
pen = S.lathe("lapicera", [(0, 0), (0.02, 0.0), (0.05, 0.12), (0.075, 0.2), (0.08, 1.5), (0.06, 1.6), (0, 1.62)], gold, seg=48)
tip = bpy.data.objects.new("punta", None); bpy.context.collection.objects.link(tip)
pen.parent = tip; pen.rotation_euler = (math.radians(-35), math.radians(18), 0)
for fr, i in [(1, 0), (12, 0), (40, 23), (N, 23)]:
    x, y, z = pts[i]; tip.location = (x, y, z + (0.5 if fr == 1 else 0.0)); tip.keyframe_insert("location", frame=fr)
cam = S.camera((1.6, -3.6, 2.6), (0.2, -0.6, 0.0), lens=42)
S.orbit(N, (1.8, -4.0, 3.0), (0.9, -3.0, 2.2), (0, -0.4, 0), (0.3, -0.9, 0))
cam.data.dof.aperture_fstop = 2.4
S.render("pen")
