from django.contrib import admin

from .models import ImageObject, VideoObject, Model
from django.shortcuts import render, get_object_or_404, redirect

admin.site.register(ImageObject)
admin.site.register(VideoObject)


class ModelAdmin(admin.ModelAdmin):
    list_display = ['version', 'model', 'pub_date', 'is_active']
    #list_editable = ['is_active']
    actions = ['activate', 'deactivate', 'compare']

    def activate(self, request, queryset):
        queryset.update(is_active= True ) #queryset.update
    activate.short_description = '지정 모델을 active 상태로 변경'
    
    def deactivate(self, request, queryset):
        queryset.update(is_active= False) #queryset.update
    deactivate.short_description = '지정 모델을 deactive 상태로 변경'

    
    def compare(self, request, queryset):
        labels, values = [], []

        for v in queryset.values('version').distinct():
            img_qs = ImageObject.objects.filter(version=v['version'])
            answer_qa = img_qs.filter(answer=1)
            if img_qs.count() > 0:
                labels += [str(v['version'])]
                values += [100 * (answer_qa.count() / img_qs.count())]
        
        print(labels, values)
        return super().changelist_view(request, extra_context={"labels_selected" : labels, "values_selected" : values})
    compare.short_description = '지정 모델의 성능 비교'

    
    def changelist_view(self, request, extra_context=None):
        response = super(ModelAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response


        labels, values = [], []
        print(response.context_data)
        
        result_qs = qs.values('version').all()
        print(result_qs)
        list(map(lambda r: r.update({'check_box': admin.helpers.checkbox.render(admin.helpers.ACTION_CHECKBOX_NAME, r['version'])}), result_qs))
        print(result_qs)
        for v in result_qs.values('version').distinct():
            img_qs = ImageObject.objects.filter(version=v['version'])
            answer_qa = img_qs.filter(answer=1)
            if img_qs.count() > 0:
                labels += [str(v['version'])]
                values += [100 * (answer_qa.count() / img_qs.count())]
        
        response.context_data['labels'] = labels
        response.context_data['values'] = values
        print(labels, values)
        return response
        

admin.site.register(Model, ModelAdmin)