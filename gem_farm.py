import time
import logging
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
        self.LEVEL1_CLEAR_WAIT = 6

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
        self.IMG_CLOSE_RANGE = 5

        if self.STOP_LVL % 100 > 50:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100)
        else:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100) - 50
        
        self.logger = util.init_logger('logfile_', name='idler', level=logging.WARNING)
        self.timer = util.init_logger('time_brakdown_', name='timer')


config = Config()

# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------


def progess(pos, config):
    '''
    '''
    t = time.time()
    lvl_ref = util.init_lvl_dict(config)
    last_pt = None
    safety_counter = 0
    lvl = None
    config.logger.info('Staring: progress()')
    while True:
        time.sleep(config.PROGRESS_WAIT)
        lvl, last_pt = util.get_base_level(pos, config, lvl_ref=lvl_ref, last_pt=last_pt)
        if lvl is not None:
            if lvl >= config.SAFETY_LVL:
                safety_counter +=1
            if (lvl >= config.STOP_LVL) and (safety_counter > config.LVL_SAFETY_COUNT):
                pyautogui.press('g')
                time.sleep(config.FINAL_CLEAR_WAIT_TIME)
                config.logger.info(f'Exiting progress() with lvl: {lvl_string}   sc: {safety_counter}')
                config.timer.info(f'progress:  {time.time() - t:5.1f}')
                return
        lvl_string = str(lvl).zfill(4) if lvl is not None else '  - '
        config.logger.info(f'lvl: {lvl_string}   sc: {safety_counter}')


def prepare_to_stack(pos, config):
    '''
    Idea is to go back a few lvls and then select a nice level to stack on.
    This also means that we have a "screen transition", which should allow for
    switching formation without error.
    '''
    t = time.time()
    config.logger.info('Staring: prepare_to_stack()')
    for _ in range(config.NUMBER_CLICK_BACK):
        config.logger.info("Clicking back")
        util.click_back(pos)
        time.sleep(config.CLICK_BACK_WAIT_TIME)
    config.logger.info(f"Clicking to specific stack lvl: {config.STACK_LVL_MOD_FIVE}")
    util.click_level(pos, config)
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.press(config.STACK_GROUP)
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.moveTo(pos.safe[0], pos.safe[1])
    config.logger.info(f"Switched to stack group")
    config.logger.info(f"Base lvl read to be: {util.get_base_level(pos, config)}")
    # config.timer.info(f'to stack:  {time.time() - t:5.1f}')


def wait_for_enrage(pos, config):
    t = time.time()
    config.logger.info('Staring: wait_for_enrage()')
    update_counter = 0
    while update_counter < 1000:
        time.sleep(config.RAGE_CHECK_WAIT)
        rage = util.check_enrage_status(pos)
        if rage:
            config.logger.info('Exiting wait_for_enrage() successfully')
            config.timer.info(f'rage wait: {time.time() - t:5.1f}')
            return
        if update_counter % 10 == 0:
            config.logger.info(f'Waiting...  uc: {update_counter}')
        update_counter += 1
    config.logger.info(f'Exiting wait_for_enrage() unsuccessfully  uc: {update_counter}')
    config.timer.info(f'rage wait: {time.time() - t:5.1f}')


def wait_for_more_stacks(config):
    t = time.time()
    config.logger.info(f'Waitig {config.STACK_WAIT_TIME} seconds for a few more stacks.')
    time.sleep(config.STACK_WAIT_TIME)
    # config.timer.info(f'more stak: {time.time() - t:5.1f}')


def progress_to_reset(config):
    t = time.time()
    config.logger.info('Attack!')
    pyautogui.press('g')
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.press(config.KILL_GROUP)
    config.logger.info("Switched to KILL_GROUP, and 'g'ing")
    # config.timer.info(f'to reset:  {time.time() - t:5.1f}')


def wait_for_reset(pos, config):
    t = time.time()
    lvl_ref = util.init_lvl_dict(config)
    last_pt = None
    safety_counter = 0
    lvl = None
    config.logger.info('Staring: wait_for_reset()')
    while safety_counter < 1000:
        time.sleep(config.PROGRESS_WAIT)
        lvl, last_pt = util.get_base_level(pos, config, lvl_ref=lvl_ref, last_pt=last_pt)
        if lvl is not None:
            if lvl == 1:
                pyautogui.press('g')
                time.sleep(config.LEVEL1_CLEAR_WAIT)
                pyautogui.press('g')
                break
            safety_counter += 1
    config.logger.info("Click away the server error messages")
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(config.LONG_CLICK_WAIT)
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.moveTo(pos.safe[0], pos.safe[1])
    t = time.time()
    config.timer.info(f'reset wai: {time.time() - t:5.1f}')


# --------------------------------------------------------------------------------
# Main program
# --------------------------------------------------------------------------------

print("==== Starting running")

pos = Locations(config.SETUP)

mouse_pos = pyautogui.position()
print(f"Initial mouse position: (x={mouse_pos[0]}, y={mouse_pos[1]})", )

# exit()

print(f'''
STOP_LVL:   {config.STOP_LVL}
NUMBER_CLICK_BACK: {config.NUMBER_CLICK_BACK}
STACK_LVL_MOD_FIVE: {config.STACK_LVL_MOD_FIVE}
FINAL_CLEAR_WAIT_TIME: {config.FINAL_CLEAR_WAIT_TIME}
STACK_WAIT_TIME: {config.STACK_WAIT_TIME}
SAFETY_LVL: {config.SAFETY_LVL}
''')

print("==== Switching to Idle Champions")
util.alt_tab()
time.sleep(config.SHORT_CLICK_WAIT)
pyautogui.moveTo(pos.safe[0], pos.safe[1])

print("==== Starting main loop:")

reset_counter = 0
start_datetime = None
start_time = time.time()
time_delta = None
bph = None
while True:
    # Calculate basic data:
    if start_datetime is not None:
        time_delta = time.time() - start_time
        bph = int((int(config.STOP_LVL / 5) + config.EXTRA_BOSSES) / (time_delta / 3600))
        time_delta = int(time_delta)
    else:
        time_delta = 0
    start_time = time.time()
    start_datetime = util.round_datetime_seconds(datetime.now())

    # Write some info to file:
    config.timer.info(f'Run stats: {time_delta},    BPH: {bph}')
    config.timer.info(f'---------- Starting new run at: {start_datetime}')
    print(f'{start_datetime} |  delta: {int(time_delta / 60)}:{str(time_delta % 60).zfill(2)}  BPH: {bph}')

    # Run program:
    progess(pos, config)
    prepare_to_stack(pos, config)
    wait_for_enrage(pos, config)
    wait_for_more_stacks(config)
    progress_to_reset(config)
    wait_for_reset(pos, config)
    reset_counter += 1

