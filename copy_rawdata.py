# -*- coding: utf-8 -*-
import os
import time
import shutil
import hashlib
from tqdm import tqdm


# 计算文件MD5值
def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    md5 = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        md5.update(b)
    f.close()
    return md5.hexdigest()


# 将文件按时间进行排序，筛掉含STRONGWASH的文件
def get_raw_list(file_path):
    dir_list = os.listdir(file_path)
    raw_list = []
    if not dir_list:
        return
    else:
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse = True)
        for file in dir_list:
            if ".raw" in file:
                if "STRONGWASH" not in file:
                    raw_list.append(file)
        return raw_list


# 筛选days天内生成的文件，不含最新的1个正在被质谱写入的文件
def get_raw_path(raw_path, days):
    rawfile_path = list()
    now = time.time()
    rawfile = get_raw_list(raw_path)
    del (rawfile[0])
    for i in rawfile:
        file_time = os.path.getmtime(raw_path+i)
        if (now - file_time) < 86400 * days:
            rawfile_path.append(i)
    return rawfile_path


# 复制days天内指定文件，并校验
def copy_file(days):
    for i in tqdm(get_raw_path(raw_path, days)):
        raw_file_path = raw_path + i
        new_file_path = new_path + i
        try:
            shutil.copy(raw_file_path, new_file_path)
            raw_md5 = get_file_md5(raw_file_path)
            new_md5 = get_file_md5(new_file_path)
            if raw_md5 != new_md5:
                print(raw_file_path + "\nCOPY ERROR!!!FILE HAS DIFFERENT MD5!!!")
        except Exception as e:
            print(raw_file_path + "\nCOPY ERROR!!!" + str(e))


if __name__ == '__main__':
    # 原始数据存放的路径
    raw_path = "D:\\raw data\\"
    # 搜库电脑暂存的路径
    new_path = "\\\\172.16.101.211\\Project MS service\\Proteomics project\\Temporary rawdata\\"
    week_day = int(time.strftime("%w"))
    # 主要用于周末不进行文件的复制
    if week_day == 1:
        copy_file(3)
        os.system("pause")
    elif week_day >= 2 and week_day <= 5:
        copy_file(1)
        os.system("pause")
    else:
        print("TODAY IS WEEKEND")
