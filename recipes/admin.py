from django.contrib import admin
from .models import Ingredient
from .models import Recipe
from .models import IngredientDetails

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientDetails)