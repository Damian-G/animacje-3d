import bpy
import math

INTENSYWNOSC_DESZCZU = 35000
PREDKOSC_OPADANIA = 20.0
CHAOS_PRĘDKOSCI = 4.0
ROZMIAR_KROPLI = 0.2
CZAS_ZYCIA_KROPLI = 140
SILA_TURBULENCJI = 8.0

MOC_EMISJI_DESZCZU = 5.0       

DLUGOSC_CHMURY = 160.0          
SZEROKOSC_CHMURY = 35.0
WYSOKOSC_CHMURY = 28.0          

def wyczysc_stary_deszcz():
    do_usuniecia = ["Emiter_Deszczu", "Baza_Kropli", "Turbulencja_Powietrza"]
    for nazwa in do_usuniecia:
        obj = bpy.data.objects.get(nazwa)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

def stworz_material_deszczu():
    mat_nazwa = "Mat_Realistyczny_Deszcz"
    
    stary_mat = bpy.data.materials.get(mat_nazwa)
    if stary_mat:
        bpy.data.materials.remove(stary_mat, do_unlink=True)
        
    mat = bpy.data.materials.new(name=mat_nazwa)
    mat.use_nodes = True
    mat.diffuse_color = (0.0, 0.4, 1.0, 1.0)
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.02, 0.15, 0.8, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.0
        
        for klucz in ['Emission', 'Emission Color']:
            if klucz in bsdf.inputs:
                bsdf.inputs[klucz].default_value = (0.0, 0.3, 1.0, 1.0)
        
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = MOC_EMISJI_DESZCZU
        
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = 0.6
        elif 'Transmission' in bsdf.inputs:
            bsdf.inputs['Transmission'].default_value = 0.6
            
    return mat

def stworz_baze_kropli():
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=(0, 0, -50))
    kropla = bpy.context.active_object
    kropla.name = "Baza_Kropli"
    
    kropla.scale = (0.015, 1.7, 0.015) 
    
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.shade_smooth()
    kropla.data.materials.append(stworz_material_deszczu())
    kropla.hide_set(True)
    kropla.hide_render = True
    return kropla

def dodaj_system_deszczu(kropla_obj):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, DLUGOSC_CHMURY/2, WYSOKOSC_CHMURY))
    emiter = bpy.context.active_object
    emiter.name = "Emiter_Deszczu"
    emiter.scale = (SZEROKOSC_CHMURY, DLUGOSC_CHMURY, 1.0)
    
    emiter.show_instancer_for_render = False
    emiter.show_instancer_for_viewport = False

    mod = emiter.modifiers.new(name="System_Deszczu", type='PARTICLE_SYSTEM')
    psys = emiter.particle_systems[0]
    settings = psys.settings
    
    settings.count = INTENSYWNOSC_DESZCZU
    settings.frame_start = -50  
    settings.frame_end = 250    
    settings.lifetime = CZAS_ZYCIA_KROPLI     
    
    settings.physics_type = 'NEWTON'
    settings.normal_factor = -PREDKOSC_OPADANIA 
    settings.factor_random = CHAOS_PRĘDKOSCI  
    
    settings.damping = 0.01           
    settings.brownian_factor = 0.2   
    
    settings.particle_size = ROZMIAR_KROPLI
    settings.size_random = 0.3  
    settings.render_type = 'OBJECT'
    settings.instance_object = kropla_obj
    
    settings.use_rotations = True
    settings.rotation_mode = 'VEL'

def dodaj_turbulencje_powietrza():
    bpy.ops.object.effector_add(type='TURBULENCE', location=(0, DLUGOSC_CHMURY/2, WYSOKOSC_CHMURY/2))
    turb = bpy.context.active_object
    turb.name = "Turbulencja_Powietrza"
    turb.field.strength = SILA_TURBULENCJI
    turb.field.size = 6.0          
    turb.field.flow = 0.2          

def generuj_deszcz():
    wyczysc_stary_deszcz()
    baza = stworz_baze_kropli()
    dodaj_system_deszczu(baza)
    dodaj_turbulencje_powietrza()

generuj_deszcz()