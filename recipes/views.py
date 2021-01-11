from django.shortcuts import render
from .models import Recipe

# Create your views here.
def recipes_view(request):
  recipes = Recipe.objects.all()
  context = {
    "recipes": recipes
  }
  return render(request, 'recipes.html', context)

def single_recipe_view(request, id):
  chosen_recipe = Recipe.objects.get(id=id)
  context = {
      "recipe": chosen_recipe
  }
  return render(request, 'recipe.html', context)
