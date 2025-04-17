# coding=utf-8
import cv2
import numpy as np


def find_guidi(im, res_line, res_lines):
    # 将彩色图片转换为灰度图片

    if res_line[4] - 50 < 0 or res_line[4] + 50 > im.shape[0]:
        return [], []

    lines_guidi = [line for line in res_lines if (line[1] > res_line[4] - 50 or line[3] > res_line[4] - 50) and (line[1] < res_line[4] + 50 or line[3] < res_line[4] + 50)]
    lines_guidi = [line for line in lines_guidi if np.sqrt((line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2) > 10]
    lines_guidi.sort()

    lines = []
    result = []
    result1 = []
    pre = 0
    while pre < len(lines_guidi):
        pos = []
        neg = []

        for i in range(pre, len(lines_guidi)):

            if i == len(lines_guidi) - 1:
                lines.append(lines_guidi[i])
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

                elif len(pos) > 0 and len(neg) == 0 and any([l > 20 for l in lens]) and len(pos) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    x0_check = max(0, int(avg_x0 - length))
                    y0_check = max(0, int(avg_y0 - length))
                    x1_check = min(im.shape[1] - 1, int(avg_x0 + length))
                    y1_check = min(im.shape[0] - 1, int(avg_y0 + length))
                    
                    yellow_pixels = np.argwhere(np.all(im[y0_check:y1_check, x0_check:x1_check] == [0, 255, 255], axis=-1))
                    # yellow_pixels = np.where((im[y0_check:y1_check, x0_check:x1_check, 0] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 1] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 2] == 0))
                    if len(yellow_pixels) > 0:
                        continue
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])

                elif len(pos) == 0 and len(neg) > 0 and any([l > 20 for l in lens]) and len(neg) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    x0_check = max(0, int(avg_x0 - length))
                    y0_check = max(0, int(avg_y0 - length))
                    x1_check = min(im.shape[1] - 1, int(avg_x0 + length))
                    y1_check = min(im.shape[0] - 1, int(avg_y0 + length))
                    
                    yellow_pixels = np.argwhere(np.all(im[y0_check:y1_check, x0_check:x1_check] == [0, 255, 255], axis=-1))
                    # yellow_pixels = np.where((im[y0_check:y1_check, x0_check:x1_check, 0] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 1] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 2] == 0))
                    if len(yellow_pixels) > 0:
                        continue
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])

                lines.clear()
                pre = i + 1
                break

            if lines_guidi[i + 1][0] - lines_guidi[i][0] < 20:
                lines.append(lines_guidi[i])
            else:
                lines.append(lines_guidi[i])
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
                    x0_check = max(0, int(avg_x0 - length))
                    y0_check = max(0, int(avg_y0 - length))
                    x1_check = min(im.shape[1] - 1, int(avg_x0 + length))
                    y1_check = min(im.shape[0] - 1, int(avg_y0 + length))
                    
                    yellow_pixels = np.argwhere(np.all(im[y0_check:y1_check, x0_check:x1_check] == [0, 255, 255], axis=-1))
                    # yellow_pixels = np.where((im[y0_check:y1_check, x0_check:x1_check, 0] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 1] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 2] == 0))
                    if len(yellow_pixels) > 0:
                        continue
                    result.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])
                    
                elif len(pos) > 0 and len(neg) == 0 and any([l > 20 for l in lens]) and len(pos) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    # Check if there are any pixels with RGB value (255, 255, 0) in the specified range
                    x0_check = max(0, int(avg_x0 - length))
                    y0_check = max(0, int(avg_y0 - length))
                    x1_check = min(im.shape[1] - 1, int(avg_x0 + length))
                    y1_check = min(im.shape[0] - 1, int(avg_y0 + length))
                    
                    yellow_pixels = np.argwhere(np.all(im[y0_check:y1_check, x0_check:x1_check] == [0, 255, 255], axis=-1))
                    # yellow_pixels = np.where((im[y0_check:y1_check, x0_check:x1_check, 0] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 1] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 2] == 0))
                    if len(yellow_pixels) > 0:
                        continue
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])
                    
                    
                elif len(pos) == 0 and len(neg) > 0 and any([l > 20 for l in lens]) and len(neg) <= 3:
                    avg_x0 = np.mean([line[0] for line in lines])
                    avg_y0 = np.mean([line[1] for line in lines])
                    # Check if there are any pixels with RGB value (255, 255, 0) in the specified range
                    x0_check = max(0, int(avg_x0 - length))
                    y0_check = max(0, int(avg_y0 - length))
                    x1_check = min(im.shape[1] - 1, int(avg_x0 + length))
                    y1_check = min(im.shape[0] - 1, int(avg_y0 + length))
                    
                    yellow_pixels = np.argwhere(np.all(im[y0_check:y1_check, x0_check:x1_check] == [0, 255, 255], axis=-1))
                    # yellow_pixels = np.where((im[y0_check:y1_check, x0_check:x1_check, 0] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 1] == 255) & 
                    #                          (im[y0_check:y1_check, x0_check:x1_check, 2] == 0))
                    if len(yellow_pixels) > 0:
                        continue
                    result1.append([avg_x0 - length, avg_y0 - length,avg_x0 + length, avg_y0 + length])

                lines.clear()
                pre = i + 1
                break
    
    # Ensure result does not exceed image boundaries
    for i in range(len(result)):
        x0, y0, x1, y1 = result[i]
        x0 = max(0, min(x0, im.shape[1] - 1))
        y0 = max(0, min(y0, im.shape[0] - 1))
        x1 = max(0, min(x1, im.shape[1] - 1))
        y1 = max(0, min(y1, im.shape[0] - 1))
        result[i] = [x0, y0, x1, y1]
            
    for i in range(len(result1)):
        x0, y0, x1, y1 = result1[i]
        x0 = max(0, min(x0, im.shape[1] - 1))
        y0 = max(0, min(y0, im.shape[0] - 1))
        x1 = max(0, min(x1, im.shape[1] - 1))
        y1 = max(0, min(y1, im.shape[0] - 1))
        result1[i] = [x0, y0, x1, y1] 
    
    return result, result1  # 返回检测结果 result1存储单边
