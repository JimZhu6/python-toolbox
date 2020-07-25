# -*- coding: utf-8 -*-
import os
from name_dict import ndict


def batch_rename(path, name_dict, suffix_tuple):
    """
    修改替换指定文件名\r\n
    @path: 文件夹路径\r\n
    @name_dict: 要替换的部分文件名字典\r\n
    @suffix_tuple: 要替换的文件后缀名元组
    """
    # 切换到 path 路径下面
    os.chdir(path)
    filenames = os.listdir(path=path)
    for filename in filenames:
        file, suffix = os.path.splitext(filename)
        # 从尾部开始寻找第一个' - '，用于区分歌手名与专辑名
        last_column_index = filename.rfind(' - ')

        for i in range(len(suffix_tuple)):
            if suffix == suffix_tuple[i]:
                old_name = file + suffix
                # 查找要替换的部分文件名
                for key in name_dict:
                    flag = True
                    if old_name.rfind(key, last_column_index, len(old_name)) > -1:
                        # 查找是否文件名是否存在要替换的关键字
                        # 从尾部开始查找
                        new_name = replace_last(
                            old_name, key, name_dict[key])
                        # 从头部寻找第一个' - '，用于区分歌曲名与专辑名
                        first_column_index = new_name.find(' - ')
                        # 从尾部开始寻找第一个' - '，用于区分歌手名与专辑名
                        last_column_index = filename.rfind(' - ')
                        head = new_name[0:first_column_index+3]
                        # 将多余空格去掉
                        middle = new_name[first_column_index+3:last_column_index]
                        middle = middle.replace(' ', '')
                        tail = new_name[last_column_index:len(new_name)]
                        new_name = head+middle+tail

                        # 替换文件名称
                        os.rename(old_name, new_name)
                        print(f"{filename!r} rename-> {new_name!r}  done.")
                        if flag == True:
                            old_name = new_name
                    else:
                        flag = False


def replace_last(source_string, replace_what, replace_with):
    """
    从尾部替换字符串\r\n
    @source_string: 原字符串\r\n
    @replace_what: 要替换的字符串\r\n
    @replace_with: 替换为
    @return: 替换完成的字符串
    """
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


def start_rename():
    path_tuple = ('F:/musicBG/AGA', 'F:/musicBG/Deemo',
                  'F:/musicBG/陈慧琳', 'F:/musicBG/陈奕迅#1', 'F:/musicBG/陈奕迅#2', 'F:/musicBG/古巨基', 'F:/musicBG/李克勤',
                  'F:/musicBG/梁静茹', 'F:/musicBG/卢巧音', 'F:/musicBG/其他中文歌手#1', 'F:/musicBG/其他中文歌手#2', 'F:/musicBG/其他中文歌手#3',
                  'F:/musicBG/其他中文歌手#4', 'F:/musicBG/卫兰', 'F:/musicBG/谢安琪', 'F:/musicBG/薛凯琪', 'F:/musicBG/杨千嬅', 'F:/musicBG/张敬轩', 'F:/musicBG/周杰伦')
    name_dict = ndict
    suffix_tuple = ('.flac',)
    for path in path_tuple:
        batch_rename(path=path, name_dict=name_dict, suffix_tuple=suffix_tuple)
    input('Press the enter key to exit.')


if __name__ == '__main__':
    start_rename()
    pass
