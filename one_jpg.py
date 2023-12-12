import sys
import cv2
import os
import numpy as np
import shutil
import time
import pic_cut as cut
import pic2Anki as anki
import log
from tqdm import tqdm

# 定义初始化函数
src_DIR ="img/1.jpg"
Matrix_Transform_DIR ="img/1_crop.jpg"
crop_DIR ="img/cropped/"
anki_out_DIR = "out2Anki.txt"
anki_data_DIR = "data2Anki.txt"
AHKexe_DIR = "C:/Program Files/AutoHotkey/AutoHotkeyU64.exe"
AHK_data2anki_DIR = "C:/Users/vboxuser/Documents/Pictures2Anki_jj1x4/data2anki.ahk"
onedrive_DIR = "C:/Users/vboxuser/Nutstore/1/anki_sync_jj"

def init():
    # 删除anki_out_DIR文件夹下的内容
    try:
        os.remove(anki_out_DIR)
    except:
        pass

def clean():
    if (os.path.exists("img/history") == 0):
        os.mkdir("img/history")

    History_Number = 0
    # 读取img/History_Number.txt文件
    with open("img/History_Number.txt", "r") as file_History_Number:
        line = file_History_Number.readline()
        History_Number = int(line)
        print(History_Number)
    # 将img/History_Number.txt文件写入img/History_Number.txt文件
    with open("img/History_Number.txt", "w") as file_History_Number:
        file_History_Number.write(str(History_Number + 1))

    # 获取图片的原始路径
    src = os.path.join(src_DIR)
    # 获取图片的裁剪路径
    dst = os.path.join("img/history/" + str(History_Number + 1) + '.jpg')
    # 移动图片到img/history文件夹下
    shutil.move(src, dst)

    os.rename(crop_DIR, "img/" + str(History_Number + 1) + "_croped")
    # 移动img/history文件夹下的裁剪路径到img/history文件夹下
    shutil.move("img/" + str(History_Number + 1) + "_croped", "img/history")
    # 移动img/history文件夹下的裁剪路径到img/history文件夹下
    shutil.move(Matrix_Transform_DIR, "img/history/" + str(History_Number+1) + '_crop.jpg')
    # 删除anki_out_DIR文件夹下的内容
    try:
        os.remove(anki_out_DIR)
    except:
        pass
    # 删除tmp文件夹下的内容
    try:
        shutil.rmtree('tmp')
    except:
        pass
    
# 处理jpg图片
def process_1jpg():
    img = cv2.imread("img/1.jpg")
    # 切割图片
    perspectiveImg = cut.Matrix_Transform(img)
    # 将切割后的图片保存到Matrix_Transform_DIR文件夹中
    cv2.imwrite(Matrix_Transform_DIR, perspectiveImg)
    # 截取图片
    cut.crop_pic(perspectiveImg,1,4,crop_DIR)

    # 读取截取的图片
    files_in_crop_DIR = os.listdir(crop_DIR)
    for i_files in range(len(files_in_crop_DIR)):
        anki_pic_DIR = crop_DIR + str(files_in_crop_DIR[i_files])
        img_anki= cv2.imread(anki_pic_DIR)
        anki.picImOcclusion(img_anki,files_in_crop_DIR[i_files],anki_out_DIR)
    print("?????????????Anki...")
    # 将anki.anki_data.txt中的内容插入anki.anki_data.txt中
    card_count = 0
    try:
        with open(anki_out_DIR, "r", encoding="utf-8") as file_anki_data:
            for line in file_anki_data :
                filename = line.replace('\n','')
                line = file_anki_data.readline()
                line_data = line.split("	")
                positions = [int(line_data[0]),int(line_data[1]),int(line_data[2]),int(line_data[3])]
                anki.media_import_to_anki(filename,positions)
                card_count+=1
    except:
        pass
    clean()

# 单张jpg图片处理
def one_jpg():
    # 读取原始图片
    img = cv2.imread(src_DIR)
    # 如果原始图片不存在，则输出警告信息
    if img is None :
        log.log_print("===Warn===    1.jpg not exist")
        return 1
    # 处理jpg图片
    process_1jpg()
    return 0

#等待同步完成
def wait_sync():
    # 等待直到文件发生更改,最多等300秒
    in_time = time.time()
    for i in range(3):
        time.sleep(1)
        # 读取文件夹最后更改日期
        time_modified = os.path.getmtime("C:\\Users\\vboxuser\\Nutstore\\1\\anki_sync_jj")
        # 计算时间差
        dif = time_modified - in_time
        # 判断时间差是否大于1秒
        if dif > 1:
            break

    #延迟直到文件超过30秒不修改
    sec_count = 0
    new_modified = os.path.getmtime("C:\\Users\\vboxuser\\Nutstore\\1\\anki_sync_jj")
    while sec_count <5 : 
        last_modified = os.path.getmtime("C:\\Users\\vboxuser\\Nutstore\\1\\anki_sync_jj")
        #等待一秒
        # 判断时间差是否大于30秒
        if(last_modified == new_modified):
            sec_count += 1
        else:
            sec_count = 0
        time.sleep(1)
        new_modified = os.path.getmtime("C:\\Users\\vboxuser\\Nutstore\\1\\anki_sync_jj")

def process_all_onedrive_pictures():
    # 初始化
    init()
    wait_sync()
    #读取onedrive文件夹下文件
    files_in_onedrive = os.listdir(onedrive_DIR)
    # 逐个处理jpg图片
    for i_files in range(len(files_in_onedrive)):
        print(files_in_onedrive[i_files])
        #移动到img文件夹下
        shutil.copy(onedrive_DIR+'/'+files_in_onedrive[i_files],"img")

        #重命名为1.jpg
        try:
            os.remove("img/1.jpg")
        except:
            pass
        os.rename("img/"+files_in_onedrive[i_files],"img/1.jpg")
        
        #处理1.jpg
        if(one_jpg() == 0):
            #删除原文件
            os.remove(onedrive_DIR+'/'+files_in_onedrive[i_files])
    if len(files_in_onedrive) != 0:
        data2anki()

def data2anki():
    os.system('"'+AHKexe_DIR+'" '+ AHK_data2anki_DIR)