from django.test import TestCase
from django.core.urlresolvers import reverse
from videos.models import *
from videos.views import NUMBER_OF_ELEMENTS_ON_PAGE, INITIAL_PAGE_SIZE
import string
import random


def generate_random_string():
    chars = string.ascii_uppercase + string.digits
    length = random.randint(1, 100)

    return ''.join(random.choice(chars) for _ in range(length))


def add_video(video_url):
    return Video.objects.create(
        video_url=video_url,
        title=generate_random_string(),
        description=generate_random_string(),
    )


def sort_object_list_by(list_to_sort, parameter):
    return sorted(list_to_sort, key=lambda elem: getattr(elem, parameter))


def sort_dict_list_by(list_to_sort, parameter):
    return sorted(list_to_sort, key=lambda elem: elem[parameter])

# THOSE TESTS DEPEND ON THE FACT, THAT INITIAL PAGE SIZE = 2 AND
# NUMBER_OF_ELEMENTS_ON_PAGE = 2, because it was hard to generate
# random valid video slugs.


class VideosListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("videos:videos_list")

    def test_basic(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("video_index.html")
        self.assertTrue("page" in response.context)
        self.assertTrue("display_likes" in response.context)
        self.assertTrue(response.context['display_likes'])

    def test_pagination(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        self.video2 = add_video('HOQS3fTPDsw')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_too_much(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        self.video2 = add_video('HOQS3fTPDsw')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['page']), INITIAL_PAGE_SIZE)

    def test_pagination_not_enough(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['page']), 1)

    def test_good_order(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        self.video2 = add_video('HOQS3fTPDsw')
        response = self.client.get(self.url)
        sorted_by_published_date = sort_object_list_by(response.context['page'].object_list,
                                        'published_date')

        self.assertEqual(response.context['page'].object_list, sorted_by_published_date)

    def test_initial_page(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        self.video2 = add_video('HOQS3fTPDsw')
        self.video3 = add_video('UaAhS-rtvl0')

        response = self.client.get(self.url)

        self.assertTrue(self.video1 in response.context['page'].object_list)


class VideoPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("videos:page")
        cls.data = {
            'page': 1,
            'sorting': 'published_date',
        }

    def setUp(self):
        self.video1 = add_video('hBQ8fh_Fp04')
        self.video2 = add_video('HOQS3fTPDsw')
        self.video3 = add_video('UaAhS-rtvl0')
        self.video4 = add_video('iNyN6noGRqg')

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
            'page': 2,
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

        expected_fields = ['slug', 'title', 'published_date',
                           'up_votes', 'down_votes', 'url']
        self.assertTrue(all(field in page for field in expected_fields))

    def test_correct_data_sent(self):
        video = add_video('bZ1WmeKir78')
        data = {
            'page': 3,
            'sorting': 'published_date',
        }
        response = self.client.get(self.url, data)
        response_json = response.json()
        response_video = response_json['page']['objects'][0]

        self.assertEqual(video.slug, response_video['slug'])
        self.assertEqual(video.title, response_video['title'])
        self.assertEqual(video.published_date.timestamp(),
                         response_video['published_date'])
        self.assertEqual(video.up_votes, response_video['up_votes'])
        self.assertEqual(video.down_votes, response_video['down_votes'])
        self.assertEqual(reverse('videos:single_video', kwargs={'video_slug': video.slug}),
                         response_video['url'])

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
            'page': 5,
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


class SingleVideoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.video = add_video('hBQ8fh_Fp04')
        cls.video_url = reverse('videos:single_video',
                                kwargs={'video_slug': cls.video.slug})

    def test_basic(self):
        response = self.client.get(self.video_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_detail.html')
        self.assertTrue('slug' in response.context)
        self.assertTrue('title' in response.context)
        self.assertTrue('published_date' in response.context)
        self.assertTrue('description' in response.context)
        self.assertTrue('up_votes' in response.context)
        self.assertTrue('down_votes' in response.context)

    def test_correct_response_data(self):
        response = self.client.get(self.video_url)
        response_video = response.context

        self.assertEqual(self.video.slug, response_video['slug'])
        self.assertEqual(self.video.title, response_video['title'])
        self.assertEqual(self.video.published_date, response_video['published_date'])
        self.assertEqual(self.video.description, response_video['description'])
        self.assertEqual(self.video.up_votes, response_video['up_votes'])
        self.assertEqual(self.video.down_votes, response_video['down_votes'])

    def test_incorrect_slug_passed(self):
        nonexistent_slug = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                   for _ in range(123))
        response = self.client.get(reverse('videos:single_video',
                                   kwargs={'video_slug': nonexistent_slug}))

        self.assertEqual(response.status_code, 404)

# Not testing vote view, because its 100% same as the one already tests in news
