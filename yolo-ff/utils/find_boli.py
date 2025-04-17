# coding=utf-8
import cv2
import numpy as np

def find_boli(im0, res_line):
    im = im0.copy()
    height, width = im.shape[:2]
    step_size = 90  # Define the step size for splitting the image
    offset = 45  # Offset for the second loop
    # Extract the part of the image above res_line[0]
    im_above_res_line = im[10 : res_line[0] - 10, :]
    im_above_res_line[np.all(im_above_res_line == [192, 192, 192], axis=2)] = [0, 0, 0]
    
    result = []
    result1 = [] 
    result2 = []
    
    # Precompute non-black masks and unique colors for efficiency
    non_black_mask = np.any(im_above_res_line != [0, 0, 0], axis=-1)
    unique_colors_cache = {}

    def compute_segment_features(segment, segment_mask):
        """Helper function to compute unique colors and non-black ratio."""
        segment_key = segment.tobytes()
        if segment_key not in unique_colors_cache:
            unique_colors = len(np.unique(segment.reshape(-1, 3), axis=0))
            unique_colors_cache[segment_key] = unique_colors
        else:
            unique_colors = unique_colors_cache[segment_key]
        non_black_pixels = np.count_nonzero(segment_mask)
        total_pixels = segment_mask.size
        non_black_ratio = non_black_pixels / total_pixels
        return unique_colors - 1, non_black_ratio

    for x in range(0, width, step_size):
        if x + step_size <= width:
            segment = im_above_res_line[:, x:x + step_size]
            segment_mask = non_black_mask[:, x:x + step_size]
            unique_colors, non_black_ratio = compute_segment_features(segment, segment_mask)
            result.append([unique_colors, len(result), non_black_ratio])
    
    for x in range(0, width, step_size):
        if x + offset + step_size <= width:
            segment = im_above_res_line[:, x + offset:x + step_size + offset]
            segment_mask = non_black_mask[:, x + offset:x + step_size + offset]
            unique_colors, non_black_ratio = compute_segment_features(segment, segment_mask)
            result1.append([unique_colors, len(result1), non_black_ratio])

    def process_results(results, offset=0):
        """Helper function to process results and calculate confidence."""
        for i in range(1, len(results) - 1):
            if results[i][0] >= 3 and results[i - 1][0] < 3 and results[i + 1][0] < 3:
                conf = (results[i][2] * 2 - results[i - 1][2] - results[i + 1][2]) / (results[i][2] * 2)
                if conf > 0:
                    result2.append([
                        results[i][1] * step_size + offset, 
                        0, 
                        (results[i][1] + 1) * step_size + offset, 
                        conf * res_line[0] + 10
                    ])

    process_results(result)
    process_results(result1, offset=offset)

    # Clamp coordinates to image bounds
    for i in range(len(result2)):
        x0, y0, x1, y1 = result2[i]
        x0 = max(0, min(x0, im.shape[1] - 1))
        y0 = max(0, min(y0, im.shape[0] - 1))
        x1 = max(0, min(x1, im.shape[1] - 1))
        y1 = max(0, min(y1, im.shape[0] - 1))
        result2[i] = [int(x0), int(y0), int(x1), int(y1)]

    return result2
