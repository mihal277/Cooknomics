from django.conf.urls import url
from . import views

app_name = 'partners'
urlpatterns = [
    url(r'^$', views.partners_list, name='partners_list'),

]