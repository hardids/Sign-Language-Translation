from django.contrib import admin

# Register your models here.
from .models import ImageObject, VideoObject

# 관리에서 ImageObject 객체에 대해  기본 CRUD 관리를 한다. 
admin.site.register(ImageObject)
admin.site.register(VideoObject)
