import os
import time
import logging
import datetime
import pyautogui
import pytesseract

logger = logging.getLogger('idler.util')

def alt_tab(wait=0.1, end_wait=0.1):
    '''
    Alt tabs between window and previous.
    '''
    pyautogui.keyDown('command')
    time.sleep(wait)
    pyautogui.press('tab')
    time.sleep(wait)
    pyautogui.keyUp('command')
    time.sleep(end_wait)


def get_base_level_number_img(pos):
    '''
    Gets the image from the upper right of the base level number
    '''
    return pyautogui.screenshot(region=pos.base_level_number).convert('RGB')


def get_base_level(pos, config):
    '''
    Returns the base lvl number, or None, based on the lvl number in upper right.
    '''
    im = get_base_level_number_img(pos)
    text = pytesseract.image_to_string(im)
    if text == '':
        return None
    else:
        # if text[0] == 'z': text = text.replace('B', '3')
        text = text[:-1]
        text = text.replace('B', '3')
        text = text.replace('z', '2')
        text = text.replace('Z', '2')
        text = text.replace('t', '1')
        text = text.replace('l', '1')
        text = text.replace('}', '1')
        text = text.replace('o', '0')
        text = text.replace(')', '1')
        text = text.replace('A', '4')
        if text == '836': text = None
        try:
            lvl = int(text)
            if lvl > config.LVL_READ_MAX:
                return None
        except:
            return None
        return lvl



def get_enrage_img(pos):
    '''
    Gets an image of the region where the enrage stacks come up.
    '''
    return pyautogui.screenshot(region=pos.enrage_box).convert('RGB')


def check_enrage_status(pos):
    im = get_enrage_img(pos)
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


def get_background_img(pos):
    '''
    Gets a little bit of background from just under the formation to the left.
    '''
    return pyautogui.screenshot(region=pos.background_snippet).convert('RGB')


def click_back(pos):
    pyautogui.click(x=pos.back[0], y=pos.back[1])


def click_level(pos, config):
    if config.STACK_LVL_MOD_FIVE == 1:
        pyautogui.click(x=pos.level1[0], y=pos.level1[1])
    elif config.STACK_LVL_MOD_FIVE == 2:
        pyautogui.click(x=pos.level2[0], y=pos.level2[1])
    elif config.STACK_LVL_MOD_FIVE == 3:
        pyautogui.click(x=pos.level3[0], y=pos.level3[1])
    elif config.STACK_LVL_MOD_FIVE == 4:
        pyautogui.click(x=pos.level4[0], y=pos.level4[1])
    elif config.STACK_LVL_MOD_FIVE == 5:
        pyautogui.click(x=pos.level5[0], y=pos.level5[1])
    else:
        raise ValueError


def init_logger(logfile, name='idler'):
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
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(
        './logs', logfile + datetime.datetime.now().strftime('%Y%m%d')), 'a+')
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

    return logger


def round_datetime_seconds(obj: datetime.datetime) -> datetime.datetime:
    if obj.microsecond >= 500_000:
        obj += datetime.timedelta(seconds=1)
    return obj.replace(microsecond=0)