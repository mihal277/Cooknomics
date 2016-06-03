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

    # prawidlowy sposob zbierania URLa - object.image.url
    print("path2: " + recipe.image.url)

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
    ingredients = IngredientRecipe.objects.filter(recipe=current_recipe)

    ingredients_list = []

    price = 0
    for ingredient in ingredients:
        ingredients_list.append(str(ingredient.ingredient) + " - " + str(ingredient.amount_name))
        price += ingredient.ingredient.price * ingredient.amount

    print(ingredients_list)

    context = {
        'slug': recipe_slug,
        'author': current_recipe.author,
        'title': current_recipe.title,
        'published_date': current_recipe.published_date,
        'content': current_recipe.content,
        'image_url': current_recipe.image.url,
        'ingredients': ingredients_list,
        'price': price
    }

    return render(request, 'recipes_detail.html', context)


# widok ktory zwraca AJAXEM liste produktow
@require_GET
def get_items(request):
    items = Ingredient.objects.all().order_by('name')

    # return list of {item.name: item.pk}
    context = []
    for item in items:
        context.append({item.name: item.pk})

    return HttpResponse(json.dumps(context), content_type='application/json')


@require_GET
def process_items(request):
    # If GET data is empty, assume no filters and return list of all recipes
    if not request.GET:
        recipes = Recipe.objects.all()
    else:
        # filter the recipes
        # recipes =
        pass

    #narazie nie filtrujex
    recipes = Recipe.objects.all()
    #recipes = []

    # If there are no recipes, return empty data <- POPRAWIC ZEBY MOZE JAKIES INFO WYPISYWALO (BRAK PRZEPISOW~)
    if len(recipes) == 0:
        return HttpResponse(json.dumps({}), content_type='application/json')

    page_data = {'objects': {}}

    for r in recipes:
        page_data['objects'][r.slug] = \
            model_to_dict(recipe, exclude=['published_date', 'image'])
        page_data['objects'][r.slug]['image_url'] = \
            recipe.image.url
        page_data['objects'][r.slug]['published_date'] = \
            recipe.published_date.timestamp()
        page_data['objects'][r.slug]['url'] = \
            reverse('recipes:recipe', kwargs={'recipe_slug': r.slug})

    context = {
        "page": page_data
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
