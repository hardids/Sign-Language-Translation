from django.contrib import admin
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin import helpers, widgets
from .models import ImageObject, VideoObject, Model
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.html import format_html

admin.site.register(ImageObject)
admin.site.register(VideoObject)


class ModelAdmin(admin.ModelAdmin):
    list_display = ['version', 'model', 'pub_date', 'is_active']
    #list_editable = ['is_active']
    actions = ['activate', 'deactivate']
    change_list_template = 'admin/sign_lang/model/change_list.html'

    def activate(self, request, queryset):
        queryset.update(is_active= True ) #queryset.update
    activate.short_description = '지정 모델을 active 상태로 변경'
    
    def deactivate(self, request, queryset):
        queryset.update(is_active= False) #queryset.update
    deactivate.short_description = '지정 모델을 deactive 상태로 변경'
    
    def changelist_view(self, request, extra_context=None):
        response = super(ModelAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        context = []        
        for v in qs.values('version').distinct():
            img_qs = ImageObject.objects.filter(version=v['version'])
            answer_qa = img_qs.filter(answer=1)
            if img_qs.count() > 0:
                context += [{"label" : str(v['version']), "value" : 100 * (answer_qa.count() / img_qs.count())}]
        
        response.context_data['context'] = context
        print(context)
        return response
        

admin.site.register(Model, ModelAdmin)