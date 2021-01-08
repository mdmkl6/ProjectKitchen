from django.shortcuts import render
from .models import Recipe

# Create your views here.


def recipes_view(request):
  all_recipes = Recipe.objects.all()
  data = []
  for item in all_recipes:
    data.append(item.get_dict())
  return render(request, 'recipes.html', {"data": data})


def single_recipe_view(request, id):
  chosen_recipe = Recipe.objects.get(id=id)
  context = {
      "recipe": chosen_recipe.get_dict(),
      #"recipe": chosen_recipe,
  }
  return render(request, 'recipe.html', context)
