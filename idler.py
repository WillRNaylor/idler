import os
import time
import logging
import datetime
import cv2
import numpy as np
from termcolor import colored
import mss
import pyautogui
import pytesseract

from locations import Locations

class Idler:
    def __init__(self, setup, reset_lvl=None, gem_pot=True, verbose=True, note=None):
        # ==== Basic
        self.reset_lvl = reset_lvl
        self.gem_pot=gem_pot
        self.note=note
        # ===== Advanced
        self.short_click_wait = 0.1
        self.long_click_wait = 0.4
        self.progress_wait = 0.02
        self.image_ref_path = 'img_reference'
        self.lvl_match_tollerance = 3
        self.alt_tab_wait = 0.1
        self.alt_tab_end_wait = 0.3
        self.verbose = verbose
        # ==== Internal
        self.setup = setup
        self.pos = Locations(setup)
        self.lvl_ref = None
        self.last_pt = None
        self.pc_cmd = 'light_cyan'
        self.pc_imp = 'light_yellow'
        self.startup_time = time.time()
        self.run_start_time = None
        self.run_count = 0
        self.prev_run_times = []
        # self.init_logger('logfile_', name='idler', level=logging.INFO)

    # def init_logger(self, logfile, name='idler', level=logging.INFO):
    #     '''
    #     Define the logger object for logging.
    #     Parameters
    #     ----------
    #     logfile : str
    #         Full path of the output log file.
    #     name : str
    #         Name of the logger, used by the logging library.
    #     Returns
    #     -------
    #         logger."logging-object"
    #     '''
    #     logger = logging.getLogger(name)
    #     logger.setLevel(level)
    #     fh = logging.FileHandler(os.path.join(
    #         './logs', logfile + datetime.datetime.now().strftime('%Y%m%d')), 'a+')
    #     fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    #     logger.addHandler(fh)
    #     self.logger = logger
    # # #     Usage example:
    # #     self.logger.info(text)

    def print_major(self, text=''):
        start = colored('==', 'light_magenta')
        time_string = colored(datetime.datetime.now().strftime("%H:%M:%S "), 'light_magenta')
        print(start + time_string + text)

    def print_minor(self, text=''):
        start = colored('--', 'light_magenta')
        time_string = colored(datetime.datetime.now().strftime("%H:%M:%S "), 'magenta')
        print(start + time_string + text)

    def print_major_seperator(self):
        start = colored('==', 'light_magenta')
        time_string = colored(datetime.datetime.now().strftime("%H:%M:%S"), 'light_magenta')
        ending = colored('================================================================', 'light_magenta')
        print(start + time_string + ending)

    def print_minor_seperator(self):
        start = colored('--', 'light_magenta')
        time_string = colored(datetime.datetime.now().strftime("%H:%M:%S"), 'light_magenta')
        ending = colored('----------------------------------------------------------------', 'light_magenta')
        print(start + time_string + ending)

    def zero_run_clock(self):
        self.run_start_time = time.time()
        if self.verbose:
            print(f'Run clock reset.')

    def increment_run_count(self):
        self.run_count += 1

    def increment_run_count(self):
        self.run_count += 1

    def zero_session_clock(self):
        self.run_start_time = time.time()

    def print_run_stats(self, extra_bosses=0):
        # ---- Calculate all the stats:
        num_bosses = int(self.reset_lvl / 5) + int(extra_bosses)
        up_time = int(time.time() - self.startup_time)
        run_time = int(time.time() - self.run_start_time)
        self.prev_run_times.append(run_time)
        min, sec = divmod(run_time, 60)
        run_time_st = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
        run_count_st = str(self.run_count).zfill(3)
        datetime_st = datetime.datetime.now().strftime('%H:%M:%S')
        bph_st = str(int(num_bosses * 3600 / run_time))
        if self.gem_pot:
            gem_factor = 1.5
        else:
            gem_factor = 1.
        gph_st = str(int(num_bosses * 3600 / run_time * 9.15 * gem_factor))
        if self.run_count <= 1:
            avg_time = run_time
        else:
            avg_time = np.sum(np.array(self.prev_run_times[1:])) / (self.run_count)
        print(np.array(self.prev_run_times))
        print(np.array(self.prev_run_times[1:]))
        print(self.run_count)
        print(np.sum(np.array(self.prev_run_times[1:])))
        print(run_time)
        print(avg_time)
        min, sec = divmod(int(avg_time), 60)
        avg_time_st = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
        avg_bph_st = str(int(num_bosses * 3600 / avg_time))
        avg_gph_st = str(int(num_bosses * 3600 / avg_time * 9.15 * gem_factor))

        # ---- Printing those stats:
        self.print_minor_seperator()
        self.print_major('Run count: ' + colored(run_count_st, self.pc_imp))
        self.print_major('Run time:  ' + colored(run_time_st, self.pc_imp))
        if self.verbose:
            self.print_major(f"Total time: {str(datetime.timedelta(seconds=up_time))}")
            if num_bosses is not None:
                self.print_major("BPH:     " + colored(bph_st, self.pc_imp))
                self.print_major("GPH:     " + colored(gph_st, 'light_green'))
                self.print_major("avg BPH: " + colored(avg_bph_st, self.pc_imp))
                self.print_major("avg GPH: " + colored(avg_gph_st, 'light_green'))
            if len(self.prev_run_times) > 1:
                runs = colored(run_time, self.pc_imp) + ', '
                for t in reversed(self.prev_run_times[1:]):
                    runs += str(t) + ', '
                self.print_major(f"Previous runs: " + runs)
        self.print_major_seperator()
        # Now write a single summary ling to a 'logfile':
        with open('./logs/logfile_' + datetime.datetime.now().strftime('%y%m%d'), 'a') as f:
            if len(self.prev_run_times) == 1:
                f.write(f'         | r # | r time | r BPH | r GPH | a time | a BPH | a GPH | {self.note}\n')
            else:
                f.write(f"{datetime_st} | {run_count_st} | {run_time_st.rjust(6)} | {bph_st.rjust(5)} | {gph_st.rjust(5)} | {avg_time_st.rjust(6)} | {avg_bph_st.rjust(5)} | {avg_gph_st.rjust(5)} |\n")

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
        # Different IC setups need a diff. prefix to the files or folders.
        if self.setup == 'fullscreen_hermes':
            prefix = ''
        elif self.setup == 'windowed_hermes':
            prefix = 'wind_'
        else:
            print(f"ValueError? self.setup = {self.setup}")
        # Load the transition image:
        transition = cv2.imread(os.path.join(self.image_ref_path, prefix + 'transition.png'))
        # Load images:
        lvls = []
        imgs = []
        lvls_done = []
        imgs_done = []
        # First the undone levels:
        files = os.listdir(os.path.join(self.image_ref_path, prefix + 'base_lvls'))
        files.sort()
        for f in files:
            if f[-4:] != '.png':
                continue
            lvls.append(int(f[:-4]))
            imgs.append(cv2.imread(os.path.join(self.image_ref_path, prefix + 'base_lvls', f)))
        # Now the completed levels:
        files = os.listdir(os.path.join(self.image_ref_path, prefix + 'base_lvls_done'))
        files.sort()
        for f in files:
            if f[-4:] != '.png':
                continue
            lvls_done.append(int(f[:-4]))
            imgs_done.append(cv2.imread(os.path.join(self.image_ref_path, prefix + 'base_lvls_done', f)))
        # Now riffle them together:
        lvls = [val for pair in zip(lvls, lvls_done) for val in pair]
        imgs = [val for pair in zip(imgs, imgs_done) for val in pair]
        self.lvl_ref = {'lvls': lvls, 'imgs': imgs, 'transition': transition}

    def get_base_level_number_img(self):
        '''
        Gets the image from the upper right of the base level number
        '''
        with mss.mss() as sct:
            return np.array(sct.grab(self.pos.base_level_number))[:, :, :3]
    
    def save_base_level_number_img(self, filename):
        with mss.mss() as sct:
            im = np.array(sct.grab(self.pos.base_level_number))[:, :, :3]
        cv2.imwrite(os.path.join('.', filename + '.png'), im)

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
        if np.square(np.subtract(self.lvl_ref['transition'], img)).mean() < self.lvl_match_tollerance:
            return None
        # Find lvl number
        m = len(self.lvl_ref['lvls'])
        counter = 0
        while counter < m:
            pt = (self.last_pt + counter) % m
            if np.square(np.subtract(self.lvl_ref['imgs'][pt], img)).mean() < self.lvl_match_tollerance:
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
            return np.array(sct.grab(self.pos.enrage_box))[:, :, :3]

    def save_enrage_img(self, filename):
        with mss.mss() as sct:
            im = np.array(sct.grab(self.pos.enrage_box))[:, :, :3]
        cv2.imwrite(os.path.join('.', filename + '.png'), im)

    def get_steam_start_button(self):
        with mss.mss() as sct:
            return np.array(sct.grab(self.pos.steam_start_button_box))

    def get_welcome_back(self):
        with mss.mss() as sct:
            return np.array(sct.grab(self.pos.welcome_back))

    def check_steam_ic_running(self):
        im = self.get_steam_start_button()
        avgs = [np.mean(im[:, :, 0]), np.mean(im[:, :, 1]), np.mean(im[:, :, 2])]
        if (avgs[0] < 90) and (avgs[1] > 140) and (avgs[2] > 75):
            return False
        elif (avgs[0] > 150) and (avgs[1] < 120) and (avgs[2] < 75):
            return True
        else:
            return None

    def check_welcome_back_button_present(self):
        im = self.get_welcome_back()
        # cv2.imwrite(os.path.join('.', f"ok_button_{number}.png"), im)  # Reqs num in input
        text = pytesseract.image_to_string(im)
        if isinstance(text, str):
            if 'welcome' in text.lower():
                return True
            elif 'back' in text.lower():
                return True
            elif 'you were away' in text.lower():
                return True
        else:
            return False
    
    def wait_welcome_back_button_present(self):
        sleep_time = 0.2
        safety_cutoff = int(30 * 60 / sleep_time)
        safety_counter = 0
        while True:
            time.sleep(sleep_time)
            if self.check_welcome_back_button_present() is True:
                return
            if safety_counter > safety_cutoff:
                print("We ran into the welcome back cutoff")
                return
            safety_counter += 1

    def wait_steam_ic_not_running(self):
        sleep_time = 0.3
        safety_cutoff = int(10 * 60 / sleep_time)
        safety_counter = 0
        while True:
            time.sleep(sleep_time)
            check = self.check_steam_ic_running()
            if check is False:
                return
            elif check is None:
                print("got a none in reading steam ic start icon")
            if safety_counter > safety_cutoff:
                print("We ran into the steam ic running cutoff")
                return None
            safety_counter += 1

    def check_enrage_status(self):
        im = self.get_enrage_img()
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
        if self.verbose:
            print(f'Waitig {wait_time} seconds')
        time.sleep(wait_time)

    def click_welcome_back_button(self):
        pyautogui.click(x=self.pos.welcome_back_button[0], y=self.pos.welcome_back_button[1])
        pyautogui.click(x=self.pos.welcome_back_button_2[0], y=self.pos.welcome_back_button_2[1])

    def select_group(self, group):
        pyautogui.press(group)
        if self.verbose:
            print("Selected group: " + colored(group.upper(), self.pc_cmd))

    def move_mouse_to_safe(self):
        pyautogui.moveTo(self.pos.safe[0], self.pos.safe[1])

    def click_server_error_msg(self):
        pyautogui.click(x=self.pos.server_error[0], y=self.pos.server_error[1])

    def click_back(self):
        pyautogui.click(x=self.pos.back[0], y=self.pos.back[1])
        if self.verbose:
            print("Clicked: " + colored('BACK', self.pc_cmd))
        time.sleep(self.short_click_wait)

    def click_back_one_lvl(self):
        pyautogui.press('left')
        if self.verbose:
            print("Clicked back one lvl: " + colored('LEFT', self.pc_cmd))

    def click_level(self, lvl):
        if lvl == 1:
            pyautogui.click(x=self.pos.level1[0], y=self.pos.level1[1])
            if self.verbose:
                print("Clicked: " + colored('LVL-1', self.pc_cmd))
        elif lvl == 2:
            pyautogui.click(x=self.pos.level2[0], y=self.pos.level2[1])
            if self.verbose:
                print("Clicked: " + colored('LVL-2', self.pc_cmd))
        elif lvl == 3:
            pyautogui.click(x=self.pos.level3[0], y=self.pos.level3[1])
            if self.verbose:
                print("Clicked: " + colored('LVL-3', self.pc_cmd))
        elif lvl == 4:
            pyautogui.click(x=self.pos.level4[0], y=self.pos.level4[1])
            if self.verbose:
                print("Clicked: " + colored('LVL-4', self.pc_cmd))
        elif lvl == 5:
            pyautogui.click(x=self.pos.level5[0], y=self.pos.level5[1])
            if self.verbose:
                print("Clicked: " + colored('LVL-5', self.pc_cmd))
        else:
            raise ValueError
        time.sleep(self.short_click_wait)
        self.move_mouse_to_safe()

    def click_load_OK(self):
        pyautogui.click(x=self.pos.load_ok[0], y=self.pos.load_ok[1])
    
    def press_start_stop(self):
        pyautogui.press('g')
        if self.verbose:
            print('Progress started/stopped: ' + colored('G', self.pc_cmd))

    def wait_for_base_lvl(self, target_lvl, stop_at_lvl=False, safety_lvl=50, safety_lvl_count=20):
        '''
        Wait until you find a base lvl >= target_lvl
        '''
        if self.verbose:
            self.print_minor('Waiting to stop at or over base lvl: ' + colored(target_lvl, self.pc_imp))
        safety_counter = 0
        same_lvl_counter = 0
        prev_lvl = 0
        while True:
            time.sleep(self.progress_wait)
            lvl = self.get_base_level()
            if (lvl is not None) and lvl != prev_lvl:
                same_lvl_counter = 0
                lvl_string = '\n' + str(lvl)
            elif (lvl is not None) and lvl == prev_lvl:
                lvl_string = '-'
            else:
                same_lvl_counter = 0
                lvl_string = '.'
            prev_lvl = lvl
            if lvl is not None:
                same_lvl_counter += 1
                if lvl >= (target_lvl - safety_lvl):
                    safety_counter +=1
                if (lvl >= target_lvl) and (safety_counter > safety_lvl_count):
                    if self.verbose:
                        print(f'\nFound base lvl {lvl_string} ( >= {target_lvl}).')
                    if stop_at_lvl:
                        self.press_start_stop()
                    return
            colour = 'dark_grey'
            if safety_counter > 0:
                colour = 'green'
            elif same_lvl_counter > 200:
                colour = 'red'
            elif same_lvl_counter > 50:
                colour = 'light_grey'
            if self.verbose:
                print(colored(lvl_string, colour), end='', flush=True)

    def wait_for_enrage(self, check_wait_time=0.2, max_waiting_loops=1000):
        if self.verbose:
            self.print_minor('Waiting for enemy rage' + colored(f' check_wait_time={check_wait_time}, max_waiting_loops={max_waiting_loops}', 'dark_grey'))
        update_counter = 0
        while update_counter < max_waiting_loops:
            time.sleep(check_wait_time)
            rage = self.check_enrage_status()
            if rage:
                if self.verbose:
                    print('\nExiting rage successfully')
                return
            if update_counter % 10 == 0:
                if self.verbose:
                    print(colored(update_counter, 'dark_grey'), end=colored(',', 'dark_grey'), flush=True)
            update_counter += 1
        if self.verbose:
            print(colored('\nExiting rage unsuccessfully (timeout)', 'light_red'))

    def swap_to_group_and_start_progress(self, group):
        if self.verbose:
            self.print_minor('Swapping to group ' + colored(group.upper(), self.pc_cmd) + ' and starting progress')
        self.click_back_one_lvl()
        time.sleep(self.short_click_wait)
        self.select_group(group)
        time.sleep(self.short_click_wait)
        self.select_group(group)
        time.sleep(self.short_click_wait)
        self.press_start_stop()
        time.sleep(self.short_click_wait)
        self.select_group(group)
        # # Hack to check the "OK" button is pressed.
        # time.sleep(2)
        # self.click_welcome_back_button()
        
    def wait_for_reset(self, safety_lvl_upper=60, pause_at_reset=None, wait_iterations=100000):
        '''
        pause_at_reset should be None, or a pause time
        '''
        if self.verbose:
            self.print_minor('Waiting for reset lvl')
        safety_counter = 0
        prev_lvl = 0
        while safety_counter < wait_iterations:
            time.sleep(self.progress_wait)
            self.last_pt = 0  # We care about finding lvl 1, so start from 0
            lvl = self.get_base_level()
            if (lvl is not None) and lvl != prev_lvl:
                lvl_string = '\n' + str(lvl)
            elif (lvl is not None) and lvl == prev_lvl:
                lvl_string = '-'
            else:
                lvl_string = '.'
            prev_lvl = lvl
            if lvl is not None:
                if (lvl >= 1) and (lvl <= safety_lvl_upper):
                    print("\nGo go go")
                    if pause_at_reset is not None:
                        print("Pausing at reset")
                        pyautogui.press('g')
                        time.sleep(pause_at_reset)
                        pyautogui.press('g')
                    break
                safety_counter += 1
            colour = 'dark_grey'
            if safety_counter > int(wait_iterations * 0.5):
                colour = 'red'
            elif safety_counter > int(wait_iterations * 0.05):
                colour = 'light_grey'
            if self.verbose:
                print(colored(lvl_string, colour), end='', flush=True)
        # Added another safety layer:
        if safety_counter >= (wait_iterations - 1):
            print(colored("Passed the 'wait for reset' safety counter", 'light_red'))
            self.swap_to_group_and_start_progress('w')
        # self.click_server_error_msg()
        # time.sleep(self.long_click_wait)
        # self.click_server_error_msg()
        # time.sleep(self.short_click_wait)
        # self.move_mouse_to_safe()
    
    def restart_ic(self):
        # Quit ic
        pyautogui.hotkey('command', 'q')
        time.sleep(1)
        # Open steam (it must be in a full screen type format)
        pyautogui.keyDown('command')
        pyautogui.press('space')
        time.sleep(0.1)
        pyautogui.keyUp('command')
        for l in "steam":
            time.sleep(0.01)
            pyautogui.press(l)
        time.sleep(0.05)
        pyautogui.press('enter')
        time.sleep(0.5)
        # Wait for the green button then start ic
        self.wait_steam_ic_not_running()
        time.sleep(self.short_click_wait)
        pyautogui.click(x=self.pos.steam_start_button[0], y=self.pos.steam_start_button[1])
        # Click a few times in a safe pos for the opening credits
        time.sleep(5)
        for _ in range(5):
            time.sleep(1)
            pyautogui.click(x=self.pos.safe[0], y=self.pos.safe[1])
        # Wait for the "welcome back button", this can take a while, as needs to do
        # the offline progress before this appears.
        self.wait_welcome_back_button_present()
        print('b', end='')
        time.sleep(self.short_click_wait)
        self.click_welcome_back_button()
        time.sleep(0.2)
        self.click_welcome_back_button()
        print('c', end='')
        

