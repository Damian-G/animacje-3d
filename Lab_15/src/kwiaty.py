import bpy
import random
import math

GĘSTOŚĆ_KWIATÓW = 360

USTAWIENIA_KWIATOW = {
    "Stokrotka": {"min_skala": 1.0, "max_skala": 2.5},
    "Mak":       {"min_skala": 1.2, "max_skala": 2.8},
    "Tulipan":   {"min_skala": 0.8, "max_skala": 2.2}
}

def stworz_material(nazwa, kolor, roughness=0.8):
    mat = bpy.data.materials.get(nazwa)
    if not mat:
        mat = bpy.data.materials.new(name=nazwa)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = kolor
            bsdf.inputs['Roughness'].default_value = roughness
    return mat

def wygładź_obiekt(obj):
    """Pomocnicza funkcja dodająca ładne wygładzenie krawędzi (Shade Smooth)"""
    if obj.type == 'MESH':
        for poly in obj.data.polygons:
            poly.use_smooth = True

def dodaj_do_kolekcji(obj, nazwa_kolekcji):
    if nazwa_kolekcji not in bpy.data.collections:
        nowa_col = bpy.data.collections.new(nazwa_kolekcji)
        bpy.context.scene.collection.children.link(nowa_col)
    kolekcja = bpy.data.collections[nazwa_kolekcji]
    if obj.name not in kolekcja.objects:
        kolekcja.objects.link(obj)
    for col in list(obj.users_collection):
        if col.name != nazwa_kolekcji:
            col.objects.unlink(obj)

def wyczysc_stare_kwiaty():
    if "07_Kwiaty" in bpy.data.collections:
        col = bpy.data.collections["07_Kwiaty"]
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

def zbuduj_baze_stokrotki():
    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.12, location=(0, 0, 0.06))
    lodyga = bpy.context.active_object
    wygładź_obiekt(lodyga)
    lodyga.data.materials.append(stworz_material("Mat_Kwiat_Lodyga", (0.08, 0.35, 0.08, 1.0)))
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(0, 0, 0.12))
    srodek = bpy.context.active_object
    srodek.scale = (1, 1, 0.6)
    wygładź_obiekt(srodek)
    srodek.data.materials.append(stworz_material("Mat_Stokrotka_Srodek", (0.9, 0.65, 0.0, 1.0)))
    
    platki = []
    ilosc_platkow = 12
    for i in range(ilosc_platkow):
        kat = math.radians(i * (360 / ilosc_platkow))
        px = math.cos(kat) * 0.022
        py = math.sin(kat) * 0.022
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(px, py, 0.12))
        platek = bpy.context.active_object
        platek.scale = (2.2, 0.6, 0.15)  # Spłaszczenie sfery w płatek
        platek.rotation_euler = (0, math.radians(10), kat)
        wygładź_obiekt(platek)
        platek.data.materials.append(stworz_material("Mat_Kwiat_Bialy", (0.95, 0.95, 0.95, 1.0)))
        platki.append(platek)
        
    lodyga.select_set(True)
    srodek.select_set(True)
    for p in platki: p.select_set(True)
    bpy.context.view_layer.objects.active = lodyga
    bpy.ops.object.join()
    
    lodyga.name = "Baza_Stokrotka"
    lodyga.hide_set(True)
    lodyga.hide_render = True
    dodaj_do_kolekcji(lodyga, "00_Ukryte_Bazy")
    return lodyga

def zbuduj_baze_maka():
    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.18, location=(0, 0, 0.09))
    lodyga = bpy.context.active_object
    wygładź_obiekt(lodyga)
    lodyga.data.materials.append(stworz_material("Mat_Kwiat_Lodyga", (0.08, 0.35, 0.08, 1.0)))
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(0, 0, 0.18))
    srodek = bpy.context.active_object
    wygładź_obiekt(srodek)
    srodek.data.materials.append(stworz_material("Mat_Mak_Srodek", (0.02, 0.01, 0.03, 1.0)))
    
    platki = []
    for i in range(5):
        kat = math.radians(i * (360 / 5))
        px = math.cos(kat) * 0.025
        py = math.sin(kat) * 0.025
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(px, py, 0.185))
        platek = bpy.context.active_object
        platek.scale = (1.1, 0.8, 0.12)
        platek.rotation_euler = (math.radians(25), 0, kat)
        wygładź_obiekt(platek)
        platek.data.materials.append(stworz_material("Mat_Mak_Czerwony", (0.8, 0.01, 0.02, 1.0)))
        platki.append(platek)
        
    lodyga.select_set(True)
    srodek.select_set(True)
    for p in platki: p.select_set(True)
    bpy.context.view_layer.objects.active = lodyga
    bpy.ops.object.join()
    
    lodyga.name = "Baza_Mak"
    lodyga.hide_set(True)
    lodyga.hide_render = True
    dodaj_do_kolekcji(lodyga, "00_Ukryte_Bazy")
    return lodyga

