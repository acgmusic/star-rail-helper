import time
from pynput.keyboard import Key
from pynput.keyboard import Controller as kcontroller
from pynput.mouse import Controller as mcontroller
from pynput.mouse import Button
from common.utils import *
import json


class MapCr:
    def __init__(self):
        self.cr_data = []

    def load(self, path):
        data_abs_path = get_abs_path(r"resource/map_data/" + path)
        with open(data_abs_path, "r", encoding="utf-8") as f:
            self.cr_data = json.loads(f.read())
        for i in range(len(self.cr_data)):
            item = self.cr_data[i]
            if "button" in item:
                if item["button"] == "Button.left":
                    item["button"] = Button.left
                else:
                    item["button"] = Button.right

    def run(self, times=1, speed=1.0):
        mouse = mcontroller()
        keyboard = kcontroller()
        for _ in range(times):
            if not self.cr_data:
                logger.error('error empty record.')
                return
            action_start_time = self.cr_data[0]['time']
            for idx, action in enumerate(self.cr_data):
                gtime = action['time'] - action_start_time
                if gtime < 0.02 and idx != 0 and action['action'] == 'move':
                    # 针对鼠标移动的稍稍优化
                    continue
                if action['type'] == 'mouse':
                    mouse.position = (int(action['x']), int(action['y']))
                    act = action['action']
                    if act == 'scroll':
                        getattr(mouse, action['action'])(action['dx'], action['dy'])
                    elif act == 'press' or act == 'release':
                        getattr(mouse, action['action'])(action['button'])
                elif action['type'] == 'keyboard':
                    if getattr(action['key'], 'name', None) not in ['f7', 'f9', 'f8', 'esc', 'f10']:
                        getattr(keyboard, action['action'])(action['key'])
                if speed:
                    time.sleep(gtime / speed)
                action_start_time = action['time']


if __name__ == '__main__':
    mc = MapCr()
    mc.load("20230528_132935_370.json")
    mc.run()
    print(mc.cr_data)
