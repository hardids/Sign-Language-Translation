
from django.urls import path, include
from . import views

app_name = 'sign_lang'
urlpatterns = [
    path('', views.home, name='home'),
    path('model_cnn/', views.model_cnn, name='model_cnn'),
    path('about/', views.about, name='about'),
    
    path('translate/', views.translate, name='translate'),
    path('multi_translate/', views.multi_translate, name='multi_translate'),
    path('single_translate/', views.single_translate, name='single_translate'),
    path('video_translate/', views.video_translate, name='video_translate'),
    
    path('about/', views.about, name='about'),
    path('learn/', views.learn, name='learn'),

]