def zbuduj_baze_tulipana():
    """NOWOŚĆ: Generowanie bazy dla tulipana o kielichowatym kształcie"""
    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.22, location=(0, 0, 0.11))
    lodyga = bpy.context.active_object
    wygładź_obiekt(lodyga)
    lodyga.data.materials.append(stworz_material("Mat_Kwiat_Lodyga", (0.08, 0.35, 0.08, 1.0)))
    
    platki = []
    ilosc_platkow = 6
    for i in range(ilosc_platkow):
        kat = math.radians(i * (360 / ilosc_platkow))
        px = math.cos(kat) * 0.018
        py = math.sin(kat) * 0.018
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(px, py, 0.22))
        platek = bpy.context.active_object
        
        platek.scale = (0.7, 0.3, 1.4)
        
        platek.rotation_euler = (math.radians(-15), 0, kat)
        wygładź_obiekt(platek)
        
        platek.data.materials.append(stworz_material("Mat_Tulipan_Fiolet", (0.65, 0.05, 0.5, 1.0), roughness=0.6))
        platki.append(platek)
        
    lodyga.select_set(True)
    for p in platki: p.select_set(True)
    bpy.context.view_layer.objects.active = lodyga
    bpy.ops.object.join()
    
    lodyga.name = "Baza_Tulipan"
    lodyga.hide_set(True)
    lodyga.hide_render = True
    dodaj_do_kolekcji(lodyga, "00_Ukryte_Bazy")
    return lodyga

def pobierz_wymiary_pasa(nazwa_pasa):
    pas = bpy.data.objects.get(nazwa_pasa)
    if not pas: return None
    x, y, z = pas.location
    sx, sy, sz = pas.scale
    return {
        'x_min': x - sx/2, 'x_max': x + sx/2,
        'y_min': y - sy/2, 'y_max': y + sy/2,
        'z_top': z + sz/2
    }

def rozsiej_kwiaty():
    wyczysc_stare_kwiaty()
    
    stokrotka = zbuduj_baze_stokrotki()
    mak = zbuduj_baze_maka()
    tulipan = zbuduj_baze_tulipana()
    
    bazy_slownik = {
        stokrotka: "Stokrotka",
        mak: "Mak",
        tulipan: "Tulipan"
    }
    
    typy_kwiatow = list(bazy_slownik.keys())
    pasy_zieleni = ["Pas_Zieleni_Lewy", "Pas_Zieleni_Prawy"]
    
    for nazwa_pasa in pasy_zieleni:
        wymiary = pobierz_wymiary_pasa(nazwa_pasa)
        if not wymiary:
            print(f"Brak obiektu o nazwie: {nazwa_pasa}")
            continue
            
        for i in range(GĘSTOŚĆ_KWIATÓW):
            baza = random.choice(typy_kwiatow)
            klon = baza.copy()
            
            rx = random.uniform(wymiary['x_min'] + 0.1, wymiary['x_max'] - 0.1)
            ry = random.uniform(wymiary['y_min'] + 0.5, wymiary['y_max'] - 0.5)
            rz = wymiary['z_top']
            
            klon.location = (rx, ry, rz)
            
            klon.rotation_euler = (
                random.uniform(-0.15, 0.15),
                random.uniform(-0.15, 0.15),
                random.uniform(0, 2 * math.pi)
            )
            
            klucz_gatunku = bazy_slownik[baza]
            min_s = USTAWIENIA_KWIATOW[klucz_gatunku]["min_skala"]
            max_s = USTAWIENIA_KWIATOW[klucz_gatunku]["max_skala"]
            
            losowa_skala = random.uniform(min_s, max_s)
            klon.scale = (losowa_skala, losowa_skala, losowa_skala)
            
            klon.name = f"Kwiat_{klucz_gatunku}_{nazwa_pasa}_{i}"
            klon.hide_set(False)
            klon.hide_render = False
            
            dodaj_do_kolekcji(klon, "07_Kwiaty")

rozsiej_kwiaty()