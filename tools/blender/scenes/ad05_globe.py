"""AD05: globo de vidrio azul con meridianos dorados y la ruta de vuelo que se dibuja entre dos países."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.backdrop(y=7, color="#1546d8", scale=(3.6, 3.0))
S.three_point(key=1000, rim=2400, fill=220)
gold = S.gold(0.15)
core = S.mat("globo", hexlin("#0a1a5c"), rough=0.15, coat=1.0)
glow = S.mat("ruta", (1.0, 0.7, 0.2), emit=(1.0, 0.62, 0.1), emit_strength=8)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.25, location=(0, 0, 2.2)); gl = bpy.context.object; gl.data.materials.append(core); S.smooth(gl)
bpy.ops.mesh.primitive_uv_sphere_add(segments=36, ring_count=18, radius=1.27, location=(0, 0, 2.2)); wf = bpy.context.object
w = wf.modifiers.new("wf", "WIREFRAME"); w.thickness = 0.005; wf.data.materials.append(gold)
for o in (gl, wf):
    S.kf(o, 1, rotation_euler=(math.radians(18), 0, 0)); S.kf(o, N, rotation_euler=(math.radians(18), 0, math.radians(10)))
# ruta: arco entre dos puntos de la superficie (interpolación esférica + elevación)
R0 = 1.25
def sph(lat, lon, r):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((r * math.cos(la) * math.sin(lo), -r * math.cos(la) * math.cos(lo), 2.2 + r * math.sin(la)))
A = sph(-10, -40, 1.0); B = sph(30, 35, 1.0)
cu = bpy.data.curves.new("arco", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.02; cu.bevel_resolution = 4
sp = cu.splines.new("NURBS"); pts = []
for i in range(13):
    t = i / 12
    d = (A - Vector((0, 0, 2.2))).slerp(B - Vector((0, 0, 2.2)), t) if hasattr(Vector, "slerp") else (A.lerp(B, t) - Vector((0, 0, 2.2)))
    d = d.normalized() * (R0 * (1.02 + 0.32 * math.sin(math.pi * t)))
    pts.append(Vector((0, 0, 2.2)) + d)
sp.points.add(len(pts) - 1)
for p, c in zip(sp.points, pts):
    p.co = (c.x, c.y, c.z, 1)
sp.order_u = 4; sp.use_endpoint_u = True
arc = bpy.data.objects.new("arco", cu); bpy.context.collection.objects.link(arc); arc.data.materials.append(glow)
cu.bevel_factor_end = 0.0; cu.keyframe_insert("bevel_factor_end", frame=6)
cu.bevel_factor_end = 1.0; cu.keyframe_insert("bevel_factor_end", frame=int(N * 0.7))
for c in (pts[0], pts[-1]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=c); d = bpy.context.object; d.data.materials.append(glow)
cam = S.camera((0, -7.2, 2.6), (0, 0, 2.3), lens=48)
S.orbit(N, (-1.2, -7.6, 3.0), (0.9, -6.4, 2.4), (0, 0, 2.3), (0, 0, 2.3))
cam.data.dof.aperture_fstop = 4
S.render("globe")
