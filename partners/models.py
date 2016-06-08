from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from partners.utils import validate_url
from Cooknomics.utils import validate_image
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# === Models for partners app ===


class Partner(models.Model):
    """

    The Partner class defines a single partner.
    Each partner has the following fields:

    1. **name** - name of the partner
    2. **url** -  a url pointing to the partner's website
    3. **image** -  the representation of the image file (partner's logo)

    The Partner Class has also the following functions:

    1. **__str__** - returns the name of the partner
    2. **clean** - validates the url and the image
    3. **save** - custom save method to delete the image file when updating
    4. **image_tag** - used to create a thumbnail in admin

    """
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, blank=True)
    image = ThumbnailerImageField(upload_to="partners/", resize_source=dict(size=(300, 300), sharpen=True),
                                  blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        try:
            if self.url:
                validate_url(self.url)
            if self.image:
                validate_image(self.image.file.size, self.image.name)
        except:
            raise

    def save(self, *args, **kwargs):
        try:
            this = Partner.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # new photo
        super(Partner, self).save(*args, **kwargs)

    def image_tag(self):
        return u'<img src="%s" />' % self.image.url
    image_tag.short_description = 'Thumbnail'
    image_tag.allow_tags = True


@receiver(pre_delete, sender=Partner)
def image_delete(sender, instance, **kwargs):
    """

    image_delete makes sure to delete the file whenever an image object is deleted

    """
    instance.image.delete(False)


