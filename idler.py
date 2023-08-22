import os
import time
import logging
import datetime
import cv2
import numpy as np
import mss
import pyautogui
import pytesseract

from locations import Locations

class Idler:
    def __init__(self, setup):
        # ==== Basic
        # ===== Advanced
        self.short_click_wait = 0.1
        self.long_click_wait = 0.4
        self.progress_wait = 0.02
        self.image_ref_path = 'img_reference'
        self.lvl_match_tollerance = 5
        self.alt_tab_wait = 0.1
        self.alt_tab_end_wait = 0.1
        # ==== Internal
        self.pos = Locations(setup)
        self.lvl_ref = None
        self.last_pt = None
        self.init_logger('logfile_', name='idler', level=logging.INFO)
    
    def init_logger(self, logfile, name='idler', level=logging.INFO):
        '''
        Define the logger object for logging.
        Parameters
        ----------
        logfile : str
            Full path of the output log file.
        name : str
            Name of the logger, used by the logging library.
        Returns
        -------
            logger."logging-object"
        '''
        logger = logging.getLogger(name)
        logger.setLevel(level)
        fh = logging.FileHandler(os.path.join(
            './logs', logfile + datetime.datetime.now().strftime('%Y%m%d')), 'a+')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)
        self.logger = logger

    
    def alt_tab(self):
        '''
        Alt tabs between window and previous.
        '''
        pyautogui.keyDown('command')
        time.sleep(self.alt_tab_wait)
        pyautogui.press('tab')
        time.sleep(self.alt_tab_wait)
        pyautogui.keyUp('command')
        time.sleep(self.alt_tab_end_wait)

    def init_lvl_dict(self):
        '''
        Makes a dictionary of all of the images of the base numbers, a
        numeric value for their number, and a transition image.

        Used for the search of getting the base lvl (i.e. the level mod 5 + 1).
        '''
        # Load the transition image:
        transition = cv2.imread(os.path.join(self.image_ref_path, 'transition.png'))
        # Load images:
        lvls = []
        imgs = []
        # First the undone levels:
        files = os.listdir(os.path.join(self.image_ref_path, 'base_lvls'))
        files.sort()
        for f in files:
            if f[-4:] != '.png':
                continue
            lvls.append(int(f[:-4]))
            imgs.append(cv2.imread(os.path.join(self.image_ref_path, 'base_lvls', f)))
        # Now the completed levels:
        files = os.listdir(os.path.join(self.image_ref_path, 'base_lvls_done'))
        files.sort()
        for f in files:
            if f[-4:] != '.png':
                continue
            lvls.append(int(f[:-4]))
            imgs.append(cv2.imread(os.path.join(self.image_ref_path, 'base_lvls_done', f)))        
        self.lvl_ref = {'lvls': lvls, 'imgs': imgs, 'transition': transition}


    def get_base_level_number_img(self):
        '''
        Gets the image from the upper right of the base level number
        '''
        with mss.mss() as sct:
            return np.array(sct.grab(self.pos.base_level_number))[:, :, :3]


    def get_base_level(self):
        '''
        Returns lvl, being the found base lvl
        lvl being None means it didn't find one (quite common)
        Will start search from self.last_pt being the previously found lvl location in self.lvl_ref
        '''
        if self.lvl_ref is None:
            self.init_lvl_dict()
        if self.last_pt is None:
            self.last_pt = 0
        # Grab the base lvl image
        img = self.get_base_level_number_img()
        # First, check if we are in a transition:
        if np.allclose(img, self.lvl_ref['transition'], atol=self.lvl_match_tollerance):
            return None
        # Find lvl number
        m = len(self.lvl_ref['lvls'])
        counter = 0
        while counter < m:
            pt = (self.last_lvl + counter) % m
            if np.allclose(img, self.lvl_ref['imgs'][pt], atol=self.lvl_match_tollerance):
                self.last_pt = pt
                return (self.lvl_ref['lvls'][pt])
            counter += 1
        self.last_pt = None
        return None
    
    def get_enrage_img(self):
        '''
        Gets the image from where the enrage stacks text comes up
        '''
        with mss.mss() as sct:
            return np.array(sct.grab(self.pos.enrage_box))

    def check_enrage_status(self):
        im = self.get_enrage_img(self.pos)
        text = pytesseract.image_to_string(im)
        if isinstance(text, str):
            if 'pow' in text.lower():
                return True
            elif 'uo:' in text.lower():
                return True
            elif 'up:' in text.lower():
                return True
        else:
            return False

    def wait(self, wait_time):
        t = time.time()
        self.logger.info(f'Waitig {wait_time}.')
        time.sleep(wait_time)

    def select_group(self, group):
        pyautogui.press(group)

    def move_mouse_to_safe(self):
        pyautogui.moveTo(self.pos.safe[0], self.pos.safe[1])

    def click_server_error_msg(self):
        pyautogui.click(x=self.pos.server_error[0], y=self.pos.server_error[1])

    def click_back(self):
        pyautogui.click(x=self.pos.back[0], y=self.pos.back[1])

    def click_level(self, lvl):
        if lvl == 1:
            pyautogui.click(x=self.pos.level1[0], y=self.pos.level1[1])
        elif lvl == 2:
            pyautogui.click(x=self.pos.level2[0], y=self.pos.level2[1])
        elif lvl == 3:
            pyautogui.click(x=self.pos.level3[0], y=self.pos.level3[1])
        elif lvl == 4:
            pyautogui.click(x=self.pos.level4[0], y=self.pos.level4[1])
        elif lvl == 5:
            pyautogui.click(x=self.pos.level5[0], y=self.pos.level5[1])
        else:
            raise ValueError
        time.sleep(self.short_click_wait)
        self.move_mouse_to_safe()

    def wait_and_stop_at_base_lvl(self, target_lvl, safety_lvl=50, safety_lvl_count=20):
        '''
        Wait until you find a base lvl >= target_lvl
        '''
        t = time.time()
        self.logger.info(f'Starting waiting to lvl {lvl} in: wait_to_lvl()')
        safety_counter = 0
        while True:
            time.sleep(self.progress_wait)
            lvl = self.get_base_level()
            lvl_string = str(lvl).zfill(4) if lvl is not None else '  - '
            if lvl is not None:
                if lvl >= (target_lvl - safety_lvl):
                    safety_counter +=1
                if (lvl >= target_lvl) and (safety_counter > safety_lvl_count):
                    pyautogui.press('g')
                    self.logger.info(f'Exiting waiting() with lvl: {lvl_string}   sc: {safety_counter}')
                    return
            self.logger.info(f'lvl: {lvl_string}   sc: {safety_counter}')

    def wait_for_enrage(self, check_wait_time=0.2, max_waiting_loops=1000):
        t = time.time()
        self.logger.info('Staring: wait_for_enrage()')
        update_counter = 0
        while update_counter < max_waiting_loops:
            time.sleep(check_wait_time)
            rage = self.check_enrage_status()
            if rage:
                self.logger.info('Exiting wait_for_enrage() successfully')
                return
            if update_counter % 10 == 0:
                self.logger.info(f'Waiting...  uc: {update_counter}')
            update_counter += 1
        self.logger.info(f'Exiting wait_for_enrage() unsuccessfully  uc: {update_counter}')

    def swap_to_group_and_start_progress(self, group):
        self.logger.info('swap_to_group_and_start_progress()')
        pyautogui.keyDown('shift')
        self.click_level(1)
        pyautogui.keyUp('shift')
        time.sleep(self.short_click_wait)
        pyautogui.press(group)
        time.sleep(self.short_click_wait)
        pyautogui.press('g')
        self.logger.info("Switched to KILL_GROUP, and 'g'ing")
        
    def wait_for_reset(self, safety_lvl_upper=100, pause_at_reset=None):
        '''
        pause_at_reset should be None, or a pause time
        '''
        t = time.time()
        self.logger.info('Starting: wait_for_reset()')
        safety_counter = 0
        while safety_counter < 1000:
            time.sleep(self.progress_wait)
            self.last_pt = 0  # We care about finding lvl 1, so start from 0
            lvl = self.get_base_level()
            if lvl is not None:
                if (lvl >= 1) and (lvl <= safety_lvl_upper):
                    if pause_at_reset is not None:
                        pyautogui.press('g')
                        time.sleep(pause_at_reset)
                        pyautogui.press('g')
                    break
                safety_counter += 1
        self.logger.info("Click away the server error messages")
        self.click_server_error_msg()
        time.sleep(self.long_click_wait)
        self.click_server_error_msg()
        time.sleep(self.short_click_wait)
        self.move_mouse_to_safe()
        t = time.time()
        self.timer.info(f'reset wait: {time.time() - t:5.1f}')