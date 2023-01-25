"""fotoawards_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from foto import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User

from foto.models import Foto
from foto.serializers import router

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('foto/<int:foto_id>/', views.foto, name='foto'),
    path('like/<int:foto_id>/', views.like, name='foto_like'),
    path('accounts/', include('allauth.urls')),
    path('user/', views.user, name='user'),
    path('add/', views.add_foto, name='add_foto'),
    path('foto/<int:foto_id>/add_comment/', views.add_comment, name='add_comment'),
    path('foto/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('foto/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('search/', views.search, name='search'),
    path('foto/<int:foto_id>/delete_foto/', views.delete_foto, name='delete_foto'),
    path('foto/<int:foto_id>/no_delete_foto/', views.no_delete_foto, name='no_delete_foto'),
    path('foto/<int:foto_id>/edit_foto/', views.edit_foto, name='edit_foto'),
    path('subscribe/', views.subscribe, name='subscribe'),
    #REST API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    #Moderation
    path('moderation/', views.moderation, name='moderation'),
    path('moderation/<int:foto_id>/approve_foto/', views.approve, name='approve'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
