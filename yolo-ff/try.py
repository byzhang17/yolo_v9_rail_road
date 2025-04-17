import cv2
import numpy as np

wenzi = cv2.imread('./datasets/0KM18.0M _15.png')  # 读取原图像
cv2.imshow('src', wenzi)

kernel = np.ones((2, 2), np.uint8)  # 设置kenenel大小
wenzi_new = cv2.dilate(wenzi, kernel, iterations=2)  # 膨胀操作
cv2.imshow('./datasets/0KM18.0M _15.png_new', wenzi_new)
cv2.waitKey(100000)