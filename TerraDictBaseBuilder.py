import pandas as pd

# 雾凇拼音 8105
FILE_ICE_DICT = "./sourceDict/8105.dict.yaml"
# 地球拼音基础
FILE_TERRA_DICT = "./sourceDict/terra_pinyin_base.dict.yaml"
# 输出文件
FILE_OUTPUT = "./targetDict/terra_pinyin_base.dict.yaml"

# 输出文件的头部
NEW_HEADER_DESC = """
# Rime dictionary
# encoding: utf-8

# 使用Python3 pypinyin 自动转换
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
max_phrase_length: 7
min_phrase_weight: 100
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


def read_keymap_from_ice():
    # 查找开始读取的行号
    start_row = __find_start_row(FILE_ICE_DICT, '...')
    header = ['key', 'value', 'freq']
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(FILE_ICE_DICT, sep='\t', names=header, skiprows=start_row + 1, comment='#')
    else:
        print("The specified content '...' was not found in the file.")
    return data


def read_keymap_from_terra():
    # 查找开始读取的行号
    start_row = __find_start_row(FILE_TERRA_DICT, '...')
    header = ['key', 'value', 'freq']
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(FILE_TERRA_DICT, sep='\t', names=header, skiprows=start_row + 1, comment='#')
    else:
        print("The specified content '...' was not found in the file.")
    return data

if __name__ == '__main__':
    ice_data = read_keymap_from_ice()
    ice_keymap = ice_data.set_index('key')['freq'].to_dict()
    terra_data = read_keymap_from_terra()
    for terra_row in terra_data.iterrows():
        key = terra_row[1]['key']
        if key in ice_keymap:
            terra_row[1]['freq'] = ice_keymap[key]
        else:
            terra_row[1]['freq'] = 1
    terra_data.to_csv(FILE_OUTPUT, sep='\t', header=None, index=False)
    new_header_desc_string = NEW_HEADER_DESC.format(name_placeholder="terra_pinyin_base", version_placeholder="20241030")
    __prepend_to_file(FILE_OUTPUT, new_header_desc_string)
