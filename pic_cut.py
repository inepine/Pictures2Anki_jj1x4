# import sys
import cv2
import os
import numpy as np
crop_DIR ="img/cropped/"
The_Ponit = [[0,0],[0,0],[0,0],[0,0]]
arr = []
#左右扫描像素点，如果有超过30个黑点，则算作找到纵向点。返回横向中心值。
#如果不超过30个黑点，返回0
#turn 1 表示右上，0表示左下
def scan_line_30black(img,x,y,turn) :
    black_count = 0
    for i in range(1,45,1):
        px = img[y, (turn*i+x)]
        if (px[0] <80 and px[1] <80 and px[2] <80):
            black_count +=1
        else:
            break
    if black_count>15 and black_count<35:
        # print("Findx: "+str(x+turn*black_count/2))
        return int(x+turn*black_count/2)
    else:
        return 0


#上下扫描像素点，如果有超过30个黑点，则算作找到横向中点。返回横向中心值。
#如果不超过30个黑点，或者超过70个黑点，返回0
def scan_vertical(img,x,y) :
    black_up = 0
    black_down = 0
    flag_stop_up = 0
    flag_stop_down = 0
    for j in range(1,20,1):
        if flag_stop_down ==1 and flag_stop_up ==1:
            break
        if(y-j <0):
            flag_stop_up =1
        else:
            px = img[y-j, x]
            if (flag_stop_up == 0 and px[0] <80 and px[1] <80 and px[2] <80):
                black_up+=1
            else :
                flag_stop_up =1

        if(y+j >=img.shape[0]):
            flag_stop_down =1
        else:
            px = img[y+j, x]
            if (flag_stop_down == 0 and px[0] <80 and px[1] <80 and px[2] <80):
                black_down+=1
            else :
                flag_stop_down =1
    if black_up + black_down>15 and black_up + black_down<36:
        return int(y+(black_down-black_up)/2)
    else:
        return 0

def is_the_pattern(img,point):
    if point[0] <= 60 or point[0] >=img.shape[1] -60 or point[1] <=60 or point[1]>=img.shape[0] -60:
        # print("not a pattern , too close to the age")
        return 0

    #判断左边有至少8个连续白色像素点
    continue_while = 0
    maxcount = 0
    for j in range(55):
        px = img[point[1],point[0]-j]
        if (px[0] >110 and px[1] >110 and px[2] >110):
            continue_while+=1
        else:
            if(continue_while>maxcount):
                maxcount = continue_while
            continue_while =0
    if(continue_while>maxcount):
        maxcount = continue_while
    continue_while =0
    if maxcount<=8:
        # print("not a pattern , left white")
        return 0

    #判断右边有至少8个连续白色像素点
    continue_while = 0
    maxcount = 0
    for j in range(55):
        px = img[point[1],point[0]+j]
        if (px[0] >110 and px[1] >110 and px[2] >110):
            continue_while+=1
        else:
            if(continue_while>maxcount):
                maxcount = continue_while
            continue_while =0
    if(continue_while>maxcount):
        maxcount = continue_while
    continue_while =0
    if maxcount<=8:
        # print("not a pattern , right white")
        return 0

    #判断上方有至少8个连续白色像素点
    continue_while = 0
    maxcount = 0
    for j in range(55):
        px = img[point[1]-j,point[0]]
        if (px[0] >110 and px[1] >110 and px[2] >110):
            continue_while+=1
        else:
            if(continue_while>maxcount):
                maxcount = continue_while
            continue_while =0
    if(continue_while>maxcount):
        maxcount = continue_while
    continue_while =0
    if maxcount<=8:
        # print("not a pattern , up white")
        return 0
    
    #判断下方有至少8个连续白色像素点
    continue_while = 0
    maxcount = 0
    for j in range(55):
        px = img[point[1]+j,point[0]]
        if (px[0] >110 and px[1] >110 and px[2] >110):
            continue_while+=1
        else:
            if(continue_while>maxcount):
                maxcount = continue_while
            continue_while =0
    if(continue_while>maxcount):
        maxcount = continue_while
    continue_while =0
    if maxcount<=8:
        # print("not a pattern , down white")
        return 0
    return 1

