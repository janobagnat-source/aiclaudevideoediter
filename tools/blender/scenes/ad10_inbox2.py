"""AD10 v2: bandeja de 10 conversaciones apiladas; la luz baja por la lista y se detiene en la que quedó sin respuesta, que sale al frente con borde dorado."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.backdrop(y=6, color="#1546d8", scale=(3.4, 3.0))
S.three_point(key=500, rim=1800, fill=160)
cardm = S.mat("tarjeta", hexlin("#0d1c5e"), rough=0.3, coat=0.4)
gold = S.gold(0.2)
green = S.mat("ok", (0, 0.9, 0.35), emit=(0, 0.88, 0.32), emit_strength=5)
red = S.mat("pendiente", (1, 0.25, 0.3), emit=(1, 0.2, 0.25), emit_strength=9)
line = S.mat("linea", (0.7, 0.75, 0.9), emit=(0.6, 0.65, 0.85), emit_strength=0.5)
rimm = S.mat("borde", (1.0, 0.7, 0.2), emit=(1.0, 0.62, 0.12), emit_strength=0.0)
STOP = 6; T0, T1 = int(N * 0.42), int(N * 0.62)
Z0, DZ = 4.35, 0.36
for i in range(10):
    z = Z0 - i * DZ
    par = bpy.data.objects.new(f"card{i}", None); bpy.context.collection.objects.link(par); par.location = (0, 0, z)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); c = bpy.context.object; c.scale = (2.0, 0.06, 0.3); c.parent = par
    b = c.modifiers.new("bev", "BEVEL"); b.width = 0.06; b.segments = 4; c.data.materials.append(cardm)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-0.8, -0.05, 0)); d = bpy.context.object; d.parent = par; d.data.materials.append(red if i == STOP else green)
    for k, w in enumerate((1.0, 0.65)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.62 + w / 2, -0.05, 0.06 - k * 0.12)); l = bpy.context.object; l.parent = par; l.scale = (w, 0.01, 0.035); l.data.materials.append(line)
    if i == STOP:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.02, 0)); r = bpy.context.object; r.parent = par; r.scale = (2.08, 0.04, 0.38); r.data.materials.append(rimm)
        S.kf(par, 1, location=(0, 0, z), scale=(1, 1, 1)); S.kf(par, T0, location=(0, 0, z), scale=(1, 1, 1)); S.kf(par, T1, location=(0, -0.55, z), scale=(1.03, 1.03, 1.03)); S.kf(par, N, location=(0, -0.6, z), scale=(1.04, 1.04, 1.04))
        em = rimm.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        em.default_value = 0.0; em.keyframe_insert("default_value", frame=T0); em.default_value = 5.0; em.keyframe_insert("default_value", frame=T1)
# foco que baja por la lista y se queda en la pendiente
bpy.ops.object.light_add(type="SPOT", location=(0, -4.5, 5.5)); sp = bpy.context.object; sp.data.spot_size = math.radians(10); sp.data.spot_blend = 0.6; sp.data.color = (1, 0.82, 0.55); sp.data.energy = 700
for fr, i in [(1, 0), (T1, STOP), (N, STOP)]:
    tgt = Vector((0, 0, Z0 - i * DZ)); sp.rotation_euler = (tgt - sp.location).to_track_quat("-Z", "Y").to_euler(); sp.keyframe_insert("rotation_euler", frame=fr)
mid = Z0 - 5.2 * DZ
cam = S.camera((1.2, -7.4, mid + 0.6), (0, 0, mid), lens=42)
S.orbit(N, (1.5, -7.8, mid + 0.8), (0.8, -6.2, mid + 0.2), (0, 0, mid), (0, -0.5, Z0 - STOP * DZ + 0.3))
cam.data.dof.aperture_fstop = 3.2
S.render("inbox")
