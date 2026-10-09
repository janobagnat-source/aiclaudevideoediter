"""B-roll: reloj de arena de vidrio y oro — “tu tiempo también cuenta”."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import Studio, hexlin  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

N = int(os.environ.get("FRAMES", 50))
S = Studio(frames=N)
S.sc.cycles.transmission_bounces = 8
S.floor(color="#020a26", rough=0.1)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 5, 4), rotation=(math.radians(90), 0, 0))
wall = bpy.context.object; wall.scale = (40, 30, 1)
mw = bpy.data.materials.new("pared"); mw.use_nodes = True; nt = mw.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
grad = nt.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*hexlin("#020617"), 1); ramp.color_ramp.elements[1].color = (*hexlin("#1546d8"), 1)
ramp.color_ramp.elements[0].position = 0.05; ramp.color_ramp.elements[1].position = 0.92
mapn.inputs["Location"].default_value = (0, -0.05, 0); mapn.inputs["Scale"].default_value = (5.0, 3.6, 1)
nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.1; nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
wall.data.materials.append(mw)
S.three_point(key=1200, rim=2600, fill=260)
gold = S.gold(0.15)
glass = S.glass()
sand = S.mat("arena", (0.85, 0.42, 0.08), rough=0.85, emit=(1.0, 0.45, 0.06), emit_strength=0.25)

Z0, HH = 0.32, 2.6  # base del vidrio y altura total


def lathe(name, prof, mat, seg=96):
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    verts = [bm.verts.new((r, 0, z)) for r, z in prof]
    for a, b in zip(verts[:-1], verts[1:]):
        bm.edges.new((a, b))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=math.radians(360), steps=seg)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bm.to_mesh(me); bm.free()
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


# vidrio: dos bulbos unidos por un cuello fino
prof = []
for i in range(41):
    t = i / 40
    z = Z0 + t * HH
    u = abs(t - 0.5) * 2  # 0 en el cuello, 1 en los extremos
    r = 0.06 + 0.62 * math.sin(min(1, u * 1.05) * math.pi / 2) ** 1.6 * (1 - 0.35 * max(0, u - 0.85) / 0.15)
    prof.append((r, z))
g = lathe("vidrio", prof, glass)
sol = g.modifiers.new("solid", "SOLIDIFY"); sol.thickness = 0.025
# tapas y columnas de oro
for z in (Z0 - 0.12, Z0 + HH + 0.12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.92, depth=0.18, location=(0, 0, z))
    c = bpy.context.object; c.data.materials.append(gold); bpy.ops.object.shade_smooth()
    b = c.modifiers.new("bev", "BEVEL"); b.width = 0.03; b.segments = 3
for k in range(3):
    a = k * 2 * math.pi / 3 + 0.4
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.045, depth=HH + 0.24, location=(0.82 * math.cos(a), 0.82 * math.sin(a), Z0 + HH / 2))
    p = bpy.context.object; p.data.materials.append(gold); bpy.ops.object.shade_smooth()

# arena superior (cono invertido que se vacía) e inferior (montículo que crece)
mid = Z0 + HH / 2
bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=0.05, radius2=0.5, depth=0.8, location=(0, 0, mid + 0.45))
top = bpy.context.object; top.data.materials.append(sand); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=0.56, radius2=0.02, depth=0.7, location=(0, 0, Z0 + 0.35))
bot = bpy.context.object; bot.data.materials.append(sand); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.012, depth=HH / 2 - 0.1, location=(0, 0, Z0 + HH / 4 + 0.05))
stream = bpy.context.object; stream.data.materials.append(sand)
for f, st, sb in [(1, 1.0, 0.35), (N, 0.45, 0.85)]:
    top.scale = (st, st, st); top.location = (0, 0, mid + 0.05 + 0.4 * st)
    bot.scale = (sb, sb, sb); bot.location = (0, 0, Z0 + 0.35 * sb)
    for o in (top, bot):
        o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)

# cámara: órbita lenta + push-in
cam = S.camera((2.5, -6.8, 1.9), (0, 0, mid), lens=46)
for f, loc in [(1, (3.0, -7.2, 1.5)), (N, (1.0, -5.9, 2.1))]:
    cam.location = loc; cam.keyframe_insert("location", frame=f)
cam.data.dof.aperture_fstop = 3.2
S.render("hourglass")
