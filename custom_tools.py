from datetime import datetime

import yaml


def config_dict():
    """
    加载配置文件
    :return:
    """

    # 读取配置文件
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config


def say_somethings(message, print_time=True):
    """
    打印信息
    :return:
    """
    if print_time:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {message}")
    else:
        print(message)
