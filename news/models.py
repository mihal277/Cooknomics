from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from tinymce.models import HTMLField
import unidecode
from unidecode import unidecode

# === Models for news app ===


class Article(models.Model):
    """

    The Article class defines a single article.
    Each article has the following fields:

    1. **slug** - primary key and URL of the article
    2. **title** - title of the article
    3. **author** - author of the article
    4. **content** - content of the article
    5. **published_date** - when the article was published
    6. **up_votes** - how many people liked the article
    7. **down_votes** - how many people disliked the article

    The Article Class has also two functions:

    1. **__str__** - returns the name (title) of the article
    2. **clean** - validates the published_date field

    """
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

