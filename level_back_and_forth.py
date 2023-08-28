import time
import pyautogui

'''
Will just toggle back and forth between two lvls, waiting
WAIT time on each lvl.

This can be useful for some quests (like getting many stacks
of some ability that caps to a low number of each lvl).
'''

WAIT = 12

while True:
    time.sleep(WAIT)
    pyautogui.press('left')
    time.sleep(WAIT)
    pyautogui.press('right')
  