from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from .models import Video, FavoriteList
from .serializers import FavoriteListSerializer, VideoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def clear_cache():
    cache.clear()


class VideoView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        try:
            videos = Video.objects.filter(is_validated=True)
            serializer = VideoSerializer(videos, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
    
    
    
    
    def post(self, request):
        try:
            serializer = VideoSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                clear_cache()

                return Response({'status': 'success', 'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
        
        
class SearchView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        value = request.data.get('search_title', None)
        if value:
            videos = self.search_videos(value)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        else: 
            return Response("Search value not provided", status=status.HTTP_400_BAD_REQUEST)
       
    def search_videos(self, search_value):
        return Video.objects.filter(title__icontains=search_value)
    
    
    
class FavoriteListViewSet(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer