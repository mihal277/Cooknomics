from django.conf.urls import url
from . import views

app_name = 'videos'
urlpatterns = [
    url(r'^$', views.videos_list, name='videos_list'),
    url(r'^page$', views.video_page, name='page'),
    url(r'^vote$', views.vote, name='vote'),
    url(r'^(?P<video_slug>([a-zA-Z0-9-])+)/$', views.single_video, name='single_video'),
]