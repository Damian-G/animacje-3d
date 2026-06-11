import bpy
import math

PREDKOSC_KROKOW = 0.35
AMPLITUDA_PIONOWA = 0.08
AMPLITUDA_POZIOMA = 0.09
PREDKOSC_MARSZU = -0.09

START_FRAME = 1
END_FRAME = 150

camera = bpy.data.objects.get("Camera")

if camera:
    print("Generowanie pełnego ruchu POV...")
    
    bpy.context.scene.frame_set(START_FRAME)
    BASE_X = camera.location.x
    BASE_Y = camera.location.y
    BASE_Z = camera.location.z
    
    if camera.animation_data:
        camera.animation_data_clear()

    for frame in range(START_FRAME, END_FRAME + 1):
        
        current_y = BASE_Y + ((frame - START_FRAME) * PREDKOSC_MARSZU)
        
        stomp_z = math.sin(frame * PREDKOSC_KROKOW) * AMPLITUDA_PIONOWA
        sway_x = math.cos(frame * PREDKOSC_KROKOW * 0.5) * AMPLITUDA_POZIOMA
        
        camera.location.x = BASE_X + sway_x
        camera.location.y = current_y
        camera.location.z = BASE_Z + stomp_z
        
        camera.keyframe_insert(data_path="location", index=0, frame=frame)
        camera.keyframe_insert(data_path="location", index=1, frame=frame)
        camera.keyframe_insert(data_path="location", index=2, frame=frame)
        
    bpy.context.scene.frame_set(START_FRAME)
    print("Animacja zaprogramowana.")
else:
    print("Programowanie animacji nieudane.")