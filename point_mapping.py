# -*- coding: utf-8 -*-
"""
# 左 IMG_1265 <-> 右IMG_5732
1. 車尾 (1257, 411)  <->  (369, 393)
2. 石頭 (1071, 480)  <-> (209, 459)
3. 樹Y (1112, 192)  <-> (251, 181)
4. 樹尖 (931, 92)  <->  (60, 31)
5. 樹尖倒影 (1046, 850)  <-> (202, 825)
6. 右邊石頭 (1266,492) <-> (376, 463)
7. 車燈 (1192, 426) <-> (318, 406)
"""

import numpy as np
import cv2


# 讀入兩張影像
pic1 = cv2.imread("imgs/IMG_1265.JPG")  #左
pic2 = cv2.imread("imgs/IMG_5732.JPG")  #右
pic2 = cv2.resize(pic2, (pic1.shape[1], pic1.shape[0]), interpolation=cv2.INTER_CUBIC)

print(pic1.shape)
print(pic2.shape)

merged = np.zeros((pic1.shape[0], pic1.shape[1]*2, 3))
print(merged.shape)

merged[:pic1.shape[0], :pic1.shape[1], :] = pic1
merged[:pic1.shape[0], pic1.shape[1]:, :] = pic2


# 在圖片上畫一個綠色方框，線條寬度為 2 px

cv2.line(merged, (1257, 411), (1649, 393), (0, 230, 255), 2)
cv2.line(merged, (1071, 480), (1489, 459), (0, 230, 255), 2)
cv2.line(merged, (1112, 192), (1531, 181), (0, 230, 255), 2)
cv2.line(merged, (931, 92), (1340, 31), (0, 230, 255), 2)
cv2.line(merged, (1046, 850), (1482, 825), (0, 230, 255), 2)
cv2.line(merged, (1266, 492), (1656, 463), (0, 230, 255), 2)
cv2.line(merged, (1192, 426), (1508, 406), (0, 230, 255), 2)

cv2.rectangle(merged, (1254, 408), (1260, 414), (255, 0, 0), 2)
cv2.rectangle(merged, (1068, 477), (1074, 483), (255, 0, 0), 2)
cv2.rectangle(merged, (1109, 189), (1115, 195), (255, 0, 0), 2)
cv2.rectangle(merged, (928, 89), (934, 95), (255, 0, 0), 2)
cv2.rectangle(merged, (1043, 847), (1049, 853), (255, 0, 0), 2)
cv2.rectangle(merged, (1263, 489), (1269, 495), (255, 0, 0), 2)
cv2.rectangle(merged, (1189, 423), (1195, 429), (255, 0, 0), 2)

cv2.rectangle(merged, (1646, 390), (1652, 396), (255, 0, 0), 2)
cv2.rectangle(merged, (1486, 456), (1492, 462), (255, 0, 0), 2)
cv2.rectangle(merged, (1528, 178), (1534, 184), (255, 0, 0), 2)
cv2.rectangle(merged, (1337, 28), (1343, 34), (255, 0, 0), 2)
cv2.rectangle(merged, (1479, 822), (1485, 828), (255, 0, 0), 2)
cv2.rectangle(merged, (1653, 460), (1659, 466), (255, 0, 0), 2)
cv2.rectangle(merged, (1595, 403), (1601, 409), (255, 0, 0), 2)


merged = merged.astype(np.uint8)

cv2.imshow("res", merged)            
cv2.imwrite("mapping.jpg", merged)


cv2.waitKey(0)
cv2.destroyAllWindows()

