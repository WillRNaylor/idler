import time
import os
import numpy as np
import cv2
import pyautogui
import pytesseract
import mss

import util
from locations import Locations


# --------------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------------

class Config:
    def __init__(self):

        # ======================== BASIC INPUT =======================
        # Tall Tales (v):
        # Stacks needed: 5822 (736) 6.6k for (756) 657/3.5k657
        self.STOP_LVL = 641
        self.NUMBER_CLICK_BACK = 4  # Ideally stack on X21 / X26
        self.STACK_LVL_MOD_FIVE = 1

        self.FINAL_CLEAR_WAIT_TIME = 2
        self.STACK_WAIT_TIME = 4
        self.EXTRA_BOSSES = 2
        self.RESET_WAIT = 30

        # ======================= ADVANCED INPUT =====================
        self.VERBOSE = True
        self.STACK_GROUP = 'e'
        self.KILL_GROUP = 'w'
        self.FULLSCREEN = True
        # self.SETUP = 'windowed_hermes'
        self.SETUP = 'fullscreen_hermes'
        self.LVL_SAFETY_COUNT = 20
        self.LVL_READ_MAX = 800
        self.RES_FACTOR = 2
        self.CLICK_BACK_WAIT_TIME = 0.3
        self.SHORT_CLICK_WAIT = 0.1
        self.LONG_CLICK_WAIT = 0.3
        self.PROGRESS_WAIT = 0.05
        self.RAGE_CHECK_WAIT = 0.2
        self.IMG_REF_PATH = 'img_reference'


        if self.STOP_LVL % 100 > 50:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100)
        else:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100) - 50
        
        self.logger = util.init_logger('logfile_', name='idler')
        self.timer = util.init_logger('time_brakdown_', name='timer')

config = Config()
pos = Locations('fullscreen_hermes')


util.alt_tab()
time.sleep(0.1)
pyautogui.moveTo(pos.safe[0], pos.safe[1])

# --------------------------------------- TESTING THE IMG COMPARE FOR BASE LVLS:

lvl_ref = util.init_lvl_dict(config)
# img = util.get_base_level_number_img(pos)
# print('pytess:', pytesseract.image_to_string(img))

t = time.time()
lvl, last = util.get_base_level(pos, config, lvl_ref=lvl_ref, last_pt=0)
print(time.time() - t, lvl, last)

# i = 288
# print(lvl_ref['lvls'][i])
# cv2.imshow("OpenCV/Numpy", lvl_ref['imgs'][i])
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

# print(type(img))
# print(img.shape)
# cv2.imshow("OpenCV/Numpy", img)
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

# img = util.get_base_level_number_img(pos)
# print(type(img))
# print(img.shape)
# print(img[:, :, 0])
# print(img[:, :, 1])
# print(img[:, :, 2])
# print(img[:, :, 3])

# --------------------------------------- TESTING THE MSS MODULE:

# with mss.mss() as sct:
#     # Part of the screen to capture
#     monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

#     while "Screen capturing":
#         last_time = time.time()

#         # Get raw pixels from the screen, save it to a Numpy array
#         img = numpy.array(sct.grab(monitor))

#         # Display the picture
#         cv2.imshow("OpenCV/Numpy normal", img)

#         # Display the picture in grayscale
#         # cv2.imshow('OpenCV/Numpy grayscale',
#         #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

#         print(f"fps: {1 / (time.time() - last_time)}")

#         # Press "q" to quit
#         if cv2.waitKey(25) & 0xFF == ord("q"):
#             cv2.destroyAllWindows()
#             break


# util.alt_tab()
# time.sleep(0.1)
# pyautogui.moveTo(pos.safe[0], pos.safe[1])

# t = time.time()
# lvl = util.get_base_level(pos, config)
# print(lvl, time.time() - t)


# def get_base_level_number_img(pos):
#     '''
#     Gets the image from the upper right of the base level number
#     '''
#     with mss.mss() as sct:
#         return np.array(sct.grab(pos))

# pos = {"top": 171, "left": 1222, "width": 30, "height": 16}
# img = get_base_level_number_img(pos)
# cv2.imshow("OpenCV/Numpy", img)
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 
# print(pytesseract.image_to_string(img))

# while True:
#     # pos = {"top": 169, "left": 1222, "width": 30, "height": 21}
#     pos = {"top": 171, "left": 1220, "width": 34, "height": 16}
#     img = get_base_level_number_img(pos)
#     cv2.imshow("OpenCV/Numpy", img)
#     cv2.waitKey(0) 
#     cv2.destroyAllWindows() 
