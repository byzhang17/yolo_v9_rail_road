import os

labels1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0}
labels2 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0}
rpath1 = 'D:/yolov9-main/datasets/new_rail5/labels/train'
files1 = os.listdir(rpath1)
for file in files1:
    path = rpath1 + '/' + file
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        num = int(line.strip('\n').split(' ')[0])
        labels1[num] = labels1[num]+1
rpath2 = 'D:/yolov9-main/datasets/new_rail5/labels/val'
files2 = os.listdir(rpath2)
for file in files2:
    path = rpath2 + '/' + file
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        num = int(line.strip('\n').split(' ')[0])
        labels2[num] = labels2[num]+1
print(labels1)
print(labels2)