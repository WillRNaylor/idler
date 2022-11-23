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
        self.RAGE_CHECK_WAIT = 0.2

        if self.STOP_LVL % 100 > 50:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100)
        else:
            self.SAFETY_LVL = self.STOP_LVL - (self.STOP_LVL % 100) - 50
        
        self.logger = util.init_logger('logfile_', name='idler')
        self.timer = util.init_logger('time_brakdown_', name='timer')


config = Config()

# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------


def progess(pos, config):
    '''
    '''
    t = time.time()
    safety_counter = 0
    lvl = None
    config.logger.info('Staring: progress()')
    while True:
        lvl = util.get_base_level(pos, config)
        if lvl is not None:
            if lvl >= config.SAFETY_LVL:
                safety_counter +=1
            if (lvl >= config.STOP_LVL) and (safety_counter > config.LVL_SAFETY_COUNT):
                pyautogui.press('g')
                time.sleep(config.FINAL_CLEAR_WAIT_TIME)
                config.logger.info(f'Exiting progress() with lvl: {lvl_string}   sc: {safety_counter}')
                config.timer.info(f'{time.time() - t:.4f} progress() Exiting with lvl {lvl_string}')
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
    config.logger.info(f"Switched to stack group")
    config.logger.info(f"Base lvl read to be: {util.get_base_level(pos, config)}")
    config.timer.info(f'{time.time() - t:.4f} prepare_to_stack()')


def wait_for_enrage(pos, config):
    t = time.time()
    config.logger.info('Staring: wait_for_enrage()')
    update_counter = 0
    while update_counter < 1000:
        time.sleep(config.RAGE_CHECK_WAIT)
        rage = util.check_enrage_status(pos)
        if rage:
            config.logger.info('Exiting wait_for_enrage() successfully')
            config.timer.info(f'{time.time() - t:.4f} wait_for_enrage() success')
            return
        if update_counter % 10 == 0:
            config.logger.info(f'Waiting...  uc: {update_counter}')
        update_counter += 1
    config.logger.info(f'Exiting wait_for_enrage() unsuccessfully  uc: {update_counter}')
    config.timer.info(f'{time.time() - t:.4f} wait_for_enrage() fail')


def wait_for_more_stacks(config):
    t = time.time()
    config.logger.info(f'Waitig {config.STACK_WAIT_TIME} seconds for a few more stacks.')
    time.sleep(config.STACK_WAIT_TIME)
    config.timer.info(f'{time.time() - t:.4f} wait_for_more_stacks()')


def progress_to_reset(config):
    t = time.time()
    config.logger.info('Attack!')
    pyautogui.press('g')
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.press(config.KILL_GROUP)
    config.logger.info("Switched to KILL_GROUP, and 'g'ing")
    config.timer.info(f'{time.time() - t:.4f} progress_to_reset()')


def level_reset_and_start(pos, config):
    t = time.time()
    config.logger.info("Waiting for kills and reset in level_reset_and_start()")
    time.sleep(config.RESET_WAIT)
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(config.LONG_CLICK_WAIT)
    pyautogui.click(x=pos.server_error[0], y=pos.server_error[1])
    time.sleep(config.SHORT_CLICK_WAIT)
    pyautogui.moveTo(pos.safe[0], pos.safe[1])
    config.timer.info(f'{time.time() - t:.4f} level_reset_and_start()')


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
pyautogui.moveTo(pos.safe[0], pos.safe[1])  # Put the mouse somewhere safe

print("==== Starting main loop:")

reset_counter = 0
start_time = None
time_delta = None
bph = None
while True:
    # Calculate basic data:
    if start_time is not None:
        time_delta = datetime.now() - start_time
        bph = (int(config.STOP_LVL / 5) + config.EXTRA_BOSSES) / (time_delta.total_seconds() / 3600)
        time_delta = util.round_datetime_seconds(start_time)
        bph = int(bph)
    start_time = util.round_datetime_seconds(datetime.now())

    # Write some info to file:
    config.timer.info(f'Prev run time: {time_delta},    BPH: {bph}')
    config.timer.info(f'Starting new run at: {start_time}')
    print(f'{start_time} |  delta: {time_delta}  BPH: {bph}')

    # Run program:
    progess(pos, config)
    prepare_to_stack(pos, config)
    wait_for_enrage(pos, config)
    wait_for_more_stacks(config)
    progress_to_reset(config)
    level_reset_and_start(pos, config)
    reset_counter += 1

