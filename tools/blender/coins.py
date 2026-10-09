"""B-roll: una torre de monedas de oro que se desarma al “pagar todo” y quedan apenas dos monedas."""
import math
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import Studio, hexlin  # noqa: E402
import bpy  # noqa: E402

N = int(os.environ.get("FRAMES", 60))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.12)
# pared con glow azul
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 6, 4), rotation=(math.radians(90), 0, 0))
wall = bpy.context.object; wall.scale = (40, 30, 1)
mw = bpy.data.materials.new("pared"); mw.use_nodes = True; nt = mw.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
grad = nt.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*hexlin("#020617"), 1); ramp.color_ramp.elements[1].color = (*hexlin("#123cc8"), 1)
ramp.color_ramp.elements[0].position = 0.05; ramp.color_ramp.elements[1].position = 0.9
mapn.inputs["Location"].default_value = (0, -0.1, 0); mapn.inputs["Scale"].default_value = (4.5, 3.4, 1)
nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.0; nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
wall.data.materials.append(mw)
S.three_point(key=1300, rim=2400, fill=220)
gold = S.gold(0.14)

# moneda base: cilindro biselado con canto estriado (modificador de array no: usamos un cilindro de 64 lados)
R, H = 0.62, 0.11
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R, depth=H, location=(0, 0, 0))
base = bpy.context.object
bev = base.modifiers.new("bev", "BEVEL"); bev.width = 0.018; bev.segments = 3
base.data.materials.append(gold)
bpy.ops.object.shade_smooth()
base.hide_render = True; base.hide_viewport = True

random.seed(7)
COUNT = 16
coins = []
for i in range(COUNT):
    c = base.copy(); c.data = base.data; bpy.context.collection.objects.link(c)
    c.hide_render = False; c.hide_viewport = False
    jitter = (random.uniform(-0.03, 0.03), random.uniform(-0.03, 0.03))
    z = H / 2 + i * (H + 0.004)
    c.location = (jitter[0], jitter[1], z); c.rotation_euler = (0, 0, random.uniform(0, 6.28))
    coins.append((c, z, jitter))

# animación: de arriba hacia abajo se van volando (pagos); quedan 2
start, step = 6, 3.0
gone = COUNT - 2
for k in range(gone):
    c, z, j = coins[COUNT - 1 - k]
    f0 = int(start + k * step)
    side = 1 if k % 2 == 0 else -1
    c.keyframe_insert("location", frame=1); c.keyframe_insert("rotation_euler", frame=1)
    c.keyframe_insert("location", frame=f0); c.keyframe_insert("rotation_euler", frame=f0)
    c.location = (side * random.uniform(5.5, 7.5), random.uniform(-2.5, 1.5), z + random.uniform(1.5, 3.5))
    c.rotation_euler = (random.uniform(2, 5) * side, random.uniform(-2, 2), random.uniform(0, 6))
    c.keyframe_insert("location", frame=f0 + 9); c.keyframe_insert("rotation_euler", frame=f0 + 9)
    for fc in c.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "QUAD" if int(kp.co[0]) == f0 else "BEZIER"
            kp.easing = "EASE_IN"

# cámara: empieza viendo la torre completa y termina empujando sobre lo poco que queda
cam = S.camera((2.6, -7.5, 1.6), (0, 0, 1.0), lens=45)
for f, loc, tg in [(1, (2.6, -7.6, 1.9), (0, 0, 1.0)), (int(N * 0.55), (2.2, -6.6, 1.3), (0, 0, 0.7)), (N, (1.0, -3.6, 0.55), (0, 0, 0.12))]:
    cam.location = loc; cam.keyframe_insert("location", frame=f)
    S.tgt.location = tg; S.tgt.keyframe_insert("location", frame=f)
cam.data.dof.aperture_fstop = 2.2
S.render("coins")
