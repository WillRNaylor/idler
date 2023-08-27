import time
import pyautogui

WAIT = 12

while True:
    time.sleep(WAIT)
    pyautogui.press('left')
    time.sleep(WAIT)
    pyautogui.press('right')
  