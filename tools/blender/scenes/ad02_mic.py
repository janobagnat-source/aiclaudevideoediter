"""AD02: micrófono de estudio dorado — “cuenta eso con tus palabras”."""
import math, os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy  # noqa
N = int(os.environ.get("FRAMES", 48))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.12)
S.backdrop(y=6, color="#1546d8", scale=(4.6, 3.4))
S.three_point(key=1200, rim=2600, fill=220)
gold = S.gold(0.15)
chrome = S.mat("cromo", (0.9, 0.92, 0.95), metal=1.0, rough=0.08)
grille = S.mat("rejilla", (0.75, 0.75, 0.78), metal=1.0, rough=0.35)
dark = S.mat("negro", (0.01, 0.012, 0.02), rough=0.3)
# cápsula: cuerpo + rejilla (esfera con modificador wireframe)
prof = [(0.0, 0.0), (0.26, 0.0), (0.3, 0.05), (0.3, 0.8), (0.27, 0.85), (0.0, 0.86)]
body = S.lathe("cuerpo", prof, gold); body.location = (0, 0, 1.25)
bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=0.33, location=(0, 0, 2.28)); g = bpy.context.object; g.scale = (1, 1, 1.25)
g.data.materials.append(grille); w = g.modifiers.new("wf", "WIREFRAME"); w.thickness = 0.012
bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=0.3, location=(0, 0, 2.28)); gi = bpy.context.object; gi.scale = (1, 1, 1.22)
gi.data.materials.append(dark); S.smooth(gi)
bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.03, location=(0, 0, 2.12)); ring = bpy.context.object; ring.data.materials.append(gold); S.smooth(ring)
# soporte y base
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.035, depth=1.25, location=(0, 0, 0.62)); st = bpy.context.object; st.data.materials.append(chrome); S.smooth(st)
base = S.lathe("base", [(0, 0), (0.7, 0), (0.72, 0.04), (0.6, 0.1), (0.08, 0.14), (0, 0.14)], chrome)
# luz “ON AIR” cálida que respira
bpy.ops.object.light_add(type="POINT", location=(0, -0.9, 2.3)); pl = bpy.context.object; pl.data.color = (1, 0.7, 0.35); pl.data.shadow_soft_size = 0.5
for f, e in [(1, 30), (N // 2, 140), (N, 90)]:
    pl.data.energy = e; pl.data.keyframe_insert("energy", frame=f)
cam = S.camera((1.4, -4.6, 2.2), (0, 0, 1.9), lens=55)
S.orbit(N, (1.8, -4.8, 1.9), (-0.9, -3.9, 2.4), (0, 0, 1.8), (0, 0, 2.0))
cam.data.dof.aperture_fstop = 2.0
S.render("mic")
