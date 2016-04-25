from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from videos.utils import youtube_video_exists
import unidecode
from unidecode import unidecode

# === Models for videos app ===


class Video(models.Model):
    """

    The Video class defines a single video.
    Each video has the following fields:

    1. **slug** - primary key and URL of the video
    2. **title** - title of the video
    3. **video_url** - youtube link
    4. **description** - description of the video
    5. **published_date** - when the article was published
    6. **up_votes** - how many people liked the article
    7. **down_votes** - how many people disliked the article

    The Video Class has also two functions:

    1. **__str__** - returns the name (title) of the video
    2. **clean** - validates the published_date field and the youtube link

    The Video Class has also a subclass:

    1. **Meta** - validates the uniqueness of the video

    """
    slug = AutoSlugField(populate_from=unidecode('title'),
                         unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    video_url = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    up_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    down_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    def clean(self):
        if self.published_date > timezone.now():
            raise ValidationError('The date cannot be in the future')
        if not youtube_video_exists(self.video_url):
            raise ValidationError('Video doesn\'t exist')

    class Meta:
        unique_together = ('title', 'published_date', 'video_url')