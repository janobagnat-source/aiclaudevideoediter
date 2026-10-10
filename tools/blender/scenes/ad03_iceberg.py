"""AD03: iceberg en corte — arriba del agua se ve poco (seguidores), abajo está el negocio que no ves."""
import math, os, sys, random; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); from studio import Studio, hexlin; import bpy  # noqa
N = int(os.environ.get("FRAMES", 54))
S = Studio(frames=N)
S.sc.cycles.volume_step_rate = 4
S.sc.cycles.transmission_bounces = 8
S.backdrop(y=12, color="#1546d8", scale=(2.6, 2.2), strength=0.8, loc=(0, 0.1))
S.three_point(key=900, rim=2200, fill=200)
ice = S.mat("hielo", (0.82, 0.92, 1.0), rough=0.28, transmission=0.55, ior=1.31, coat=0.5)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1.0, location=(0, 0, 0)); ib = bpy.context.object
tex = bpy.data.textures.new("ruido", "VORONOI"); tex.noise_scale = 0.7
d = ib.modifiers.new("disp", "DISPLACE"); d.texture = tex; d.strength = 0.28
ib.data.materials.append(ice); bpy.ops.object.shade_flat()
ib.scale = (1.5, 1.3, 2.4); ib.location = (0, 0, -1.55)   # tope ≈ +0.85 sobre el agua, masa grande abajo
# agua: caja azul translúcida con superficie levemente ondulada
water = bpy.data.materials.new("agua"); water.use_nodes = True; nt = water.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
o = nt.nodes.new("ShaderNodeOutputMaterial"); tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (0.55, 0.68, 1.0, 1)
vol = nt.nodes.new("ShaderNodeVolumeAbsorption"); vol.inputs["Color"].default_value = (*hexlin("#2a5cff"), 1); vol.inputs["Density"].default_value = 0.18
sc = nt.nodes.new("ShaderNodeVolumeScatter"); sc.inputs["Color"].default_value = (*hexlin("#3474FF"), 1); sc.inputs["Density"].default_value = 0.02
ad = nt.nodes.new("ShaderNodeAddShader")
nt.links.new(tr.outputs[0], o.inputs["Surface"]); nt.links.new(vol.outputs[0], ad.inputs[0]); nt.links.new(sc.outputs[0], ad.inputs[1]); nt.links.new(ad.outputs[0], o.inputs["Volume"])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -4)); wb = bpy.context.object; wb.scale = (14, 8, 8); wb.data.materials.append(water)
# línea de flotación luminosa (filo)
edge = S.mat("filo", hexlin("#8fb2ff"), emit=hexlin("#8fb2ff"), emit_strength=3)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -4.0, 0.0)); ln = bpy.context.object; ln.scale = (14, 0.02, 0.02); ln.data.materials.append(edge)
# luz dorada bajo el agua que se enciende (lo que pasa dentro del negocio)
bpy.ops.object.light_add(type="POINT", location=(0, -1.6, -2.0)); pl = bpy.context.object; pl.data.color = (1, 0.7, 0.3); pl.data.shadow_soft_size = 1.5
pl.data.energy = 0; pl.data.keyframe_insert("energy", frame=int(N * 0.3))
pl.data.energy = 900; pl.data.keyframe_insert("energy", frame=int(N * 0.8))
S.kf(ib, 1, rotation_euler=(0, 0, 0)); S.kf(ib, N, rotation_euler=(0, 0, math.radians(12)))
cam = S.camera((0, -10, 0.4), (0, 0, -1.1), lens=30)
S.orbit(N, (0.4, -10.5, 0.9), (-0.2, -9.3, 0.1), (0, 0, -0.6), (0, 0, -1.4))
cam.data.dof.use_dof = False
S.render("iceberg")
