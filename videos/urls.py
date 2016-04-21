from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^videos/$', views.videos_list, name='videos_list'),
    url(r'^video/(?P<video_slug>([a-zA-Z0-9]|-)+)/$', views.single_video, name='single_video'),
]