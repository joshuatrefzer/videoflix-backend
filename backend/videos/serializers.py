from rest_framework import serializers
from .models import FavoriteList, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        
class FavoriteListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Zeigt den Besitzer als String an
    favorites = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())

    class Meta:
        model = FavoriteList
        fields = ['id', 'owner', 'favorites']