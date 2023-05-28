import re
import os
import yaml
from common.logger import logger
from common.error import *
from common.define import *
import time
import datetime

g_proj_path = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../"))


def get_abs_path(rel_path):
    return os.path.abspath(os.path.join(g_proj_path, rel_path))


def read_yaml(yaml_file: str) -> dict:
    with open(yaml_file, "r", encoding="utf-8") as f:
        file_data = f.read()
        yaml_data = yaml.full_load(file_data)
        return yaml_data


g_usr_cfg = read_yaml(get_abs_path(r"./config.yaml"))


def get_cur_time():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]


class TimeCounter:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_value, tb):
        self.end = time.time()
        print("cost time: " + str(self.end - self.start))


if __name__ == '__main__':
    with TimeCounter():
        for i in range(100000):
            pass

