"""AD06: engranajes del equipo conectados a uno central dorado (vos); al final se traba todo — el límite es tu tiempo."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 60))
S = Studio(frames=N)
S.backdrop(y=3, color="#1546d8", scale=(4.0, 3.2))
S.three_point(key=1200, rim=2600, fill=240)
gold = S.gold(0.14)
steel = S.mat("acero", hexlin("#24408f"), metal=1.0, rough=0.25)


def gear(r, teeth, mat, loc):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=0.3, location=(0, 0, 0)); g = bpy.context.object; g.data.materials.append(mat)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=r * 0.28, depth=0.4, location=(0, 0, 0)); h = bpy.context.object; h.data.materials.append(mat); h.parent = g
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        bpy.ops.mesh.primitive_cube_add(size=1, location=((r + 0.08) * math.cos(a), (r + 0.08) * math.sin(a), 0)); tt = bpy.context.object
        tt.scale = (0.2, 0.14, 0.3); tt.rotation_euler = (0, 0, a); tt.data.materials.append(mat); tt.parent = g
    g.location = loc; g.rotation_euler = (math.radians(90), 0, 0)
    return g


C = gear(1.0, 18, gold, (0, 0, 2.3))
sats = []
for k in range(5):
    a = math.radians(90 + k * 72)
    r = 0.6
    d = 1.0 + r + 0.16
    sats.append((gear(r, 11, steel, (d * math.cos(a), 0.02, 2.3 + d * math.sin(a))), r))
# giro: central lento y satélites al revés por la relación; al 75% se traba (frena + temblor)
T = int(N * 0.72)
for f in (1, T, T + 3, T + 5, N):
    ang = (min(f, T) / N) * math.radians(160)
    jitter = math.radians(1.5) if f == T + 3 else 0
    C.rotation_euler = (math.radians(90), ang + jitter, 0); C.keyframe_insert("rotation_euler", frame=f)
    for g, r in sats:
        g.rotation_euler = (math.radians(90), -ang * (1.0 / r) - jitter, 0); g.keyframe_insert("rotation_euler", frame=f)
for o in [C] + [g for g, _ in sats]:
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
cam = S.camera((0, -9.0, 2.3), (0, 0, 2.3), lens=38)
S.orbit(N, (-0.6, -9.6, 2.6), (0.4, -8.2, 2.2), (0, 0, 2.3), (0, 0, 2.3))
cam.data.dof.aperture_fstop = 4
S.render("gears")
