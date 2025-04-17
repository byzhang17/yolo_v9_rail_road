from utils.find_hs2 import *
from utils.find_hs3 import *
from utils.find_xlw import *
from utils.find_yulin import *
from utils.find_hs4 import *
from utils.find_boli import *
from utils.find_zero import *
from utils.get_res import *
from utils.find_guidi import *
from utils.get_maxlen import *
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import time

#轨底裂纹处理
def guidi(txts2, imc, res, lines):
    result_guidi1, result_guidi2 = find_guidi(imc, res, lines)
    guidi1 = get_guidi(result_guidi1)
    guidi2 = get_guidi(result_guidi2)
    txts2.extend(guidi1)
    txts2.extend(guidi2)
    return txts2

#核伤2
def hs2(txts2, imc, res, lines):
    result_hs2 = find_hs2(imc, res, lines)
    hs2 = get_hs2(result_hs2)
    txts2.extend(hs2)
    return txts2

#鱼鳞
def yulin(txts2, imc, res, lines):
    result_yulin = find_yulin(imc, res, lines)
    yulin = get_yulin(result_yulin)
    txts2.extend(yulin)
    for i in range(0, len(yulin)):
        crop3 = imc[yulin[i][1]:yulin[i][1] + yulin[i][3], yulin[i][0]:yulin[i][0] + yulin[i][2]]
        maxlen, reslines = get_maxlen(crop3)
        if len(reslines) == 0:
            continue
        else:
            x_start = max(0, reslines[0][0] - 4) + yulin[i][0]
            y_start = max(0, reslines[0][1]) + yulin[i][1]
            width = min(imc.shape[1] - x_start, 8)
            height = abs(reslines[0][3] - reslines[0][1])
            category = 27
            confidence = min(1.0, round(reslines[0][1] / 50.0, 5))
            
            txts2.append([int(x_start), int(y_start), int(width), int(height), category, confidence])
    return txts2

#核伤3
def hs3(txts2, imc, res, lines):

    
    result_hs3 = find_hs3(imc, res, lines)
    
    hs3 = get_hs3(result_hs3)
    
    txts2.extend(hs3)
    return txts2

#斜裂纹
def xlw(txts2, imc, res, lines):
    result_xlw = find_xlw(imc, res, lines)
    xlws = get_xlw(result_xlw)
    txts2.extend(xlws)
    return txts2

#核伤4
def hs4(txts2, imc, res, lines):
    hs4 = []
    result_hs4 = find_hs4(imc, res, lines)
    hs4 = get_hs4(result_hs4)
    txts2.extend(hs4)
    return txts2

#剥离
def boli(txts2, imc, res):
    result_boli = find_boli(imc, res)
    boli = get_boli(result_boli)
    txts2.extend(boli)
    return txts2

def zero(txts2, imc, res, lines):
    result_zero = find_zero(imc, res, lines)
    zero = get_zero(result_zero)
    txts2.extend(zero)
    return txts2

# def run_rules(txts2,imc,res):
    
#     lines = find_xiantiao(imc.copy())
    
#     hs4(txts2, imc, res,lines)
#     xlw(txts2, imc, res, lines)
#     yulin(txts2, imc, res, lines)
#     zero(txts2, imc, res, lines)
    

def detect_image(imc_name,res):
    txts2 = []
    imc = cv2.imread(imc_name)
    lines,lines_2 = find_xiantiao(imc.copy())
    # Define threads for each detection function
    threads = [
        threading.Thread(target=boli, args=(txts2, imc, res)),
        threading.Thread(target=hs2, args=(txts2, imc, res, lines_2)),
        threading.Thread(target=hs3, args=(txts2, imc, res, lines_2)),
        threading.Thread(target=hs4, args=(txts2, imc, res, lines)),
        threading.Thread(target=xlw, args=(txts2, imc, res, lines)),
        threading.Thread(target=yulin, args=(txts2, imc, res, lines)),
        threading.Thread(target=zero, args=(txts2, imc, res, lines)),
        threading.Thread(target=guidi, args=(txts2, imc, res, lines)),
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return txts2
         

def detect_rule(source_path, save_path):
    res = []
    first_img = get_earliest_image(source_path)
    if first_img is not None:
        img = cv2.imread(first_img)
        res = get_guize(img)
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    #启动多线程检测
    image_paths = [os.path.join(source_path, f) for f in os.listdir(source_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    def process_image(image_path):
        txts2 = detect_image(image_path, res)
        
        #image_name = os.path.splitext(os.path.basename(image_path))[0]
        #result_path = os.path.join(save_path, image_name + '.json')
        data = {'url': os.path.join(save_path,image_path), 'damage': txts2}
        # with open(result_path, 'w') as f:
        #     json.dump(data, f)
        return data
    results = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        for result in executor.map(process_image, image_paths):
            results.append(result)
    
    #print(results)
    
    # Save results to a JSON file
    result_path = os.path.join(save_path, 'results_rule.json')
    with open(result_path, 'w') as f:
        json.dump(results, f)

    return save_path


if __name__ == "__main__":
    source_path = '/home/zhangbenyi/yolov9'
    save_path = '/home/zhangbenyi/yolov9/detect'
    time_start = time.time()
    detect_rule(source_path, save_path)
    time_end = time.time()
    print("Time taken: ", time_end - time_start)

    
    