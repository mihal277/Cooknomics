from django.test import TestCase
from videos.utils import youtube_video_exists


class UtilsTestCase(TestCase):

    CORRECT_VIDEOS = [
        'https://www.youtube.com/watch?v=jdiAraeA_8k&t=638s',
        'https://www.youtube.com/watch?v=-iSxls2f0Qo',
        'https://www.youtube.com/watch?v=Eyaf1yMHx54',
    ]


    INCORRECT_VIDEOS = [
        'https://www.youtube.com/watch?v=dsguhdiufgh_',
        'https://www.google.com/',
        'Eyaf1yMHx54',
        'sdjfnksjafnbubiubsadf',
    ]

    def test_youtube_video_exists(self):
        for v in self.CORRECT_VIDEOS:
            self.assertTrue(youtube_video_exists(v))
        for v in self.INCORRECT_VIDEOS:
            self.assertFalse(youtube_video_exists(v))




