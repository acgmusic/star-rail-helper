import subprocess
from common.utils import *
import win32com.client
import win32gui
from common.game_mgr import g_game

g_game_client = None


def start_exe_with_tmout(path):
    global g_game_client
    g_game_client = subprocess.Popen(path)
    return SRH_OK


def window_enumeration_handler(hwnd, windowlist):
    windowlist.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)))


def set_game_fg():
    rgx = g_usr_cfg["game_name"]
    windowlist = []
    win32gui.EnumWindows(window_enumeration_handler, windowlist)
    for i in windowlist:
        if i[2] == 'UnityWndClass' and (re.search(rgx, i[1]) is not None):
            g_game.proc_id = i[0]
            win32gui.ShowWindow(i[0], 4)
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(i[0])
            logger.info("set game[%d, %s, %s] as foreground window success." % (i[0], i[1], i[2]))
            return SRH_OK
    else:
        return SRH_FIND_NO_GAME


def start_game():
    if SRH_OK == set_game_fg():
        # here must sleep, for pyautogui can not work immediately after win32gui
        time.sleep(1)
        logger.info("game already start.")
        return SRH_OK
    rs_path = g_usr_cfg["game_path"]
    if not os.path.isfile(rs_path):
        logger.error("can not find game exe file: <%s>", rs_path)
        exit(SRH_NOT_FILE)
    ret = start_exe_with_tmout(rs_path)
    if SRH_OK != ret:
        logger.error("game start fail! path: <%s>." % (rs_path,))
        exit(ret)

    while times := 0 < MAX_TMOUT_GAME_START:
        times += 1
        if SRH_OK == set_game_fg():
            time.sleep(1)
            logger.info("game start success.")
            return SRH_OK
    return SRH_OK


if __name__ == '__main__':
    start_game()
