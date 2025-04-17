import requests

import json

import os
import cv2
def merge_result(rpath, saveDir):
    datas_rule = []

    save_path1=rpath + '/rule_result'

    save_path2=rpath + '/rule_result_2'

    savedir_model1=rpath + '/model_result'

    savedir_model2=rpath + '/model_result_2'

    # 读取save_path1中所有json文件，将结果存储到datas中
    for file_name in os.listdir(save_path1):
        if file_name.endswith('.json'):
            file_path = os.path.join(save_path1, file_name)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    datas_rule += data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {file_path}: {e}")
                    
    # 读取save_path2中所有json文件，将结果存储到datas中
    for file_name in os.listdir(save_path2):
        if file_name.endswith('.json'):
            file_path = os.path.join(save_path2, file_name)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    datas_rule += data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {file_path}: {e}")
                

    # 删除url路径中的group1和group2
    for data in datas_rule:
        data["url"] = data["url"].replace("group1/", "").replace("group2/", "").replace("group1\\", "").replace("group2\\", "")
    
    datas_model = []
    # 读取save_path_model中所有json文件，将结果存储到datas中
    for file_name in os.listdir(savedir_model1):
            if file_name.endswith('.json'):
                file_path = os.path.join(savedir_model1, file_name)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        datas_model += data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")
                        
    # 读取save_path_model_2中所有json文件，将结果存储到datas中
    for file_name in os.listdir(savedir_model2):
            if file_name.endswith('.json'):
                file_path = os.path.join(savedir_model2, file_name)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        datas_model += data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")
                        
    # 删除url路径中的group1和group2
    for data in datas_model:
        data["url"] = data["url"].replace("group1/", "").replace("group2/", "").replace("group1\\", "").replace("group2\\", "")
                        

    # 合并url相同的
    merged_data = {}

    # 合并 datas_model
    for item in datas_model:
        url = item['url']
        if url not in merged_data:
            merged_data[url] = {'url': url, 'damage': item['damage']}
        else:            
            merged_data[url]['damage'].extend(item['damage'])
        
    # 合并 datas_rule
    for item in datas_rule:
        url = item['url']
        if url not in merged_data:
            merged_data[url] = {'url': url, 'damage': item['damage']}
        else:
            txts2 = item['damage']
            txts = merged_data[url]['damage']
            
            for i in range(0, len(txts)):
                #轨底裂纹
                if txts[i][4] == 2:
                    for j in range(0, len(txts2)):
                        if txts2[j][4] == 10:
                            if (txts2[j][0] + txts2[j][2] / 2 < txts[i][0] + txts[i][2]) and (
                                    txts2[j][0] + txts2[j][2] / 2 > txts[i][0]):
                                txts2[j][4] = 34
                #斜裂纹
                txts2_copy = txts2.copy()
                if txts[i][4] == 0 or txts[i][4] == 11:
                    for j in range(0, len(txts2_copy)):
                        if txts2_copy[j][4] == 33:
                            if (txts2_copy[j][0] + txts2_copy[j][2] / 2 < txts[i][0] + txts[i][2]) and (
                                    txts2_copy[j][0] + txts2_copy[j][2] / 2 > txts[i][0]):
                                if txts2_copy[j] in txts2:
                                    txts2.remove(txts2_copy[j])
            #hs4
            txts2_copy = txts2.copy()
            for txt in txts:
                if txt[4] == 24:
                    for j in range(0, len(txts2_copy)):
                        if txts2_copy[j][4] == 35:
                            if txts2_copy[j] in txts2:
                                txts2.remove(txts2_copy[j])
                    break
            merged_data[url]['damage'].extend(txts2)
            
    # 转换为列表形式
    datas = list(merged_data.values())

    
    # 接头过滤
    for i in range(0, len(datas)):
        damage = datas[i]["damage"]
        label0 = []
        for j in range(0, len(damage)):
            if (damage[j][4] == 0) or (damage[j][4] == 39):
                label0.append(damage[j])
        if len(label0) != 0:
            label0.sort(key=lambda x: x[0])
            for m in range(0, len(label0)):
                for n in range(m, len(label0)):
                    if m == n:
                        continue
                    else:
                        if ((label0[m][0] + label0[m][2] / 2 - 150) <= (label0[n][0] + label0[n][2] / 2)) & (
                                (label0[n][0] + label0[n][2] / 2) <= (label0[m][0] + label0[m][2] / 2 + 150)):
                            if label0[n] in damage:
                                damage.remove(label0[n])
        datas[i]["damage"] = damage

    # 焊缝标记附近伤损删除
    for i in range(0, len(datas)):
        damages = datas[i]["damage"]
        damages_copy = damages.copy()
        for damage in damages:
            if (damage[4] == 14) or (damage[4] == 15):
                for j in range(0, len(damages)):
                    if ((damages[j][4] == 5) or (damages[j][4] == 6) or (damages[j][4] == 7) or (
                            damages[j][4] == 37) or (damages[j][4] == 13)) & (
                            damages[j][0] < (damage[0] + 300)) & (damages[j][0] > (damage[0] - 300)):
                        if damages[j] in damages_copy:
                            damages_copy.remove(damages[j])
        datas[i]["damage"] = damages_copy



    # 删除焊缝和断面和接头轨底处裂纹
    for i in range(0, len(datas)):
        damages = datas[i]["damage"]
        hf_dms = []
        jts = []
        for damage in damages:
            if damage[4] == 2:
                hf_dms.append(damage)
            elif damage[4] == 12:
                hf_dms.append(damage)
            elif damage[4] == 0:
                jts.append(damage)
            else:
                continue
        damages_copy = damages
        for damage in damages:
            if damage[4] == 10:
                for hf_dm in hf_dms:
                    if (damage[0] + damage[2] / 2) > hf_dm[0] and (damage[0] + damage[2] / 2) < (hf_dm[0] + hf_dm[2]):
                        if damage in damages_copy:
                            damages_copy.remove(damage)
                        break
                for jt in jts:
                    if (damage[0] + damage[2] / 2) > (jt[0] + jt[2] / 2 - 50) and (damage[0] + damage[2] / 2) < (jt[0] + jt[2] / 2 + 50):
                        if damage in damages_copy:
                            damages_copy.remove(damage)
                        break
        datas[i]["damage"] = damages_copy
        
    
    # 删除datas中damage值为空的项
    datas = [item for item in datas if item["damage"]]

    if os.path.isdir(saveDir):
        wpath = saveDir + '/result.json'
        f = open(wpath, 'w')
        f.write(json.dumps(datas))
        return wpath


