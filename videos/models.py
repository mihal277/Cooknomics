from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from videos.utils import youtube_video_exists, trim_youtube_url, \
                         get_youtube_video_title, \
                         get_youtube_video_description
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

    The Video Class has also six functions:

    1. **__str__** - returns the name (title) of the video
    2. **clean** - validates the published_date field and the youtube link
    3. **upvote** - incerements up_votes count
    4. **downvote** - increments down_vote count
    5. **cancel_upvote** - decrements up_votes count
    6. **cancel_downvote** - decrements down_votes count

    The Video Class has also a subclass:

    1. **Meta** - validates the uniqueness of the video

    """
    slug = AutoSlugField(populate_from=unidecode('title'),
                         unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    video_url = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    up_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    down_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    def clean(self):
        original_url = self.video_url
        if self.published_date > timezone.now():
            raise ValidationError('The date cannot be in the future')
        if not youtube_video_exists(self.video_url):
            raise ValidationError('Video doesn\'t exist')
        else:
            self.video_url = trim_youtube_url(self.video_url)

        if not self.title:
            self.title = get_youtube_video_title(original_url)
        if not self.description:
            self.description = get_youtube_video_description(original_url)

    def upvote(self):
        self.up_votes += 1
        self.save()

    def downvote(self):
        self.down_votes += 1
        self.save()

    def cancel_upvote(self):
        self.up_votes -= 1
        self.save()

    def cancel_downvote(self):
        self.down_votes -= 1
        self.save()

    class Meta:
        unique_together = ('title', 'published_date', 'video_url')
