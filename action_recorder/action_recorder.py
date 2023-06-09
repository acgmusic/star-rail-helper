#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import re
import time
import pprint
import tkinter
import threading
import traceback
from pynput.mouse import Listener as mlistener
from pynput.mouse import Controller as mcontroller
from pynput.keyboard import Key
from pynput.keyboard import Listener as klistener
from pynput.keyboard import Controller as kcontroller
import json
import datetime

SHIFT_DIFF = False


class recorder:
    def __init__(
            self,
            start_record_key='f7',
            stop_record_key='f7',
            start_repeat_key='f8',
            stop_repeat_key='f8',
            start_repeats_key='f9',
            stop_repeats_key='f9',
            close_key='esc',
            debug=True,
            debug_info=False,
            outclass=None,
    ):
        self.lock = threading.Lock()
        self.record = []
        self.debug = debug
        self.debug_info = debug_info
        self.start_record_key = start_record_key
        self.stop_record_key = stop_record_key
        self.start_repeat_key = start_repeat_key
        self.stop_repeat_key = stop_repeat_key
        self.start_repeats_key = start_repeats_key
        self.stop_repeats_key = stop_repeats_key
        self.close_key = close_key
        self.record_status = 'stop'  # only [start or stop]
        self.repeat_status = 'stop'  # only [start or stop]
        self.unrecord_key = [
            self.start_record_key,
            self.stop_record_key,
            self.start_repeat_key,
            self.stop_repeat_key,
            self.start_repeats_key,
            self.stop_repeats_key,
            self.close_key,
        ]
        self.outclass = outclass
        self.key_hook = getattr(self.outclass, 'key_hook', None)
        if self.key_hook:
            self.unrecord_key.extend(list(self.key_hook))

        self.keyboard_listen_thread = None
        self.mouse_listen_thread = None
        self.main_keybord_thread = None
        self.speed = 1.0

    def safe_add_action(self, msg):
        with self.lock:
            self.record.append(msg)
        if self.debug_info:
            print('{} {} {}'.format(msg['type'], msg['action'], msg['time']))
            if msg['type'] == 'mouse':
                if msg['action'] == 'scroll':
                    print('    scroll:{}'.format((msg['x'], msg['y'], msg['dx'], msg['dy'])))
                else:
                    print('    xy:{}'.format((msg['x'], msg['y'])))
            if msg['type'] == 'keyboard':
                print('    key:{}'.format(msg['key']))

    def on_move(self, x, y):
        msg = {}
        msg['type'] = 'mouse'
        msg['action'] = 'move'
        msg['time'] = time.time()
        msg['x'], msg['y'] = x, y
        self.safe_add_action(msg)

    def on_click(self, x, y, button, pressed):
        msg = {}
        msg['type'] = 'mouse'
        msg['action'] = 'press' if pressed else 'release'
        msg['time'] = time.time()
        msg['x'], msg['y'] = x, y
        msg['button'] = button
        self.safe_add_action(msg)

    def on_scroll(self, x, y, dx, dy):
        msg = {}
        msg['type'] = 'mouse'
        msg['action'] = 'scroll'
        msg['time'] = time.time()
        msg['x'], msg['y'] = x, y
        msg['dx'], msg['dy'] = dx, dy
        self.safe_add_action(msg)

    def on_press(self, key):
        msg = {}
        msg['type'] = 'keyboard'
        msg['action'] = 'press'
        msg['time'] = time.time()
        msg['key'] = key
        self.safe_add_action(msg)
        if key == Key.shift and not SHIFT_DIFF:
            msg = msg.copy()  # 由于某些原因，shift 必须与 shift_r 配合才能实现 “shift选中”
            msg['key'] = Key.shift_r  # 所以这里将 “按下shift” 粗暴的填充为同时按下 左右shift。通常不会有影响
            self.safe_add_action(msg)  # 相较于左右shift的区分，shift 处理文本时的选中更为重要

    def on_release(self, key):
        msg = {}
        msg['type'] = 'keyboard'
        msg['action'] = 'release'
        msg['time'] = time.time()
        msg['key'] = key
        self.safe_add_action(msg)
        if key == Key.shift and not SHIFT_DIFF:
            msg = msg.copy()
            msg['key'] = Key.shift_r
            self.safe_add_action(msg)

    def start_record(self):
        self.record.clear()
        self.mouse_listen_thread = mlistener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.keyboard_listen_thread = klistener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.mouse_listen_thread.start()
        self.keyboard_listen_thread.start()
        self.mouse_listen_thread.join()
        self.keyboard_listen_thread.join()

    def repeat_times(self, times=1):
        mouse = mcontroller()
        keyboard = kcontroller()
        record_data = self.record
        self.repeat_stop_toggle = False
        for _ in range(times):
            if not record_data:
                self.record_status = 'stop'
                print('error empty record.')
                return
            action_start_time = record_data[0]['time']
            for idx, action in enumerate(record_data):
                if self.repeat_stop_toggle:
                    return
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
                    if getattr(action['key'], 'name', None) not in self.unrecord_key:
                        getattr(keyboard, action['action'])(action['key'])
                if self.speed: time.sleep(gtime / self.speed)
                action_start_time = action['time']
        self.hook_repeat_stop('force_stop')

    def hook_record_start(self, key):
        if key == getattr(Key, self.start_record_key) and self.record_status == 'stop':
            try:
                self.hook_repeat_stop('force_stop')
            except:
                traceback.print_exc()
            self.record_status = 'start'
            threading.Thread(target=self.start_record).start()
            if self.debug: print('{} record start.'.format(key))
            return True

    def hook_record_stop(self, key):
        ''' force_stop 是为了处理在未结束录制时就开始 repeat 时的问题。可以强制结束录制行为。 '''
        if (key == getattr(Key, self.stop_record_key) and self.record_status == 'start') or key == 'force_stop':
            self.record_status = 'stop'
            if self.keyboard_listen_thread: self.keyboard_listen_thread.stop()
            if self.mouse_listen_thread:    self.mouse_listen_thread.stop()
            if self.debug: print('{} record stop.'.format(key))
            return True

    def hook_repeat_start(self, key):
        if (key == getattr(Key, self.start_repeat_key) or key == getattr(Key, self.start_repeats_key)) \
                and self.repeat_status == 'stop':
            if self.record_status == 'start': self.hook_record_stop('force_stop')
            self.repeat_status = 'start'
            args = (1,) if key == getattr(Key, self.start_repeat_key) else (100000000,)
            threading.Thread(target=self.repeat_times, args=args).start()
            if self.debug: print('{} repeat start.'.format(key))
            return True

    def hook_repeat_stop(self, key):
        if ((key == getattr(Key, self.stop_repeat_key) or key == getattr(Key, self.stop_repeats_key)) \
            and self.repeat_status == 'start') or key == 'force_stop':
            self.repeat_status = 'stop'
            self.repeat_stop_toggle = True
            if self.debug: print('{} repeat stop.'.format(key))
            return True

    def hook_main_stop(self, key):
        if (key == getattr(Key, self.close_key)) or key == 'force_stop':
            if self.main_keybord_thread: self.main_keybord_thread.stop()
            if self.debug: print('{} tool stop.'.format(key))
            return True

    def hook_outclass_stop(self, key):
        if self.outclass:
            try:
                self.outclass.close_sign()
            except:
                traceback.print_exc()

    def hook_outclass(self, key):
        for _key in self.key_hook:
            if key == getattr(Key, _key):
                self.key_hook[_key]()

    def main_keybord(self, key):
        self.hook_record_start(key) or self.hook_record_stop(key)
        self.hook_repeat_start(key) or self.hook_repeat_stop(key)
        self.hook_outclass(key)
        if self.hook_main_stop(key):
            self.hook_outclass_stop(key)

    def start(self):
        self.main_keybord_thread = klistener(on_release=self.main_keybord)
        self.main_keybord_thread.start()
        self.main_keybord_thread.join()


