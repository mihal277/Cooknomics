from django.test import TestCase
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from news.models import *
from datetime import timedelta
from django.utils import timezone
from news.views import NUMBER_OF_ELEMENTS_ON_PAGE, INITIAL_PAGE_SIZE
import string
import random


def generate_random_string():
    chars = string.ascii_uppercase + string.digits
    length = random.randint(1, 100)

    return ''.join(random.choice(chars) for _ in range(length))


def add_random_news():
    return Article.objects.create(
        title=generate_random_string(),
        author=generate_random_string(),
        content=generate_random_string(),
    )


def add_news(title, author, up_votes=0, down_votes=0):
    return Article.objects.create(
        title=title,
        author=author,
        content=generate_random_string(),
        up_votes=up_votes,
        down_votes=down_votes,
    )


def sort_object_list_by(list_to_sort, parameter):
    return sorted(list_to_sort, key=lambda elem: getattr(elem, parameter))


def sort_dict_list_by(list_to_sort, parameter):
        return sorted(list_to_sort, key=lambda elem: elem[parameter])


class NewsListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('news:news_list')

    def test_basic(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_index.html')
        self.assertTrue('page' in response.context)
        self.assertTrue('display_likes' in response.context)
        self.assertTrue(response.context['display_likes'])

    def test_pagination(self):
        for i in range(0, INITIAL_PAGE_SIZE):
            add_random_news()

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_too_much(self):
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_news()

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_not_enough(self):
        for i in range(0, INITIAL_PAGE_SIZE-1):
            add_random_news()

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE-1)

    def test_good_order(self):
        for i in range(0, INITIAL_PAGE_SIZE-1):
            add_random_news()

        response = self.client.get(self.url)
        sorted_by_published_date = sort_object_list_by(response.context['page'].object_list,
                                                'published_date')

        self.assertEqual(response.context['page'].object_list, sorted_by_published_date)

    def test_initial_page(self):
        article = add_news('title', 'me')
        for i in range(0, 2*INITIAL_PAGE_SIZE):
            add_random_news()

        response = self.client.get(self.url)

        self.assertTrue(article in response.context['page'].object_list)


class NewsPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("news:page")
        cls.data = {
            'page': 1,
            'sorting': 'published_date',
        }
        cls.NUMBER_OF_PAGES = 2

    def setUp(self):
        for i in range(0, self.NUMBER_OF_PAGES * NUMBER_OF_ELEMENTS_ON_PAGE):
            add_random_news()

    def test_basic(self):
        response = self.client.get(self.url, self.data)
        response_json = response.json()
        page_data = response_json['page']

        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response_json)
        self.assertTrue('has_next' in page_data)
        self.assertTrue('objects' in page_data)
        self.assertEqual(len(page_data['objects']), NUMBER_OF_ELEMENTS_ON_PAGE)

    def test_has_next(self):
        response = self.client.get(self.url, self.data)
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
        response = self.client.get(self.url, self.data)
        response_json = response.json()
        page = response_json['page']['objects'][0]

        expected_fields = ['slug', 'title', 'author', 'content',
                           'published_date', 'up_votes', 'down_votes', 'url']
        self.assertTrue(all(field in page for field in expected_fields))

    def test_correct_data_sent(self):
        article = add_news('news', 'me')
        data = {
            'page': self.NUMBER_OF_PAGES + 1,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)
        response_json = response.json()

        response_article = response_json['page']['objects'][0]

        self.assertEqual(article.slug, response_article['slug'])
        self.assertEqual(article.title, response_article['title'])
        self.assertEqual(article.author, response_article['author'])
        self.assertEqual(article.content, response_article['content'])
        self.assertEqual(article.published_date.timestamp(),
                         response_article['published_date'])
        self.assertEqual(article.up_votes, response_article['up_votes'])
        self.assertEqual(article.down_votes, response_article['down_votes'])
        self.assertEqual(reverse('news:article', kwargs={'article_slug': article.slug}),
                         response_article['url'])

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
            'page': self.NUMBER_OF_PAGES + 5,
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
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 405)


class ArticleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(
            title="title",
            author="me",
            content=generate_random_string(),
            up_votes=1337,
            down_votes=54337,
        )
        cls.article_url = reverse('news:article',
                                  kwargs={'article_slug': cls.article.slug})

    def setUp(self):
        for i in range(0, 40):
            add_random_news()

    def test_basic(self):
        response = self.client.get(self.article_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_detail.html')
        self.assertTrue('slug' in response.context)
        self.assertTrue('author' in response.context)
        self.assertTrue('title' in response.context)
        self.assertTrue('published_date' in response.context)
        self.assertTrue('content' in response.context)
        self.assertTrue('up_votes' in response.context)
        self.assertTrue('down_votes' in response.context)

    def test_correct_response_data(self):
        response = self.client.get(self.article_url)
        response_article = response.context

        self.assertEqual(self.article.slug, response_article['slug'])
        self.assertEqual(self.article.author, response_article['author'])
        self.assertEqual(self.article.title, response_article['title'])
        self.assertEqual(self.article.published_date, response_article['published_date'])
        self.assertEqual(self.article.content, response_article['content'])
        self.assertEqual(self.article.up_votes, response_article['up_votes'])
        self.assertEqual(self.article.down_votes, response_article['down_votes'])

    def test_incorrect_slug_passed(self):
        nonexistent_slug = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                   for _ in range(123))
        response = self.client.get(reverse('news:article',
                                   kwargs={'article_slug': nonexistent_slug}))

        self.assertEqual(response.status_code, 404)


class VoteTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="title",
            author="me",
            content=generate_random_string(),
            up_votes=0,
            down_votes=0,
        )

        self.url = reverse("news:vote")

    def test_basic_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.up_votes, 1)

    def test_basic_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.down_votes, 1)

    def test_upvote_on_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.up_votes, 0)

    def test_downvote_on_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.down_votes, 0)

    def test_upvote_on_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)
        data['type'] = 'upvote'
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.up_votes, 1)
        self.assertEqual(self.article.down_votes, 0)

    def test_downvote_on_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)
        data['type'] = 'downvote'
        response = self.client.post(self.url, data)
        self.article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.up_votes, 0)
        self.assertEqual(self.article.down_votes, 1)

    # Session tests

    def test_session_no_vote(self):
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict.get(
            'vote_state_article_%s' % self.article.slug),
            None)

    def test_session_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "upvoted")

    def test_session_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "downvoted")

    def test_session_upvote_on_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)

        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "none")

    def test_session_downvote_on_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)

        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "none")

    def test_session_downvoted_an_upvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)

        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "downvoted")

    def test_session_upvoted_a_downvote(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        self.client.post(self.url, data)

        data = {
            'pk': self.article.pk,
            'type': 'upvote',
        }
        self.client.post(self.url, data)
        session = self.client.session
        session_dict = Session.objects.get(pk=session.session_key).get_decoded()

        self.assertEqual(session_dict['vote_state_article_%s' % self.article.slug],
                         "upvoted")

    def test_basic_return_value(self):
        data = {
            'pk': self.article.pk,
            'type': 'downvote',
        }
        response = self.client.post(self.url, data)
        response_data = response.json()

        self.article = Article.objects.get(pk=self.article.pk)
        self.assertEqual(response_data['pk'], self.article.pk)
        self.assertEqual(response_data['upvotes'], self.article.up_votes)
        self.assertEqual(response_data['upvotes'], self.article.up_votes)

    def test_incorrect_data_pk(self):
        nonexistent_slug = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                   for _ in range(123))
        data = {
            'pk': nonexistent_slug,
            'type': 'upvote'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 404)

    def test_incorrect_data_type(self):
        data = {
            'pk': self.article.pk,
            'type': 'incorrect',
        }
        response = self.client.post(self.url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['pk'], self.article.pk)
        self.assertEqual(response_data['upvotes'], self.article.up_votes)
        self.assertEqual(response_data['downvotes'], self.article.down_votes)

    def test_incorrect_data_no_type(self):
        data = {
            'pk': self.article.pk,
        }
        response = self.client.post(self.url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['pk'], self.article.pk)
        self.assertEqual(response_data['upvotes'], self.article.up_votes)
        self.assertEqual(response_data['downvotes'], self.article.down_votes)

    def test_votes_expiry_date(self):
        data = {
            'pk': self.article.pk,
        }
        self.client.post(self.url, data)
        session = self.client.session

        self.assertGreater(session.get_expiry_date(),
                           timezone.now() + timedelta(days=364))
