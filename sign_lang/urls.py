
from django.urls import path, include
from . import views

app_name = 'sign_lang'
urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

]
