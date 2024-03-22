import os

import requests

from custom_tools import say_somethings, config_dict

USER_CONFIG = config_dict()
DOWNLOAD_DICT_ITEM = USER_CONFIG['rime-radical-pinyin']['dict_source_path']
CONVERT_TARGET = USER_CONFIG['rime-radical-pinyin']['target_download_dir']


def download_dict_with_request(target_save_path, download_url, target_file_name):
    say_somethings(f"开始下载 {download_url}")
    url = download_url
    r = requests.get(url)
    with open(os.path.join(target_save_path, target_file_name), 'w', encoding='utf-8') as f:
        f.write(r.text)


if __name__ == '__main__':
    if not os.path.exists(CONVERT_TARGET):
        os.makedirs(CONVERT_TARGET)
    for download_item in DOWNLOAD_DICT_ITEM:
        download_dict_with_request(target_save_path=CONVERT_TARGET,download_url=DOWNLOAD_DICT_ITEM[download_item],
                                   target_file_name=download_item)
