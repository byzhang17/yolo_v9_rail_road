import cv2
import os
from concurrent.futures import ThreadPoolExecutor
import pytesseract
from pytesseract import Output
import time
import json
import os

def find_HF(im0):
    """
    识别字符并返回所识别的字符及它们的坐标
    :param im: 需要识别的图片
    :return data: 字符及它们在图片的位置
    """
    im = im0.copy()
    height, width, _ = im.shape
    im = im[height//7*6:height, 0:width]

    mask = (im >= [230, 230, 230]).all(axis=2) | (im == [52, 255, 191]).all(axis=2)
    im[mask] = [0, 0, 0]
    
    #data = {}
    result = []
    d = pytesseract.image_to_data(im, output_type=Output.DICT)
    for i in range(len(d['text'])):
        if 0 < len(d['text'][i]) and d['text'][i] == 'HF':
            
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            #data[d['text'][i]] = ([d['left'][i], d['top'][i], d['width'][i], d['height'][i]])
            result.append([int(x), int(y), int(w), int(h), 14, 0.5])
            #cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 1)
 
    #cv2.imshow("recoText", im)
    return result

# Function to process a single image
def process_image(image_path):
    im = cv2.imread(image_path)
    if im is None:
        return 0  # Return 0 if the image cannot be read
    
    result_HF = find_HF(im)
    #result_HF = []
    #print('time_HF:', end_time - start_time)
    data = {"url" : image_path, "damage": result_HF}
    return data # Return processing time for the image

def find_HF_in_images(image_folder, save_path):
    # Read all images in the current folder and process them
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Created directory: {save_path}")

    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    image_paths = [os.path.join(image_folder, f) for f in image_files]

    result_HF = []

    with ThreadPoolExecutor() as executor:
        for result in executor.map(process_image, image_paths):
            result_HF.append(result)

    result_path = os.path.join(save_path, 'results_HF.json')
    with open(result_path, 'w') as f:
        json.dump(result_HF, f)
        
    return save_path
