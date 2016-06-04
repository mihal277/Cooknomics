from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partners'
urlpatterns = [
    url(r'^$', views.partners_list, name='partners_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
