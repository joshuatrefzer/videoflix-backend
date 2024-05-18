from django.db import models
from django_resized import ResizedImageField
from datetime import date
from rest_framework import viewsets
from ..users.models import CustomUser

from .enum import VideoGenre

def generate_genre_choices():
    return [(tag.value, tag.value) for tag in VideoGenre]


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title =  models.CharField(max_length = 30)
    description =  models.CharField(max_length = 500)
    genre = models.CharField(max_length=20, choices=generate_genre_choices())
    actors =  models.CharField(max_length = 100)
    thumbnail = ResizedImageField(force_format="WEBP", size=[150, None], quality=75, upload_to="thumbnails", blank=True, null=True)
    video_file =  models.FileField(upload_to='videos', blank=True, null=True)
    is_validated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
    
class FavoriteList(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Video, related_name='favorites', blank=True)

    def __str__(self):
        return f"{self.owner}'s Favorite List"
    

    
    
    