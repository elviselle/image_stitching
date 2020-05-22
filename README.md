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
|     | (左)IMG_1265.JPG  | (右)IMG_5732.JPG | A 組合 | B 組合 | C 組合 | D 組合 |
| --- | ------------- | ------------- | - | - | - | - |
| 1 | (1257, 411)  | (369, 393) | V | V | V |   |
| 2 | (1071, 480)  | (209, 459) | V |   |   |   |
| 3 | (1112, 192)  | (251, 181) | V |   |   |   |
| 4 | (931, 92)    |  (60, 31)  |   | V |   | V |
| 5 | (1046, 850)  | (202, 825) |   | V |   | V |
| 6 | (1266,492)   | (376, 463) |   |   | V | V |
| 7 | (1192, 426)  | (318, 406) |   |   | V |   |

![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/mapping_corp.png)
### 每三點可決定一個 Affine Transform，進行四個組合測試，看哪個組合拼接效果比較好


