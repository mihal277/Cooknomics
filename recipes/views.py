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

INITIAL_PAGE_SIZE = 1
NUMBER_OF_ELEMENTS_ON_PAGE = 1

def recipes_list(request):
    """

    Generates site containing first page of recipes list sorted by published_date.
    :param request: HttpRequest passed by browser.
    :return: HTML rendered from aproppriate template with initial data.
    """
    recipes = Recipe.objects.all().order_by('published_date')

    # prawidlowy sposob zbierania URLa - object.image.url
    # recipe = recipes[0]
    # print("path: " + recipe.image.url)

    paginator = Paginator(recipes, INITIAL_PAGE_SIZE)
    page = paginator.page(1)

    context = {
        'page': page,
        'display_likes': True,
    }

    return render(request, 'recipes_index.html', context)

@require_GET
def get_ingredients(request):
    """

    View responding to AJAX request for list of all ingredients currently stored in database.
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
    :param request: HttpRequest passed by browser. Its data hould contain 'page' -
    :return:
    """
    page_number = request.GET.get('page', None)
    if page_number is None:
        raise Http404

    # Get sorting parameter, if none is provides, sort by published_date
    sorting = request.GET.get('sorting', 'published_date')
    if sorting == 'up_votes':
        sorting = '-up_votes'

    recipes = Recipe.objects.all().order_by(sorting)

    context = do_pagination(recipes, NUMBER_OF_ELEMENTS_ON_PAGE, page_number)

    return HttpResponse(json.dumps(context), content_type='application/json')


@require_GET
def get_filtered_recipes(request):
    """

    View called when user clicks on search button on website. Searches database for recipces that contain
    ingredients selected by user.
    :param request: HttpRequest passed by browser. Should contain dict with keys:
                    'page' - number of page to fetch from server,
                    and the rest of keys: '<ingrednient_pk>', values don't matter.
    :return: List of recipes that contain at least one of ingredients selected by user. Format: JSON.
    """
    page_number = 1

    if not request.GET:
        # If GET data is empty, assume no filters and return list of all recipes
        recipes = Recipe.objects.all().order_by('published_date')
    else:
        get_data = request.GET.dict()

        page_number = get_data.get('page', None)
        if page_number is None:
            raise Http404

        sorting = request.GET.get('sorting', 'published_date')
        if sorting == 'up_votes':
            sorting = '-up_votes'

        get_data.pop('page')
        get_data.pop('sorting')
        # If GET data is not empty, choose only recipes that match passed ingredients
        ingredients = []
        for pk in get_data:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredients.append(ingredient)

        # Filter the recipes, gets all the recipes that match at least 1 element
        recipes_all = Recipe.objects.filter(ingredients__in=ingredients).order_by(sorting)
        # Remove duplicates
        unique_recipes = set()
        recipes = [r for r in recipes_all if not (r in unique_recipes or unique_recipes.add(r))]

    # Paginate, throws 404 on error
    context = do_pagination(recipes, NUMBER_OF_ELEMENTS_ON_PAGE, page_number)

    return HttpResponse(json.dumps(context), content_type='application/json')


@require_GET
def search_recipes(request):
    """

    View called when user enters some string into textbox on website.
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
    a recipe. Part of AJAX interface.
    Requires following parameters to be passed:
    ***pk*** - recipes database pk
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                downvote - increase down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given recipe
    ***downvotes*** - down_vote count of given recipe
    ***pk*** - primary key of the up/down voted recipe
    """
    if request.method == 'POST':
        recipe_pk = request.POST.get('pk', None)
        current_recipe = get_object_or_404(Recipe, pk=recipe_pk)

        status = request.session.get('vote_state_recipe_%s' % recipe_pk, 'none')
        request_type = request.POST.get('type', None)

        # set cookie expiry to 1 year
        request.session.set_expiry(31556926)

        if request_type == 'upvote':
            if status == 'none':
                current_recipe.upvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'upvoted'
            elif status == 'upvoted':
                current_recipe.cancel_upvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'none'
            elif status == 'downvoted':
                current_recipe.upvote()
                current_recipe.cancel_downvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'upvoted'
        elif request_type == 'downvote':
            if status == 'none':
                current_recipe.downvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'downvoted'
            elif status == 'upvoted':
                current_recipe.cancel_upvote()
                current_recipe.downvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'downvoted'
            elif status == 'downvoted':
                current_recipe.cancel_downvote()
                request.session['vote_state_recipe_%s' % recipe_pk] = 'none'

        context = {
            'upvotes': current_recipe.up_votes,
            'downvotes': current_recipe.down_votes,
            'pk': current_recipe.pk,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')
