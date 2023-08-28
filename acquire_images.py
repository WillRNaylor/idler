import time
import os
import numpy as np
import cv2
import pyautogui
import pytesseract
import mss

import util
from idler import Idler
from locations import Locations

'''
File to take screenshots of the game running to form the 'reference'.
This should be used to as a setup step, not in actual farming.
'''

pos = Locations('fullscreen_hermes')

# util.alt_tab()
# time.sleep(0.1)
# pyautogui.moveTo(pos.safe[0], pos.safe[1])
# time.sleep(0.1)

# # Note the 'temp' dir must exist
# counter = 0
# while True:
#     img = util.get_base_level_number_img(pos)
#     cv2.imwrite(os.path.join('img_reference', 'temp', f"{counter}.png"), img)
#     counter += 1
#     time.sleep(0.4)

# # You may want code to zfill the numbers:
# files = os.listdir(os.path.join(img_ref_path, 'base_lvls_done'))
# files.sort()
# for f in files:
#     if f[-4:] != '.png':
#         continue
#     os.rename(os.path.join(img_ref_path, 'base_lvls_done', f), os.path.join(img_ref_path, 'base_lvls_done', f[:-4].zfill(4) + '.png'))


# ==== Get a single image:
ic = Idler('windowed_hermes')
ic.alt_tab()
ic.move_mouse_to_safe()
counter = 0
while True:
    ic.save_base_level_number_img(f'img_reference/temp/{counter}')
    time.sleep(0.3)
    counter += 1
    print(counter, end=',', flush=True)