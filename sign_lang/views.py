import os

from .models import *

from os.path import join as pjoin

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .translate import Classifier

MODEL_NAME = "cnn-epoch-50-batch-32-trial-001.h5"
model = Classifier(model_name=MODEL_NAME)

def main(request):
    context = {}
    file = None
    if request.method == "POST" and request.FILES['files']:
        print("POST")
        file = request.FILES['files']
        
        img_obj = ImageObject()
        img_obj.filename = str(file)

        img_obj.answer = request.POST.get('answer', '')
        img_obj.image = file
        img_obj.created = timezone.datetime.now()
        img_obj.save()
        
        label, prob = model.predict(img_path=img_obj.image.path)
        img_obj.label = label
        img_obj.save()
        
        context['image'] = os.sep + f"{os.sep}".join(img_obj.image.path.split(os.sep)[-3:])
        context['legend'] = f"{label} ({prob:.3f}%)"
        
    else:
        context['image'] = "/static/assets/dummy_600_400.png"
        context['legend'] = ""
        
        
        print("GET")
    print(context)
        
    return render(request, 'sign_lang/index.html', context)       

def about(request):
    return render(request, 'sign_lang/about.html')

def faq(request):
    return render(request, 'sign_lang/faq.html')

def contact(request):
    if request.method == "POST":
        form = (request.POST)
        print(form.cleaned_data)
        if form.is_valid():
            print(form.cleaned_data)
            post = form.save()
            return redirect(post)
    else:
        # 템플릿으로 응답
        form = ContactInfoForm()
        return render(request, 'sign_lang/contact.html', {'form' : form})        


