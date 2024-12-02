import os

from Terra8105Builder import terra_8105_make
from custom_tools import config_dict, say_somethings
from autoDownloadIceDict import download_dict_with_request
from autoDownloadIcePhrase import download_phrase_with_request
from TerraDictBuilder import terra_dict_start

USER_CONFIG = config_dict()
DOWNLOAD_DICT_ITEM = USER_CONFIG['rime_ice_dict']['dict_source_path']
DOWNLOAD_PHRASE_ITEM = USER_CONFIG['rime_ice_dict']['phrase_source_path']
DOWNLOAD_PATH = USER_CONFIG['rime_ice_dict']['source_download_dir']
CONVERT_TARGET = USER_CONFIG['rime_ice_dict']['target_download_dir']

if __name__ == '__main__':
    say_somethings("下载雾凇拼音字典")
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    if not os.path.exists(CONVERT_TARGET):
        os.makedirs(CONVERT_TARGET)
    for download_item in DOWNLOAD_DICT_ITEM:
        download_dict_with_request(source_save_path=DOWNLOAD_PATH, target_save_path=CONVERT_TARGET,
                                   download_url=DOWNLOAD_DICT_ITEM[download_item],
                                   target_file_name=download_item)
    say_somethings("下载雾凇短语词典")
    for download_item in DOWNLOAD_PHRASE_ITEM:
        download_phrase_with_request(source_save_path=DOWNLOAD_PATH, target_save_path=CONVERT_TARGET,
                                     download_url=DOWNLOAD_PHRASE_ITEM[download_item],
                                     target_file_name=download_item)
    say_somethings("构造地球评议基础词典")
    terra_8105_make()
    say_somethings("将其中的字典转换为地球拼音字典")
    terra_dict_start("./targetDict/rime_ice.base.dict.yaml",
                     "./targetDict/terra_rime_ice.base.dict.yaml",
                     "terra_rime_ice.base"
                     )
    terra_dict_start("./targetDict/rime_ice.ext.dict.yaml",
                     "./targetDict/terra_rime_ice.ext.dict.yaml",
                     "terra_rime_ice.ext"
                     )
