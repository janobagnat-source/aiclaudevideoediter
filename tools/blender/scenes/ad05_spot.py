"""AD05: escenario oscuro; tres focos se encienden y revelan un trofeo dorado sobre un pedestal — “hazlo visible”."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.15
S.floor(color="#020617", rough=0.2)
S.backdrop(y=6, color="#0b2a9c", scale=(3.0, 2.6), strength=0.35)
gold = S.gold(0.1)
S.softboxes()
S.area((-4, 3, 4), (math.radians(-60), 0, math.radians(-140)), 1800, hexlin('#3474FF'), 5, 'rim')
ped = S.mat("pedestal", hexlin("#16245e"), rough=0.25, coat=0.8)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.9, depth=1.2, location=(0, 0, 0.6)); p = bpy.context.object; p.data.materials.append(ped); S.smooth(p)
b = p.modifiers.new("bev", "BEVEL"); b.width = 0.04; b.segments = 3
cup = [(0, 0), (0.42, 0), (0.42, 0.06), (0.14, 0.14), (0.08, 0.45), (0.12, 0.55), (0.45, 0.75), (0.55, 1.15), (0.5, 1.2), (0.0, 1.0)]
t = S.lathe("trofeo", cup, gold); t.location = (0, 0, 1.2)
S.kf(t, 1, rotation_euler=(0, 0, 0)); S.kf(t, N, rotation_euler=(0, 0, math.radians(40)))
for k, (x, f0) in enumerate([(-2.5, 8), (2.5, 18), (0, 28)]):
    bpy.ops.object.light_add(type="SPOT", location=(x, -2.0, 5.2)); sp = bpy.context.object
    sp.data.spot_size = math.radians(24); sp.data.spot_blend = 0.3; sp.data.color = (1, 0.86, 0.62) if k < 2 else (0.75, 0.82, 1.0)
    dirv = Vector((0, 0, 1.8)) - sp.location; sp.rotation_euler = dirv.to_track_quat("-Z", "Y").to_euler()
    sp.data.energy = 0; sp.data.keyframe_insert("energy", frame=f0)
    sp.data.energy = 7000; sp.data.keyframe_insert("energy", frame=f0 + 2)
cam = S.camera((0, -6.5, 1.9), (0, 0, 1.6), lens=45)
S.orbit(N, (0.8, -7.0, 1.6), (-0.4, -5.6, 2.0), (0, 0, 1.5), (0, 0, 1.8))
cam.data.dof.aperture_fstop = 2.8
S.render("spot")
