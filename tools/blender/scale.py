"""B-roll: balanza de oro — TIEMPO vs GANANCIA. Caen monedas en el plato de la ganancia hasta equilibrar."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import Studio, hexlin  # noqa: E402
import bpy  # noqa: E402

N = int(os.environ.get("FRAMES", 60))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.12)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 6, 4), rotation=(math.radians(90), 0, 0))
wall = bpy.context.object; wall.scale = (40, 30, 1)
mw = bpy.data.materials.new("pared"); mw.use_nodes = True; nt = mw.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
grad = nt.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*hexlin("#020617"), 1); ramp.color_ramp.elements[1].color = (*hexlin("#123cc8"), 1)
ramp.color_ramp.elements[0].position = 0.05; ramp.color_ramp.elements[1].position = 0.9
mapn.inputs["Location"].default_value = (0, -0.12, 0); mapn.inputs["Scale"].default_value = (4.2, 3.2, 1)
nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.0; nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
wall.data.materials.append(mw)
S.three_point(key=1300, rim=2500, fill=240)
gold = S.gold(0.15)
dark = S.mat("acero", hexlin("#0b1640"), metal=1.0, rough=0.25)
white = S.mat("texto", (1, 1, 1), emit=(1, 1, 1), emit_strength=2.5)
goldtxt = S.mat("texto_oro", (1.0, 0.62, 0.1), emit=(1.0, 0.6, 0.08), emit_strength=3.0)


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


# pedestal y columna
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.9, depth=0.16, location=(0, 0, 0.08)); b = bpy.context.object
b.data.materials.append(gold); smooth(b); m = b.modifiers.new("bev", "BEVEL"); m.width = 0.03; m.segments = 3
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.07, depth=3.0, location=(0, 0, 1.6)); c = bpy.context.object
c.data.materials.append(gold); smooth(c)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(0, 0, 3.12)); s = bpy.context.object; s.data.materials.append(gold); smooth(s)

# brazo (pivote en la punta de la columna)
pivot = bpy.data.objects.new("pivot", None); bpy.context.collection.objects.link(pivot); pivot.location = (0, 0, 3.05)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3.05)); beam = bpy.context.object
beam.scale = (2.5, 0.08, 0.08); beam.data.materials.append(gold)
m = beam.modifiers.new("bev", "BEVEL"); m.width = 0.03; m.segments = 2
beam.parent = pivot; beam.location = (0, 0, 0)

plates = []
for side, label, mat in [(-1, "TIEMPO", white), (1, "GANANCIA", goldtxt)]:
    hang = bpy.data.objects.new(f"hang{side}", None); bpy.context.collection.objects.link(hang)
    hang.parent = pivot; hang.location = (side * 1.18, 0, 0)
    # el colgante NO rota con el brazo: lo compensamos con una restricción de rotación nula
    cr = hang.constraints.new("LIMIT_ROTATION"); cr.use_limit_x = cr.use_limit_y = cr.use_limit_z = True; cr.owner_space = "WORLD"
    from mathutils import Vector
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 2
        rim = Vector((0.44 * math.cos(a), 0.44 * math.sin(a), -1.5)); top = Vector((0, 0, 0))
        d = rim - top
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.01, depth=d.length, location=(0, 0, 0))
        ch = bpy.context.object; ch.data.materials.append(gold); ch.parent = hang
        ch.location = (top + rim) / 2
        ch.rotation_mode = "QUATERNION"; ch.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.5, depth=0.05, location=(0, 0, 0)); pl = bpy.context.object
    pl.data.materials.append(gold); smooth(pl); pl.parent = hang; pl.location = (0, 0, -1.5)
    m = pl.modifiers.new("bev", "BEVEL"); m.width = 0.02; m.segments = 2
    t = S.text(label, size=0.19, font="Montserrat/Montserrat-ExtraBold.ttf", extrude=0.01, mat=mat, loc=(0, 0, 0), rot=(math.radians(90), 0, 0))
    t.parent = hang; t.location = (0, -0.55, -1.72)
    plates.append((hang, pl))

# en TIEMPO: reloj (disco oscuro + agujas); en GANANCIA: monedas que caen
hang_l = plates[0][0]
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.27, depth=0.09, location=(0, 0, 0)); ck = bpy.context.object
ck.data.materials.append(dark); smooth(ck); ck.parent = hang_l; ck.location = (0, 0, -1.2); ck.rotation_euler = (math.radians(90), 0, 0)
for L, w, ang in [(0.18, 0.025, 0.0), (0.12, 0.035, 2.1)]:
    bpy.ops.mesh.primitive_cube_add(size=1); hd = bpy.context.object; hd.data.materials.append(gold)
    hd.parent = hang_l; hd.scale = (w, 0.02, L); hd.location = (math.sin(ang) * L / 2, -0.055, -1.2 + math.cos(ang) * L / 2); hd.rotation_euler = (0, ang, 0)
hang_r = plates[1][0]
bpy.ops.mesh.primitive_cylinder_add(vertices=72, radius=0.2, depth=0.05); base_coin = bpy.context.object
base_coin.data.materials.append(gold); smooth(base_coin); base_coin.hide_render = True
coins = []
for i in range(6):
    cc = base_coin.copy(); cc.data = base_coin.data; bpy.context.collection.objects.link(cc); cc.hide_render = False
    cc.parent = hang_r
    f_land = 10 + i * 6
    cc.location = (0.05 * ((i % 3) - 1), 0.04 * ((i % 2) * 2 - 1), 2.6); cc.keyframe_insert("location", frame=1)
    cc.keyframe_insert("location", frame=f_land - 8)
    cc.location = (0.05 * ((i % 3) - 1), 0.04 * ((i % 2) * 2 - 1), -1.45 + i * 0.052); cc.keyframe_insert("location", frame=f_land)
    for fc in cc.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "QUAD"; kp.easing = "EASE_IN"
    coins.append(cc)

# el brazo: arranca inclinado hacia el TIEMPO (pesa más) y se equilibra, termina levemente a favor de la GANANCIA
for f, ang in [(1, -14), (12, -13), (22, -8), (30, -2), (38, 3), (46, 5.5), (56, 4.6), (N, 5)]:
    pivot.rotation_euler = (0, math.radians(ang), 0); pivot.keyframe_insert("rotation_euler", frame=f)

cam = S.camera((0.0, -8.0, 2.0), (0, 0, 1.75), lens=38)
for f, loc in [(1, (-1.0, -8.4, 1.5)), (N, (0.7, -7.2, 2.2))]:
    cam.location = loc; cam.keyframe_insert("location", frame=f)
cam.data.dof.aperture_fstop = 4.0
S.render("scale")
