import pyautogui
from common.utils import *
from common.game_mgr import *
from common.system_op import *
from detector.detector import Detector
from ctrl.action_list import ActMgr, Action
from typing import *
import random


class Player:
    def __init__(self):
        self.detector = Detector()
        self.act_mgr = ActMgr()
        self.cur_action_list = []
        self.ctrl_cmd_list = {
            "enter_game": self.enter_game,
            "home": self.home,
            "add_support": self.try_add_support,
            "wait_combat": self.wait_combat,
            "wait_loading": self.wait_loading,
            "close_warning": self.check_and_close_warning,
            "close_warning_and_stop": self.stop_if_find_warning,
            "assignment": self.assignment,
        }

    def log_in(self):
        pass

    def pos_offset(self, pos):
        real_pos = (pos[0] + self.detector.last_game_pos[0],
                    pos[1] + self.detector.last_game_pos[1])
        return real_pos

    def click(self, pos, sleep_time=SLEEP_TIME_SHORT):
        real_pos = self.pos_offset(pos)
        pyautogui.moveTo(*real_pos, duration=SLEEP_TIME_SHORT)
        pyautogui.click()
        pyautogui.sleep(sleep_time)

    def move(self, pos, sleep_time=SLEEP_TIME_SHORT):
        real_pos = self.pos_offset(pos)
        pyautogui.moveTo(real_pos, duration=SLEEP_TIME_SHORT)
        pyautogui.sleep(sleep_time)

    def drag(self, pos_start, pos_end, sleep_time=SLEEP_TIME_SHORT):
        real_pos_end = self.pos_offset(pos_end)
        self.move(pos_start)
        pyautogui.dragTo(*real_pos_end, duration=SLEEP_TIME_NORMAL, button="left")
        pyautogui.sleep(sleep_time)

    def check_combat(self):
        return self.detector.get_target_img_pos(
            "gaming.png", (1606, 65, 1870, 108), threshold=0.9, bin_flag=True) is not None

    def wait_combat(self):
        ang_value = 0
        while True:
            if self.check_combat():
                ang_value = 0
                pyautogui.sleep(SLEEP_TIME_VERY_LONG)
            else:
                if ang_value >= 20:
                    logger.info("detect combat finish")
                    return SRH_OK
                ang_value += self.detector.last_match_score ** 3
                logger.debug("ang_value = %f" % (ang_value, ))
                pyautogui.sleep(SLEEP_TIME_MIDDLE)

    def check_home(self):
        return self.detector.get_target_img_pos(
            "home.png", (20, 106, 53, 134), threshold=0.8, bin_flag=True) is not None

    def home(self):
        ang_value = 0
        while not self.check_home():
            pyautogui.press("ESC")
            pyautogui.sleep(2)
            if ang_value >= 10:
                logger.error("cannot go home")
                return SRH_ERROR
            ang_value += 1
        pyautogui.sleep(SLEEP_TIME_NORMAL)
        logger.info("go home ok.")
        return SRH_OK

    def enter_game(self):
        ang_value = 0
        while not self.check_home():
            pyautogui.click(500, 500)
            pyautogui.press("ESC")
            pyautogui.sleep(2)
            if ang_value >= 60:
                logger.error("cannot enter game, try home")
                return self.home()
            ang_value += 1
        pyautogui.sleep(SLEEP_TIME_NORMAL)
        logger.info("enter game ok.")
        return SRH_OK

    def check_loading(self):
        return self.detector.get_target_img_pos(
            "loading.png", (100, 70, 420, 360), threshold=0.01, bin_flag=True) is not None

    def wait_loading(self):
        ang_value = 0
        while self.check_loading():
            pyautogui.sleep(1)
            if ang_value >= 10:
                logger.error("cannot enter game")
                return SRH_ERROR
            ang_value += 1
        pyautogui.sleep(SLEEP_TIME_NORMAL)
        logger.info("loading ok.")
        return SRH_OK

    def try_add_support(self):
        self.click([1700, 775], SLEEP_TIME_NORMAL)
        for _ in range(3):
            for i in range(6):
                pos = [260, 260 + 130 * i]
                self.click(pos)  # 入队
                self.click([1670, 1030], SLEEP_TIME_LONG)
                if self.detector.get_target_img_pos("warning.png", (915, 435, 985, 470), bin_flag=True, threshold=0.5) is None:
                    logger.info("support add OK.")
                    return
                self.click([745, 710])
            self.drag([280, 940], [280, 230], SLEEP_TIME_MIDDLE)
        logger.error("cannot find valid support character")

    def check_and_close_warning(self):
        if self.detector.get_target_img_pos("warning.png", (915, 435, 985, 470), bin_flag=True, threshold=0.5) is not None:
            logger.warning("close waring popups")
            self.click([745, 710])
        return SRH_OK

    def stop_if_find_warning(self):
        if self.detector.get_target_img_pos("warning.png", (915, 435, 985, 470), bin_flag=True, threshold=0.5) is not None:
            logger.warning("close waring popups")
            self.click([745, 710])
            return SRH_SIG_STOP_ACTION
        return SRH_OK

    def check_assignment_ok(self):
        return self.detector.get_target_img_pos(
            "assignment.png", (1420, 923, 1511, 958), threshold=0.5, bin_flag=False) is not None

    def assignment(self):
        cnt = 0
        # 专属材料、经验材料、合成材料
        item_num = [6, 3, 4]
        for i in range(3):
            self.click([440 + i * 260, 270], sleep_time=SLEEP_TIME_NORMAL)
            for j in range(item_num[i]):
                self.click([580, 380 + j * 92], sleep_time=SLEEP_TIME_NORMAL)
                if self.check_assignment_ok():
                    self.click([1465, 945], sleep_time=SLEEP_TIME_NORMAL)
                    self.click([1170, 1000], sleep_time=SLEEP_TIME_VERY_LONG)
                    cnt += 1
                    logger.info("assignment ok")
                    if cnt == 4:
                        logger.info("assignment ok for all")
                        return SRH_OK
        logger.warning("assignment num is %d, less than 4" % (cnt, ))
        return SRH_TASK_NOT_ALL_OK

    def ctrl(self, name):
        return self.ctrl_cmd_list[name]()

    def random_walk(self):
        director = ["A", "W", "D", "S"]
        T = 5
        while True:
            if self.check_loading():
                self.wait_loading()
                self.wait_combat()
                pyautogui.press("ESC")
                self.wait_loading()
                continue
            if self.check_combat():
                self.wait_combat()
                pyautogui.press("ESC")
                self.wait_loading()
                continue
            press_time = random.randint(1, 9) / 5
            d = director[random.randint(0, 3)]
            pyautogui.keyDown(d)
            pyautogui.sleep(press_time)
            pyautogui.keyUp(d)

    def append_action_list(self, *args):
        action_list = args
        for action in action_list:
            if type(action) is Action:
                self.cur_action_list.append(action)
            elif type(action) is tuple or type(action) is list:
                self.append_action_list(*action)
            else:
                raise Exception("unknown action type")

    def debug_print_action_list(self):
        logger.debug("=====  print current action list start  =====")
        for action in self.cur_action_list:
            print(action)
        logger.debug("=====  print current action list end  =====")

    def do(self, *args):
        self.cur_action_list = []
        self.append_action_list(*args)
        self.debug_print_action_list()
        for action in self.cur_action_list:
            times = action.repeat if action.repeat else 1
            for _ in range(times):
                if action.ctrl:
                    if self.ctrl(action.ctrl) == SRH_SIG_STOP_ACTION:
                        logger.error("receive action stop signal")
                        return
                elif action.press:
                    pyautogui.press(action.press)
                elif action.keydown:
                    pyautogui.keyDown(action.keydown[0])
                    pyautogui.sleep(action.keydown[1])
                    pyautogui.keyUp(action.keydown[0])
                elif action.move:
                    pyautogui.moveTo(*action.move[:2], duration=SLEEP_TIME_SHORT)
                    if len(action.move) == 3:
                        pyautogui.click()
                elif action.click:
                    if action.click == 1:
                        pyautogui.click()
                    else:
                        self.click(action.click)
                elif action.drag:
                    self.drag(*action.drag, SLEEP_TIME_MIDDLE)
                if action.sleep:
                    pyautogui.sleep(action.sleep)
        return SRH_OK


if __name__ == '__main__':
    start_game()
    set_game_fg()
    p = Player()

    def test_case01():
        p.do(
            p.act_mgr.goto_calyx_golden_1,
            p.act_mgr.wait_loading,
            p.act_mgr.play_calyx,
            # p.act_mgr.add_support,
            p.act_mgr.start_game,
            p.act_mgr.wait_combat,
            p.act_mgr.home,
        )

    def test_case_02():
        # p.enter_game()

        p.do(
            p.act_mgr.assignment
        )


    test_case_02()

    # for _ in range(500):
    #     if p.check_loading():
    #         logger.info("in home")
    #     else:
    #         logger.error("not in home")
    #     time.sleep(0.2)
