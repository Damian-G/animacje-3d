import bpy
import math
import os
import random

#czyszczenie
def cleanup_scene():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras]:
        for item in block:
            block.remove(item)

#funkcja tworzaca materialy
def create_biomech_material(name, color, metal, rough, emiss=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    out = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = rough
    if emiss > 0:
        bsdf.inputs["Emission Color"].default_value = color
        bsdf.inputs["Emission Strength"].default_value = emiss
    return mat

def stworz_rosline(location=(0, 0, 0), wysokosc=1.5, liczba_lisci=24, promien_lisci=0.5, liczba_korzeni=5):
    #materialy
    mat_lodyga = bpy.data.materials.get("LodygaZ") or create_biomech_material("LodygaZ", (0.05, 0.2, 0.05, 1), 0.9, 0.5)
    mat_platek_bialy = bpy.data.materials.get("Platek_Bialy") or create_biomech_material("Platek_Bialy", (0.8, 0.8, 0.8, 1), 0.8, 0.1, emiss=1.5)
    mat_lisc_zielony = bpy.data.materials.get("Lisc_Zielony") or create_biomech_material("Lisc_Zielony", (0.05, 0.2, 0.05, 1), 0.5, 0.5)
    mat_srodek_zolty = bpy.data.materials.get("SrodekZ") or create_biomech_material("SrodekZ", (0.8, 0.5, 0.0, 1), 1.0, 0.2, emiss=0.8)

    #łodyga
    r_lod = 0.03
    bpy.ops.mesh.primitive_cylinder_add(radius=r_lod, depth=wysokosc, location=(location[0], location[1], location[2] + wysokosc/2))
    lodyga = bpy.context.active_object
    lodyga.data.materials.append(mat_lodyga)

    #srodek kwiatka
    z_gora = location[2] + wysokosc
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(location[0], location[1], z_gora))
    srodek = bpy.context.active_object
    srodek.scale.z = 0.4
    srodek.data.materials.append(mat_srodek_zolty)

    #płatki
    for i in range(liczba_lisci):
        kat = (2 * math.pi / liczba_lisci) * i
        dist = 0.06
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        p = bpy.context.active_object
        for v in p.data.vertices: v.co.x += 0.5
        p.scale = (promien_lisci, 0.06, 0.03)
        bpy.ops.object.transform_apply(scale=True)
        p.location = (location[0] + dist*math.cos(kat), location[1] + dist*math.sin(kat), z_gora)
        p.rotation_euler = (0, math.radians(-10), kat)
        p.modifiers.new(name="Taper", type='SIMPLE_DEFORM').deform_method = 'TAPER'
        p.modifiers["Taper"].factor = -0.7
        p.modifiers.new(name="Bend", type='SIMPLE_DEFORM').deform_method = 'BEND'
        p.modifiers["Bend"].angle = math.radians(45)
        # POPRAWKA: teraz używamy mat_platek_bialy
        p.data.materials.append(mat_platek_bialy)
        bpy.ops.object.shade_smooth()

    # 4. LIŚCIE ŁODYGOWE (Zielone)
    for i in range(3):
        h = location[2] + (wysokosc * (0.2 + i * 0.25))
        kat = (i * (2 * math.pi / 3)) + random.uniform(-0.1, 0.1)
        l_dlugosc = wysokosc * 0.25
        l_szerokosc = l_dlugosc * 0.4
        
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        l = bpy.context.active_object
        for v in l.data.vertices: v.co.x += 0.52 
        
        l.scale = (l_dlugosc, l_szerokosc, 0.005)
        bpy.ops.object.transform_apply(scale=True)
        l.location = (location[0], location[1], h)
        l.rotation_euler = (0, math.radians(20), kat)
        
        l.modifiers.new(name="Sub", type='SUBSURF').levels = 2
        # POPRAWKA: liście boczne dostają swój zielony materiał
        l.data.materials.append(mat_lisc_zielony)
        bpy.ops.object.shade_smooth()

    #korzenie
    for i in range(liczba_korzeni):
        kat = (2 * math.pi / liczba_korzeni) * i
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        k = bpy.context.active_object
        for v in k.data.vertices: v.co.x += 0.5
        k.scale = (0.25, 0.02, 0.01)
        bpy.ops.object.transform_apply(scale=True)
        k.location = (location[0] + 0.01*math.cos(kat), location[1] + 0.01*math.sin(kat), location[2] + 0.05)
        k.rotation_euler = (0, math.radians(20), kat)
        k.data.materials.append(mat_lodyga)

cleanup_scene()

#wywolanie
stworz_rosline((-2, 0, 0), 0.6, 16, 0.3, liczba_korzeni=3)
stworz_rosline((0, 0, 0), 1.2, 24, 0.4, liczba_korzeni=5)
stworz_rosline((2, 0, 0), 1.8, 36, 0.5, liczba_korzeni=10)

#kamera i swiatlo
bpy.ops.object.camera_add(location=(1.5, -7.5, 3.5))
cam = bpy.context.active_object
bpy.context.scene.camera = cam
cam.rotation_euler = (math.radians(72), 0, math.radians(8))

bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.context.active_object.data.energy = 4.0

#render
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = os.path.abspath("stokrotka.png")
print("ZAPISANO W: " + scene.render.filepath)

bpy.ops.render.render(write_still=True)