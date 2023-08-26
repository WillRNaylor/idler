import os
import sys
import time
import cv2
import numpy as np
from termcolor import colored
import pyautogui
import pytesseract
from PIL import Image

from idler import Idler
from locations import Locations

ic = Idler('windowed_hermes')

mouse_pos = pyautogui.position()
print(f"Initial mouse position: ({mouse_pos[0]}, {mouse_pos[1]})", )

# ic.alt_tab()
# ic.click_level(1)

# print(colored('red ', 'red') + colored('green ', 'green') + colored('yellow ', 'yellow') + colored('blue ', 'blue') + colored('magenta ', 'magenta'))
# print(colored('light_grey ', 'light_grey') + colored('dark_grey ', 'dark_grey') + colored('light_red ', 'light_red') + colored('light_yellow ', 'light_yellow') + colored('light_green ', 'light_green'))
# print(colored('light_blue ', 'light_blue') + colored('light_magenta ', 'light_magenta') + colored('light_cyan ', 'light_cyan') + colored('cyan ', 'cyan'))

# ic.alt_tab()
# ic.wait_and_stop_at_base_lvl(400)

# ic.alt_tab()
# counter = 0
# while True:
#     print(f"{counter}:  {ic.get_base_level()}")
#     time.sleep(0.2)
#     counter += 1

# ic.alt_tab()
# while True:
#     lvl = ic.get_base_level()
#     if lvl is None:
#         lvl = '.'
#     print(colored(lvl, 'red'), end='-', flush=True)
#     time.sleep(ic.progress_wait)

# while True:
#     cv2.imshow("Title", ic.lvl_ref['imgs'][280])
#     cv2.waitKey(0)
#     sys.exit()