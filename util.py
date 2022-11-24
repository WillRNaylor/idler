import os
import time
import logging
import datetime
import numpy as np
import pyautogui
import pytesseract
import mss
import cv2


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


def init_lvl_dict(config):
    # Load the transition image:
    transition = cv2.imread(os.path.join(config.IMG_REF_PATH, 'transition.png'))

    # Load images:
    lvls = []
    imgs = []
    # First the undone levels:
    files = os.listdir(os.path.join(config.IMG_REF_PATH, 'base_lvls'))
    files.sort()
    for f in files:
        if f[-4:] != '.png':
            continue
        lvls.append(int(f[:-4]))
        imgs.append(cv2.imread(os.path.join(config.IMG_REF_PATH, 'base_lvls', f)))
    # Now the completed levels:
    files = os.listdir(os.path.join(config.IMG_REF_PATH, 'base_lvls_done'))
    files.sort()
    for f in files:
        if f[-4:] != '.png':
            continue
        lvls.append(int(f[:-4]))
        imgs.append(cv2.imread(os.path.join(config.IMG_REF_PATH, 'base_lvls_done', f)))
    
    return {'lvls': lvls, 'imgs': imgs, 'transition': transition}


def get_base_level_number_img(pos):
    '''
    Gets the image from the upper right of the base level number
    '''
    with mss.mss() as sct:
        return np.array(sct.grab(pos.base_level_number))[:, :, :3]


def get_base_level(pos, config, lvl_ref=None, last_pt=None):
    '''
    Returns (lvl, last_pt)
    '''

    if lvl_ref is None:
        lvl_ref = init_lvl_dict(config)
    if last_pt is None:
        last_pt = 0

    img = get_base_level_number_img(pos)

    # First, check if we are in a transition:
    if np.allclose(img, lvl_ref['transition'], atol=config.IMG_CLOSE_RANGE):
        return (None, None)

    m = len(lvl_ref['lvls'])
    counter = 0
    while counter < m:
        pt = (last_pt + counter) % m
        if np.allclose(img, lvl_ref['imgs'][pt], atol=config.IMG_CLOSE_RANGE):
            return (lvl_ref['lvls'][pt], pt)
        counter += 1
    return (None, None)


def get_enrage_img(pos):
    '''
    Gets the image from where the enrage stacks text comes up
    '''
    with mss.mss() as sct:
        return np.array(sct.grab(pos.enrage_box))


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


def init_logger(logfile, name='idler', level=logging.INFO):
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

    return logger


def round_datetime_seconds(dt):
    return dt - datetime.timedelta(microseconds=dt.microsecond)
