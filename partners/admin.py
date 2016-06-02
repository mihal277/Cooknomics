from django.contrib import admin
from .models import Partner, Image

admin.site.register(Partner)
admin.site.register(Image)

fields = ('image_tag',)
readonly_fields = ('image_tag',)
