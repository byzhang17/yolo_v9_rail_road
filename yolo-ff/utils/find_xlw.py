# coding=utf-8
import cv2
import numpy as np


def get_guize1(im):
    
    height, width = im.shape[:2]
    #im = im[:, 2 * width // 3:]

    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(gray_img, 30, 150)
    
    lines = cv2.HoughLines(canny, 1, np.pi / 180, 180)
    if lines is None:
        return []
    lines1 = lines[:, 0, :]

    res = []
    line = []
    for rho, theta in lines1[:]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 3000 * (-b))
        y1 = int(y0 + 3000 * (a))
        x2 = int(x0 - 3000 * (-b))
        y2 = int(y0 - 3000 * (a))
        #cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 2)  
        res.append(y1)
        
    res.sort()
    
    res1 = [y for y in res if y > 600 and y < im.shape[0] - 4]


    return res ,res1


def find_xlw(im, res_line, res_lines):
    # 将彩色图片转换为灰度图片

    if res_line[3] - 50 < 0 :
        return []
    
    lines_hs3 = [line for line in res_lines if (line[1] > res_line[0] or line[3] > res_line[0]) and (line[1] < res_line[1] or line[3] < res_line[1])]
 
    
    lines_xlw = [line for line in res_lines if (line[1] > res_line[3] - 50 or line[3] > res_line[3] - 50) and (line[1] < res_line[3] + 50 or line[3] < res_line[3] + 50)]
    lines_xlw = [line for line in lines_xlw if np.sqrt((line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2) > 10]
    lines_xlw.sort()
    lines_hs3.sort()

    lines = []
    result = []
    result1 = []
    pre = 0
    while pre < len(lines_xlw):
        pos = []
        neg = []
        for i in range(pre, len(lines_xlw)):

            if i == len(lines_xlw) - 1:
                lines.append(lines_xlw[i])
                length = 0
                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))
                    if x1 - x0 != 0:
                        k = (y1 - y0) / (x1 - x0)
                        if k > 0:
                            pos.append(line)
                        else:
                            neg.append(line)
                length = int(length / len(lines))
                if len(pos) > 0 and len(neg) > 0 and any([l > 15 for l in lens]) and (len(pos) + len(neg) > 2):
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    result.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])
                elif len(pos) > 0 and len(neg) == 0 and any([l > 18 for l in lens]) and len(pos) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    
                    min_y0 = min([line[1] for line in lines])
                    min_y1 = min([line[3] for line in lines])
                    
                    min_y = abs(min(min_y0, min_y1) - res_line[3])  
                    
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length, min_y])
                elif len(pos) == 0 and len(neg) > 0 and any([l > 18 for l in lens]) and len(neg) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    min_y0 = min([line[1] for line in lines])
                    min_y1 = min([line[3] for line in lines])
                    
                    min_y = abs(min(min_y0, min_y1) - res_line[3])  
                    
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length, min_y])

                lines.clear()
                pre = i + 1
                break

            if lines_xlw[i + 1][0] - lines_xlw[i][0] < 50:
                lines.append(lines_xlw[i])
            else:
                lines.append(lines_xlw[i])
                length = 0
                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))
                    if x1 - x0 != 0:
                        k = (y1 - y0) / (x1 - x0)
                        if k > 0:
                            pos.append(line)
                        else:
                            neg.append(line)
                length = int(length / len(lines))
                if len(pos) > 0 and len(neg) > 0 and any([l > 15 for l in lens]) and (len(pos) + len(neg) > 2):
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    result.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])
                elif len(pos) > 0 and len(neg) == 0 and any([l > 18 for l in lens]) and len(pos) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    
                    min_y0 = min([line[1] for line in lines])
                    min_y1 = min([line[3] for line in lines])
                    min_y = abs(min(min_y0, min_y1) - res_line[3])  
                    
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length, min_y])
                elif len(pos) == 0 and len(neg) > 0 and any([l > 18 for l in lens]) and len(neg) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    
                    min_y0 = min([line[1] for line in lines])
                    min_y1 = min([line[3] for line in lines])
                    
                    min_y = abs(min(min_y0, min_y1) - res_line[3])  
                    
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length, min_y])

                lines.clear()
                pre = i + 1
                break
            
    for i in range(len(result1)):
        x0, y0, x1, y1, miny= result1[i]
        x0 = int(max(0, min(x0 , im.shape[1] - 1)))
        y0 = int(max(0, min(y0, im.shape[0] - 1)))
        x1 = int(max(0, min(x1 , im.shape[1] - 1)))
        y1 = int(max(0, min(y1, im.shape[0] - 1)))
        result1[i] = [x0, y0, x1, y1, miny]
    
    result4 = []
    #检测上面有没有出波
    for res in result1:
        x1, y1, x2, y2 ,miny= res
        
        x_min = max(x1 - 10, 0)
        x_max = min(x2 + 10, im.shape[1] - 1)
        
        for line in lines_hs3:
            x3, y3, x4, y4 = line
            if x3 >= x_min and x4 <= x_max:
                result4.append(res)
                break
    
    result1 = [res for res in result1 if res not in result4]        
    
    #检测零度区域有没有失波 
    
    result2 = []
    
    res1 , res2 = get_guize1(im.copy())
    
    if len(res2) == 0:
        return result1
    
    for line in result1:
        black_pixel_found = False
        x0, y0, x1, y1 ,miny= line
        for x in range(int(x0), int(x1)):
            if  np.all(im[res2[0] + 4, x] == [0, 0, 0]):
                black_pixel_found = True
                break
        if black_pixel_found:
            result2.append(line)
            
    #result2.clear()
    

    result3 = []
    #检测有没有零度出波
    for line in result2:
        white_pixel_found = False
        x0, y0, x1, y1 ,miny= line     
        
        for y in range(res_line[-1] + 10, res2[0] - 30):
            for x in range(int(x0), int(x1)):
                if np.all(im[y, x] >= [200, 200, 200]):
                    white_pixel_found = True
                    break
        #cv2.rectangle(im, (int(x0), int(res_line[-1] + 10)), (int(x1), int(res2[0] - 30),), (0, 0, 255), 2)
        if not white_pixel_found:
            result3.append(line)
    
    return result3  # 返回检测结果 result1存储单边
