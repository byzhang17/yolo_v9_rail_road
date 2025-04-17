import cv2
import numpy as np
import os

# 找到第一张图片
def get_earliest_image(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    if not image_files:
        return None

    earliest_image = min(image_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    return os.path.join(folder_path, earliest_image)

#结果格式转化
def get_guidi(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         10, min(float(1), round(float((int(y1) - int(y0)) / 50), 5))] for x0, y0, x1, y1 in result]
    return filtered_result

def get_hs2(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         30, min(float(1), round(float((int(y1) - int(y0)) / 50), 5))] for x0, y0, x1, y1 in result]
    return filtered_result

def get_xlw(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         33, min(float(1), round(float(dis / 50), 5))] for x0, y0, x1, y1, dis in result]
    return filtered_result

def get_hs4(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         35, 0.5] for x0, y0, x1, y1 in result]
    return filtered_result

def get_hs3(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         26, min(float(1), round(float((int(y1) - int(y0)) / 50), 5))] for x0, y0, x1, y1 in result]
    return filtered_result

def get_HF(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         14, 0.5] for x0, y0, x1, y1 in result]
    return filtered_result

def get_boli(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         38, min(float(1), round(float((int(y1) - int(y0)) * (int(x1) - int(x0)) / 10000), 5))] for x0, y0, x1, y1 in result]
    return filtered_result

def get_zero(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         32, min(float(1), round(float((int(x1) - int(x0)) / 50), 5))] for x0, y0, x1, y1 in result]
    return filtered_result

def get_yulin(result):
    filtered_result = []
    filtered_result = [
        [int(x0), int(y0), int(x1) - int(x0), int(y1) - int(y0),
         23, 0.5] for x0, y0, x1, y1 in result]
    return filtered_result

# 读取输入图片
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

        return inter_area / union_area

    def convert_to_box(model_result):
        boxes = []
        for item in model_result:
            x, y, w, h, class_id, _ = item
            boxes.append([x, y, x + w, y + h, class_id])
        return boxes

    model_boxes = convert_to_box(model_result)

    filtered_result = []
    for box in result:
        keep = True
        for model_box in model_boxes:
            yolo_box = model_box[0:4]
            class_id = model_box[4]
            if iou(box, yolo_box) > 0 and class_id != 23 and class_id != 27:
                keep = False
                break
        if keep:
            filtered_result.append(box)

    filtered_result = [
        [int(max(0, x0)), int(max(0, y0)), min(im0.shape[1] - int(max(0, x0)), int(x1) - int(x0)), int(y1) - int(y0),
         30, 0.5] for x0, y0, x1, y1 in
        filtered_result]
    return filtered_result


def get_guize(im):
    height, width = im.shape[:2]
    im = im[:, 2 * width // 3:]

    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray_img, 30, 150)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, 180)
    if lines is None:
        return []

    res = sorted([int(rho * np.sin(theta)) for rho, theta in lines[:, 0, :] if
                  40 < int(rho * np.sin(theta)) < im.shape[0] - 190])

    filtered_res = [res[0]] if res else []
    for i in range(1, len(res)):
        if res[i] - res[i - 1] >= 20:
            filtered_res.append(res[i])

    for y in filtered_res:
        cv2.line(im, (0, y), (im.shape[1], y), (0, 0, 255), 2)

    return filtered_res


def find_xiantiao(img0):

    fld = cv2.ximgproc.createFastLineDetector()
    
    img_hs = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    mask = (img0 >= [230, 230, 230]).all(axis=2)
    img0[mask] = [0, 0, 0]
    
    kernel = np.ones((5, 5), np.uint8)
    img0 = cv2.dilate(img0, kernel, iterations=1)
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    dlines = fld.detect(img)
    dlines_2 = fld.detect(img_hs)
    lines2 = []
    lines2_2 = []
    if isinstance(dlines_2, np.ndarray):
        for dline in dlines_2:
            x0, y0, x1, y1 = map(int, dline[0])
            length = np.hypot(x1 - x0, y1 - y0)

            if 1 < length < 100:
                k = (y1 - y0) / (x1 - x0) if x1 - x0 != 0 else float('inf')
                if abs(k) < 0.6:
                    continue

                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0

                lines2_2.append([x0, y0, x1, y1])
    

    if isinstance(dlines, np.ndarray):
        for dline in dlines:
            x0, y0, x1, y1 = map(int, dline[0])
            length = np.hypot(x1 - x0, y1 - y0)

            if 1 < length < 100:
                k = (y1 - y0) / (x1 - x0) if x1 - x0 != 0 else float('inf')
                if abs(k) < 0.6:
                    continue

                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0

                lines2.append([x0, y0, x1, y1])


    return lines2, lines2_2
    


#im = cv2.imread("720250219165616.png")

#找到图片的直线
#res_line = get_guize(im.copy())

#找到图片的线条
#lines = find_xiantiao(im.copy())

#处理hs2
#result_hs2 = find_hs2.findhs2(im, res_line, lines)

#处理hs3
#result_hs3 = find_hs3.findhs3(im, res_line, lines)

#处理鱼鳞
#result_yulin = find_yulin.find_yulin(im, res_line, lines)

#处理轨底
#result_guidi = find_guidi.find_guidi(im, res_line,lines)

#处理斜裂纹
#result_xlw = find_xlw.find_xlw(im, res_line, lines)

#处理三通道出波
#result_hs4 = find_hs4.findhs4(im, res_line, lines)











