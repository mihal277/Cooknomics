from django.test import TestCase
from news.models import Article
from Cooknomics.utils import one_day_hence
from django.core.exceptions import ValidationError


class ArticleTestCase(TestCase):

    def setUp(self):
        Article.objects.create(title='What\'s your favorite pizza?',
                               author='Adam', content='pizza')
        Article.objects.create(title='What\'s your favorite pizza?',
                               author='Eva', content='pizza')
        Article.objects.create(title='Aaa', author='Joe',
                               published_date=one_day_hence())

    def test_article(self):
        article = Article.objects.get(author='Adam')
        article2 = Article.objects.get(author='Eva')
        article3 = Article.objects.get(author='Joe')

        article.clean()
        self.assertEqual(article.slug, 'whats-your-favorite-pizza')
        self.assertEqual(article2.slug, 'whats-your-favorite-pizza-2')
        self.assertEqual(article2.title, article2.__str__())
        with self.assertRaises(ValidationError):
            article3.clean()

