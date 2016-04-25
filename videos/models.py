from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from videos.utils import youtube_video_exists
import unidecode
from unidecode import unidecode


class Video(models.Model):
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