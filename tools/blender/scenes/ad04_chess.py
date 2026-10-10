"""AD04: el rey dorado se mueve con decisión sobre el tablero — “una decisión de negocio, no por miedo”."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.backdrop(y=8, color="#0f33b0", scale=(3.4, 2.8))
S.three_point(key=1200, rim=2600, fill=200)
gold = S.gold(0.12)
dk = S.mat("casilla_osc", hexlin("#030817"), rough=0.12, coat=1.0)
lt = S.mat("casilla_cla", hexlin("#1a2c6b"), rough=0.12, coat=1.0)
pawnm = S.mat("peon", hexlin("#3474FF"), rough=0.05, transmission=0.9, ior=1.45)
for i in range(8):
    for j in range(8):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i - 3.5, j - 3.5, -0.05)); c = bpy.context.object; c.scale = (1, 1, 0.1)
        c.data.materials.append(dk if (i + j) % 2 else lt)
king = [(0, 0), (0.42, 0), (0.44, 0.08), (0.36, 0.16), (0.3, 0.2), (0.22, 0.5), (0.16, 1.1), (0.26, 1.2), (0.2, 1.28), (0.24, 1.5), (0.12, 1.62), (0, 1.62)]
pawn = [(0, 0), (0.34, 0), (0.36, 0.07), (0.28, 0.14), (0.15, 0.4), (0.12, 0.55), (0.2, 0.6), (0.12, 0.66), (0.17, 0.82), (0.1, 0.95), (0, 0.97)]
k = S.lathe("rey", king, gold)
bpy.ops.mesh.primitive_cube_add(size=1); cr = bpy.context.object; cr.scale = (0.06, 0.06, 0.3); cr.location = (0, 0, 1.78); cr.data.materials.append(gold); cr.parent = k
bpy.ops.mesh.primitive_cube_add(size=1); cr2 = bpy.context.object; cr2.scale = (0.22, 0.06, 0.06); cr2.location = (0, 0, 1.8); cr2.data.materials.append(gold); cr2.parent = k
for (x, y) in [(-2.5, 1.5), (-1.5, 2.5), (1.5, 2.5), (2.5, 0.5), (-0.5, 3.5), (0.5, -1.5)]:
    p = S.lathe("peon", pawn, pawnm); p.location = (x, y, 0)
S.kf(k, 1, location=(-0.5, -0.5, 0)); S.kf(k, 14, location=(-0.5, -0.5, 0))
S.kf(k, 26, location=(0.0, 0.0, 0.9)); S.kf(k, 38, location=(0.5, 0.5, 0.0)); S.kf(k, N, location=(0.5, 0.5, 0.0))
cam = S.camera((3.5, -6.5, 2.4), (0.2, 0.2, 0.8), lens=42)
S.orbit(N, (4.2, -6.8, 2.0), (1.8, -5.6, 1.4), (0, 0, 0.8), (0.5, 0.5, 0.9))
cam.data.dof.aperture_fstop = 2.2
S.render("chess")
