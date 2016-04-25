from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from tinymce.models import HTMLField
import unidecode
from unidecode import unidecode


class Article(models.Model):
    slug = AutoSlugField(populate_from=unidecode('title'), editable=False, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = HTMLField()
    published_date = models.DateTimeField(default=timezone.now)
    up_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    down_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    def clean(self):
        if self.published_date > timezone.now():
            raise ValidationError('The date cannot be in the future')

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

