from django.db import models
from datetime import date

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title =  models.CharField(max_length = 30)
    description =  models.CharField(max_length = 500)
    genre =  models.CharField(max_length = 20)
    actors =  models.CharField(max_length = 20)
    thumbnail = models.FileField(upload_to='thumbnails' , blank=True, null=True)
    video_file =  models.FileField(upload_to='videos', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    