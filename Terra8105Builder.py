import os.path
from datetime import date

import pandas as pd
from pypinyin import lazy_pinyin, Style

# 雾凇拼音
FILE_ICE_DICT_8105 = "./sourceDict/8105.dict.yaml"
# 地球拼音基础
FILE_TERRA_DICT = "./asserts/terraMap8105.yaml"
# 输出文件
FILE_OUTPUT = "./targetDict/terra.8105.dict.yaml"

# 输出文件的头部
NEW_HEADER_DESC = """
# Rime dictionary
# encoding: utf-8

# 加工逻辑:
#  - 从雾凇拼音读取拼音表
#  - 从地球拼音人工复合词表读取拼音表(感谢 @Jian787 的人工复合)
# Project: https://github.com/Mintimate/RimeTerraDictBuilder
# WebSite:
#  - 薄荷输入法: https://www.mintimate.cc
#  - Mintimate's Blog: https://www.mintimate.cn
#  - Mintimate's Bilibili: https://space.bilibili.com/355567627

# referenced works:
# CC-CEDICT
# community maintained free chinese-english dictionary.
#
# published by MDBG
#
# license:
# creative commons attribution-share alike 3.0
# http://creativecommons.org/licenses/by-sa/3.0/
#
# http://cc-cedict.org/wiki/

---

name: {name_placeholder}
version: "{version_placeholder}"
sort: by_weight
...
"""


# 辅助函数，用于查找包含特定内容的行号
def __find_start_row(file_path, start_content):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            # 检查行内容
            if start_content in line:
                return i
    # 如果没有找到，返回None
    return None


def __prepend_to_file(file_path, text_to_prepend):
    """
    在文件开头插入内容
    :param file_path:
    :param text_to_prepend:
    :return:
    """
    # 首先，读取原始文件的内容
    with open(file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()

    # 接着，将新的头部内容和原始内容合并
    new_content = text_to_prepend.strip() + '\n\n' + original_content

    # 最后，将合并后的内容写入同一文件，从而覆盖它
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


def __pinyin_transform_key(key):
    """
    将普通拼音转换为地球拼音
    :param key: 普通字
    :return:
    """
    # 将拼音转换为汉语拼音，使用pypinyin库并开启第五音
    pinyin_result = lazy_pinyin(key, style=Style.TONE3, neutral_tone_with_five=True)
    new_value = ' '.join(pinyin_result)
    return new_value


def __read_keymap_from_ice(dict_source):
    """
    从雾凇拼音读取拼音表
    :param dict_source:
    :return:
    """
    # 查找开始读取的行号
    start_row = __find_start_row(dict_source, '...')
    header = ['key', 'value', 'freq']
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(dict_source, sep='\t', names=header, skiprows=start_row + 1, comment='#')
    else:
        print("The specified content '...' was not found in the file.")
        exit(-1)
    return data


def __read_keymap_from_terra(dict_source):
    # 查找开始读取的行号
    start_row = __find_start_row(dict_source, '...') if None else 0
    header = ['key', 'value', 'freq']
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(dict_source, sep='\t', names=header, skiprows=start_row + 1, comment='#')
    else:
        print("The specified content '...' was not found in the file.")
        exit(-1)
    return data


def terra_8105_make():
    # 读取雾凇拼音构造词频表
    ice_data_8105 = __read_keymap_from_ice(FILE_ICE_DICT_8105)
    ice_keymap = ice_data_8105.set_index('key')['freq'].to_dict()
    # 读取地球拼音人工复合词表
    terra_data = __read_keymap_from_terra(FILE_TERRA_DICT)
    terra_keyFreqMap = terra_data.set_index('key')['freq'].to_dict()
    terra_keyValueMap = terra_data.set_index('key')['value'].to_dict()
    # 用于结果输出
    result = list()
    for ice_row in ice_data_8105.iterrows():
        key = ice_row[1]['key']
        if key in terra_keyValueMap:
            continue
        result.append({'key': key, 'value': __pinyin_transform_key(key), 'freq': ice_row[1]['freq']})
    # 使用地球拼音人工复合词表补充
    for terra_patch_row in terra_data.iterrows():
        result.append({'key': terra_patch_row[1]['key'], 'value': terra_patch_row[1]['value'],
                       'freq': terra_patch_row[1]['freq']})
    # list 转换为 DataFrame
    resultDataFrame = pd.DataFrame(result)
    resultDataFrame.to_csv(FILE_OUTPUT, sep='\t', header=None, index=False)
    # 当前日期 YYYYMMDD
    versionCode = date.today().strftime("%Y%m%d")
    terra_output_name = os.path.basename(FILE_OUTPUT).replace('.dict.yaml', '')
    new_header_desc_string = NEW_HEADER_DESC.format(name_placeholder=terra_output_name,
                                                    version_placeholder=versionCode)
    __prepend_to_file(FILE_OUTPUT, new_header_desc_string)


if __name__ == '__main__':
    terra_8105_make()
    print("地球拼音词典构造完成")