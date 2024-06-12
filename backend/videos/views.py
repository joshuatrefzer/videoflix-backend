from django.shortcuts import get_object_or_404, render
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

from users.models import CustomUser
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
    
    
class FavoriteListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            
            if not user_id:
                return Response({"error": "user_id is required for this view"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(CustomUser, id=user_id)
            try:
                favorite_list = FavoriteList.objects.filter(owner=user).first()
            except Exception as e:
                return Response({'error': 'An error occurred while retrieving the favorite list.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            if not favorite_list:
                return Response({'error': 'No list for this user exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            favorite_videos = favorite_list.favorites.all()
            
            favorite_videos_serializer = VideoSerializer(favorite_videos, many=True)
            favorite_list_serializer = FavoriteListSerializer(favorite_list) 
            
            data = {
                "favorite_videos": favorite_videos_serializer.data,
                "favorite_list": favorite_list_serializer.data
            }
            
            return Response(data)  

        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
    
        