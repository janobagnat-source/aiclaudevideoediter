"""AD07: una puerta que se entreabre y deja pasar luz cálida — respetar su derecho a decir que no (la puerta queda abierta)."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 50))
S = Studio(frames=N)
S.sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.06
S.floor(color="#030a2a", rough=0.25)
wallm = S.mat("pared", hexlin("#071242"), rough=0.6)
doorm = S.mat("puerta", hexlin("#0d1c5e"), rough=0.35, coat=0.4)
gold = S.gold(0.15)
for x in (-3.15, 3.15):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 2.5)); w = bpy.context.object; w.scale = (5, 0.2, 5); w.data.materials.append(wallm)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 4.6)); w = bpy.context.object; w.scale = (1.3, 0.2, 0.8); w.data.materials.append(wallm)
hinge = bpy.data.objects.new("bisagra", None); bpy.context.collection.objects.link(hinge); hinge.location = (-0.62, -0.05, 0)
bpy.ops.mesh.primitive_cube_add(size=1); d = bpy.context.object; d.scale = (1.22, 0.08, 4.18); d.location = (0.61, 0, 2.1); d.data.materials.append(doorm); d.parent = hinge
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(1.1, -0.08, 2.0)); k = bpy.context.object; k.data.materials.append(gold); k.parent = hinge
bpy.ops.object.light_add(type="AREA", location=(0, 1.6, 2.2), rotation=(math.radians(90), 0, 0)); L = bpy.context.object
L.data.size = 1.2; L.data.shape = "RECTANGLE"; L.data.size_y = 4.0; L.data.color = (1.0, 0.78, 0.48)
L.data.energy = 600; L.data.keyframe_insert("energy", frame=1)
L.data.energy = 2600; L.data.keyframe_insert("energy", frame=N)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 3.0, 2.2), rotation=(math.radians(90), 0, 0)); g = bpy.context.object; g.scale = (2, 5, 1)
g.data.materials.append(S.mat("luz", (1, 0.8, 0.5), emit=(1.0, 0.75, 0.42), emit_strength=6))
S.kf(hinge, 1, rotation_euler=(0, 0, math.radians(-6))); S.kf(hinge, N, rotation_euler=(0, 0, math.radians(-48)))
cam = S.camera((0.6, -6.5, 1.7), (0, 0, 2.0), lens=40)
S.orbit(N, (0.9, -7.0, 1.6), (0.3, -5.6, 1.9), (0, 0, 2.0), (0, 0, 2.0))
cam.data.dof.aperture_fstop = 4
S.render("door")
