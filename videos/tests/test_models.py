from django.test import TestCase
from videos.models import Video
from Cooknomics.utils import one_day_hence
from django.core.exceptions import ValidationError


class VideoTestCase(TestCase):

    def setUp(self):
        Video.objects.create(title='A', description='B',
                             video_url='HMNoC-EMzw8')
        Video.objects.create(title='C', description='D',
                             video_url='C-EMzw8')
        Video.objects.create(title='E', description='F',
                             video_url='HMNoC-EMzw8',
                             published_date=one_day_hence())

    def test_video(self):
        video = Video.objects.get(title='A')
        video2 = Video.objects.get(title='C')
        video3 = Video.objects.get(title='E')

        video.clean()
        self.assertTrue(video.__str__() == video.title)
        with self.assertRaises(ValidationError):
            video2.clean()
        with self.assertRaises(ValidationError):
            video3.clean()

