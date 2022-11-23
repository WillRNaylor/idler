import time
from datetime import datetime
import pyautogui

import util
from locations import Locations

'''
Basic automated Briv gem farming

You need to make three formations.
  1. A speed formation for going through the levels (with clicking killing)
  2. A kill formation, this can be your speed formation
  3. A stacking formation, probably just briv

The following formations need to be in the correct hotkey slots:
  w - kill
  e - stacking

The modron core should do the following:
  Starts with the speed formation
  It sets any speed pots you'd like to
  It resets 5, maybe 10, lvls above your STOP_LVL

Fullscreen:
  True: 1920x1080, 75% UI, fullscreen.
  False: 1080x720, 100% UI, in upper right corner

BUGS
  It will never stop on lvl 836
'''

# ======================== BASIC INPUT =======================

# Tall Tales (v):
# Stacks needed: 5822 (736) 6.6k for (756) 657/3.5k657
STOP_LVL = 641
NUMBER_CLICK_BACK = 4  # Ideally stack on X26
STACK_LVL_MOD_FIVE = 1

FINAL_CLEAR_WAIT_TIME = 2
STACK_WAIT_TIME = 4
EXTRA_BOSSES = 2

# ======================= ADVANCED INPUT =====================

VERBOSE = False
FULLSCREEN = True
# SETUP = 'windowed_hermes'
SETUP = 'fullscreen_hermes'
LVL_SAFETY_COUNT = 20
LVL_READ_MAX = 800
RES_FACTOR = 2
CLICK_BACK_WAIT_TIME = 0.3
SHORT_CLICK_WAIT = 0.1
RAGE_CHECK_WAIT = 0.2

# ==================== REQUIRED FUNCTIONS ====================


def progess():
    '''
    '''
    safety_counter = 0
    lvl = None
    while True:
        lvl = util.get_base_level(LVL_READ_MAX, FULLSCREEN, RES_FACTOR)
        if lvl is not None:
            if lvl >= SAFETY_LVL:
                safety_counter +=1
            if (lvl >= STOP_LVL) and (safety_counter > LVL_SAFETY_COUNT):
                pyautogui.press('g')
                time.sleep(FINAL_CLEAR_WAIT_TIME)
                return lvl
        if VERBOSE:
            lvl_string = str(lvl).zfill(4) if lvl is not None else '-'
            print(lvl_string, safety_counter)


def prepare_to_stack():
    '''
    Idea is to go back a few lvls and then select a nice level to stack on.
    This also means that we have a "screen transition", which should allow for
    switching formation without error.
    '''
    for _ in range(NUMBER_CLICK_BACK):
        if VERBOSE:
            print("clicking back")
        util.click_back(FULLSCREEN)
        time.sleep(CLICK_BACK_WAIT_TIME)
    if VERBOSE:
        print("clicking to specific stack lvl")
    util.click_level(STACK_LVL_MOD_FIVE, FULLSCREEN)
    time.sleep(SHORT_CLICK_WAIT)
    pyautogui.press('e')
    current_base_lvl = util.get_base_level(LVL_READ_MAX, FULLSCREEN, RES_FACTOR)
    return current_base_lvl


def wait_for_enrage():
    update_counter = 0
    while update_counter < 1000:
        time.sleep(RAGE_CHECK_WAIT)
        rage = util.check_enrage_status(FULLSCREEN, RES_FACTOR)
        if rage:
            return True
        if VERBOSE:
            if update_counter % 10 == 0:
                print(update_counter, "Waiting for enemies to enrage...")
        update_counter += 1
    return False


def wait_for_more_stacks():
    time.sleep(STACK_WAIT_TIME)


def progress_to_reset():
    pyautogui.press('g')
    time.sleep(SHORT_CLICK_WAIT)
    pyautogui.press('w')


# ======================= MAIN PROGRAM =======================

print("==== Starting running")

pos = Locations(SETUP)

m_pos = pyautogui.position()
print(f"Initial mouse position: (x={m_pos[0]}, y={m_pos[1]})", )

if STOP_LVL % 100 > 50:
    SAFETY_LVL = STOP_LVL -  (STOP_LVL % 100)
else:
    SAFETY_LVL = STOP_LVL -  (STOP_LVL % 100) - 50

print(f'''
STOP_LVL:   {STOP_LVL}
NUMBER_CLICK_BACK: {NUMBER_CLICK_BACK}
STACK_LVL_MOD_FIVE: {STACK_LVL_MOD_FIVE}
FINAL_CLEAR_WAIT_TIME: {FINAL_CLEAR_WAIT_TIME}
STACK_WAIT_TIME: {STACK_WAIT_TIME}
SAFETY_LVL: {SAFETY_LVL}
''')

print("==== Switching to Idle Champions")
util.alt_tab()
pyautogui.moveTo(pos.safe[0], pos.safe[1])  # Put the mouse somewhere safe

print("==== Starting main loop:")

reset_counter = 0
start_time = None
time_delta = None
bph = None
while True:
    if start_time is not None:
        time_delta = datetime.now() - start_time
        bph = (int(STOP_LVL / 5) + EXTRA_BOSSES) / (time_delta.total_seconds() / 3600)
    start_time = datetime.now()
    print(f'''---- Starting a new run:
Start time: {start_time}
Time delta: {time_delta}
BPH:        {bph}
Resets:     {reset_counter}
''')

    base_lvl = progess()
    if VERBOSE:
        print("---- Stopping at base lvl:", base_lvl)

    base_lvl = prepare_to_stack()
    if VERBOSE:
        print("---- Stacking at base lvl:", base_lvl)

    out = wait_for_enrage()
    if VERBOSE:
        print("---- Enemies enraged with result:", out)

    wait_for_more_stacks()

    progress_to_reset()
    if VERBOSE:
        print("---- Attack!!!")

    time.sleep(30)
    
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(0.2)
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(0.2)
    pyautogui.moveTo(pos.safe[0], pos.safe[1])
    reset_counter += 1