from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Toplevel
from tkinter.font import Font
import tkinter.messagebox

Frame = tkinter.Frame
Text = scrolledtext.ScrolledText
Label = ttk.Label
TTKButton = ttk.Button
Combobox = ttk.Combobox
hidden = True

info = '''
录制工具方法介绍：
F7  开始/停止录制
F8  执行/停止录制好的任务
F9  执行/停止录制好的任务(重复执行)
F10 生成代码
ESC 关闭工具
'''.strip()

warning = '''
**注意：
原因：某些环境无法实现 shift 选中文本
方法:在代码中左右 shift 同时按,实现选中文本
为兼容，默认每次同时按下左右 shift
若取消，将 “是否区分左右shift” 设置为“是”即可
'''.strip()

record_code = '''
#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from pynput.keyboard import Key
from pynput.keyboard import Controller as kcontroller
from pynput.mouse import Controller as mcontroller
from pynput.mouse import Button
record_data = $record_data
def repeat_times(record_data, times=1, speed=1.0):
    mouse = mcontroller()
    keyboard = kcontroller()
    for _ in range(times):
        if not record_data:
            print('error empty record.')
            return
        action_start_time = record_data[0]['time']
        for idx,action in enumerate(record_data):
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
                if getattr(action['key'], 'name', None) not in $unrecord_key:
                    getattr(keyboard, action['action'])(action['key'])
            if speed:
                time.sleep(gtime/speed)
            action_start_time = action['time']
if __name__ == '__main__':
    speed = $speed
    repeat_times(record_data, speed=speed)
'''.strip()


