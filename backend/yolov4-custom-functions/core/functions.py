import json
import os
import cv2
import random
import numpy as np
import tensorflow as tf
import pytesseract
from core.utils import read_class_names
from core.config import cfg

# function to count objects, can return total classes or count per class
def count_objects(data, by_class = False, allowed_classes = list(read_class_names(cfg.YOLO.CLASSES).values())):
    boxes, scores, classes, num_objects = data

    #create dictionary to hold count of objects
    counts = dict()

    # if by_class = True then count objects per class
    if by_class:
        class_names = read_class_names(cfg.YOLO.CLASSES)

        # loop through total number of objects found
        for i in range(num_objects):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            if class_name in allowed_classes:
                counts[class_name] = counts.get(class_name, 0) + 1
            else:
                continue

    # else count total objects found
    else:
        counts['total object'] = num_objects
    
    return counts

# function for cropping each detection and saving as new image
def crop_objects(img, data, path, allowed_classes):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)
    #create dictionary to hold count of objects for image name
    counts = dict()
    for i in range(num_objects):
        # get count of class for part of image name
        class_index = int(classes[i])
        class_name = class_names[class_index]
        if class_name in allowed_classes:
            counts[class_name] = counts.get(class_name, 0) + 1
            # get box coords
            xmin, ymin, xmax, ymax = boxes[i]
            # crop detection from image (take an additional 5 pixels around all edges)
            cropped_img = img[int(ymin)-2:int(ymax)+2, int(xmin)-2:int(xmax)+2]
            # construct image name and join it to path for saving crop properly
            img_name = class_name + '_' + str(counts[class_name]) + '.png'
            img_path = os.path.join(path, img_name )
            # save image
            cv2.imwrite(img_path, cropped_img)
        else:
            continue
        
# function to run general Tesseract OCR on any detections 
def ocr(img, data, path):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)

    pth = 'Detection.json'
    pth = os.path.join(path, pth)
    print(pth)
    print(path)
    f = open(pth, "w+")

    rs = {}
    print(f)
    for i in range(num_objects):
        # get class name for detection
        class_index = int(classes[i])
        class_name = class_names[class_index]
        # separate coordinates from box
        xmin, ymin, xmax, ymax = boxes[i]
        # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
        box = img[int(ymin) - 2:int(ymax) + 2, int(xmin) - 2:int(xmax) + 2]
        #cv2.imwrite('detection_box' + class_name + "" + str(class_index) + '.png', box)

        #sans_Deux = img[int(ymin):int(ymax) , int(xmin) :int(xmax) ]
        #cv2.imwrite('detection_sans_Deux' + class_name + "" + str(class_index) + '.png', sans_Deux)
        # grayscale region within bounding box
        gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY)
        #cv2.imwrite('detection_gray' + class_name + "" + str(class_index) + '.png', gray)

        # threshold the image using Otsus method to preprocess for tesseract
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #cv2.imwrite('detection_thresh' + class_name + "" + str(class_index) + '.png', thresh)
        # perform a median blur to smooth image slightly
        blur = cv2.medianBlur(thresh, 3)
        #cv2.imwrite('detection_blur' + class_name + "" + str(class_index) + '.png', blur)
        # resize image to double the original size as tesseract does better with certain text size
        blur = cv2.resize(blur, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite('detection_blur_resize' + class_name + "" + str(class_index) + '.png', blur)
        # run tesseract and convert image text to string
        text = pytesseract.image_to_string(blur, config='--psm 11 --oem 3')
        try:
            if text.strip():
                text = pytesseract.image_to_string(blur, config='--psm 11 --oem 3')
                #print("Class: {}, Text Extracted: {}".format(class_name, text))
                rs[class_name] = text
                #f.write(class_name + " " + text)
                #print(rs)
        except:
            text = None
    with open(pth, 'w') as fp:
        json.dump(rs, fp)
    # close file

    f.close()