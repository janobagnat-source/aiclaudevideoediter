"""AD04: etiqueta de precio premium que se balancea — “está caro”."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 48))
S = Studio(frames=N)
S.backdrop(y=4, color="#1546d8", scale=(4.0, 3.2))
S.three_point(key=1300, rim=2400, fill=240)
gold = S.gold(0.14)
card = S.mat("tarjeta", hexlin("#060b1f"), rough=0.35, coat=0.8)
pivot = bpy.data.objects.new("pivot", None); bpy.context.collection.objects.link(pivot); pivot.location = (0, 0, 3.4)
bpy.ops.mesh.primitive_cube_add(size=1); t = bpy.context.object; t.scale = (1.5, 0.06, 2.3); t.location = (0, 0, -1.65)
b = t.modifiers.new("bev", "BEVEL"); b.width = 0.18; b.segments = 6; t.data.materials.append(card); t.parent = pivot
bpy.ops.mesh.primitive_cube_add(size=1); e = bpy.context.object; e.scale = (1.56, 0.04, 2.36); e.location = (0, 0.02, -1.65)
b = e.modifiers.new("bev", "BEVEL"); b.width = 0.2; b.segments = 6; e.data.materials.append(gold); e.parent = pivot
bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.035, location=(0, -0.05, -0.75), rotation=(math.radians(90), 0, 0)); g = bpy.context.object; g.data.materials.append(gold); g.parent = pivot
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.012, depth=0.75, location=(0, 0, -0.37)); s = bpy.context.object; s.data.materials.append(gold); s.parent = pivot
tx = S.text("$1.500", size=0.42, font="Montserrat/Montserrat-Black.ttf", extrude=0.02, mat=S.mat("precio", (1.0, 0.7, 0.2), emit=(1.0, 0.62, 0.1), emit_strength=2.2), rot=(math.radians(90), 0, 0)); tx.parent = pivot; tx.location = (0, -0.08, -1.75)
l2 = S.text("PRECIO", size=0.14, font="Montserrat/Montserrat-Bold.ttf", extrude=0.005, mat=S.mat("blanco", (1, 1, 1), emit=(1, 1, 1), emit_strength=1.5), rot=(math.radians(90), 0, 0)); l2.parent = pivot; l2.location = (0, -0.08, -1.25)
for f, a in [(1, -9), (12, 7), (24, -5), (36, 3), (N, -1)]:
    pivot.rotation_euler = (0, math.radians(a), math.radians(a * 0.8)); pivot.keyframe_insert("rotation_euler", frame=f)
cam = S.camera((0.6, -6.2, 1.8), (0, 0, 1.75), lens=50)
S.orbit(N, (0.4, -6.8, 1.5), (-0.3, -5.8, 2.0), (0, 0, 1.75), (0, 0, 1.8))
cam.data.dof.aperture_fstop = 2.8
S.render("tag")
