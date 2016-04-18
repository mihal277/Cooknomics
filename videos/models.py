from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
import random
import string


def url_slugify(value):
    """Returns a random slug consisting of upper-case letters,
    lower-case letters and numbers

    TODO: filter offensive words
    """
    return ''.join(random.sample(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits, 7))


class Video(models.Model):
    url_ref = AutoSlugField(populate_from=url_slugify,
                            unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    video_url = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def clean(self):
        if self.published_date > timezone.now():
            raise ValidationError('The date cannot be in the future')