class recorder_gui:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("键盘鼠标操作录制工具")
        # Button(self.root, text='置顶',command=self.topWin).pack(side=tkinter.TOP, padx=3)
        self.key_hook = {'f10': self.create_code}
        # 这里 outclass 是为了能在 recorder 内的关闭函数中接收关闭信号函数
        self.recorder = recorder(outclass=self)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.close_sign = self.on_closing
        self.ft = Font(family='Consolas', size=10)
        Label(self.root, text=info, font=self.ft).pack(padx=5)

        fr = Frame(self.root)
        fr.pack(fill=tkinter.X)
        Label(fr, text='速度 [执行速度,None模式慎用]', font=self.ft).pack(side=tkinter.LEFT, padx=5)
        self.cbx = Combobox(fr, width=5, state='readonly')
        self.cbx['values'] = (0.5, 1.0, 1.5, 2.5, 6.5, 17.5, 37.0, 67.5, 115.0, 'None')
        # 默认速度设置为：1.0
        self.cbx.current(1)
        self.cbx.pack(side=tkinter.RIGHT)
        self.cbx.bind('<<ComboboxSelected>>', self.change_speed)
        fr = Frame(self.root)
        fr.pack(fill=tkinter.X)
        Label(fr, text='是否区分左右shift [推荐默认否]', font=self.ft).pack(side=tkinter.LEFT, padx=5)
        self.cbx2 = Combobox(fr, width=5, state='readonly')
        self.cbx2['values'] = ('否', '是')
        self.cbx2.current(0)
        self.cbx2.pack(side=tkinter.RIGHT)
        self.cbx2.bind('<<ComboboxSelected>>', self.change_shift_diff)
        TTKButton(self.root, text='注意事项', command=self.create_warning).pack(fill=tkinter.X)
        TTKButton(self.root, text='生成代码', command=self.create_code).pack(fill=tkinter.X)
        self.txt = Text(self.root, width=30, height=11, font=self.ft)
        self.txt.pack(fill=tkinter.BOTH, expand=True)
        global print
        print = self.print
        try:
            from idlelib.colorizer import ColorDelegator
            from idlelib.percolator import Percolator
            p = ColorDelegator()
            Percolator(self.txt).insertfilter(p)
        except:
            traceback.print_exc()

    def topWin(self):
        tp = Toplevel(self.root)
        tp.attributes('-topmost', True)

    def _recorder_close(self):
        self.recorder.hook_repeat_stop('force_stop')
        self.recorder.hook_record_stop('force_stop')
        self.recorder.hook_main_stop('force_stop')

    def on_closing(self):
        self._recorder_close()
        toggle = tkinter.messagebox.askokcancel('关闭', '是否关闭工具？')
        if toggle:
            # 关闭前必须显示且置顶，否则 tkinter 窗口会滞黏
            self.root.wm_attributes('-toolwindow', 1)
            self.root.wm_attributes('-topmost', 1)
            self.root.quit()
        else:
            self.recorder.start()

    def start(self):
        threading.Thread(target=self.recorder.start).start()
        self.root.mainloop()

    def create_code(self):
        self.recorder.hook_record_stop('force_stop')
        self.recorder.hook_repeat_stop('force_stop')

        def format_record_data(record_data):
            _filter = lambda string: string.group(0).rsplit(':', 1)[0].replace('<', '') + ','
            record_data = re.sub(r"'key': <[^\n]+>,", _filter, record_data)
            record_data = re.sub(r"'button': <[^\n]+>,", _filter, record_data)
            return record_data

        unrecord_key = str(list(set(self.recorder.unrecord_key)))
        record_data = format_record_data(pprint.pformat(self.recorder.record, indent=2, width=200))
        self.clear_txt()
        speed = 'None' if self.cbx.get() == 'None' else self.cbx.get()

        output = self.recorder.record[:]
        end = 0
        for i, item in enumerate(output):
            if "button" in item:
                if item["button"].name == "left":
                    item["button"] = "Button.left"
                else:
                    item["button"] = "Button.right"
            if "key" in item:
                if item["key"].name == "f7":
                    end = i
                    break
        output = output[:end]
        data = json.dumps(output)
        fn = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3] + ".json"
        with open("../resource/map_data/" + fn, "w", encoding="utf-8") as f:
            f.write(data)

    def create_warning(self):
        self.clear_txt()
        global hidden
        # 判断是否隐藏，首次点击显示，再次点击不显示
        if hidden:
            print(warning)
            hidden = False
        else:
            hidden = True

    # 清空内容
    def clear_txt(self):
        self.txt.delete(0., tkinter.END)

    def print(self, *a):
        text = ' '.join(map(str, a)) + '\n'
        self.txt.insert(tkinter.END, text)
        self.txt.see(tkinter.END)

    # 更改鼠标点击速度
    def change_speed(self, *a):
        self.recorder.speed = None if self.cbx.get() == 'None' else float(self.cbx.get())

    # 更改是否左右区分 sifter
    def change_shift_diff(self, *a):
        global SHIFT_DIFF
        SHIFT_DIFF = True if self.cbx2.get() == '是' else False


def execute():
    recorder_gui().start()


if __name__ == '__main__':
    recorder_gui().start()
