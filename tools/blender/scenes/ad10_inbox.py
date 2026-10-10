"""AD10: diez conversaciones flotando en fila; la luz las recorre y se detiene en la que quedó sin respuesta."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy; from mathutils import Vector  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.backdrop(y=10, color="#1546d8", scale=(3.0, 2.6))
S.three_point(key=900, rim=2200, fill=200)
cardm = S.mat("tarjeta", hexlin("#0d1c5e"), rough=0.2, coat=1.0, transmission=0.3)
green = S.mat("ok", (0, 0.9, 0.35), emit=(0, 0.88, 0.32), emit_strength=6)
red = S.mat("pendiente", (1, 0.25, 0.3), emit=(1, 0.2, 0.25), emit_strength=8)
line = S.mat("linea", (0.7, 0.75, 0.9), emit=(0.6, 0.65, 0.85), emit_strength=0.6)
STOP = 6
for i in range(10):
    z = 4.6 - i * 0.5; y = i * 0.55
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, z)); c = bpy.context.object; c.scale = (2.4, 0.04, 0.4)
    b = c.modifiers.new("bev", "BEVEL"); b.width = 0.08; b.segments = 4; c.data.materials.append(cardm)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(-0.95, y - 0.05, z)); d = bpy.context.object; d.data.materials.append(red if i in (STOP, 8) else green)
    for k, w in enumerate((1.2, 0.8)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.75 + w / 2, y - 0.05, z + 0.08 - k * 0.16)); l = bpy.context.object; l.scale = (w, 0.01, 0.05); l.data.materials.append(line)
# foco que recorre las tarjetas y se queda en la 7
bpy.ops.object.light_add(type="SPOT", location=(0, -3, 6)); sp = bpy.context.object; sp.data.spot_size = math.radians(14); sp.data.spot_blend = 0.5; sp.data.color = (1, 0.8, 0.5)
sp.data.energy = 1500
for fr, i in [(1, 0), (int(N * 0.6), STOP), (N, STOP)]:
    tgt = Vector((0, i * 0.55, 4.6 - i * 0.5)); sp.rotation_euler = (tgt - sp.location).to_track_quat("-Z", "Y").to_euler(); sp.keyframe_insert("rotation_euler", frame=fr)
cam = S.camera((1.6, -6.0, 4.4), (0, 2.0, 3.0), lens=38)
S.orbit(N, (2.0, -6.6, 5.0), (1.0, -3.8, 2.4), (0.55, 1.0, 3.8), (0.55, STOP * 0.55, 4.6 - STOP * 0.5))
cam.data.dof.aperture_fstop = 2.8
S.render("inbox")
