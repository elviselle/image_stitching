# -*- coding: utf-8 -*-
"""
A 
           IMG_1265 <-> IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
2. 石頭 (1071, 480)  <-> (209, 459)
3. 樹Y (1112, 192)  <-> (251, 181)

B
           IMG_1265 <-> IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)    <-> (202, 825)

C
1. 車尾 (1257, 411)  <->  (369, 393)
6. 右邊石頭 (1266,492) <-> (376, 463)
7. 車燈 (1192, 426) <-> (318, 406)

D
           IMG_1265 <-> IMG_5732
6. 右邊石頭 (1266,492) <-> (376, 463)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)    <-> (202, 825)

"""

import numpy as np
import math
import cv2


h_offset = 10

print("利用三個點 算出轉換的關係式 用for跑轉換 再貼上圖")
target = np.array([[1257, 411+h_offset, 0, 0, 1, 0], [0, 0, 1257, 411+h_offset, 0, 1], [1071, 480+h_offset, 0, 0, 1, 0], [0, 0, 1071, 480+h_offset, 0, 1],
                 [1112, 192+h_offset, 0, 0, 1, 0], [0, 0, 1112, 192+h_offset, 0, 1]])
src = np.array([369,393,209,459,251,181])
param = np.linalg.solve(target,src)
print(param)

t = np.array([[0,0,0,0,1,0], [0,0,0,0,0,1]])
s = np.matmul(t,param)

print(s)


pic1 = cv2.imread("imgs/IMG_1265.JPG")
pic2 = cv2.imread("imgs/IMG_5732.JPG")
print(pic2.shape)

merged_width = 2300   #2337
merged_height = 900
merged = np.zeros((merged_height, merged_width, 3))
merged[h_offset:(854+h_offset), :1280, :] = pic1

cv2.imwrite("merged_preprocess.jpg",merged)


# print(pic1[0, 0])
# print(merged[0, 0])

# print(merged)

# condidate = np.empty((0, 2), int)

# for y in range(merged_height):
#     for x in range(merged_width):
#         t = np.array([[x,y,0,0,1,0], [0,0,x,y,0,1]])
#         s = np.matmul(t,param)
#         if s[0]>0 and s[0]<1271 and s[1]>0 and s[1]<847:
#             print('[%4d,%4d]' % (y, x))
#             condidate = np.append(condidate, np.array([[y, x]]), axis=0)
# print('condidate:', condidate)

for y in range(merged_height):
    print(y, end="")
    for x in range(merged_width):
        t = np.array([[x,y,0,0,1,0], [0,0,x,y,0,1]])
        s = np.matmul(t,param)
        if s[0]>0 and s[0]<1271 and s[1]>0 and s[1]<847:
            # print('y:', y, ', x:', x)
            # print('row:', s[1], ', column:', s[0])
            # print("row range:%d~%d, column range:%d~%d" % (math.floor(s[1]),math.ceil(s[1]), 
            #     math.floor(s[0]),math.ceil(s[0])) )
            
            xl = math.floor(s[0])
            yl = math.floor(s[1])
            xb = math.ceil(s[0])
            yb = math.ceil(s[1])
            
            ltp = pic2[yl, xl]
            rtp = pic2[yl, xb]
            lbp = pic2[yb, xl]
            rbp = pic2[yb, xb]
            
            itcp_r = (xb-s[0])*(yb-s[1])*ltp[0] + \
                (s[0]-xl)*(yb-s[1])*rtp[0] +  \
                (xb-s[0])*(s[1]-yl)*lbp[0] + \
                (s[0]-xl)*(s[1]-yl)*rbp[0] 
                
            itcp_g = (xb-s[0])*(yb-s[1])*ltp[1] + \
                (s[0]-xl)*(yb-s[1])*rtp[1] +  \
                (xb-s[0])*(s[1]-yl)*lbp[1] + \
                (s[0]-xl)*(s[1]-yl)*rbp[1] 
                
            itcp_b = (xb-s[0])*(yb-s[1])*ltp[2] + \
                (s[0]-xl)*(yb-s[1])*rtp[2] +  \
                (xb-s[0])*(s[1]-yl)*lbp[2] + \
                (s[0]-xl)*(s[1]-yl)*rbp[2] 
            
            if merged[y, x, 0] > 0 or merged[y, x, 1] > 0 or merged[y, x, 2] > 0 :
                # merged[y, x, 0] = int(itcp_r)
                # merged[y, x, 1] = int(itcp_g)
                # merged[y, x, 2] = int(itcp_b)
                rate =  (x-812) / (1280-812) * 0.8
                
                merged[y, x, 0] = int(merged[y, x, 0] * (1-rate) + int(itcp_r) * rate)
                merged[y, x, 1] = int(merged[y, x, 1] * (1-rate) + int(itcp_g) * rate)
                merged[y, x, 2] = int(merged[y, x, 2] * (1-rate) + int(itcp_b) * rate)
            else:
                merged[y, x, 0] = int(itcp_r)
                merged[y, x, 1] = int(itcp_g)
                merged[y, x, 2] = int(itcp_b)

            
            # rate =  (x-812) / (1280-812)
            
            # if rate < 0:
            #     continue
            # elif rate > 0 and rate <= 1:
            #     merged[y, x, 0] = int(merged[y, x, 0] * (1-rate) + int(itcp_r) * rate)
            #     merged[y, x, 1] = int(merged[y, x, 1] * (1-rate) + int(itcp_g) * rate)
            #     merged[y, x, 2] = int(merged[y, x, 2] * (1-rate) + int(itcp_b) * rate)
            # else:
            #     merged[y, x, 0] = int(itcp_r)
            #     merged[y, x, 1] = int(itcp_g)
            #     merged[y, x, 2] = int(itcp_b)

                
            # print(ltp)
            # print(merged[y, x]) 
        if x%80 == 0:
            print('.', end="")
    print('')

            
merged = merged.astype(np.uint8)

# minInColumns = np.amin(merged[:,:,0], axis=0)

cv2.imshow("res", merged)            
cv2.imwrite("merged.jpg",merged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# for i in range(pic2.shape[0]):
#     for j in range(pic2.shape[1]):
#         src = numpy.array([[j,i,0,0,1,0],[0,0,j,i,0,1]])
#         ans = numpy.round(numpy.matmul(src,c),0)
#         if ans[1] >= pic1.shape[0] or ans[0] >= pic1.shape[1] :
#             continue
#         if ans[1] < 0 or ans[0] < 0 :
#             continue
#         r, g, b = pic2[i,j]
#         if r >= 200 and g >= 200 and b >= 200:
#             continue
#         pic1[int(ans[1]),int(ans[0])] = pic2[i,j]

# cv2.imshow("res",pic1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("t1.jpg",pic1)