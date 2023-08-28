import pyautogui

'''
If you just need to know the location of the mouse

Can be used to find the pixel location of buttons in IC.
'''

mouse_pos = pyautogui.position()
print(f"Mouse position: ({mouse_pos[0]}, {mouse_pos[1]})")
