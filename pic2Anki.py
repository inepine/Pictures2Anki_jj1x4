# 输出到文件样例：
# file = open('1_px.txt','w')
# sys.stdout = file
# file.close()
# sys.stdout = sys.__stdout__

import os
import numpy as np
import cv2
import sys
import shutil
import re
import random
import log

crop_DIR = "img/cropped/"
temple_media_DIR = "anki_files_templates/media/"
anki_media_DIR = "C:/Users/vboxuser/AppData/Roaming/Anki2/user1/collection.media/"

anki_data_DIR = "data2Anki.txt"

x1 = 0
x2 = 0
x3 = 0
x4 = 0

# 定义红色范围
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])


# 找到红色并二值化
def show_red_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 创建掩膜
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    return cv2.bitwise_or(mask1, mask2)


def output_red_picture(img, anki_pic_name):
    if (os.path.exists("tmp") == 0):
        os.mkdir("tmp")

    # 红色识别
    img = show_red_mask(img)

    # 出线
    # 降噪
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    # 连线
    kernel = np.ones((16, 8), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    # 去除非线
    kernel = np.ones((1, 24), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("tmp/tmp_" + anki_pic_name, img)


# 定义函数judge_and_output，用于判断图片中是否存在线，并输出线的信息
def judge_and_output(x1, x2, y1, y2, anki_pic_name, anki_out_DIR):
    log.log_print("may find a line:")
    log.log_print(str(x1) + "\t" + str(x2) + "\t" + str(y1) + "\t" + str(y2))
    # 计算线的长度
    line_length2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    # 如果线的长度大于2000，则将anki_out_DIR文件中的内容输出到anki_pic_name文件中
    if line_length2 > 2000:
        file = open(anki_out_DIR, 'a')
        sys.stdout = file
        print(anki_pic_name)
        print(str(int(x1)) + "\t" + str(int(y1)) + "\t" + str(int(x2)) + "\t" + str(int(y2)))

        file.close()
        sys.stdout = sys.__stdout__


def find_line(maskimg, anki_pic_name, anki_out_DIR):
    # 找到各线左右端点：
    j_down_max = 0
    j_up_max = 0
    line_length2 = 0
    first_find = 0
    for k in range(70,maskimg.shape[1] - 3):
        for j in range(70,maskimg.shape[0] - 3):
            px = maskimg[j, k]
            if (px[0] > 230 and px[1] > 230 and px[2] > 230):
                for i in range(k, maskimg.shape[1] - 3, 1):
                    px = maskimg[j, i]
                    maskimg[j, i] = [0, 0, 0]
                    if first_find == 0:  # 遇到白色像素，开始找线
                        x1 = i
                        y1 = j
                        first_find += 1
                    # 上下检索找y中点：
                    y_up = 0
                    y_down = 0
                    flag_stop_up = 0
                    flag_stop_down = 0
                    for q in range(25):
                        if flag_stop_down == 1 and flag_stop_up == 1:
                            break
                        if (j - q > 0 and flag_stop_up != 1):
                            px = maskimg[j - q, i + 1]
                            if (px[0] > 230 and px[1] > 230 and px[2] > 230):
                                maskimg[j - q, i + 1] = [0, 0, 0]
                                y_up += 1
                            else:
                                flag_stop_up == 1
                        if (j + q < maskimg.shape[0] - 1 and flag_stop_down != 1):
                            px = maskimg[j + q, i + 1]
                            if (px[0] > 230 and px[1] > 230 and px[2] > 230):
                                maskimg[j + q, i + 1] = [0, 0, 0]
                                y_down += 1
                            else:
                                flag_stop_down == 1
                            if (q + j > j_down_max):
                                j_down_max = q + j
                            if (j - q < j_up_max):
                                j_up_max = j - q
                    if (y_down == 0 and y_up == 0):
                        x2 = i
                        y2 = j
                        j_down_max = j_up_max = j
                        for l in range(x1, x2):
                            for m in range(j_up_max, j_down_max):
                                maskimg[m][l] = [0, 0, 0]
                        judge_and_output(x1, x2, y1, y2, anki_pic_name, anki_out_DIR)
                        j_down_max = 0
                        j_up_max = 0
                        first_find = 0
                        break
                    else:
                        j = int((y_down - y_up)/2) + j


def deck_add_card_line(ID):
    card_line_sample = ""
    with open('anki_files_templates/card_sample.txt', "r", encoding="utf-8") as file_card_sample:
        card_line_sample = file_card_sample.readline()
    card_line_sample = card_line_sample.replace("$ID", ID)

    with open(anki_data_DIR, "a", encoding="utf-8") as file_anki_data:
        file_anki_data.write(card_line_sample)


def anki_svg_fix(filename, Card_ID, positions):
    src = os.path.join(temple_media_DIR + "ID" + filename)
    dst = os.path.join(temple_media_DIR + "Tmp_ID" + filename)
    shutil.copy(src, dst)
    # <svg xmlns="http://www.w3.org/2000/svg" width="$count_px_x" height="$count_px_y">
    # <rect id="$ID" height="$height" width="$width" y="$y" x="$x" stroke="#2D2D2D" fill="#FFEBA2"/>
    # 媒体文件变量替换
    img = cv2.imread(anki_media_DIR + Card_ID + ".jpg")
    new_anki_data = ""
    with open(temple_media_DIR + "Tmp_ID" + filename, "r") as file_anki_data:
        for line in file_anki_data:
            line = line.replace("$count_px_x", str(img.shape[1]))
            line = line.replace("$count_px_y", str(img.shape[0]))
            line = line.replace("$ID", str(Card_ID))
            line = line.replace("$height", str(int(img.shape[0] / 4)))
            line = line.replace("$width", str(int(positions[2]) - int(positions[0])))
            line = line.replace("$y", str(positions[1] - img.shape[0] / 4))
            line = line.replace("$x", str(positions[0]))
            new_anki_data += line

    with open(temple_media_DIR + "Tmp_ID" + filename, "w") as file_anki_data:
        file_anki_data.write(new_anki_data)

    src = os.path.join(temple_media_DIR + "Tmp_ID" + filename)
    dst = os.path.join(anki_media_DIR, Card_ID + filename)
    shutil.copy(src, dst)


def media_import_to_anki(filename, positions):
    # 准备数据模板
    if (os.path.exists(anki_data_DIR) == 0):
        shutil.copy('anki_files_templates/data2Anki.txt', './')

    # 添加卡片行
    Card_ID = str(int(random.randint(1, 10000))) + str(int(random.randint(1, 10000))) + str(
        int(random.randint(1, 10000))) + str(int(random.randint(1, 10000)))
    deck_add_card_line(Card_ID)

    # 图片移动且重命名
    src = os.path.join(crop_DIR, filename)
    dst = os.path.join(anki_media_DIR, Card_ID + '.jpg')
    shutil.copy(src, dst)

    # 拷贝三个媒体文件
    anki_svg_fix("-A.svg", Card_ID, positions)
    anki_svg_fix("-O.svg", Card_ID, positions)
    anki_svg_fix("-Q.svg", Card_ID, positions)


def picImOcclusion(img, anki_pic_name, anki_out_DIR):
    output_red_picture(img, anki_pic_name)
    img_red = cv2.imread("tmp/tmp_" + anki_pic_name)
    find_line(img_red, anki_pic_name, anki_out_DIR)
