"""B-roll: barras doradas de ventas que crecen en un estudio azul oscuro (hook “vender más”)."""
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import Studio, hexlin  # noqa: E402

N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.floor()
# pared de fondo con glow azul de marca (degradado negro→azul, “túnel de luz”)
import bpy as _b
_b.ops.mesh.primitive_plane_add(size=1, location=(0, 7, 4), rotation=(math.radians(90), 0, 0))
wall = _b.context.object; wall.scale = (40, 30, 1)
mw = _b.data.materials.new("pared"); mw.use_nodes = True; nt = mw.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
grad = nt.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*hexlin("#020617"), 1); ramp.color_ramp.elements[1].color = (*hexlin("#1c4fe0"), 1)
ramp.color_ramp.elements[1].position = 0.9; ramp.color_ramp.elements[0].position = 0.05
mapn.inputs["Location"].default_value = (0, -0.15, 0); mapn.inputs["Scale"].default_value = (4.0, 3.2, 1)
nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.1; nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
wall.data.materials.append(mw)
S.three_point(key=1100, rim=2200, fill=200)
gold = S.gold(0.2)
glow = S.mat("filo", hexlin("#3474FF"), emit=hexlin("#3474FF"), emit_strength=6)
heights = [1.0, 1.6, 2.3, 3.2, 4.4]
import bpy  # noqa: E402
for i, h in enumerate(heights):
    x = (i - 2) * 0.95
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0))
    b = bpy.context.object
    b.scale = (0.62, 0.62, 0.001)
    bev = b.modifiers.new("bev", "BEVEL"); bev.width = 0.03; bev.segments = 3
    b.data.materials.append(gold)
    f0 = 4 + i * 5
    for f, sz in [(1, 0.001), (f0, 0.001), (f0 + 16, h * 1.06), (f0 + 22, h)]:
        b.scale = (0.62, 0.62, sz); b.location = (x, 0, sz / 2)
        b.keyframe_insert("scale", frame=f); b.keyframe_insert("location", frame=f)
    # línea de luz azul en la base
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.005))
    e = bpy.context.object; e.scale = (0.66, 0.66, 0.01); e.data.materials.append(glow)
# flecha de tendencia (tubo emisivo dorado claro)
cam = S.camera((3.5, -12, 2.2), (0, 0, 2.0), lens=40)
for f, loc in [(1, (4.2, -13.0, 1.4)), (N, (1.6, -11.0, 3.2))]:
    cam.location = loc; cam.keyframe_insert("location", frame=f)
S.tgt.location = (0, 0, 1.6); S.tgt.keyframe_insert("location", frame=1)
S.tgt.location = (0.3, 0, 2.4); S.tgt.keyframe_insert("location", frame=N)
S.render("bars")
