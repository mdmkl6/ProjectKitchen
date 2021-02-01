from django.contrib import admin
from .models import Recipe
from .models import ProductInRecipe, UserRating


admin.site.register(Recipe)
admin.site.register(ProductInRecipe)
admin.site.register(UserRating)