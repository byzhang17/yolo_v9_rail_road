# coding=utf-8
import cv2
import numpy as np

# 读取输入图片
img0 = cv2.imread("./datasets/test/in/20250116191643.png")

img0[np.where((img0 >= [200, 200, 200]).all(axis=2))] = [0, 0, 0]

img0[np.where((img0 == [52, 255, 191]).all(axis=2))] = [0, 0, 0]

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
x0_max = 0
y0_max = 0
x1_max = 0
y1_max = 0

lines2 = []
if isinstance(dlines, np.ndarray):
    for dline in dlines:

        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        length = np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))

        if length > 15 and length < 100:

            k = (y1 - y0) / (x1 - x0) if x1 - x0 != 0 else 0

            if abs(k) < 0.4:
                continue

            if y0 < y1:
                lines2.append([x0, y0, x1, y1])
            else:
                lines2.append([x1, y1, x0, y0])
            cv2.line(img0, (x0, y0), (x1, y1), (255, 255, 255), 2, cv2.LINE_AA)

lines2.sort()

lines = []

result = []

pre = 0
while pre < len(lines2):
    pos = []
    neg = []

    for i in range(pre, len(lines2)):

        if i == len(lines2) - 1:
            lines.append(lines2[i])
            length = 0
            for line in lines:
                x0, y0, x1, y1 = line
                length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                if x1 - x0 != 0:
                    k = (y1 - y0) / (x1 - x0)
                    if k > 0:
                        pos.append(line)
                    else:
                        neg.append(line)
            length = int(length / len(lines))
            if len(pos) > 0 and len(neg) > 0:
                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])
                result.append([avg_x0 - length, avg_y0 - length, avg_x0 + length, avg_y0 + length])
            lines.clear()
            pre = i + 1
            break

        if lines2[i + 1][0] - lines2[i][0] < 20:
            lines.append(lines2[i])
        else:
            lines.append(lines2[i])
            print(lines)
            length = 0

            for line in lines:
                x0, y0, x1, y1 = line
                length = length + np.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
                if x1 - x0 != 0:
                    k = (y1 - y0) / (x1 - x0)
                    if k > 0:
                        pos.append(line)
                    else:
                        neg.append(line)
            length = int(length / len(lines))
            if len(pos) > 0 and len(neg) > 0:
                avg_x0 = np.mean([line[0] for line in lines])
                avg_y0 = np.mean([line[1] for line in lines])
                result.append([avg_x0 - length, avg_y0 - length, avg_x0 + length, avg_y0 + length])
            lines.clear()
            pre = i + 1
            break

for line in result:
    x0, y0, x1, y1 = line
    cv2.rectangle(img0, (int(x0), int(y0)), (int(x1), int(y1)), (255, 255, 255), 2)

cv2.imshow("img", img0)
cv2.waitKey(0)
cv2.destroyAllWindows()