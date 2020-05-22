# 影像拼接
### 自行計算 Affine Transformation, Bilinear Interpolation 與 Linear Blending

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
#### 每三點可決定一個 Affine Transformation，進行四個組合測試，看哪個組合拼接效果比較好

![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/mapping_corp.png)

## Affine Transformation
#### 座標轉換
<!-- \begin{bmatrix}x'\\y'\end{bmatrix} = \begin{bmatrix}a & b & c\\ d & e & f\end{bmatrix} \begin{bmatrix}x\\y\\1\end{bmatrix} --> 
<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7Dx%27%5C%5Cy%27%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7Da%20%26%20b%20%26%20c%5C%5C%20d%20%26%20e%20%26%20f%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7Dx%5C%5Cy%5C%5C1%5Cend%7Bbmatrix%7D" /> 

<img src="https://latex.codecogs.com/gif.latex?x%27%3D%20ax%20%2B%20by%20%2B%20c" /> 
<img src="https://latex.codecogs.com/gif.latex?y%27%3D%20dx%20%2B%20ey%20%2B%20f" /> 

#### 要解a, b, c, d, e, f，需要 6 個關係式，而三個點會有 6 個式子。可再整理成下面的聯位方程，然後解出 6 個未知數。
#### 以組合A為例：

<!-- \begin{bmatrix}369\\393\\209\\459\\251\\181\end{bmatrix} = \begin{bmatrix}1257 & 411 & 0 & 0 & 1 & 0\\0&0&1257& 411&0&1\\ 1071& 480& 0 & 0 & 1 & 0\\0&0&1071& 480&0&1 \\1112& 192& 0 & 0 & 1 & 0\\0&0&1112& 192&0&1 \\\end{bmatrix} \begin{bmatrix}a\\b\\c\\d\\e\\f\end{bmatrix} --> 
<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7D369%5C%5C393%5C%5C209%5C%5C459%5C%5C251%5C%5C181%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D1257%20%26%20411%20%26%200%20%26%200%20%26%201%20%26%200%5C%5C0%260%261257%26%20411%260%261%5C%5C%201071%26%20480%26%200%20%26%200%20%26%201%20%26%200%5C%5C0%260%261071%26%20480%260%261%20%5C%5C1112%26%20192%26%200%20%26%200%20%26%201%20%26%200%5C%5C0%260%261112%26%20192%260%261%20%5C%5C%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7Da%5C%5Cb%5C%5Cc%5C%5Cd%5C%5Ce%5C%5Cf%5Cend%7Bbmatrix%7D" /> 

numpy.libalg package 可以解線性方程

    target = np.array(
        [[1257, 411, 0, 0, 1, 0], 
         [0, 0, 1257, 411, 0, 1], 
         [1071, 480, 0, 0, 1, 0], 
         [0, 0, 1071, 480, 0, 1],
         [1112, 192, 0, 0, 1, 0], 
         [0, 0, 1112, 192, 0, 1]])  #左圖座標
    src = np.array([369,393,209,459,251,181])  #右圖座標
    
    param = np.linalg.solve(target, src)  # 解聯立方程 - 求出座標轉換矩陣
    pring(param)

解出 [a, b, e, d, e, f] = [ 8.51061314e-01 -2.46752991e-02  3.42931473e-03  9.65765979e-01 -6.90395771e+02 -1.78981257e+01 ]

然後，我們可以用這個座標轉換矩陣來計算左圖的某一點，是右圖的哪一點。
使用 numpy.matmul() 矩陣乘法即可。

    target_point = np.array([[1257,411,0,0,1,0], [0,0,1257,411,0,1]])
    source_point = np.matmul(target_point, param)  # 計算轉換後之座標，[369, 393]


## Inverse Mapping

#### 先做一張大一點的黑色影像，把左邊(pic1)填進來。先叫它 target。之後我們用 Inverse Mapping 方式把右邊填上。
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/merged_preprocess.jpg)

#### Inverse Mapping 指由要合成照片的空間(target)上的每一個點，去算它在 Source (pic2) 座標系的哪個位置。如果可以落在 source 的影像範圍內，就取它的顏色過來填到 target 上。可以避免 Forward Mapping 時 target 有空隙沒填到顏色。
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/inverse_mapping.jpg)


## Bilinear Interpolation
#### 由 target 空間轉換到 source 空間時，算出來的座標會是小數。它被四個點圍繞。
#### 這時，到底要取 source 座標的哪個點的顏色來填到 target，就會用到 Bilinear Interpolation。
![](https://github.com/elviselle/image_stitching/blob/master/.readme_imgs/bilinear.png)

假設 target image 某一點座標轉換後，落在 source image 的 (133.2, 56.3)，
則要填回的 target image 的顏色等於
    
    # target_color = 左上角鄰居顏色 * 左上角權重 +  
    #    右上上角鄰居顏色 * 右上角權重 +
    #    左下角鄰居顏色 * 左下角權重 +
    #    右下角鄰居顏色 * 右下角權重
    
    target_color = 92 * 0.8 * 0.7 +
        83 * 0.2 * 0.7 + 
        9 * 0.3 * 0.8 +
        53 * 0.2 * 0.3
