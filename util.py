import time
import pyautogui
import pytesseract

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


def get_base_level_number_img(fullscreen, res_factor):
    '''
    Gets the image from the upper right of the base level number
    '''
    if fullscreen:
        region=(1222, 167, 30, 25)  # Fullscreen
    else:
        region = (1188, 159, 38, 26)  # Windowed

    region = tuple(i * res_factor for i in region)
    return pyautogui.screenshot(region=region).convert('RGB')


def get_base_level(lvl_read_max, fullscreen, res_factor):
    '''
    Returns the base lvl number, or None, based on the lvl number in upper right.
    '''
    im = get_base_level_number_img(fullscreen, res_factor)
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
        if text == '836': text = '336'
        try:
            lvl = int(text)
            if lvl > lvl_read_max:
                return None
        except:
            return None
        return lvl



def get_enrage_img(fullscreen, res_factor):
    '''
    Gets an image of the region where the enrage stacks come up.
    '''
    if fullscreen:
        region=(629, 710, 254, 37)  # Fullscreen
    else:
        region=(708, 527, 330, 49)  # Windowed

    region = tuple(i * res_factor for i in region)
    return pyautogui.screenshot(region=region).convert('RGB')

def check_enrage_status(fullscreen, res_factor):
    im = get_enrage_img(fullscreen, res_factor)
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


def click_back(fullscreen):
    if fullscreen:
        pyautogui.click(x=1198, y=179)
    else:
        pyautogui.click(x=1158, y=176)


def click_level(lvl, fullscreen):
    if fullscreen:
        if lvl == 1:
            pyautogui.click(x=1237, y=181)
        if lvl == 2:
            pyautogui.click(x=1285, y=181)
        if lvl == 3:
            pyautogui.click(x=1330, y=181)
        if lvl == 4:
            pyautogui.click(x=1377, y=181)
        if lvl == 5:
            pyautogui.click(x=1424, y=181)
    else:
        if lvl == 1:
            pyautogui.click(x=1209, y=176)
        if lvl == 2:
            pyautogui.click(x=1255, y=176)
        if lvl == 3:
            pyautogui.click(x=1301, y=176)
        if lvl == 4:
            pyautogui.click(x=1352, y=176)
        if lvl == 5:
            pyautogui.click(x=1399, y=176)

    