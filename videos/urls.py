from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.videos_list, name='videos_list'),
    url(r'^video/[a-zA-Z0-9]{7}/$', views.single_video, name='single_video'),
]