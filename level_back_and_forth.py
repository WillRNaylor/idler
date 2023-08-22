import time
import pyautogui

WAIT = 7.5

while True:
    time.sleep(WAIT)
    pyautogui.press('left')
    time.sleep(WAIT)
    pyautogui.press('right')
  