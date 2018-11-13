import pyautogui
import time
import sys

# po = pyautogui.position()
# im = pyautogui.screenshot()
# base = im.getpixel(po)

time.sleep(5)

rag = 39
for i in range(rag):
    pyautogui.typewrite('\n')
    time.sleep(0.5)
    pyautogui.typewrite(['down'])
    # time.sleep(1)

# pyautogui.typewrite(str(i))
# pyautogui.typewrite('\n')
# time.sleep(1)
# im2 = pyautogui.screenshot()
# temp = im2.getpixel(po)
# if temp != base:
#     sys.exit("ojbk " + str(i))
