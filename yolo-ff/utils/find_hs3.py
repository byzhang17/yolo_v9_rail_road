# coding=utf-8
import cv2
import numpy as np


# 读取输入图片
def remove_overlapping_boxes3(result, model_result, im0):
    def iou(box1, box2):
        x1, y1, x2, y2 = box1
        x1_, y1_, x2_, y2_ = box2

        xi1 = max(x1, x1_)
        yi1 = max(y1, y1_)
        xi2 = min(x2, x2_)
        yi2 = min(y2, y2_)

        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x2_ - x1_) * (y2_ - y1_)

        union_area = box1_area + box2_area - inter_area

        return inter_area / union_area

    def convert_to_box(model_result):
        boxes = []
        for item in model_result:
            x, y, w, h, _, _ = item
            boxes.append([x, y, x + w, y + h])
        return boxes

    model_boxes = convert_to_box(model_result)

    filtered_result = []
    for box in result:
        keep = True
        for yolo_box in model_boxes:
            corresponding_model_result = model_result[model_boxes.index(yolo_box)]
            if iou(box, yolo_box) > 0:
                keep = False
                break
        if keep:
            filtered_result.append(box)

    filtered_result = [
        [int(max(0, x0)), int(max(0, y0)), min(im0.shape[1] - int(max(0, x0)), int(x1) - int(x0)), int(y1) - int(y0),
         26, 0.5] for x0, y0, x1, y1 in
        filtered_result]
    return filtered_result


def find_xiantiaohs3(img0):
    h, w, _ = img0.shape

    img0[np.where((img0 >= [230, 230, 230]).all(axis=2))] = [0, 0, 0]

    img0[np.where((img0 == [52, 255, 191]).all(axis=2))] = [0, 0, 0]

    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    # 创建一个LSD对象
    fld = cv2.ximgproc.createFastLineDetector()
    # 执行检测结果
    dlines = fld.detect(img)
    lines2 = []
    if isinstance(dlines, np.ndarray):
        for dline in dlines:

            x0 = int(round(dline[0][0]))
            y0 = int(round(dline[0][1]))
            x1 = int(round(dline[0][2]))
            y1 = int(round(dline[0][3]))
            length = np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))

            # if length > 14 and length < 100:
            if length > 1 and length < 100:

                k = (y1 - y0) / (x1 - x0) if x1 - x0 != 0 else 1

                if abs(k) < 0.6:
                    continue

                if y0 < y1:
                    lines2.append([x0, y0, x1, y1])
                else:
                    lines2.append([x1, y1, x0, y0])
                # cv2.line(img0, (x0, y0), (x1, y1), (255, 255, 255), 2, cv2.LINE_AA)

    return lines2


def find_hs3(im, res_line, res_lines):
    #es_lines = find_xiantiaohs3(im.copy())

    lines_hs3 = [line for line in res_lines if
                 (line[1] > res_line[0] or line[3] > res_line[0]) and (line[1] < res_line[1] or line[3] < res_line[1])]
    lines_hs3.sort()
    lines = []
    result = []
    pre = 0
    while pre < len(lines_hs3):
        for i in range(pre, len(lines_hs3)):
            if i == len(lines_hs3) - 1:
                lines.append(lines_hs3[i])
                length = 0
                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))

                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])

                length = length / len(lines)

                length1 = lines[len(lines) - 1][0] - lines[0][0]

                if ((len(lines) <= 8) and any([l > 15 for l in lens]) and length1 < 30):
                    result.append([avg_x0 - length, avg_y0 - length, avg_x0 + length, avg_y0 + length])

                lines.clear()
                pre = i + 1
                break

            if lines_hs3[i + 1][0] - lines_hs3[i][0] < 100:
                lines.append(lines_hs3[i])
            else:
                lines.append(lines_hs3[i])
                length = 0
                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))

                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])

                length = length / len(lines)

                length1 = lines[len(lines) - 1][0] - lines[0][0]
                
                #print(length1, len(lines), length, lens)

                if ((len(lines) <= 8) and any([l > 15 for l in lens]) and length1 < 30):
                    result.append([avg_x0 - length, avg_y0 - length, avg_x0 + length, avg_y0 + length])

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

    return result

