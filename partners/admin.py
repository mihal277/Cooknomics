from django.contrib import admin
from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    """

    The Django admin size will display the thumbnails of images.

    """
    readonly_fields = ('image_tag',)

admin.site.register(Partner, PartnerAdmin)




