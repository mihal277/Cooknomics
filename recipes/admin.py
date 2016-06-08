from django.contrib import admin
from .models import Ingredient
from .models import Recipe
from .models import IngredientDetails


class RecipeAdmin(admin.ModelAdmin):
    """

    The Django admin size will display the thumbnails of images.

    """
    readonly_fields = ('image_tag',)

admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientDetails)