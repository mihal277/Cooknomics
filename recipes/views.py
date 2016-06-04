from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
import json
from .models import Ingredient
from .models import Recipe
from .models import IngredientDetails
from .utils import do_pagination


# === Views for recipes app ===

NUMBER_OF_ELEMENTS_ON_PAGE = 1

def recipes_list(request):
    """

    Generates site containing first page of recipes list sorted by published_date.
    """
    recipes = Recipe.objects.all().order_by('published_date')

    # prawidlowy sposob zbierania URLa - object.image.url
    # recipe = recipes[0]
    # print("path: " + recipe.image.url)

    paginator = Paginator(recipes, NUMBER_OF_ELEMENTS_ON_PAGE)
    page = paginator.page(1)

    context = {
        'page': page,
    }

    return render(request, 'recipes_index.html', context)

# widok ktory zwraca AJAXEM liste produktow
@require_GET
def get_ingredients(request):
    items = Ingredient.objects.all().order_by('name')

    # return list of {item.name: item.pk}
    context = []
    for item in items:
        context.append({item.name: item.pk})

    return HttpResponse(json.dumps(context), content_type='application/json')

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

    context = do_pagination(recipes, NUMBER_OF_ELEMENTS_ON_PAGE, page_number)

    return HttpResponse(json.dumps(context), content_type='application/json')


@require_GET
def get_recipes(request):
    page_number = 1

    if not request.GET:
        # If GET data is empty, assume no filters and return list of all recipes
        recipes = Recipe.objects.all().order_by('published_date')
    else:
        get_data = request.GET.dict()

        page_number = get_data.get('page', None)
        if page_number is None:
            raise Http404

        get_data.pop('page')
        # If GET data is not empty, choose only recipes that match passed ingredients
        ingredients = []
        for pk in get_data:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredients.append(ingredient)

        # Filter the recipes, gets all the recipes that match at least 1 element
        recipes_all = Recipe.objects.filter(ingredients__in=ingredients)
        # Remove duplicates
        unique_recipes = set()
        recipes = [r for r in recipes_all if not (r in unique_recipes or unique_recipes.add(r))]

    # Paginate, throws 404 on error
    context = do_pagination(recipes, NUMBER_OF_ELEMENTS_ON_PAGE, page_number)

    return HttpResponse(json.dumps(context), content_type='application/json')


def recipe(request, recipe_slug):
    """

    Generates site of a given recipe

    """
    current_recipe = get_object_or_404(Recipe, pk=recipe_slug)
    ingredients = IngredientDetails.objects.filter(recipe=current_recipe)

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

