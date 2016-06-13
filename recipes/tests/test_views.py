from django.test import TestCase
from django.core.urlresolvers import reverse
from recipes.views import NUMBER_OF_ELEMENTS_ON_PAGE, INITIAL_PAGE_SIZE
from recipes.models import *
from datetime import timedelta
from django.utils import timezone
import string
import random


def generate_random_string():
    chars = string.ascii_uppercase + string.digits
    length = random.randint(1, 100)

    return ''.join(random.choice(chars) for _ in range(length))


def add_recipe(title):
    return Recipe.objects.create(
        title=title,
        author=generate_random_string(),
        image="media/uploads/images/BNN.jpg",
    )


def add_random_recipe(ingredients):
    recipe = Recipe.objects.create(
        title=generate_random_string(),
        author=generate_random_string(),
        image="media/uploads/images/BNN.jpg",
    )

    for i in ingredients:
        IngredientDetails.objects.create(
            ingredient=i,
            recipe=recipe,
            amount=random.randint(1, 10),
            amount_name=generate_random_string()
        )

    return recipe


def add_random_ingredient():
    return Ingredient.objects.create(
        name=generate_random_string(),
        price=random.uniform(0, 300)
    )


def sort_object_list_by(list_to_sort, parameter):
    return sorted(list_to_sort, key=lambda elem: getattr(elem, parameter))


def sort_dict_list_by(list_to_sort, parameter):
    return sorted(list_to_sort, key=lambda elem: elem[parameter])


class RecipeListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('recipes:recipes_list')
        cls.ingredients = [add_random_ingredient() for _ in range(0, 10)]

    def test_basic(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes_index.html')
        self.assertTrue('page' in response.context)
        self.assertTrue('display_likes' in response.context)
        self.assertTrue(response.context['display_likes'])

    def test_pagination(self):
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_recipe(self.ingredients[:i])

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_too_much(self):
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_recipe(self.ingredients[:i])

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_not_enought(self):
        expected_size = INITIAL_PAGE_SIZE-1

        for i in range(0, expected_size):
            add_random_recipe(self.ingredients[:i])

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), expected_size)

    def test_good_order(self):
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_recipe(self.ingredients[:i])

        response = self.client.get(self.url)
        sorted_by_published_date = sort_object_list_by(response.context['page'].object_list,
                                                       'published_date')

        self.assertEqual(response.context['page'].object_list, sorted_by_published_date)

    def test_initial_page(self):
        recipe = Recipe.objects.create(
            title="recipe",
            author="me",
            image="media/uploads/images/BNN.jpg"
        )
        ingredient = Ingredient.objects.create(
            name="ingredient",
            price="123"
        )
        IngredientDetails.objects.create(
            ingredient=ingredient,
            recipe=recipe,
            amount=1,
            amount_name='piece'
        )

        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_recipe(self.ingredients[:i])

        response = self.client.get(self.url)

        self.assertTrue(recipe in response.context['page'].object_list)


class GetIngredientsTestCaste(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.NUMBER_OF_INGREDIENTS = 10
        cls.url = reverse('recipes:get_ingredients')
        cls.ingredients = [add_random_ingredient() for _ in range(0, cls.NUMBER_OF_INGREDIENTS)]

    def test_basic(self):
        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), self.NUMBER_OF_INGREDIENTS)

    def test_all_ingredients(self):
        response = self.client.get(self.url)
        response_data = response.json()

        expected_ingredient_names = [i.name for i in self.ingredients]
        response_ingredient_name = [list(d.keys())[0] for d in response_data]

        self.assertEqual(len(expected_ingredient_names), len(response_ingredient_name))
        self.assertTrue(all(name in response_ingredient_name for name in expected_ingredient_names))

    def test_correct_data(self):
        response = self.client.get(self.url)
        response_data = response.json()

        ingredient_list = sorted(self.ingredients,
                                 key=lambda elem: getattr(elem, "name"))
        response_list = sorted(response_data,
                               key=lambda elem: list(elem.keys())[0])

        self.assertTrue(all((p[0].name == list(p[1].keys())[0] and
                             p[0].pk == list(p[1].values())[0])
                            for p in zip(ingredient_list, response_list)))


class RecipesPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.NUMBER_OF_PAGES = 4
        cls.NUMBER_OF_INGREDIENTS = cls.NUMBER_OF_PAGES * NUMBER_OF_ELEMENTS_ON_PAGE
        cls.url = reverse('recipes:page')
        cls.ingredients = [add_random_ingredient() for _ in range(0, cls.NUMBER_OF_INGREDIENTS)]

        for i in range(0, cls.NUMBER_OF_PAGES * NUMBER_OF_ELEMENTS_ON_PAGE):
            add_random_recipe(cls.ingredients[:i])

    def test_basic(self):
        data = {
            'page': 1,
            'sorting': 'published_date'
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('json' in response['Content-Type'])

        response_json = response.json()
        page_data = response_json['page']

        self.assertTrue('page' in response_json)
        self.assertTrue('has_next' in page_data)
        self.assertTrue('objects' in page_data)
        self.assertEqual(len(page_data['objects']), NUMBER_OF_ELEMENTS_ON_PAGE)

    def test_has_next(self):
        data = {
            'page': 1,
            'sorting': 'published_date'
        }
        response = self.client.get(self.url, data)
        response_json = response.json()
        page_data = response_json['page']

        self.assertTrue(page_data['has_next'])

    def test_doesnt_have_next(self):
        data = {
            'page': self.NUMBER_OF_PAGES,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)
        response_json = response.json()
        page_data = response_json['page']

        self.assertFalse(page_data['has_next'])

    def test_all_data_sent(self):
        data = {
            'page': 1,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)
        response_json = response.json()
        page = response_json['page']['objects'][0]

        expected_fields = ['slug', 'title', 'author', 'content', 'published_date',
                           'up_votes', 'down_votes', 'image_url', 'url']
        self.assertTrue(all(field in page for field in expected_fields))

    def test_correct_data_sent(self):
        recipe = Recipe.objects.create(
            title="title",
            author="me",
            image="media/uploads/images/BNN.jpg",
        )
        data = {
            'page': self.NUMBER_OF_PAGES + 1,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)
        response_json = response.json()

        response_recipe = response_json['page']['objects'][0]

        self.assertEqual(recipe.slug, response_recipe['slug'])
        self.assertEqual(recipe.title, response_recipe['title'])
        self.assertEqual(recipe.author, response_recipe['author'])
        self.assertEqual(recipe.content, response_recipe['content'])
        self.assertEqual(recipe.published_date.timestamp(),
                         response_recipe['published_date'])
        self.assertEqual(recipe.image.url, response_recipe['image_url'])
        self.assertEqual(recipe.up_votes, response_recipe['up_votes'])
        self.assertEqual(recipe.down_votes, response_recipe['down_votes'])
        self.assertEqual(reverse('recipes:recipe', kwargs={'recipe_slug': recipe.slug}),
                         response_recipe['url'])

    def test_sorting(self):
        sorting_options = ['up_votes', 'published_date', 'title']

        for sorting in sorting_options:
            data = {
                'page': 1,
                'sorting': sorting,
            }
            response = self.client.get(self.url, data)
            response_objects = response.json()['page']['objects']
            sorted_list = sort_dict_list_by(response_objects, sorting)

            self.assertEqual(response_objects, sorted_list)

    def test_incorrect_page_number(self):
        data = {
            'page': self.NUMBER_OF_PAGES + 1,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 404)

    def test_incorrect_sorting_parameter(self):
        data = {
            'page': 1,
            'sorting': 'slug',
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 404)

    def test_no_page_parameter_in_data(self):
        data = {
            'sorting': 'published_date'
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 404)

    def test_no_sorting_parameter(self):
        data = {
            'page': 1
        }
        response = self.client.get(self.url, data)
        response_objects = response.json()['page']['objects']
        sorted_list = sort_dict_list_by(response_objects, 'published_date')

        self.assertEqual(response_objects, sorted_list)

    def test_fail_on_non_get(self):
        data = {
            'page': 1,
            'sorting': 'up_votes'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 405)


# TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class GetFilteredRecipesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("recipes:get_filtered_recipes")

    def test_basic(self):
        pass


class SearchRecipesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("recipes:search_recipes")
        cls.good_recipe_title_contains = "good"
        cls.string_not_in_any_recipe_title = generate_random_string()
        cls.NUMBER_OF_GOOD_RECIPES = 5
        cls.NUMBER_OF_BAD_RECIPES = 10

        for i in range(0, cls.NUMBER_OF_GOOD_RECIPES):
            add_recipe(cls.good_recipe_title_contains + str(i))
        for i in range(0, cls.NUMBER_OF_BAD_RECIPES):
            add_recipe(str(i))

    def test_basic_good_request(self):
        data = {
            "term": self.good_recipe_title_contains,
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('json' in response['Content-Type'])

        response_json = response.json()

        self.assertEqual(len(response_json), self.NUMBER_OF_GOOD_RECIPES)

    def test_basic_bad_data_sent(self):
        data = {}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, 400)

    def test_empty_data_expected(self):
        data = {
            "term": self.string_not_in_any_recipe_title
        }
        response = self.client.get(self.url, data)
        response_json = response.json()

        self.assertEqual(len(response_json), 0)

    def test_correct_data_received(self):
        data = {
            "term": self.good_recipe_title_contains,
        }
        response = self.client.get(self.url, data)
        response_json = response.json()

        expected_recipes = sorted(Recipe.objects.filter(title__icontains=
                                        self.good_recipe_title_contains),
                                  key=lambda elem: getattr(elem, "title"))
        recieved_results = sorted(list(response_json.items()),
                                  key=lambda elem: elem[0])

        self.assertEqual(len(expected_recipes), len(recieved_results))
        # sorry for this one
        self.assertTrue(all((list_element[0].title == list_element[1][0]) and
                            (reverse('recipes:recipe', kwargs={'recipe_slug': list_element[0].slug}) ==
                             list_element[1][1])
                            for list_element in zip(expected_recipes, recieved_results)))

    def test_fail_on_non_get(self):
        data = {
            "term": self.good_recipe_title_contains,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 405)


def add_random_recipe(ingredients):
    recipe = Recipe.objects.create(
        title=generate_random_string(),
        author=generate_random_string(),
        image="media/uploads/images/BNN.jpg",
    )

    for i in ingredients:
        IngredientDetails.objects.create(
            ingredient=i,
            recipe=recipe,
            amount=random.randint(1, 10),
            amount_name=generate_random_string()
        )

    return recipe


class RecipeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            title="title",
            author="me",
            image="media/uploads/images/BNN.jpg",
        )
        cls.ingredients = [add_random_ingredient() for _ in range(0, 10)]

        for i in cls.ingredients:
            IngredientDetails.objects.create(
                ingredient=i,
                recipe=cls.recipe,
                amount=random.randint(1, 10),
                amount_name=generate_random_string()
            )
        cls.recipe_url = reverse('recipes:recipe',
                             kwargs={'recipe_slug': cls.recipe.slug})

    def setUp(self):
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_recipe(self.ingredients[:i])

    def test_basic(self):
        response = self.client.get(self.recipe_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes_detail.html')
        self.assertTrue('slug' in response.context)
        self.assertTrue('author' in response.context)
        self.assertTrue('title' in response.context)
        self.assertTrue('published_date' in response.context)
        self.assertTrue('content' in response.context)
        self.assertTrue('image_url' in response.context)
        self.assertTrue('ingredients' in response.context)
        self.assertTrue('price' in response.context)
        self.assertTrue('up_votes' in response.context)
        self.assertTrue('down_votes' in response.context)

    def test_correct_response_data(self):
        response = self.client.get(self.recipe_url)
        response_article = response.context

        price = 0
        ingredient_list = []
        for i in self.ingredients:
            price += i.price * i.ingredientdetails_set.get(recipe=self.recipe).amount
            ingredient_list.append(str(i) + " - " +
                                   str(i.ingredientdetails_set.get(recipe=self.recipe).amount_name))

        self.assertEqual(self.recipe.slug, response_article['slug'])
        self.assertEqual(self.recipe.author, response_article['author'])
        self.assertEqual(self.recipe.title, response_article['title'])
        self.assertEqual(self.recipe.published_date, response_article['published_date'])
        self.assertEqual(self.recipe.content, response_article['content'])
        self.assertEqual(self.recipe.image.url, response_article['image_url'])
        self.assertEqual(self.recipe.up_votes, response_article['up_votes'])
        self.assertEqual(self.recipe.down_votes, response_article['down_votes'])
        self.assertEqual(price, response_article['price'])
        self.assertEqual(ingredient_list, response_article['ingredients'])

    def test_incorrect_slug_passed(self):
        nonexistent_slug = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                   for _ in range(123))
        response = self.client.get(reverse('recipes:recipe',
                                   kwargs={'recipe_slug': nonexistent_slug}))

        self.assertEqual(response.status_code, 404)
