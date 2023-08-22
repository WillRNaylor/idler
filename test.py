import os
import time
import cv2
import pyautogui

from idler import Idler
from locations import Locations

ic = Idler('fullscreen_hermes')

mouse_pos = pyautogui.position()
print(f"Initial mouse position: (x={mouse_pos[0]}, y={mouse_pos[1]})", )

# ic.alt_tab()
# time.sleep(0.5)
# print(ic.check_steam_ic_running())

# ic.alt_tab()
# ic.press_start_stop()
# ic.click_level(1)
# time.sleep(0.2)
# ic.restart_ic()

ic.alt_tab()
im = ic.get_welcome_back_button()
cv2.imwrite(os.path.join('.', f"test.png"), im)