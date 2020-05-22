# 影像拼接
### 自行計算 Affine Transformation, Binear Interpolation 與 Linear Blending

## 原始影像 - 輕井澤王子飯店前
> 左
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/IMG_1265.JPG)

> 右
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/IMG_5732.JPG)

## 拼接結果
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/merged.jpg)

## 手動人工在兩張照片中選擇 7 個特徵點
|     | (左)IMG_1265.JPG  | (右)IMG_5732.JPG |
| --- | ------------- | ------------- |
| 1 | (1257, 411)  | (369, 393) |
| 2 | (1071, 480)  | (209, 459) |
| 3 | (1112, 192)  | (251, 181) |
| 4 | (931, 92)    |  (60, 31)  |
| 5 | (1046, 850)  | (202, 825) |
| 6 | (1266,492)   | (376, 463) |
| 7 | (1192, 426)  | (318, 406) |

![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/mapping_corp.jpg)


