import os

from custom_tools import config_dict, say_somethings
from autoDownloaIceDict import download_dict_with_request
from TerraDictBuilder import terra_dict_start

USER_CONFIG = config_dict()
CN_DOWNLOAD_ITEM = USER_CONFIG['rime_ice_dict']['cn_source_path']
DOWNLOAD_PATH = USER_CONFIG['rime_ice_dict']['source_download_dir']
CONVERT_TARGET = USER_CONFIG['rime_ice_dict']['target_download_dir']

if __name__ == '__main__':
    say_somethings("下载雾凇拼音字典")
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    for download_item in CN_DOWNLOAD_ITEM:
        download_dict_with_request(source_save_path=DOWNLOAD_PATH, target_save_path=CONVERT_TARGET,
                                   download_url=CN_DOWNLOAD_ITEM[download_item], target_file_name=download_item)

    say_somethings("将其中的字典转换为地球拼音字典")
    terra_dict_start("./targetDict/rime_ice.base.yaml",
                     "./targetDict/terra_rime_ice.base.dict.yaml",
                     "terra_rime_ice.base"
                     )
