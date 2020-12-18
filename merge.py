#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
reference: https://gist.github.com/lotem/5443073

This script is used to merge the rime-dict into one file.
Then you only need to add these lines into your `luna_pinyin.custom.yaml`:
```
patch:
  translator/dictionary: luna_pinyin.extended
```
and move `luna_pinyin.extended` into your rime_home folder
'''

from io import TextIOWrapper
import os
import time

# +: add selected dicts
# -: add all dicts except selected ones
select_mode = "-"
select_list = [
    "Moba游戏用词",
    "粤语词汇",
    "网站大全",
    "游戏",
]

dict_path = "./"
extended_path = "luna_pinyin.extended.dict.yaml"

header = (
    "---\n"
    "name: luna_pinyin.extended\n"
    "version: " + time.strftime("%Y.%m.%d", time.localtime()) + "\n"
    "sort: by_weight\n"
    "use_preset_vocabulary: true\n"
    "# 從 luna_pinyin.dict.yaml 導入包含單字的碼表\n"
    "import_tables:\n"
    "- luna_pinyin\n"
    "...\n")


def extract_dict(dict_path: str, output_yaml: TextIOWrapper) -> None:
    """
    @param: dict_yaml: path to the .dict.yaml to extract
    @param: output_yaml: file to write in. e.g. open("xxx.yaml")
    """
    dict_yaml = open(dict_path, mode="r", encoding="utf-8")
    lines = dict_yaml.readlines()
    isstarted = False
    for line in lines:
        if isstarted:
            output_yaml.write(line)
        if not isstarted and line == "...\n":
            isstarted = True

    dict_yaml.close()


if __name__ == "__main__":
    print("mode is " + select_mode)

    print("output to " + extended_path)
    extended_yaml = open(extended_path, mode="w", encoding="utf-8")
    extended_yaml.write(header)  # write header

    folder_list = os.listdir(dict_path)
    if select_mode == "+":
        for selected in select_list:
            for folder in folder_list:
                # skip files and .git/
                if not os.path.isdir(dict_path + folder) or folder == ".git":
                    continue

                if folder == selected:  # selected
                    # add the selected one
                    dict_list = os.listdir(dict_path + folder)
                    for dict in dict_list:
                        if dict.endswith(".dict.yaml"):
                            print(dict)
                            extended_yaml.write("\n# " + dict + "\n")
                            extract_dict(
                                dict_path + folder + "/" + dict, extended_yaml)
                    break

    elif select_mode == "-":
        for folder in folder_list:
            # skip files and .git/
            if not os.path.isdir(dict_path + folder) or folder == ".git":
                continue

            if folder not in select_list:  # not selected
                # add the not selected one
                dict_list = os.listdir(dict_path + folder)
                for dict in dict_list:
                    if dict.endswith(".dict.yaml"):
                        print(dict)
                        extended_yaml.write("\n# " + dict + "\n")
                        extract_dict(
                            dict_path + folder + "/" + dict, extended_yaml)

    extended_yaml.close()
