# -*- coding: utf-8 -*-
import os
import time
import shutil
from tqdm import tqdm

# 原始数据存放的路径
raw_path = "D:\\raw data\\"
# 搜库电脑暂存的路径
new_path = "\\\\172.16.101.211\\Project MS service\\Proteomics project\\Temporary rawdata\\"

#将文件按时间进行排序，筛掉含STRONGWASH的文件
def get_raw_list(file_path):
    dir_list = os.listdir(file_path)
    raw_list = []
    if not dir_list:
        return
    else:
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse = True)
        for file in dir_list:
            if "STRONGWASH" not in file:
                raw_list.append(file)
        return raw_list

#筛选24小时内生成的文件，不含最新的1个正在被质谱写入的文件
def get_raw_path(raw_path):
    rawfile_path = list()
    now = time.time()
    rawfile = get_raw_list(raw_path)
    del (rawfile[0])
    for i in rawfile:
        file_time = os.path.getmtime(raw_path+i)
        if (now - file_time) < 86400:
            rawfile_path.append(i)
    return rawfile_path

# 复制指定文件
def copy_file():
    for i in tqdm(get_raw_path(raw_path)):
        filename = i
        try:
            shutil.copy(raw_path + filename, new_path + filename)
        except:
            print(i+"文件复制失败")

if __name__ == '__main__':
    copy_file()
    os.system("pause")
