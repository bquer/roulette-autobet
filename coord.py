import keyboard
import pyautogui
import json
import time

coordinates = {}
print("App Started - Press 'K' for save coordinates")
def on_key_event(e):
    if e.name == 'k' and e.event_type == keyboard.KEY_DOWN:
        if len(coordinates) < 37:  
            x, y = pyautogui.position()
            index = len(coordinates)
            coordinates[index] = {'X': x, 'Y': y}
            with open('coords.json', 'w') as json_file:
                json.dump(coordinates, json_file, indent=2)

            print(f"Koordinat {index} eklendi: x={x}, y={y}")
        else:
            print("37 Kordinat Yeri İşlendi Kapatılıyor...")
            keyboard.unhook_all()
            time.sleep(4)
            exit()

keyboard.hook(on_key_event)

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass
finally:
    print("Bye...")
    keyboard.unhook_all()
    time.sleep(4)
