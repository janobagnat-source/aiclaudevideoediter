"""AD09: torre de bloques; caen más y más bloques encima (decir que sí a todo) hasta que se inclina peligrosamente."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 60))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.12)
S.backdrop(y=6, color="#123cc8")
S.three_point(key=1200, rim=2600, fill=220)
gold = S.gold(0.16)
blue = S.mat("bloque", hexlin("#1f4fe8"), rough=0.2, coat=0.7)
tower = bpy.data.objects.new("torre", None); bpy.context.collection.objects.link(tower)
L = 0.36; blocks = []
for lv in range(14):
    for k in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1); b = bpy.context.object
        if lv % 2 == 0:
            b.scale = (1.08, 0.34, L); b.location = (0, (k - 1) * 0.36, L / 2 + lv * (L + 0.01))
        else:
            b.scale = (0.34, 1.08, L); b.location = ((k - 1) * 0.36, 0, L / 2 + lv * (L + 0.01))
        bv = b.modifiers.new("bev", "BEVEL"); bv.width = 0.02; bv.segments = 2
        b.data.materials.append(gold if lv >= 8 else blue); b.parent = tower
        if lv >= 8:  # estos llegan cayendo desde arriba
            f0 = 4 + (lv - 8) * 7 + k * 2
            z = b.location.z
            b.location.z = z + 6; b.keyframe_insert("location", frame=1); b.keyframe_insert("location", frame=f0)
            b.location.z = z; b.keyframe_insert("location", frame=f0 + 6)
for f, a in [(1, 0), (40, 0), (46, 2.5), (52, -1.5), (N, 6.5)]:
    tower.rotation_euler = (math.radians(a * 0.4), math.radians(a), 0); tower.keyframe_insert("rotation_euler", frame=f)
cam = S.camera((3.0, -8.4, 3.0), (0, 0, 2.6), lens=34)
S.orbit(N, (3.8, -9.0, 2.4), (2.4, -7.6, 3.4), (0, 0, 2.4), (0, 0, 3.0))
cam.data.dof.aperture_fstop = 4
S.render("tower")
