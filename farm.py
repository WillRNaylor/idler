import time
import pyautogui

import util
from idler import Idler

'''
Automated Briv gem farming

You need to make two formations.
  1. [on q] A (ideally high DPS) speed formation
  2. [on e] A briv stacking formation, probably just briv

The modron core should do the following:
  Starts with the speed formation
  It sets any speed + firebreath pots you'd like to
  It resets at any high lvl, well over 500 ish.

Fullscreen:
  True: 1920x1080, 75% UI, fullscreen.
  False: 1080x720, 100% UI, in upper right corner

Known bugs:
  It will never stop on lvl 836

Run plan:
  - This is stated after the a run starts, but before the briv stack lvl.
  - It waits looking for lvls to go over the stacking lvl.
  - At the first lvl over 500 it will go to lvl 501 and stop and stack briv.
    Waiting config.FINAL_CLEAR_WAIT_TIME more than the 100 monster enrage timer
    (so a larger number is needed for more a larger reset lvl).
  - It then restarts progress with your team on 'q'. This is done by going back
    to lvl 1, pressing q, then g.
  - It then waits to find a reset + lvls under 200. It will then go back to loop
    of waiting for the first lvl over 500.

'''

# --------------------------------------------------------------------------------
# Main program
# --------------------------------------------------------------------------------

print("==== Starting running")

# Init the idler class:
ic = Idler('fullscreen_hermes')

print("==== Switching to Idle Champions")
ic.alt_tab()
ic.move_mouse_to_safe()

print("==== Starting main loop:")
reset_counter = 0
while True:
    # Run program:
    t = time.time()
    print('1', end='')
    ic.wait_and_stop_at_base_lvl(460)
    ic.click_level(1)
    ic.select_group('e')
    time.sleep(0.2)
    ic.restart_ic()
    time.sleep(0.1)
    print('s', end='')
    ic.swap_to_group_and_start_progress('q')
    print('2 ', end='')
    ic.wait_for_reset()
    reset_counter += 1
    print(f"Counter: {str(reset_counter).zfill(4)}  | Run time: {time.time() - t}")