# 找1234点，依次为上左，上右、下左，下右。
# 参数1-3：x扫描起始点、x扫描终点、扫描方向（1顺-1逆）
# 参数4-6：y扫描起始点、y扫描终点、扫描方向（1顺-1逆）
# 参数7：点数（0-3）
def foundpint(img,range_x1, range_x2, turnx, range_y1, range_y2, turny, PointNumber):
    for i in range(range_x1, range_x2, turnx):  # i被认为是横坐标
        # print("Loop i :"+str(i))
        for j in range(range_y1, range_y2, turny):
            px = img[j, i]
            if (px[0] < 80 and px[1] < 80 and px[2] < 80):
                # print("find black" + str(i)+","+str(j))
                The_Ponit[PointNumber][0] = scan_line_30black(img,i, j, turnx)
                if (The_Ponit[PointNumber][0]):
                    The_Ponit[PointNumber][1] = scan_vertical(img,The_Ponit[PointNumber][0], j)
                    if The_Ponit[PointNumber][1]:
                        if is_the_pattern(img,The_Ponit[PointNumber]):
                            print("=========found point"+str(PointNumber))
                            # cv2.circle(img,(The_Ponit[PointNumber][0],The_Ponit[PointNumber][1]), 30, (0,0,255), -1)
                            # #显示img
                            
                            # resized_image = cv2.resize(img, (800, 600))  
                            # cv2.imshow("is a point", resized_image)

                            # cv2.waitKey(0)
                            # cv2.destroyAllWindows()
                            arr.append([The_Ponit[PointNumber][0], The_Ponit[PointNumber][1]])
                            return

                        # cv2.circle(img,(The_Ponit[PointNumber][0],The_Ponit[PointNumber][1]), 30, (0,0,255), -1)
                        # #显示img
                        # resized_image = cv2.resize(img, (800, 600))  
                        # cv2.imshow("not a point", resized_image)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()
    print("NotFoundPoint" + str(PointNumber))

# 矩形裁剪函数

# 目标的像素值大小
long = 2480  # 图片的长宽 300DPI A4大小 长宽反着表示
short = 3508
def Matrix_Transform(img):
    img_transform = img.copy()
    image_width = img.shape[1] - 1
    image_height = img.shape[0] - 1
    # 获取梯形的四个顶点

    foundpint(img,0, int(image_width / 3), 1, 0, int(image_height / 3), 1, 0)
    foundpint(img,image_width, int(2 * image_width / 3), -1, 0, int(image_height / 3), 1, 1)
    foundpint(img,0, int(image_width / 3), 1, int(image_height), int(image_height * 2 / 3), -1, 2)
    foundpint(img,image_width, int(2 * image_width / 3), -1, int(image_height), int(image_height * 2 / 3), -1, 2)
    P1, P2, P3, P4 = arr[:]
    print("选定的四个角点为：{}{}{}{}".format(P1, P2, P3, P4))
    arr.clear()
    # 进行转换
    cv2.circle(img_transform, tuple(P1), 2, (255, 0, 0), 3)
    cv2.circle(img_transform, tuple(P2), 2, (255, 0, 0), 3)
    cv2.circle(img_transform, tuple(P3), 2, (255, 0, 0), 3)
    cv2.circle(img_transform, tuple(P4), 2, (255, 0, 0), 3)

    srcPoints = np.vstack(([P1[0], P1[1]], [P2[0], P2[1]], [P3[0], P3[1]], [P4[0], P4[1]]))
    srcPoints = np.float32(srcPoints)

    # 设置目标画布的大小
    canvasPoints = np.array([[0, 0], [int(long), 0], [0, int(short)], [int(long), int(short)]])
    canvasPoints = np.float32(canvasPoints)
    # 计算转换矩阵
    perspectiveMatrix = cv2.getPerspectiveTransform(srcPoints, canvasPoints)
    # 完成透视变换
    perspectiveImg = cv2.warpPerspective(img_transform, perspectiveMatrix, (int(long), int(short)))
    print("矩形转换完成。切片识别红线坐标中....")
    return perspectiveImg

# 裁剪图片并输出
def crop_pic(perspectiveImg,x,y,crop_DIR):
    if (os.path.exists(crop_DIR) == 0):
        os.mkdir(crop_DIR)

    long = perspectiveImg.shape[0]
    short = perspectiveImg.shape[1]

    for crop_i in range(x):
        if crop_i == 0:
            x1 = crop_i * (short // x)
        else:
            x1 = crop_i * (short // x) - int(long // (10*x))
        if crop_i ==x-1:
            x2 = (crop_i + 1) * (short // x)
        else:
            x2 = int(long // (10*y)) + (crop_i + 1) * (short // x)
        for crop_j in range(y):
            if crop_j ==0:
                y1 = crop_j * (long // y)
            else:
                y1=crop_j*(long // y) - int(long // (10*y))
            if crop_j == y-1:
                y2 = (crop_j + 1) * (long // y)
            else:
                y2 = int(long // (10*y))+(crop_j+1)*(long // y)

            #裁剪
            imCrop_1_1 = perspectiveImg[ y1:y2 , x1:x2]
            #图像平滑和锐化处理：
            imCrop_1_1 = cv2.bilateralFilter(imCrop_1_1,9,75,75)
            # 创建锐化滤波器的卷积核
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            # 对图像应用卷积操作
            imCrop_1_1 = cv2.filter2D(imCrop_1_1, -1, kernel)
            #写入文件
            cv2.imwrite(crop_DIR + "/"+str(crop_i+1)+"_"+str(crop_j+1)+".jpg", imCrop_1_1)