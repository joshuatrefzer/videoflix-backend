from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
  

class VideoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VideoResource
    list_display = ("id", "title", "created_at", "genre", "actors")
    search_fields = ("id", "title", "genre", "actors" )


admin.site.register(Video, VideoAdmin)
