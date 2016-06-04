from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipes'
urlpatterns = [
    url(r'^$', views.recipes_list, name='recipes_list'),
    url(r'^page$', views.recipes_page, name='page'),
    url(r'^get_ingredients$', views.get_ingredients, name='get_ingredients'),
    url(r'^get_recipes$', views.get_recipes, name='get_recipes'),
    url(r'^(?P<recipe_slug>([a-zA-Z0-9-])+)/$', views.recipe, name='recipe'),
    url(r'^search_recipes$', views.search_recipes, name='search_recipes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


