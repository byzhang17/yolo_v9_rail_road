import json
import os
import cv2

with open('./datasets/test2/out/result.json', 'r') as f:
    datas = json.load(f)
for data in datas:
    url = data["url"]
    damages = data["damage"]
    name = str(os.path.basename(url)).strip('.png')
    f = open('./datasets/test2/labels/' + name + '.txt', 'a+')
    image = cv2.imread('./datasets/test2/in/' + name + '.png')
    size = image.shape
    w = size[1]
    h = size[0]
    for damage in damages:
        x1 = int(damage[0])
        y1 = int(damage[1])
        w1 = int(damage[2])
        h1 = int(damage[3])
        label = int(damage[4])
        x = str((x1 + w1 / 2) / w)
        y = str((y1 + h1 / 2) / h)
        width = str(w1 / w)
        height = str(h1 / h)
        f.write(str(label) + ' ' + x + ' ' + y + ' ' + width + ' ' + height + '\n')