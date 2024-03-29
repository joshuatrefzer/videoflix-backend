from .tasks import convert_480p , convert_720p
from .models import Video
from .views import clear_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq

@receiver( post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New Video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_480p , instance.video_file.path)
        queue.enqueue(convert_720p , instance.video_file.path)
    
        
        
@receiver( post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance,  **kwargs):
    clear_cache()
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            remove_files(instance.video_file.path)
            print('Videofile removed')
            
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
            print('Thumbnail removed')
            
    



def remove_files(file_path):
    os.remove(file_path)
    try:
        os.remove(f'{file_path.rstrip(".mp4")}_480p.mp4')
    except: 
        print('No Video in 480p')
    try:
        os.remove(f'{file_path.rstrip(".mp4")}_720p.mp4')
    except:
        print('No Video in 720p')
    