from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.exceptions import ValidationError
from partners.utils import validate_url
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# === Models for partners app ===


class Partner(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not validate_url(self.url):
            raise ValidationError('Incorrect URL')


class Image(models.Model):
    partner = models.OneToOneField(Partner,
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    image = ThumbnailerImageField(upload_to="partners", resize_source=dict(size=(300, 300), sharpen=True))

    def image_tag(self):
        return u'<img src="%s" />' % self.image.url
    image_tag.short_description = 'Thumbnail'
    image_tag.allow_tags = True

    def __str__(self):
        return self.partner.name

    def clean(self):
        filesize = self.image.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)





