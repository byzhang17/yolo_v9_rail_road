# coding=utf-8
import cv2
import numpy as np

def is_buquan(im, res):
    tag = True
    imc = im.copy()
    crop = imc[10 : res[1] - 10, :]
    height, width = crop.shape[:2]
    crop_array = np.array(crop)
    colors = [(0, 0, 0), (255, 255, 255), (230, 230, 230)]
    num = 0
    for i in range(0, height):
        for j in range(0, width):
            color2 = tuple(crop_array[i,j])
            tag2 = False
            for color in colors:
                if color2 == color:
                    tag2 = True
                    break

            if tag2 == False:
                colors.append(color2)
                num = num + 1


    if num >= 6:
        tag = False

    return tag
