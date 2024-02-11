import re
from datetime import date

import pandas
import pandas as pd
from pypinyin import Style, lazy_pinyin

# 文件路径
FILE_INPUT = './sourceDict/rime_ice.base.dict.yaml'
FILE_OUTPUT = './targetDict/terra_rime_ice.base.dict.yaml'

# 输出文件的头部
NEW_HEADER_DESC = """
# 使用Python3 pypinyin 自动转换
# Project: https://github.com/Mintimate/RimeTerraDictBuilder
# WebSite:
#  - 薄荷输入法: https://www.mintimate.cc
#  - Mintimate's Blog: https://www.mintimate.cn
#  - Mintimate's Bilibili: https://space.bilibili.com/355567627
---

name: {name_placeholder}
version: "{version_placeholder}"
sort: by_weight
...
"""


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


# 辅助函数，用于查找包含特定内容的行号
def __find_start_row(file_path, start_content):
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # 检查行内容
            if start_content in line:
                return i
    # 如果没有找到，返回None
    return None


def __pinyin_transform(row):
    """
    将普通拼音转换为地球拼音
    :param row:
    :return:
    """
    # 将拼音转换为汉语拼音，使用pypinyin库并开启第五音
    pinyin_result = lazy_pinyin(row['key'], style=Style.TONE3, neutral_tone_with_five=True)
    new_value = ' '.join(pinyin_result)
    return pd.Series({'key': row['key'], 'new_value': new_value, 'freq': row['freq']})


def __make_terra_dict(source_dict: pandas.DataFrame):
    """
    将普通拼音转换为地球拼音
    :param source_dict:
    :return:
    """
    new_terra_data = source_dict.apply(__pinyin_transform, axis=1)
    return new_terra_data


def __get_version_code(source_path):
    # 读取文本文件内容
    with open(source_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取version内容
    match = re.search(r'version:\s*"([^"]+)"', content)

    # 提取到的版本号
    if match:
        version = match.group(1)
        return version
    else:
        # 如果没有找到版本号，使用当前日期作为版本号
        today = date.today()
        return today.strftime("%Y-%m-%d")


def terra_dict_start(file_input_path=FILE_INPUT, file_output_path=FILE_OUTPUT
                     , name='terra_rime_ice.base', version=None):
    # 查找开始读取的行号
    start_row = __find_start_row(file_input_path, '...')
    header = ['key', 'value', 'freq']
    if version is None:
        version = __get_version_code(file_input_path)
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(file_input_path, sep='\t', names=header, skiprows=start_row + 1, comment='#')
        new_data = __make_terra_dict(data)
        new_data.to_csv(file_output_path, sep='\t', header=None, index=False)
        new_header_desc_string = NEW_HEADER_DESC.format(name_placeholder=name, version_placeholder=version)
        __prepend_to_file(file_output_path, new_header_desc_string)
    else:
        print("The specified content '...' was not found in the file.")


if __name__ == '__main__':
    terra_dict_start()
