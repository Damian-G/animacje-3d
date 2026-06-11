import bpy

NAZWA_AUTA_1 = "Mclaren"
NAZWA_AUTA_2 = "CartoonCar"

PREDKOSC_AUTA_1 = 0.35
PREDKOSC_AUTA_2 = -0.45

START_FRAME = 1
END_FRAME = 150

def animuj_pojazd(nazwa_obiektu, predkosca_Y):
    auto = bpy.data.objects.get(nazwa_obiektu)
    
    if auto:
        print(f"Generuję ruch dla: {nazwa_obiektu}...")
        
        bpy.context.scene.frame_set(START_FRAME)
        BASE_Y = auto.location.y
        
        if auto.animation_data:
            auto.animation_data_clear()
            
        for frame in range(START_FRAME, END_FRAME + 1):
            auto.location.y = BASE_Y + ((frame - START_FRAME) * predkosca_Y)
            
            auto.keyframe_insert(data_path="location", index=1, frame=frame)
            
        print(f"Sukces! Ruch dla {nazwa_obiektu} gotowy.")
    else:
        print(f"BŁĄD: Nie znaleziono na scenie obiektu o nazwie '{nazwa_obiektu}'!")

animuj_pojazd(NAZWA_AUTA_1, PREDKOSC_AUTA_1)
animuj_pojazd(NAZWA_AUTA_2, PREDKOSC_AUTA_2)

bpy.context.scene.frame_set(START_FRAME)