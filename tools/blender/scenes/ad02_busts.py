"""AD02: grilla de bustos idénticos (plantillas, IA, fórmulas); uno se enciende en oro: lo que te hace diferente."""
import math, os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.floor(color="#020a26", rough=0.16)
S.backdrop(y=9, color="#0f33b0", scale=(3.6, 3.0))
S.three_point(key=700, rim=1800, fill=160)
clay = S.mat("plantilla", (0.55, 0.6, 0.7), rough=0.55)
gold = S.gold(0.14)
glowm = S.mat("aura", (1, 0.7, 0.2), emit=(1.0, 0.62, 0.15), emit_strength=0.0)


def bust(x, y, mat):
    parts = []
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.32, location=(x, y, 1.18)); h = bpy.context.object; h.scale = (0.9, 0.95, 1.1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.13, depth=0.3, location=(x, y, 0.82)); n = bpy.context.object
    prof = [(0.0, 0.0), (0.55, 0.0), (0.58, 0.08), (0.52, 0.42), (0.36, 0.62), (0.16, 0.7), (0.0, 0.7)]
    sh = S.lathe("hombros", prof, mat, seg=48); sh.location = (x, y, 0.0); sh.scale = (1.0, 0.62, 1.0)
    for o in (h, n):
        o.data.materials.append(mat); S.smooth(o)
    return [h, n, sh]


grid = []
for r, y in enumerate([0.0, 1.6, 3.2]):
    for c in range(5):
        x = (c - 2) * 1.35 + (0.65 if r % 2 else 0)
        grid.append(((r, c), x, y))
hero = (0, 2)
heroes = []
for (rc, x, y) in grid:
    parts = bust(x, y, clay)
    if rc == hero:
        heroes = parts
# el elegido: cambia a oro (material animado vía mezcla con dos slots: duplicamos con oro y animamos visibilidad)
gparts = []
for o in heroes:
    g = o.copy(); g.data = o.data.copy(); g.data.materials.clear(); g.data.materials.append(gold)
    bpy.context.collection.objects.link(g); g.scale = o.scale * 1.002
    gparts.append(g)
T = int(N * 0.55)
for o in gparts:
    o.hide_render = True; o.keyframe_insert("hide_render", frame=1); o.keyframe_insert("hide_render", frame=T - 1)
    o.hide_render = False; o.keyframe_insert("hide_render", frame=T)
for o in heroes:
    o.hide_render = False; o.keyframe_insert("hide_render", frame=T - 1)
    o.hide_render = True; o.keyframe_insert("hide_render", frame=T)
# foco cenital que se enciende sobre el elegido
bpy.ops.object.light_add(type="SPOT", location=(0, -0.6, 5.5)); sp = bpy.context.object
sp.data.spot_size = math.radians(22); sp.data.spot_blend = 0.4; sp.data.color = (1, 0.82, 0.55)
sp.rotation_euler = (math.radians(6), 0, 0)
sp.data.energy = 0; sp.data.keyframe_insert("energy", frame=T - 2)
sp.data.energy = 3500; sp.data.keyframe_insert("energy", frame=T + 3)
cam = S.camera((0, -7.5, 2.4), (0, 1.0, 0.9), lens=45)
S.orbit(N, (-0.8, -8.2, 2.6), (0.0, -5.6, 1.7), (0, 1.2, 0.9), (0, 0.2, 1.0))
cam.data.dof.aperture_fstop = 2.0
S.render("busts")
