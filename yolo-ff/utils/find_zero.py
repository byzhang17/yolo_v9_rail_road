import numpy as np
from collections import deque
import cv2 
import time 


def find_zero(im1, res_line, res_lines):
    
    img = im1.copy()
    
    img = img[res_line[-1] + 5:res_line[-1] + 130, :]
    
    lines_xlw = [line for line in res_lines if (line[1] > res_line[3] - 50 or line[3] > res_line[3] - 50) and (line[1] < res_line[3] + 50 or line[3] < res_line[3] + 50)]
    lines_xlw = [line for line in lines_xlw if np.sqrt((line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2) > 10]
    lines_xlw.sort()

    
    #低于127时设置成255，255是白色，代表亮度（能量）最高，包括三通道的图像中(255,255,255)是白色
    ret,thresh = cv2.threshold(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),127,255,0)

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#得到轮廓信息
    

    result = []
    result1 = []
    result3 = []
    result4 = []
    
    for i in contours:
        # 外接正矩形
        x, y, w, h = cv2.boundingRect(i)
        result.append([x, y, x + w, y + h])
        
    for res in result:
            x1, y1, x2, y2 = res
            img_height, img_width, _ = img.shape
            left_bound = img_width // 3
            
            x_left = max(x1 - left_bound, 0)
            x_right = min(x2 + left_bound, img_width)
            
            x_top = max(y1 - 10, 0)
            x_bottom = min(y2 + 10, img_height)
            
            x_top2 = max(y1 - 60, 0)
            x_left2 = max(x1 - 20, 0)
            x_right2 = min(x2 + 20, img_width)
            
            for other_res in result:
                if other_res != res:
                    other_x0, other_y0, other_x1, other_y1 = other_res
                    if (other_x0 >= x_left and other_x1 <= x_right and other_y0 >= x_top and other_y1 <= x_bottom) or (other_x0 >= x_left2 and other_x1 <= x_right2 and other_y0 >= x_top2 and other_y1 <= x_bottom) :
                        result1.append(res)
                        break
                        
    result3 = [res for res in result if res not in result1]
    
    
    for i in range(len(result3)):
        x1, y1, x2, y2 = result3[i]
        width = x2 - x1
        height = y2 - y1
        if width < 10:
            x2 = min(x1 + 10, img.shape[1] - 1)
            if x2 - x1 < 10:
                x1 = max(x2 - 10, 0)
        if height < 10:
            y2 = min(y1 + 10, img.shape[0] - 1)
            if y2 - y1 < 10:
                y1 = max(y2 - 10, 0)
        result3[i] = [int(x1), int(y1) + res_line[-1] + 5, int(x2), int(y2) + res_line[-1] + 5]
    
    for res in result3:
        x1, y1, x2, y2 = res
        
        x_min = max(x1 - 10, 0)
        x_max = min(x2 + 10, img.shape[1] - 1)
        
        for line in lines_xlw:
            x3, y3, x4, y4 = line
            if x3 >= x_min and x4 <= x_max:
                result4.append(res)
                break
            
    result3 = [res for res in result3 if res not in result4]
    
    return result3
        

