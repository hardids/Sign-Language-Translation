from django.db import models

class Model(models.Model):
    MODEL_CHOICE = (('CNN', "cnn"), 
                    ('DNN', 'dnn'), 
                    ('RandomForest', 'rf'), 
                    ('KNN', 'knn'), 
                    ('SGD', 'sgd'), 
                    ('XGB', 'xgb'))

    model = models.FileField(upload_to= 'sign_lang/model', blank=True)
    type = models.CharField(max_length=12, choices=MODEL_CHOICE, default='CNN')
    version = models.CharField(max_length=10)
    comment = models.CharField(default= " ", max_length=300)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.version
    
class ImageObject(models.Model):
    LETTER_CHOICE = ((i, chr(i)) for i in range(65, 91))

    class Meta:
        ordering = ['-id']
        
    filename = models.CharField('제목', max_length=250)
    image = models.ImageField(upload_to='images/', null=False)
    label = models.CharField('번역', max_length=2, choices=LETTER_CHOICE, default='A')
    
    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    version = models.ForeignKey(Model, related_name='versionR', on_delete=models.CASCADE, db_column='version', default=0)
    answer = models.IntegerField("정답여부", default=0)

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

