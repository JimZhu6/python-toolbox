# -*- coding: utf-8 -*-
import os
from name_dict import ndict
import csv
# pip install mutagen
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, COMM
from mutagen.flac import FLAC

# 获取指定文件夹下的所有音乐文件列表
def get_music_list(path, suffix_tuple):
    """
    获取指定文件夹下的所有音乐文件列表\r\n
    @path: 文件夹路径\r\n
    @suffix_tuple: 音乐文件后缀名元组\r\n
    @return: 音乐文件列表
    """
    music_list = []
    for dirs, dirnames, files in os.walk(path):
        for file in files:
            if file.endswith(suffix_tuple):
                music_list.append(dirs+'/'+file)
    return music_list

# 导出音乐文件csv数据
def export_music_csv(music_list, csv_file_path):
  """
  导出音乐文件csv数据\r\n
  @music_list: 音乐文件列表
  """
  # 创建csv文件
  with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # 定义csv文件的列名
    fieldnames = ['文件名', '专辑名', '歌手名', '歌曲名']
    # 创建csv写入器
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # 写入列名
    writer.writeheader()
    # 遍历音乐文件列表
    for file in music_list:
      # 解析文件名，获取专辑名、歌手名、歌曲名
      filename = os.path.basename(file)
      try:
        album = filename.split(' - ')[0]
        artist = filename.split(' - ')[1]
        song = filename.split(' - ')[2].split('.')[0]
      except:
        print_and_log(f"【export_music_csv】:album:{album!r} artist:{artist!r} song:{song!r} 无法解析！")
        album = ''
        artist = ''
        song = ''
      # 写入数据到csv文件
      writer.writerow({'文件名': filename, '专辑名': album, '歌手名': artist, '歌曲名': song})

# 修改替换指定文件名
def batch_rename(music_list, name_dict):
    """
    修改替换指定文件名\r\n
    @path: 文件夹路径\r\n
    @name_dict: 要替换的部分文件名字典
    """
    for file in music_list:
        old_name = file
        # 查找要替换的部分文件名
        last_column_index = file.rfind(' - ')
        for key in name_dict:
          flag = True
          if old_name.rfind(key, last_column_index, len(old_name)) > -1:
            # 查找是否文件名是否存在要替换的关键字
            # 从尾部开始查找
            new_name = replace_last(
              old_name, key, name_dict[key])
            # 替换文件名称
            os.rename(old_name, new_name)
            print_and_log(f"{old_name!r} batch_rename-> {new_name!r}  done.")
            if flag == True:
              old_name = new_name
          else:
            flag = False

# 从尾部替换字符串
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

# 替换文件名专辑栏字符串的空格
def replace_middle_space(music_list):
    """
    替换文件名专辑栏字符串的空格\r\n
    @music_list: 音乐文件列表
    """
    for filename in music_list:
        # 从头部寻找第一个' - '，用于区分歌曲名与专辑名
        first_column_index = filename.find(' - ')
        # 从尾部开始寻找第一个' - '，用于区分歌手名与专辑名
        last_column_index = filename.rfind(' - ')
        head = filename[0:first_column_index+3]
        # 将多余空格去掉
        middle = filename[first_column_index +
                            3:last_column_index]
        middle = middle.replace(' ', '')
        tail = filename[last_column_index:len(filename)]
        new_name= head+middle+tail
        os.rename(filename, new_name)
        print_and_log(f"{filename!r} replace_middle_space-> {new_name!r}  done.")

# 将所有文件名中的下划线替换为空格
def replace_underline(music_list):
    """
    替换文件名中的下划线为空格\r\n
    @music_list: 音乐文件列表
    """
    for filename in music_list:
        # 如果文件名中包含下划线
        if filename.find('_') > -1:
            new_name = filename.replace('_', ' ')
            os.rename(filename, new_name)
            print_and_log(f"{filename!r} replace_underline-> {new_name!r}  done.")

# 更新音乐文件的属性数据，将文件名的专辑名、歌手名、歌曲名写入到音乐文件的属性中
def update_music_info(music_list):
    """
    更新音乐文件的属性数据，将文件名的专辑名、歌手名、歌曲名写入到音乐文件的属性中\r\n
    @music_list: 音乐文件列表\r\n
    """
    for file in music_list:
      # 解析文件名，获取歌曲名、专辑名、歌手名
      filename = os.path.basename(file)
      # 判断文件类型是mp3还是flac
      if file.endswith('.flac'):
        try:
          song = filename.split(' - ')[0]
          album = filename.split(' - ')[1]
          artist = filename.split(' - ')[2].split('.')[0]
          # 更新音乐文件的属性数据
          audio = FLAC(file)
          audio['title'] = song
          audio['album'] = album
          audio['artist'] = artist
          # 清空“备注”字段
          audio['comment'] = ''
          audio.save()
        except:
            print_and_log(f"【update_music_info】: album:{album!r} artist:{artist!r} song:{song!r} 无法解析！")
      elif file.endswith('.mp3'):
          try:
            song = filename.split(' - ')[0]
            album = filename.split(' - ')[1]
            artist = filename.split(' - ')[2].split('.')[0]
            # 更新音乐文件的属性数据
            audio = ID3(file)
            audio.add(TIT2(encoding=3, text=song))
            audio.add(TPE1(encoding=3, text=artist))
            audio.add(TALB(encoding=3, text=album))
            # 清空“备注”字段
            audio.add(COMM(encoding=3, lang='eng', desc='desc', text=''))
            audio.save()
          except:
            print_and_log(f"【update_music_info】: album:{album!r} artist:{artist!r} song:{song!r} 无法解析！")

# 从音乐文件属性中获取歌曲名、专辑名、歌手名，并将文件名重命名为这些属性值
def rename_music_by_info(music_list):
    """
    从音乐文件属性中获取歌曲名、专辑名、歌手名，并将文件名重命名为这些属性值\r\n
    @music_list: 音乐文件列表
    """
    for file in music_list:
      # 判断文件类型是mp3还是flac
      if file.endswith('.flac'):
        audio = FLAC(file)
        song = audio['title'][0]
        album = audio['album'][0]
        artist = audio['artist'][0]
      elif file.endswith('.mp3'):
        audio = ID3(file)
        song = audio['TIT2'].text[0]
        album = audio['TALB'].text[0]
        artist = audio['TPE1'].text[0]
      # 生成新文件名
      new_name = f'{album} - {artist} - {song}.flac'
      # 重命名文件
      os.rename(file, new_name)
      print_and_log(f"{file!r} rename_music_by_info-> {new_name!r}  done.")


def print_and_log(message):
    """
    打印信息并写入日志文件\r\n
    @message: 要打印的信息
    """
    # 日志文件路径
    log_file = 'F:/log.txt'
    # log_file = ''
    print(message)
    if log_file == '':
        return
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')


def event():
    # 要处理的文件夹路径
    path_tuple = 'F:/Music'
    # 艺术家名称转换字典
    name_dict = ndict
    # 需要处理的文件后缀名
    suffix_tuple = ('.flac','.mp3',)


    music_list = get_music_list(path=path_tuple, suffix_tuple=suffix_tuple)
    export_music_csv(music_list=music_list, csv_file_path='F:/music.csv')
    # batch_rename(music_list=music_list, name_dict=name_dict)
    # replace_middle_space(music_list=music_list)
    # replace_underline(music_list=music_list)

    update_music_info(music_list=music_list)
    # rename_music_by_info(music_list=music_list)
    input('Press the enter key to exit.')


if __name__ == '__main__':
    event()
    pass
