# -*- coding: utf-8 -*-
"""
照片樣本: 經井澤王子飯店前

特徵點 (IMG_1265 <-> IMG_5732)
1. 車尾 (1257, 411)  <->  (369, 393)
2. 石頭 (1071, 480)  <-> (209, 459)
3. 樹Y (1112, 192)  <-> (251, 181)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)  <-> (202, 825)
6. 右邊石頭 (1266,492) <-> (376, 463)
7. 車燈 (1192, 426) <-> (318, 406)


A, B, C, D 四組組合實驗: 
A 組 Affine Transformation 特徵點組合
           IMG_1265 <-> IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
2. 石頭 (1071, 480)  <-> (209, 459)
3. 樹Y (1112, 192)  <-> (251, 181)

B 組 Affine Transformation 特徵點組合
           IMG_1265 <-> IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)  <-> (202, 825)

C 組 Affine Transformation 特徵點組合
           IMG_1265 <-> IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
6. 右邊石頭 (1266,492) <-> (376, 463)
7. 車燈 (1192, 426) <-> (318, 406)

D 組 Affine Transformation 特徵點組合
           IMG_1265 <-> IMG_5732
6. 右邊石頭 (1266,492) <-> (376, 463)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)    <-> (202, 825)

"""

import numpy as np
import math
import cv2


h_offset = 10

print("利用三個點 算出座標轉換的關係式 用for跑轉換 以binear方法計算內插顏色 填到目標影像中")
# A 組合
target = np.array(
    [[1257, 411+h_offset, 0, 0, 1, 0], 
     [0, 0, 1257, 411+h_offset, 0, 1], 
     [1071, 480+h_offset, 0, 0, 1, 0], 
     [0, 0, 1071, 480+h_offset, 0, 1],
     [1112, 192+h_offset, 0, 0, 1, 0], 
     [0, 0, 1112, 192+h_offset, 0, 1]])
src = np.array([369,393,209,459,251,181])

param = np.linalg.solve(target,src)  # 解聯立方程 - Affine Transformation
print(param)

# t = np.array([[0,0,0,0,1,0], [0,0,0,0,0,1]])
# s = np.matmul(t, param)  # 計算轉換後之座標
# print(s)

# 讀入兩張影像
pic1 = cv2.imread("imgs/IMG_1265.JPG")  #左
pic2 = cv2.imread("imgs/IMG_5732.JPG")  #右
print('pic1 shape:', pic1.shape)
print('pic2 shape:', pic2.shape)

# initial merged 變數，用以存放拼接影像，初始化成黑色
merged_width = 2300   
merged_height = 900
merged = np.zeros((merged_height, merged_width, 3))

# 將左邊照片pic1先放入merged
merged[h_offset:(pic1.shape[0]+h_offset), :pic1.shape[1], :] = pic1
cv2.imwrite("merged_preprocess.jpg", merged)

for y in range(merged_height):
    print(y, ' ', end="")
    for x in range(merged_width):

        # Inverse Mapping 座標轉換，由 merged 去計算要從 source 影像(pic2)的哪個點取顏色來填
        t = np.array([[x,y,0,0,1,0], [0,0,x,y,0,1]])
        s = np.matmul(t, param)   # s 為轉換後之座標

        # 計算後之座標，若落在 source 座標系的影像內，則做 binear interpolation 提取顏色
        if s[0]>0 and s[0]<1271 and s[1]>0 and s[1]<847:

            # print('y:', y, ', x:', x)
            # print('row:', s[1], ', column:', s[0])
            # print("row range:%d~%d, column range:%d~%d" % (math.floor(s[1]),math.ceil(s[1]), 
            #     math.floor(s[0]),math.ceil(s[0])) )
            
            # 座標轉換後，找周圍四個點座標，用以計算 binear interpolation
            xl = math.floor(s[0])
            yl = math.floor(s[1])
            xb = math.ceil(s[0])
            yb = math.ceil(s[1])
            
            # 四點顏色，top-left, top-right, bottom-left, bottem-right
            tlp = pic2[yl, xl]
            trp = pic2[yl, xb]
            blp = pic2[yb, xl]
            brp = pic2[yb, xb]
            
            # Binear Interpolation 顏色計算 - 3 channel
            itp_r = (xb-s[0])*(yb-s[1])*tlp[0] + \
                (s[0]-xl)*(yb-s[1])*trp[0] +  \
                (xb-s[0])*(s[1]-yl)*blp[0] + \
                (s[0]-xl)*(s[1]-yl)*brp[0] 
                
            itp_g = (xb-s[0])*(yb-s[1])*tlp[1] + \
                (s[0]-xl)*(yb-s[1])*trp[1] +  \
                (xb-s[0])*(s[1]-yl)*blp[1] + \
                (s[0]-xl)*(s[1]-yl)*brp[1] 
                
            itp_b = (xb-s[0])*(yb-s[1])*tlp[2] + \
                (s[0]-xl)*(yb-s[1])*trp[2] +  \
                (xb-s[0])*(s[1]-yl)*blp[2] + \
                (s[0]-xl)*(s[1]-yl)*brp[2] 
            
            # 照片交集的部份，以 Linear Blending 方式計算顏色比例。
            # 點靠近左邊照片，左邊權重大。點靠近右邊照片，右邊權重大。
            if merged[y, x, 0] > 0 or merged[y, x, 1] > 0 or merged[y, x, 2] > 0 :   # 3 channel 有一維不是0，表是是交集處。此處有點鳥，應該有更好的判斷方法。

                weight =  (x-812) / (1280-812)  # blending 計算，這裡也有點鳥，寫死了，手工找了交集範圍
                # weight =  (x-812) / (1280-812) * 0.8    # for testing
                # weight =  (x-812) / (1280-812) * 0.5    # for testing

                merged[y, x, 0] = int(merged[y, x, 0] * (1-weight) + int(itp_r) * weight)  # blending 計算
                merged[y, x, 1] = int(merged[y, x, 1] * (1-weight) + int(itp_g) * weight)  # blending 計算
                merged[y, x, 2] = int(merged[y, x, 2] * (1-weight) + int(itp_b) * weight)  # blending 計算
            else:
                merged[y, x, 0] = int(itp_r)  # 未在交集內，直接用 binear interpolation 的顏色
                merged[y, x, 1] = int(itp_g)
                merged[y, x, 2] = int(itp_b)

        if x%80 == 0:
            print('.', end="")  #只是輸出計算進度用
    print('')

merged = merged.astype(np.uint8)

# minInColumns = np.amin(merged[:,:,0], axis=0)

cv2.imshow("res", merged)            
cv2.imwrite("merged.jpg",merged)

cv2.waitKey(0)
cv2.destroyAllWindows()
