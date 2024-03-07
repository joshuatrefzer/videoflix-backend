from django.db import models
from datetime import date

from .enum import VideoGenre

# Create your models here.
def generate_genre_choices():
    return [(tag.value, tag.value) for tag in VideoGenre]


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title =  models.CharField(max_length = 30)
    description =  models.CharField(max_length = 500)
    genre = models.CharField(max_length=20, choices=generate_genre_choices())
    actors =  models.CharField(max_length = 100)
    thumbnail = models.FileField(upload_to='thumbnails' , blank=True, null=True)
    video_file =  models.FileField(upload_to='videos', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    