from django.conf.urls import url
from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.news_list, name='news_list'),
    url(r'^vote$', views.vote, name='vote'),
    url(r'^page$', views.news_page, name='page'),
    url(r'^(?P<article_slug>([a-zA-Z0-9-])+)/$', views.article, name='article'),
]