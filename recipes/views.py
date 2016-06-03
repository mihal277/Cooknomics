from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json
from .models import Ingredient
from .models import Recipe
from .models import IngredientRecipe


# === Views for recipes app ===


def recipes_list(request):
    """

    Generates site containing first page of recipes list sorted by published_date.
    """
    recipes = Recipe.objects.all().order_by('published_date')
    recipe = recipes[0]
    print(recipe.image.url)

    paginator = Paginator(recipes, 20)
    page = paginator.page(1)

    context = {
        'page': page,
    }

    return render(request, 'recipes_index.html', context)


@require_GET
def recipes_page(request):
    """
    View to generate updates to recipes list when user scrolls down the page.

    Returns page_number-th page as JSON.
    """
    page_number = request.GET.get('page', None)

    if page_number is None:
        raise Http404

    recipes = Recipe.objects.all().order_by('published_date')

    paginator = Paginator(recipes, 20)

    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    page_data = {'objects': {}}

    for recipes in page.object_list:
        page_data['objects'][recipes.slug] = \
            model_to_dict(recipes, exclude='published_date')
        page_data['objects'][recipes.slug]['published_date'] = \
            recipes.published_date.timestamp()
        page_data['objects'][recipes.slug]['url'] = \
            reverse('recipes:recipe', kwargs={'recipe_slug': recipes.slug})

    page_data['has_next'] = page.has_next()

    context = {
        "page": page_data
    }

    return HttpResponse(json.dumps(context), content_type='application/json')


def recipe(request, recipe_slug):
    """

    Generates site of a given recipe

    """
    current_recipe = get_object_or_404(Recipe, pk=recipe_slug)

    context = {
        'slug': recipe_slug,
        'author': current_recipe.author,
        'title': current_recipe.title,
        'published_date': current_recipe.published_date,
        'content': current_recipe.content,
        'image_url': current_recipe.image_url
    }

    return render(request, 'recipes_detail.html', context)
