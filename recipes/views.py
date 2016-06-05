from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .models import Ingredient
from .models import Recipe
from .models import IngredientDetails
from .utils import do_pagination
import json


# === Views for recipes app ===

NUMBER_OF_ELEMENTS_ON_PAGE = 1

def recipes_list(request):
    """

    Generates site containing first page of recipes list sorted by published_date.
    """
    recipes = Recipe.objects.all().order_by('published_date')

    # prawidlowy sposob zbierania URLa - object.image.url
    recipe = recipes[0]
    print("path: " + recipe.image.url)

    paginator = Paginator(recipes, NUMBER_OF_ELEMENTS_ON_PAGE)
    page = paginator.page(1)

    context = {
        'page': page,
    }

    return render(request, 'recipes_index.html', context)

# widok ktory zwraca AJAXEM liste produktow
@require_GET
def get_ingredients(request):
    """

    :param request: HttpRequest passed by browser.
    :return: List of all ingredients stored in a database in format {'ingredient.name': ingredient.pk}.
    """
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


@require_GET
def search_recipes(request):
    """

    :param request: HttpRequest passed by browser. Should contain string to be searched for.
    :return: List of recipes whose title contains given string. Format: JSON.
    """

    string_to_find = request.GET.get("term", None)

    if string_to_find is None:
        return HttpResponse(status=400)

    matching_recipes = Recipe.objects.filter(title__icontains=string_to_find)

    context = {}
    for r in matching_recipes:
        context[r.title] = reverse('recipes:recipe', kwargs={'recipe_slug': r.slug})

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

    print(current_recipe.image.url)

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

@require_POST
def vote(request):
    """

    Generates JSON response to a POST request sent after user up(down)votes
    a video. Part of AJAX interface.
    Requires following parameters to be passed:
    ***pk*** - recipes database pk
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                downvote - increase down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given video
    ***downvotes*** - down_vote count of given video
    """
    if request.method == 'POST':
        object_pk = request.POST.get('pk', None)
        current_object = get_object_or_404(Recipe, pk=object_pk)

        status = request.session.get('vote_state_recipe_%s' % object_pk, 'none')
        request_type = request.POST.get('type', None)

        # set cookie expiry to 1 year
        request.session.set_expiry(31556926)

        if request_type == 'upvote':
            if status == 'none':
                current_object.upvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'upvoted'
            elif status == 'upvoted':
                current_object.cancel_upvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'none'
            elif status == 'downvoted':
                current_object.upvote()
                current_object.cancel_downvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'upvoted'
        elif request_type == 'downvote':
            if status == 'none':
                current_object.downvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'downvoted'
            elif status == 'upvoted':
                current_object.cancel_upvote()
                current_object.downvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'downvoted'
            elif status == 'downvoted':
                current_object.cancel_downvote()
                request.session['vote_state_recipe_%s' % object_pk] = 'none'

        context = {
            'upvotes': current_object.up_votes,
            'downvotes': current_object.down_votes,
            'pk': current_object.pk,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')
