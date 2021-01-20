from django.contrib import admin

# Register your models here.
from .models import Recipe
from .models import ProductInRecipe, UserRating

admin.site.register(Recipe)
admin.site.register(ProductInRecipe)
admin.site.register(UserRating)