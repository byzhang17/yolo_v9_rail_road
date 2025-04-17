from flask import Flask, request, jsonify
from detect_dual import DetectAPI
import os
import requests
import time

from detect_rule import detect_rule
import threading
import json
import shutil
from merge_result import merge_result

app = Flask(__name__)

yolov9 = DetectAPI(device = '0')

yolov9_2 = DetectAPI(device = '0')


@app.route('/endpoint', methods=['POST'])
def process_post_request():
    print(request.form)
    if 'rpath' and 'wpath' in request.form:
        rpath = request.form['rpath']
        wpath = request.form['wpath']
        print(rpath+'\n'+wpath)
        # 在这里进行你的处理逻辑，这里我们简单地返回一个固定的结果
        if os.path.exists(rpath) and os.path.isdir(rpath):
            start_time = time.time()
            
            # 获取rpath中的图片文件列表
            image_files = [f for f in os.listdir(rpath) if os.path.isfile(os.path.join(rpath, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            
            # 将图片文件均分为两组
            mid_index = len(image_files) // 2
            group1 = image_files[:mid_index]
            group2 = image_files[mid_index:]
            
            # 创建两个子目录用于存放分组后的图片
            group1_dir = os.path.join(rpath, 'group1')
            group2_dir = os.path.join(rpath, 'group2')
            os.makedirs(group1_dir, exist_ok=True)
            os.makedirs(group2_dir, exist_ok=True)

            # 将图片文件复制到两个子目录
            for file in group1:
                shutil.copy(os.path.join(rpath, file), os.path.join(group1_dir, file))
            for file in group2:
                shutil.copy(os.path.join(rpath, file), os.path.join(group2_dir, file))
            
            def run_model():
                nonlocal save_path_model
                save_path_model = yolov9.run(source=group1_dir, savedir=rpath + '/model_result')
                
            def run_model_2():
                nonlocal save_path_model_2
                save_path_model_2 = yolov9_2.run(source=group2_dir, savedir=rpath + '/model_result_2')
 
            def run_rule():
                nonlocal save_path_rule
                save_path_rule = detect_rule(source_path=group1_dir, save_path=rpath + '/rule_result')
                
            def run_rule_2():
                nonlocal save_path_rule
                save_path_rule = detect_rule(source_path=group2_dir, save_path=rpath + '/rule_result_2')    

            save_path_model = None
            save_path_rule = None
            save_path_model_2 = None

            # 创建线程来运行模型和规则检测
            model_thread = threading.Thread(target=run_model)
            model_thread_2 = threading.Thread(target=run_model_2)
            model_thread_rule = threading.Thread(target=run_rule)
            model_thread_rule_2 = threading.Thread(target=run_rule_2)
            
            # 启动所有线程
            model_thread.start()
            model_thread_2.start()
            model_thread_rule.start()
            model_thread_rule_2.start()
            
            # 等待所有线程完成
            model_thread.join()
            model_thread_2.join()
            model_thread_rule.join()
            model_thread_rule_2.join()
            
            end_time = time.time()
            
            save_path = merge_result(rpath,wpath)
            
            time_sum = end_time - start_time
            
            print(str(time_sum) + 's')
            
            return jsonify({"save_path": save_path})
        elif os.path.exists(rpath) and os.path.isfile(rpath):
            result = yolov9.run(source=rpath)
            return jsonify(result)
        else:
            return jsonify({"error": "Wrong 'rpath' parameter"}), 500
    elif 'rpath' in request.form and 'wpath' not in request.form:
        rpath = request.form['rpath']
        print(rpath)
        # 在这里进行你的处理逻辑，这里我们简单地返回一个固定的结果
        if os.path.exists(rpath):
            result = yolov9.run(source=rpath)
            return jsonify(result)
        else:
            return jsonify({"error": "Wrong 'rpath' parameter"}), 500
    elif 'get_progress' in request.form:
        progress = yolov9.get_progress()
        return jsonify({"progress": progress})
    else:
        return jsonify({"error": "Missing 'rpath' or 'wpath' parameter"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3333, debug=True)
    
