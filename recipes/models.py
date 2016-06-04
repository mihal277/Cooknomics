from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from unidecode import unidecode

# === Models for recipes app ===


class Ingredient(models.Model):
    """

    The Ingredient class defines a single ingredient.
    Each ingredient has the following fields:

    1. **name** - name of the ingredient
    2. **price** - price of the ingredient for 1kg or 1l

    The Ingredient Class has also two functions:

    1. **__str__** - returns the name of the ingredient
    2. **clean** - validates the fields

    """
    name = models.CharField(max_length=200, primary_key=True, verbose_name="Nazwa składnika")
    price = models.FloatField(default=0, verbose_name="Cena w PLN za 1kg lub 1l")

    def __str__(self):
        return self.name

    def clean(self):
        if self.name == '':
            raise ValidationError('The ingredient name should not be empty')

        if self.price < 0:
            raise ValidationError('The price should be >= 0')

    class Meta:
        verbose_name = "Składnik"
        verbose_name_plural = "Składniki"


class Recipe(models.Model):
    """

    The Recipe class defines a single recipe.
    Each recipe has the following fields:

    1. **slug** - primary key and URL of the recipe
    2. **title** - title of the recipe
    3. **author** - author of the recipe
    4. **content** - content of the recipe
    5. **published_date** - when the recipe was published
    6. **image** - image of the ready meal
    7. **image_url** - short url of the image

    The Recipe Class has also two functions:

    1. **__str__** - returns the name (title) of the recipe
    2. **clean** - validates the published_date field and sets the image_url field value

    """
    slug = AutoSlugField(populate_from=unidecode('title'), editable=False, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = HTMLField()
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='images/BNN.jpg', upload_to='images/')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientDetails')

    def __str__(self):
        return self.title

    def clean(self):
        self.image_url = self.image.url[self.image.url.find('/media/'):]
        if self.published_date > timezone.now():
            raise ValidationError('The date cannot be in the future')

    class Meta:
        verbose_name = "Przepis"
        verbose_name_plural = "Przepisy"


class IngredientDetails(models.Model):
    """

        The IngredientRecipe class defines ingredients used in recipe
        Each recipe has the following fields:

        1. **ingredient**
        2. **recipe**
        3. **amountt** - amount of the given ingredient

        The Recipe Class has also two functions:

        1. **__str__**
        2. **clean** - validates the amount field

        """

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Składnik")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Przepis")
    amount = models.FloatField(default=0, verbose_name="Ilość składnika (kilogramów lub litrów)")
    amount_name = models.CharField(max_length=200, default="", verbose_name="Nazwa ilosci, np. 1 szklanka, 2 łyżeczki")

    def __str__(self):
        return str(self.ingredient) + " -> " + str(self.recipe) + " x " + str(self.amount)

    def clean(self):
        if self.amount < 0:
            raise ValidationError('Amount should be >= 0')

    class Meta:
        verbose_name = "Dodatkowe dane składnika"
        verbose_name_plural = "Dodatkowe dane składników"


