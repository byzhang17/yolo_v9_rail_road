# coding=utf-8
import cv2
import numpy as np


def remove_overlapping_boxes(result, model_result, im0):
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

        return inter_area / union_area if union_area > 0 else 0

    model_boxes = [
        [x, y, x + w, y + h, class_id]
        for x, y, w, h, class_id, _ in model_result
    ]

    filtered_result = [
        box for box in result
        if all(
            iou(box, model_box[:4]) <= 0 or model_box[4] in {23, 27}
            for model_box in model_boxes
        )
    ]

    h, w = im0.shape[:2]
    return [
        [
            int(max(0, x0)),
            int(max(0, y0)),
            min(w - int(max(0, x0)), int(x1) - int(x0)),
            int(y1) - int(y0),
            30,
            0.5,
        ]
        for x0, y0, x1, y1 in filtered_result
    ]


def find_xiantiaohs2(img0):
    h, w, _ = img0.shape

    img0[(img0 >= [230, 230, 230]).all(axis=2)] = [0, 0, 0]
    img0[(img0 == [52, 255, 191]).all(axis=2)] = [0, 0, 0]

    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    fld = cv2.ximgproc.createFastLineDetector()
    dlines = fld.detect(img)

    if not isinstance(dlines, np.ndarray):
        return []

    lines2 = []
    for dline in dlines:
        x0, y0, x1, y1 = map(int, map(round, dline[0]))
        length = np.hypot(x1 - x0, y1 - y0)

        if 1 < length < 100:
            k = (y1 - y0) / (x1 - x0) if x1 - x0 != 0 else float('inf')
            if abs(k) >= 0.6:
                lines2.append([x0, y0, x1, y1] if y0 < y1 else [x1, y1, x0, y0])

    return lines2


def find_hs2(im, res_line, res_lines):
    #res_lines = find_xiantiaohs2(im.copy())

    lines_hs2 = [
        line for line in res_lines
        if line[1] < res_line[0] - 10 or line[3] < res_line[0] - 10
    ]
    lines_hs2 = [
        line for line in lines_hs2
        if np.hypot(line[2] - line[0], line[3] - line[1]) > 12
    ]
    lines_hs2.sort()

    result = []
    lines = []
    pre = 0
    len_lines_hs2 = len(lines_hs2)

    while pre < len_lines_hs2:
        for i in range(pre, len_lines_hs2):
            lines.append(lines_hs2[i])
            if i == len_lines_hs2 - 1 or lines_hs2[i + 1][0] - lines_hs2[i][0] >= 30:
                length = np.mean([
                    np.hypot(line[2] - line[0], line[3] - line[1])
                    for line in lines
                ])
                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])

                if len(lines) in {1, 2, 3}:
                    result.append([
                        avg_x0 - length, avg_y0 - length,
                        avg_x0 + length, avg_y0 + length
                    ])

                lines.clear()
                pre = i + 1
                break

    h, w = im.shape[:2]
    return [
        [
            max(0, min(x0, w - 1)),
            max(0, min(y0, h - 1)),
            max(0, min(x1, w - 1)),
            max(0, min(y1, h - 1)),
        ]
        for x0, y0, x1, y1 in result
    ]
