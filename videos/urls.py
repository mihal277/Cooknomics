from django.conf.urls import url
from . import views

app_name = 'videos'
urlpatterns = [
    url(r'^$', views.videos_list, name='videos_list'),
    url(r'^vote$', views.vote, name='vote'),
    url(r'^page$', views.video_page, name='page'),
    url(r'^(?P<video_slug>([a-zA-Z0-9-])+)/$', views.single_video, name='single_video'),
    ####### URLE DO WYSZUKIWANIA DLA MAJKELA ########################
    url(r'^get_items$', views.get_items, name='get_items'),
    url(r'^process_items', views.process_items, name='process_items'),
]