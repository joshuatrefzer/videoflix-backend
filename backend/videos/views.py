from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from .models import Video
from .serializers import VideoSerializer



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
@api_view(['GET'])
def get_videos(request):
    try:
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)

        return Response({'status': 'success', 'videos': serializer.data})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)