from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe
# Create your views here.


def recipes_view(request):
  all_recipes = Recipe.objects.all()
  data = []
  for item in all_recipes:
    data.append(item.get_dict())
  return render(request, 'recipes.html', {"data": data})