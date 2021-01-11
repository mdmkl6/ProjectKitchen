from django.contrib import admin

# Register your models here.
from .models import Recipe
from .models import ProductInRecipe

admin.site.register(Recipe)
admin.site.register(ProductInRecipe)