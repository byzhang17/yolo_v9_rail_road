# coding=utf-8
import cv2
import numpy as np


# 读取输入图片
def remove_overlapping_boxes2(result, model_result, im0):
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

    filtered_result = [[int(max(0, x0)), int(max(0, y0)), min(im0.shape[1]-int(max(0, x0)),int(x1) - int(x0)), int(y1) - int(y0), 23, 0.5] for x0, y0, x1, y1 in
                       filtered_result]
    return filtered_result


def find_yulin(im, res_line, res_lines):
    
    
    lines_yunlin = [line for line in res_lines if (line[1] > res_line[0] or line[3] > res_line[0]) and (line[1] < res_line[1] or line[3] < res_line[1])]
    lines_yunlin = [line for line in lines_yunlin if np.sqrt((line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2) > 10]
    lines_yunlin.sort()
    
    lines = []

    result = []

    pre = 0
    while pre < len(lines_yunlin):
        pos = []
        neg = []
        for i in range(pre, len(lines_yunlin)):

            if i == len(lines_yunlin) - 1:
                lines.append(lines_yunlin[i])
                length = 0
                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))

                min_x0 = min([line[0] for line in lines])
                min_y0 = min([line[1] for line in lines])
                max_x1 = max([line[2] for line in lines])
                max_y1 = max([line[3] for line in lines])

                length = length / len(lines)
                if (len(lines) > 6):
                    result.append([min_x0, min_y0 , max_x1, max_y1 ])

                lines.clear()
                pre = i + 1
                break

            if lines_yunlin[i + 1][0] - lines_yunlin[i][0] < 90:
                lines.append(lines_yunlin[i])
            else:
                lines.append(lines_yunlin[i])
                length = 0

                lens = []
                for line in lines:
                    x0, y0, x1, y1 = line
                    length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                    lens.append(np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))

                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])

                min_x0 = min([line[0] for line in lines])
                min_y0 = min([line[1] for line in lines])
                max_x1 = max([line[2] for line in lines])
                max_y1 = max([line[3] for line in lines])

                length = length / len(lines)
                if (len(lines) > 6):
                    result.append([min_x0, min_y0 , max_x1, max_y1 ])
                    
                lines.clear()
                pre = i + 1
                break
    
    for i in range(len(result)):
        x0, y0, x1, y1 = result[i]
        x0 = max(0, min(x0, im.shape[1] - 1))
        y0 = max(0, min(y0, im.shape[0] - 1))
        x1 = max(0, min(x1, im.shape[1] - 1))
        y1 = max(0, min(y1, im.shape[0] - 1))
        result[i] = [x0, y0, x1, y1]
           
    return result