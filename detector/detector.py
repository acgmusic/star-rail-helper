import logging

import pyautogui
from common.utils import *
from common.game_mgr import g_game
# from ultralytics import YOLO
import win32gui
import mss
import mss.tools
import cv2
import numpy as np


game_img_path = "./resource/game_img/"


class Detector:
    windows_offset = (-1, -1, -1, -1)
    last_game_pos = (-1, -1, -1, -1)       # left, top, right, bottom
    img_mgr = {}
    cur_left_top_icon_idx = 0

    def __init__(self):
        self.camera = mss.mss()
        self.init_img_mgr()
        self.init_game_pos()
        self.last_match_score = 1

    # load all img to memory
    def init_img_mgr(self):
        img_root_path = get_abs_path(game_img_path)
        for img_file in os.listdir(img_root_path):
            img_path = os.path.join(img_root_path, img_file)
            self.img_mgr[img_file] = cv2.imread(img_path)

    def init_game_pos(self):
        find_flag = False
        for _ in range(g_usr_cfg["find_game_window_max_retry_time"]):
            for idx, icon in enumerate(g_usr_cfg["left_top_icon"]):
                img_pos = self.get_target_img_pos_abs(icon)
                if img_pos is None:
                    continue
                # modify win rect
                left, top = int(img_pos[0]), int(img_pos[1])
                right, bottom = left + g_game.game_width, top + g_game.game_height
                self.last_game_pos = (left, top, right, bottom)
                _left, _top, _right, _bottom = win32gui.GetWindowRect(g_game.proc_id)
                self.windows_offset = (left - _left, top - _top, right - _right, bottom - _bottom)
                find_flag = True
                self.cur_left_top_icon_idx = idx
                break
            else:
                logging.warning("please set game foreground")
                time.sleep(1)
            if find_flag:
                return
        logger.error("can not find game on your screen, exit...")
        exit(SRH_FIND_NO_GAME)

    def get_game_screenshot(self):
        #  check left top icon pos right
        img = self.camera.grab(self.last_game_pos)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        check_img = self.img_mgr[g_usr_cfg["left_top_icon"][self.cur_left_top_icon_idx]]
        img_check = img[0:check_img.shape[0], 0:check_img.shape[1]]
        if self.match_template(img_check, check_img) is None:
            logger.warning("lose game windows, try to detect again.")
            self.init_game_pos()
        # check game window grab ok and check left top icon ok
        if DEBUG_FLAG:
            fp = "/debug/img/" + get_cur_time() + ".png"
            # self.save_img(img_check, fp[:-4]+"check.png")
            self.save_img(img, fp)
        return img

    @staticmethod
    def get_img_abs_path(img_name):
        return get_abs_path(r"%s/%s" % (game_img_path, img_name))

    @staticmethod
    def get_bin_img(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩图转换为灰度图
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 输入灰度图，实现图像二值化
        return cv2.cvtColor(binary, cv2.COLOR_BGRA2BGR)

    def match_template(self, img, template, threshold=g_usr_cfg["match_template_threshold"], bin_flag=False):
        if bin_flag:
            img = self.get_bin_img(img)
            template = self.get_bin_img(template)
        results = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        min_value, _, min_loc, _ = cv2.minMaxLoc(results)
        self.last_match_score = min_value
        if DEBUG_FLAG:
            self.save_img(img, get_cur_time() + "_debug_01.png")
            self.save_img(template, "debug_02.png")
        if min_value > threshold:
            logger.debug("cannot find template on img, match score: %f" % (min_value,))
            return None
        return min_loc

    def get_target_img_pos_abs(self, img_name, grab_range=(0, 0, g_game.screen_width, g_game.screen_height),
                               threshold=g_usr_cfg["match_template_threshold"], bin_flag=False):
        # default grab full screenshot
        img = self.camera.grab(grab_range)
        screen_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        return self.match_template(screen_img, self.img_mgr[img_name], threshold, bin_flag)

    def get_target_img_pos(self, img_name, grab_range=(0, 0, 0, 0),
                           threshold=g_usr_cfg["match_template_threshold"], bin_flag=False):
        rel_range = (
            self.last_game_pos[0] + grab_range[0],
            self.last_game_pos[1] + grab_range[1],
            self.last_game_pos[0] + grab_range[2],
            self.last_game_pos[1] + grab_range[3],
        )
        return self.get_target_img_pos_abs(img_name, rel_range, threshold, bin_flag)

    @staticmethod
    def save_img(img, img_name, mod="cv2"):
        img_abs_path = get_abs_path(r"output/" + img_name)
        if mod == "mss":
            mss.tools.to_png(img.rgb, img.size, output=img_abs_path)
        elif mod == "cv2":
            cv2.imwrite(img_abs_path, img)
        else:
            logger.error("img save fail, invalid mod: %s" % (mod, ))


if __name__ == '__main__':
    # Create a new YOLO model from scratch
    # model = YOLO('yolov8s.yaml').load('yolov8s.pt')
    d = Detector()
