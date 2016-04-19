from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_list, name='news_list'),
    url(r'^news/(?P<article_id>([a-zA-Z0-9]|-)+)/$', views.article, name='article'),
]