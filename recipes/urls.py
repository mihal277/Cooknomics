from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipes'
urlpatterns = [
    url(r'^$', views.recipes_list, name='recipes_list'),
    url(r'^page$', views.recipes_page, name='page'),
    url(r'^(?P<recipe_slug>([a-zA-Z0-9-])+)/$', views.recipe, name='recipe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


