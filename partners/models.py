from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    partner = models.ForeignKey(Partner)
    image = models.ImageField(upload_to="partners")

    def image_tag(self):
        return u'<img src="%s" />' % self.image.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.partner.name


