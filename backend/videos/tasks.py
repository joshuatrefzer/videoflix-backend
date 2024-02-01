import ffmpeg
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

def convert_480p(source):    
    new_file_name = source + '_480p.mp4'
    ffmpeg.input(source).output(new_file_name, s='hd480', vcodec='libx264', crf=23, acodec='aac', strict='experimental').run()


def convert_720p(source):    
    new_file_name = source + '_720p.mp4'
    ffmpeg.input(source).output(new_file_name, s='hd720', vcodec='libx264', crf=23, acodec='aac', strict='experimental').run()


