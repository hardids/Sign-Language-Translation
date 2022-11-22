import os, json
from .models import *
from os.path import join as pjoin

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .translate import Translator

MODEL_NAME = "cnn-epoch-50-batch-32-trial-001.h5"
MODEL_TYPE = "CNN"

translator = Translator(model_name=MODEL_NAME, model_type=MODEL_TYPE)

def home(request):
    return render(request, 'sign_lang/home.html')

def translate(request):
    return render(request, 'sign_lang/trans.html')

def single_translate(request):
    context = {}
    file = None
    if request.method == "POST" and request.FILES['files']:
        print("POST")
        file = request.FILES['files']
        answer = request.POST.get('answer').lower()
        
        img_obj = ImageObject()
        img_obj.filename = str(file)

        img_obj.answer = answer
        img_obj.image = file
        img_obj.created = timezone.datetime.now()
        img_obj.save()
        
        label, prob = translator.predict(img_path=img_obj.image.path)
        img_obj.label = label
        img_obj.save()
        
        context['image'] = os.sep + f"{os.sep}".join(img_obj.image.path.split(os.sep)[-3:])
        context['pred'] = label.upper()
        context['prob'] = f"{prob:.3f}"
        context['answer'] = answer.upper()
        
    else:
        context['image'] = "/static/assets/dummy_600_400.png"
        
        print("GET")
        
    return render(request, 'sign_lang/single_trans.html', context)       

def multi_translate(request):
    context = {}

    if request.method == "POST" and request.FILES['files']:
        print("POST")
        files = request.FILES.getlist('files')
        answers = list(map(lambda x: x.upper(), request.POST.getlist('answer')))
                
        image_paths = []
        preds, probs = [], []        
        
        for f, a in zip(files, answers):
            img_obj = ImageObject()
            img_obj.filename = str(f)

            img_obj.answer = a
            img_obj.image = f
            img_obj.created = timezone.datetime.now()
            img_obj.save()
            
            print(img_obj.image.path)
            label, prob = translator.predict(img_path=img_obj.image.path)
            img_obj.label = label
            img_obj.save()
            
            img_relative_path = os.sep + f"{os.sep}".join(img_obj.image.path.split(os.sep)[-3:])
            image_paths += [img_relative_path]
            probs += [f"{prob:.3f}"]
            preds += [label.upper()]            
            
        
        predicts = []
        for i in range(len(image_paths)):
            predicts += [{"image" : image_paths[i],
                          "pred" : preds[i],
                          "prob" : probs[i],
                          "answer" : answers[i]}]
            
        context['predicts'] = predicts
        
        return render(request, 'sign_lang/muti_trans_result.html', context)
        
    else:
        pass
        
    return render(request, 'sign_lang/multi_trans.html')       


def video_translate(request):
    context = {}
    
    return render(request, 'sign_lang/video_trans.html', context)       


def model_cnn(request):
    return render(request, 'sign_lang/model_cnn.html')

def about(request):
    return render(request, 'sign_lang/about.html')

def learn(request):
    return render(request, 'sign_lang/learn.html')