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
    print("Load ", model_type, model_path)
    if model_type in ["RandomForest", 'KNN', 'SGD', 'XGB']:
        return joblib.load(model_path)
    
    return load_model(model_path)
    
def preprocess(img_path, height, width):        
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    resize_img = cv2.resize(img, (height, width))
    scaled_img = resize_img / 255.

    return scaled_img

# Pipeline 구성
def predict(model, model_type, img_path, height=HEIGHT, width=WIDTH):
    img = preprocess(img_path=img_path, height=height, width=width)
    
    if model_type in ["RandomForest", 'KNN', 'SGD', 'XGB']:
        return ml_predict(model, img)
    
    resized_img = img.reshape(-1, height, width, 1)

    pred = model.predict(resized_img)
    prob = np.max(pred, axis=1)[0]
    pred = np.argmax(pred, axis=1)[0]
        
    return CLASS_MAP[pred], prob

def ml_predict(model, img):
    X = np.array(img).flatten().reshape(-1, 1)
    
    pred = model.predict(X)
    prob = np.max(pred, axis=1)[0]
    pred = np.argmax(pred, axis=1)[0]
        
    return CLASS_MAP[pred], prob
