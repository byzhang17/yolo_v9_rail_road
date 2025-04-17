# coding=utf-8
import cv2
import numpy as np


def remove_overlapping_boxes4(result, model_result, im0):
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

    model_boxes = [[x, y, x + w, y + h] for x, y, w, h, _, _ in model_result]

    filtered_result = [
        box for box in result
        if all(iou(box, yolo_box) <= 0 for yolo_box in model_boxes)
    ]

    filtered_result = [
        [int(max(0, x0)), int(max(0, y0)), min(im0.shape[1] - int(max(0, x0)), int(x1) - int(x0)), int(y1) - int(y0),
         26, 0.5] for x0, y0, x1, y1 in filtered_result
    ]
    return filtered_result


def find_hs4(im, res_line, res_lines):

    line_hs4 = [
        line for line in res_lines
        if np.sqrt((line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2) > 10 and
        (line[1] < res_line[4] or line[3] < res_line[4])
    ]
    line_hs4.sort()

    lines_res = []
    pre = 0
    while pre < len(line_hs4):
        lines = []
        for i in range(pre, len(line_hs4)):
            lines.append(line_hs4[i])
            if i == len(line_hs4) - 1 or line_hs4[i + 1][0] - line_hs4[i][0] >= 20:
                length = np.mean([
                    np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
                    for x0, y0, x1, y1 in lines
                ])
                if len(lines) >= 2:
                    lines_head = [line for line in lines if line[1] < res_line[1] or line[3] < res_line[1]]
                    lines_mid = [line for line in lines if (res_line[1] < line[1] < res_line[3] or res_line[1] < line[3] < res_line[3])]
                    if lines_head and lines_mid:
                        lines_res.append(lines.copy())
                lines.clear()
                pre = i + 1
                break

    result = []
    for lines in lines_res:
        min_x0 = min(line[0] for line in lines)
        min_y0 = min(line[1] for line in lines)
        max_x1 = max(line[2] for line in lines)

        white_pixel_found = np.any(
            np.all(im[res_line[-2] + 10:res_line[-1] - 10, min_x0:max_x1] >= [200, 200, 200], axis=2)
        )

        if white_pixel_found:
            result.append([min_x0, min_y0, max_x1, res_line[-1]])

    # Ensure result does not exceed image boundaries
    result = [
        [
            max(0, min(x0, im.shape[1] - 1)),
            max(0, min(y0, im.shape[0] - 1)),
            max(0, min(x1, im.shape[1] - 1)),
            max(0, min(y1, im.shape[0] - 1))
        ]
        for x0, y0, x1, y1 in result
    ]

    return result
