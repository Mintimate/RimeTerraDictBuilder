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

name: terra_rime_ice.base
version: "2023-11-29"
sort: by_weight
...
"""


def prepend_to_file(file_path, text_to_prepend):
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
def find_start_row(file_path, start_content):
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


def make_terra_dict(source_dict: pandas.DataFrame):
    """
    将普通拼音转换为地球拼音
    :param source_dict:
    :return:
    """
    new_terra_data = source_dict.apply(__pinyin_transform, axis=1)
    return new_terra_data


if __name__ == '__main__':
    # 查找开始读取的行号
    start_row = find_start_row(FILE_INPUT, '...')
    header = ['key', 'value', 'freq']
    # 确保找到了有效的行号，然后使用Pandas读取文件
    if start_row is not None:
        data = pd.read_csv(FILE_INPUT, sep='\t', names=header, skiprows=start_row + 1, comment='#')
        new_data = make_terra_dict(data)
        new_data.to_csv(FILE_OUTPUT, sep='\t', header=None, index=False)
        prepend_to_file(FILE_OUTPUT, NEW_HEADER_DESC)
    else:
        print("The specified content '...' was not found in the file.")
