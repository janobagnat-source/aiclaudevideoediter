"""AD03: embudo de vidrio lleno de esferas azules (comunidad) del que salen apenas dos monedas (ventas)."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.sc.cycles.transmission_bounces = 8
S.floor(color="#020a26", rough=0.12)
S.backdrop(y=6, color="#123cc8")
S.three_point(key=1100, rim=2500, fill=220)
glass = S.glass(); gold = S.gold(0.14)
blue = S.mat("seguidor", hexlin("#1f55ff"), rough=0.2, metal=0.3, emit=hexlin("#3474FF"), emit_strength=0.25)
prof = [(1.5, 3.4), (1.45, 3.2), (0.25, 1.6), (0.12, 1.2), (0.12, 0.8)]
fun = S.lathe("embudo", prof, glass, solid=0.03); fun.location = (0, 0, 0.6)
random.seed(3)
for i in range(170):
    r = random.uniform(0, 1.2); a = random.uniform(0, 6.283); z = random.uniform(2.6, 4.0)
    rr = min(r, 0.25 + (z - 2.2) * 0.9)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.085, location=(rr * math.cos(a), rr * math.sin(a), z))
    s = bpy.context.object; s.data.materials.append(blue); S.smooth(s)
    # las esferas “hierven” un poco
    for f in (1, N):
        s.location.z = z + (0.06 if f == N else 0) * random.uniform(-1, 1); s.keyframe_insert("location", frame=f)
# dos monedas que caen por la boca
for k, f0 in enumerate((int(N * 0.35), int(N * 0.62))):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.24, depth=0.05, location=(0, 0, 1.3)); c = bpy.context.object
    c.data.materials.append(gold); S.smooth(c)
    S.kf(c, 1, location=(0, 0, 1.4), rotation_euler=(1.4, 0, 0))
    S.kf(c, f0, location=(0, 0, 1.4), rotation_euler=(1.4, 0, 0))
    S.kf(c, f0 + 10, location=(0.15 * (k * 2 - 1), 0, 0.03 + k * 0.045), rotation_euler=(0, 0, 0))
cam = S.camera((2.2, -9.0, 2.6), (0, 0, 2.0), lens=36)
S.orbit(N, (2.4, -9.6, 3.0), (1.0, -7.4, 1.4), (0, 0, 2.3), (0, 0, 0.9))
cam.data.dof.aperture_fstop = 3.5
S.render("funnel")
