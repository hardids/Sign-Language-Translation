import cv2
import joblib
import string
import numpy as np
import os
from .models import *
from pathlib import Path

from django.conf import settings
from keras.models import load_model

CLASSES = list(string.ascii_lowercase)
CLASS_MAP = {i: CLASSES[i] for i in range(len(CLASSES))}

HEIGHT = 28
WIDTH = 28
        
def load(model_path, model_type):
    if model_type in ["rf", 'knn', 'sgd', 'xgb']:
        return joblib.load(model_path)
    
    return load_model(model_path)
    
def preprocess(img_path, height, width):        
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    resize_img = cv2.resize(img, (height, width))
    scaled_img = resize_img / 255.
    resized_img = scaled_img.reshape(-1, height, width, 1)
    return resized_img

# Pipeline 구성
def predict(model, img_path, height=HEIGHT, width=WIDTH):
    img = preprocess(img_path=img_path, height=height, width=width)
    
    pred = model.predict(img)
    prob = np.max(pred, axis=1)[0]
    pred = np.argmax(pred, axis=1)[0]
        
    return CLASS_MAP[pred], prob
