"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from videos.views import VideoView, SearchView, FavoriteListViewSet, FavoriteListView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'favorites', FavoriteListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('users/', include('users.urls')),
    path('favorites/', include(router.urls), name='favorites'), 
    path('favorite_list/', FavoriteListView.as_view(), name='favorite-list'), 
    path('api/videos/', VideoView.as_view(), name='get_videos'),
    path('api/upload/' , VideoView.as_view(), name='upload'),
    path('api/videos/search/' , SearchView.as_view(), name='search'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
