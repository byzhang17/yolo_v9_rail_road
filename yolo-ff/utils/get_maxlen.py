# coding=utf-8
import cv2
import numpy as np

def get_maxlen(img0):
    height, width, _ = img0.shape
    if height < 10 or width < 10:
        return 10, []
    else:
        # 将彩色图片转换为灰度图片
        img0[np.where((img0 >= [200, 200, 200]).all(axis=2))] = [0, 0, 0]
        kernel = np.ones((3, 3), np.uint8)
        img0 = cv2.dilate(img0, kernel, iterations=1)
        img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

        # 创建一个LSD对象
        fld = cv2.ximgproc.createFastLineDetector()
        # 执行检测结果
        dlines = fld.detect(img)
        # 绘制检测结果
        # drawn_img = fld.drawSegments(img0,dlines, )
        maxlen = 0
        # x0_max = 0
        # y0_max = 0
        # x1_max = 0
        # y1_max = 0
        lines = []
        if isinstance(dlines, np.ndarray):
            for dline in dlines:

                x0 = int(round(dline[0][0]))
                y0 = int(round(dline[0][1]))
                x1 = int(round(dline[0][2]))
                y1 = int(round(dline[0][3]))
                k = 2
                length = np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                if x0 == x1:
                    continue
                else:
                    k = abs((y1 - y0) / (x1 - x0))
                if k > 1:
                    if y0 < y1:
                        lines.append([x0, y0, x1, y1])
                    else:
                        lines.append([x1, y1, x0, y0])
                    if length > maxlen:
                        maxlen = length
                        # x0_max = x0
                        # y0_max = y0
                        # x1_max = x1
                        # y1_max = y1
        if len(lines) > 0:
            lines.sort(key=lambda x: x[1])
        # cv2.line(img0, (x0_max, y0_max), (x1_max,y1_max), (0,0,255), 3, cv2.LINE_AA)
        # 显示并保存结果
        # cv2.imwrite('test3_r.jpg', img0)
        return maxlen, lines