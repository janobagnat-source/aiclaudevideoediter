"""AD07: un avión de papel quieto que por fin despega dejando una estela dorada — enviar el mensaje."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.12)
S.backdrop(y=10, color="#1546d8", scale=(3.0, 2.6))
S.three_point(key=1200, rim=2400, fill=220)
paper = S.mat("papel", (0.95, 0.95, 0.97), rough=0.6)
glow = S.mat("estela", (1.0, 0.7, 0.2), emit=(1.0, 0.62, 0.1), emit_strength=6)
me = bpy.data.meshes.new("avion")
v = [(0, 0.9, 0), (-0.5, -0.5, 0.05), (0, -0.4, 0.0), (0.5, -0.5, 0.05), (0, -0.45, -0.18)]
f = [(0, 1, 2), (0, 2, 3), (0, 2, 4)]
me.from_pydata(v, [], f); pl = bpy.data.objects.new("avion", me); bpy.context.collection.objects.link(pl); pl.data.materials.append(paper); pl.scale = (1.6, 1.6, 1.6)
sol = pl.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.01
path = [(0, 0, 0.2), (0, 0, 0.2), (0.2, 2.0, 1.0), (1.2, 5.0, 2.6), (2.6, 9.0, 4.2)]
frames = [1, 16, 28, 42, N]
for fr, p in zip(frames, path):
    pl.location = p; pl.keyframe_insert("location", frame=fr)
for fr, r in zip(frames, [(0, 0, 0), (0, 0, 0), (math.radians(14), math.radians(-6), 0), (math.radians(18), math.radians(-14), math.radians(-8)), (math.radians(20), math.radians(-18), math.radians(-14))]):
    pl.rotation_euler = r; pl.keyframe_insert("rotation_euler", frame=fr)
cu = bpy.data.curves.new("estela", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.012
sp = cu.splines.new("NURBS"); sp.points.add(len(path) - 2)
for pnt, c in zip(sp.points, path[1:]):
    pnt.co = (c[0], c[1] - 0.45, c[2] - 0.05, 1)
sp.order_u = 3; sp.use_endpoint_u = True
tr = bpy.data.objects.new("estela", cu); bpy.context.collection.objects.link(tr); tr.data.materials.append(glow)
cu.bevel_factor_end = 0.0; cu.keyframe_insert("bevel_factor_end", frame=16)
cu.bevel_factor_end = 1.0; cu.keyframe_insert("bevel_factor_end", frame=N)
cam = S.camera((1.6, -3.6, 1.0), (0, 0, 0.3), lens=38)
# la cámara persigue al avión: target pegado al avión y cámara que lo sigue con retraso
ct = S.tgt.constraints.new("COPY_LOCATION"); ct.target = pl
for fr, p in zip(frames, path):
    cam.location = (p[0] + 1.6, p[1] - 3.4 - (0.6 if fr > 16 else 0), p[2] + 0.7); cam.keyframe_insert("location", frame=fr)
cam.data.dof.aperture_fstop = 2.8
S.render("plane")
