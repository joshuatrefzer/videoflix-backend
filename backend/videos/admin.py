from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "genre", "actors")
    search_fields = ("id", "title", "genre", "actors")


admin.site.register(Video, VideoAdmin)
