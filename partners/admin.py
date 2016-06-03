from django.contrib import admin
from .models import Partner, Image


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


class ImageInline(admin.StackedInline):
    model = Image


class PartnerAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Image, ImageAdmin)



