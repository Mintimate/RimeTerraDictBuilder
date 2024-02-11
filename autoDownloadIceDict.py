import os
import re

from custom_tools import say_somethings
import requests


def download_dict_with_request(source_save_path, target_save_path, download_url, target_file_name):
    say_somethings(f"开始下载 {download_url}")
    url = download_url
    file_name = url.split("/")[-1]
    r = requests.get(url)
    with open(os.path.join(source_save_path, file_name), 'w', encoding='utf-8') as f:
        f.write(r.text)
    __rename_dict_to_mint_style(
        os.path.join(source_save_path, file_name),
        os.path.join(target_save_path, target_file_name),
        target_file_name)


def __rename_dict_to_mint_style(source_path, target_path, file_name):
    # 读取文本文件内容
    with open(source_path, 'r', encoding='utf-8') as file:
        content = file.read()
    file_name = file_name.replace(".dict.yaml", "")
    # 替换name中的原本文件名
    content = re.sub(r'name:(\s*)(\S+)', f'name: {file_name}', content)

    # 将修改后的内容写回文件
    with open(target_path, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == '__main__':
    from custom_tools import config_dict
    USER_CONFIG = config_dict()
    DOWNLOAD_ITEM = USER_CONFIG['rime_ice_dict']['dict_source_path']
    DOWNLOAD_PATH = USER_CONFIG['rime_ice_dict']['source_download_dir']
    CONVERT_TARGET = USER_CONFIG['rime_ice_dict']['target_download_dir']
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    for download_item in DOWNLOAD_ITEM:
        download_dict_with_request(source_save_path=DOWNLOAD_PATH, target_save_path=CONVERT_TARGET,
                                   download_url=DOWNLOAD_ITEM[download_item], target_file_name=download_item)
