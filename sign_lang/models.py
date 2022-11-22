import os
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class ImageObject(models.Model):
    LETTER_CHOICE = ((i, chr(i)) for i in range(65, 91))

    class Meta:
        ordering = ['-id']
        
    filename = models.CharField('제목', max_length=250)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    label = models.CharField('번역', max_length=2, choices=LETTER_CHOICE, default='A')
    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename
    
    
class VideoObject(models.Model):
    class Meta:
        ordering = ['-id']
        
    filename = models.CharField('제목', max_length=250)
    video = models.FileField(upload_to='videos/',blank=True, null=True)
    text = models.CharField('번역', max_length=250)

    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

