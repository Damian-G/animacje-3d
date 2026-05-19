import bpy
import math
import os

#czysta scena i ścieżka do assetu
SCIEZKA_LAB07 = r"C:\Users\Damian\Desktop\Lab_07\roslina07.blend"
NAZWA_KOLEKCJI = "RoslinaHero"

KLATKA_START = 1
KLATKA_KONIEC = 125
FPS = 25

#funkcja czyszcząca
def wyczysc_animacje(obj):
    if obj.animation_data and obj.animation_data.action:
        obj.animation_data.action = None

#import roślinki
def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    bpy.ops.wm.append(
        filepath=sciezka_kolekcji,
        directory=os.path.join(sciezka_blend, "Collection"),
        filename=nazwa_kolekcji,
    )

#sinusoidalna animacja lisci
def animuj_lisc(obj, faza, czestosc=0.05, amplituda=0.3, klatka_start=1, klatka_koniec=125):
    wyczysc_animacje(obj)
    rotacja_bazowa_y = obj.rotation_euler[1]
    
    for klatka in range(klatka_start, klatka_koniec + 1):
        kat = rotacja_bazowa_y + amplituda * math.sin(klatka * czestosc + faza)
        obj.rotation_euler[1] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)

#pętla po liściach z różnymi fazami
def animuj_wszystkie_liscie(prefix_nazwy="lisc"):
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]
    for i, lisc in enumerate(liscie):
        faza_lisc = i * (2 * math.pi / max(len(liscie), 1))
        animuj_lisc(lisc, faza=faza_lisc)
    print(f"Zaanimowano {len(liscie)} liści.")

#animacja pąka
def animuj_pak(nazwa_obj="Sphere.001", klatka_start=30, klatka_koniec=90,
               skala_min=0.9, skala_max=1.8):
    obj = bpy.data.objects.get(nazwa_obj)
    if obj is None:
        print(f"Obiekt '{nazwa_obj}' nie istnieje. Pomijam animację pąka.")
        return

    wyczysc_animacje(obj)

    obj.scale = (skala_min, skala_min, skala_min)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    obj.keyframe_insert(data_path="scale", frame=klatka_start)

    obj.scale = (skala_max, skala_max, skala_max)
    obj.keyframe_insert(data_path="scale", frame=klatka_koniec)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)

#konfiguracja sceny i wywołanie
def ustaw_scene():
    bpy.context.scene.frame_start = KLATKA_START
    bpy.context.scene.frame_end = KLATKA_KONIEC
    bpy.context.scene.render.fps = FPS

if __name__ == "__main__":
    ustaw_scene()
    
    if NAZWA_KOLEKCJI not in bpy.data.collections:
        importuj_rosline(SCIEZKA_LAB07, NAZWA_KOLEKCJI)
    
    animuj_wszystkie_liscie(prefix_nazwy="lisc")
    animuj_pak(nazwa_obj="Sphere")
    
    print("Skrypt zakończony pomyślnie.")