from common.utils import *
import pyautogui


class GameMgr:
    proc_id = -1
    screen_width = pyautogui.size()[0]
    screen_height = pyautogui.size()[1]
    game_width = int(g_usr_cfg["resolution_ratio"][0])
    game_height = int(g_usr_cfg["resolution_ratio"][1]) + 40


class Positions:
    # position
    log_in = [500, 500]  # 登录按钮（任意屏幕中间位置）
    assignments = [1728, 410]  # 每日委托
    synthesize = [1596, 540]  # 合成
    camera = [1865, 614]  # 相机
    claim = [1466, 941]  # 每日委托领取
    three_point = [1748, 140]  # 手机界面右上角的三个点，里面有漫游签证
    trailblazer = [1660, 176]  # 漫游签证
    present = [1614, 471]  # 漫游签证礼物
    survival_index = [715, 235]  # 生存索引
    daily_training = [480, 235]  # 每日实训（必须先点生存索引，才能点击每日实训）
    daily_training_right_click = [731, 822]     # 每日实训，右侧空白点击一下后，才能用滚轮对右侧内容进行滚动
    sim_universe = [510, 360]   # 模拟宇宙
    calyx_golden = [510, 480]  # 拟造花萼赤
    calyx_crimson = [510, 600]  # 拟造花萼金
    stagnant_shadow = [510, 720]    # 凝滞虚影
    corrosion = [510, 840]    # 遗器
    echo_of_war = [510, 720]    # 周本
    forgotten_hall = [510, 840]     # 忘却之庭
    bud_of_destruction = [1477, 420]    # 毁灭之蕾

    # sub regions
    assignments_tab = [308, 226, 1124, 318]  # 每日委托界面，页签区域
    assignments_detail = [344, 323, 808, 909]  # 每日委托界面，详细信息区域


g_game = GameMgr()
g_pos = Positions()
