from common.define import *


class Action:
    def __init__(self, ctrl=None, click=None, move=None, drag=None,
                 scroll=None, press=None, keydown=None, sleep=None, repeat=None):
        self.ctrl = ctrl
        self.click = click
        self.move = move
        self.drag = drag
        self.scroll = scroll
        self.press = press
        self.keydown = keydown
        self.sleep = sleep
        self.repeat = repeat

    def __repr__(self):
        return f"Action(ctrl={self.ctrl}, click={self.click}, move={self.move }, drag={self.drag}, " \
               f"scroll={self.scroll}, press={self.press}, keydown={self.keydown}, sleep={self.sleep}, " \
               f"repeat={self.repeat})"


class ActMgr:
    def __init__(self):
        # 打开生存索引
        self.open_survival_index = (
            Action(ctrl="home"),
            Action(press="F4", sleep=SLEEP_TIME_NORMAL),
            Action(click=[715, 235]),
        )
        # 传送模拟宇宙
        self.goto_sim_universe = (
            self.open_survival_index,
            Action(click=[510, 360]),
            Action(click=[1474, 533]),
            Action(ctrl="wait_loading")
        )
        # 传送：回忆之蕾·拟造花萼（金）
        self.goto_calyx_golden_1 = (
            self.open_survival_index,
            Action(click=[510, 480]),
            Action(click=[1475, 420]),
        )
        # 传送：以太之蕾·拟造花萼（金）
        self.goto_calyx_golden_2 = (
            self.open_survival_index,
            Action(click=[510, 480]),
            Action(click=[1475, 600]),
        )
        # 传送：藏珍之蕾·拟造花萼（金）
        self.goto_calyx_golden_3 = (
            self.open_survival_index,
            Action(click=[510, 480]),
            Action(click=[1475, 780]),
        )
        # 传送：毁灭之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_1 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(click=[1475, 420]),
        )
        # 传送：存护之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_2 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(click=[1475, 600]),
        )
        # 传送：巡猎之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_3 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(click=[1475, 780]),
        )
        # 传送：丰饶之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_4 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 470]),
        )
        # 传送：智识之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_5 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 650]),
        )
        # 传送：同谐之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_6 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 830]),
        )
        # 传送：虚无之蕾·拟造花萼（赤）
        self.goto_calyx_crimson_7 = (
            self.open_survival_index,
            Action(click=[510, 600]),
            Action(drag=([1300, 850], [1300, 400]), repeat=2, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 830]),
        )
        # 传送：空海之形·凝滞虚影
        self.goto_stagnant_shadow_1 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(click=[1475, 420]),
        )
        # 传送：巽风之形·凝滞虚影
        self.goto_stagnant_shadow_2 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(click=[1475, 600]),
        )
        # 传送：鸣雷之形·凝滞虚影
        self.goto_stagnant_shadow_3 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(click=[1475, 780]),
        )
        # 传送：炎华之形·凝滞虚影
        self.goto_stagnant_shadow_4 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 420]),
        )
        # 传送：锋芒之形·凝滞虚影
        self.goto_stagnant_shadow_5 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 600]),
        )
        # 传送：霜晶之形·凝滞虚影
        self.goto_stagnant_shadow_6 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 780]),
        )
        # 传送：幻光之形·凝滞虚影
        self.goto_stagnant_shadow_7 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), repeat=2, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 470]),
        )
        # 传送：冰棱之形·凝滞虚影
        self.goto_stagnant_shadow_8 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), repeat=2, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 650]),
        )
        # 传送：震厄之形·凝滞虚影
        self.goto_stagnant_shadow_9 = (
            self.open_survival_index,
            Action(click=[510, 720]),
            Action(drag=([1300, 850], [1300, 400]), repeat=2, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 830]),
        )
        # 传送：漂泊之径·侵蚀隧洞
        self.goto_corrosion_1 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(click=[1475, 420]),
        )
        # 传送：圣颂之径·侵蚀隧洞
        self.goto_corrosion_2 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(click=[1475, 600]),
        )
        # 传送：野焰之径·侵蚀隧洞
        self.goto_corrosion_3 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(click=[1475, 780]),
        )
        # 传送：霜风之径·侵蚀隧洞
        self.goto_corrosion_4 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(drag=([1300, 850], [1300, 400]), repeat=1, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 470]),
        )
        # 传送：迅拳之径·侵蚀隧洞
        self.goto_corrosion_5 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(drag=([1300, 850], [1300, 400]), repeat=1, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 650]),
        )
        # 传送：睿治之径·侵蚀隧洞
        self.goto_corrosion_6 = (
            self.open_survival_index,
            Action(click=[510, 840]),
            Action(drag=([1300, 850], [1300, 400]), repeat=1, sleep=SLEEP_TIME_NORMAL),
            Action(click=[1475, 830]),
        )
        # 传送：毁灭的开端·历战余响
        self.goto_echo_of_war_1 = (
            self.open_survival_index,
            Action(drag=([500, 830], [500, 400]), repeat=1, sleep=SLEEP_TIME_NORMAL),
            Action(click=[510, 700]),
            Action(click=[1475, 600]),
        )
        # 传送：寒潮的落幕·历战余响
        self.goto_echo_of_war_2 = (
            self.open_survival_index,
            Action(drag=([500, 830], [500, 400]), repeat=1, sleep=SLEEP_TIME_NORMAL),
            Action(click=[510, 700]),
            Action(click=[1475, 780]),
        )
        # (先传送，睡眠)打6把拟造花萼(不点开始挑战)
        self.play_calyx = (
            Action(click=[1840, 937], repeat=5),
            Action(click=[1605, 1020]),
        )
        # 选择支援
        self.add_support = (
            Action(ctrl="add_support")
        )
        # 等待加载
        self.wait_loading = (
            Action(sleep=SLEEP_TIME_VERY_LONG)
        )
        # 开始挑战
        self.start_game = (
            Action(click=[1670, 1020], sleep=SLEEP_TIME_NORMAL),
        )
        # 完成挑战（忘却之庭）
        self.combat_commit = (
            Action(click=[955, 995], sleep=SLEEP_TIME_SHORT),
            Action(click=[410, 1000], sleep=SLEEP_TIME_SHORT),
        )
        self.one_more_time = (
            Action(click=[1485, 1000], sleep=SLEEP_TIME_MIDDLE),
        )
        # 等待战斗完成
        self.wait_combat = (
            Action(ctrl="wait_combat"),
        )
        # 回家
        self.home = (
            Action(ctrl="home"),
        )
        # 关闭提示
        self.close_warning = (
            Action(ctrl="close_warning"),
        )
        # 派遣
        self.assignment = (
            Action(ctrl="home"),
            Action(press="ESC", sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1730, 410], sleep=SLEEP_TIME_NORMAL),
            Action(ctrl="assignment"),
        )
        # 关闭提示，如果发现提示信息，则提前退出。
        # 场景：1. 判断周本是否达到3次上限
        self.close_warning_and_stop = (
            Action(ctrl="close_warning_and_stop"),
        )
        # 传送到黑塔基地
        self.goto_herta = (
            self.goto_sim_universe,
            Action(press="ESC")
        )
        # 传送雅利洛VI
        self.goto_jarilo_vi = (
            self.goto_calyx_golden_2,
        )
        # 传送到仙舟
        self.goto_xianzhou = (
            self.goto_corrosion_6,
        )

        # 打周本
        self.play_echo_of_war_1 = (
            self.goto_echo_of_war_1,
            self.wait_loading,
            self.start_game,
            self.close_warning_and_stop,
            self.add_support,
            self.start_game,
            self.wait_combat,
            self.one_more_time,
        )
        self.play_echo_of_war_2 = (
            self.goto_echo_of_war_2,
            self.wait_loading,
            self.start_game,
            self.close_warning_and_stop,
            self.add_support,
            self.start_game,
            self.wait_combat,
            self.one_more_time,
        )

        # 每日任务：拍照
        self.camera = (
            Action(ctrl="home"),
            Action(press="ESC", sleep=SLEEP_TIME_NORMAL),
            Action(click=[1860, 615], sleep=SLEEP_TIME_NORMAL),
            Action(press="F", sleep=SLEEP_TIME_NORMAL),
            Action(press="ESC", repeat=2, sleep=SLEEP_TIME_NORMAL),
        )
        # 每日任务：忘却之庭
        self.goto_forgotten_hall = (
            self.open_survival_index,
            Action(drag=([500, 830], [500, 400]), sleep=SLEEP_TIME_NORMAL),
            Action(click=[500, 830], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1470, 590], sleep=SLEEP_TIME_LONG),
            Action(ctrl="wait_loading"),
            Action(drag=([60, 200], [1800, 200]), repeat=5),
            Action(click=[580, 670], sleep=SLEEP_TIME_NORMAL),
            Action(click=[115, 250], sleep=SLEEP_TIME_SHORT),
            Action(click=[250, 250], sleep=SLEEP_TIME_SHORT),
            Action(click=[370, 250], sleep=SLEEP_TIME_SHORT),
            Action(click=[500, 250], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1700, 1030], sleep=SLEEP_TIME_MIDDLE),
            Action(ctrl="wait_loading", sleep=SLEEP_TIME_LONG),
            Action(press="ESC", sleep=SLEEP_TIME_LONG),
            Action(keydown=("w", 4)),
            Action(click=1, sleep=SLEEP_TIME_VERY_LONG),
            Action(ctrl="wait_combat"),
            self.combat_commit,
            Action(ctrl="wait_loading"),
        )
        # 每日任务： 累积释放2次秘技
        self.use_skill_twice = (
            Action(ctrl="home", sleep=SLEEP_TIME_MIDDLE),
            Action(press="E", sleep=SLEEP_TIME_VERY_LONG, repeat=2),
        )
        # 每日任务：分解遗器(分解失败不会报错)
        self.salvage_relics = (
            Action(ctrl="home"),
            Action(press="B", sleep=SLEEP_TIME_NORMAL),
            Action(click=[820, 100], sleep=SLEEP_TIME_SHORT),
            Action(click=[1230, 1025], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[535, 1020], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1425, 380], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1650, 380], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1725, 1025], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[575, 300], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1725, 1025], sleep=SLEEP_TIME_MIDDLE),
            Action(click=[1160, 830], sleep=SLEEP_TIME_MIDDLE),
        )
        # 每日任务：合成消耗品、合成材料
        self.daily_synthesize = (
            Action(ctrl="home"),
            Action(press="ESC", sleep=SLEEP_TIME_NORMAL),
            Action(click=[1600, 540], sleep=SLEEP_TIME_NORMAL),
            Action(click=[800, 100], sleep=SLEEP_TIME_NORMAL),
            Action(click=[1170, 1000], sleep=SLEEP_TIME_NORMAL),
            Action(click=[1160, 735], sleep=SLEEP_TIME_VERY_LONG),
            Action(press="ESC", sleep=SLEEP_TIME_SHORT),
            Action(click=[900, 100], sleep=SLEEP_TIME_NORMAL),
            Action(click=[1170, 1000], sleep=SLEEP_TIME_NORMAL),
            Action(click=[1160, 735], sleep=SLEEP_TIME_NORMAL),
        )




if __name__ == '__main__':
    mgr = ActMgr()
    print(mgr.open_survival_index[0].ctrl)
    print(type(mgr.open_survival_index))
