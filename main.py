import time

from common.system_op import *
from detector.detector import *


start_game()
d = Detector()

while True:
    d.get_game_screenshot()
    exit(0)
    time.sleep(0.2)
