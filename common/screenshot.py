import pyautogui
from common.utils import *
import win32gui
from PIL import ImageGrab

# screen_width, screen_height = ImageGrab.grab().size
# print(screen_width, screen_height)
# game_window = win32gui.FindWindow(None, "崩坏：星穹铁道")
# print(game_window)
left, top, right, bottom = win32gui.GetWindowRect(4460814)
print(left, top, right, bottom)
# img = ImageGrab.grab((0, 0, 1920, 1120))
# img.save("123.png")

time.sleep(3)
app_pos = pyautogui.locateOnScreen(r"C:\Users\11527\Desktop\project\github\star-rail-helper\detector\../resource/game_img/PosterGirl_01.png")
print(list(app_pos))
left2, top2 = app_pos[0], app_pos[1]
print([left2, top2, left+1920, top+1120])

print([left2-left, top2-top, left+1920-right, top+1120-bottom])

# mg = pyautogui.screenshot(region=(left, top, 1920, 1120))
# img = pyautogui.screenshot(region=app_pos)
# img.save("123.png")
