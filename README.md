## Rime 地球拼音词典构建器

该脚本使用 Python 3 和 `pypinyin` 库，辅助将 Rime 词典文件转换为地球拼音（Terra Pinyin）格式。

## 概述

使用 Pandas 读取Rime 词典文件，将其中的拼音转换为带声调的地球拼音格式，并生成一个新的 Rime 词典文件以供使用。

## 功能特点

- 读取现有 Rime 词典文件。
- 利用 `pypinyin` 将标准拼音转换为带有第五声（轻声）的地球拼音。
- 在输出文件中添加头部描述，定义 Rime 词典的元信息。
- 可根据需求修改转换规则或不同 Rime 词典格式。

## 依赖

确保安装了 `pandas` 和 `pypinyin`。您可以使用以下命令安装这些依赖项：

```bash
pip install pandas pypinyin
```

## 使用说明

参考以下使用说明: 
1. 修改脚本中的 FILE_INPUT 和 FILE_OUTPUT，以与您的源词典和目标词典文件的位置相匹配。
2. 运行脚本。
3. 转换后的词典文件将保存在指定的输出路径。

## 支持
- [薄荷输入法 -- 一套Rime输入法配置模版](https://www.mintimate.cc)
- [Mintimate 的博客](https://www.mintimate.cn)
- [Mintimate 的哔哩哔哩](https://space.bilibili.com/355567627)

如果觉得项目对你有用,想支持项目:
- [Mintimate的爱发电: https://afdian.net/a/mintimate](https://afdian.net/a/mintimate)

> 请务必备注 Rime ,这样你的爱发电ID和寄语将出现在[薄荷输入法-鸣谢](https://www.mintimate.cc/zh/guide/#%E9%B8%A3%E8%B0%A2)里(｡>ㅅ<｡)

## 贡献

我们欢迎对本项目做出贡献。
