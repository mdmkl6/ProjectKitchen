from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from kitchen.models import Products
from recipes.models import Recipe
from recipes.models import ProductInRecipe

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def get_suggested_recipes(request):
  user = request.user
  kitchen_products = Products.objects.filter(owner=user).values_list('product')
  recipes = Recipe.objects.all()
  for recipe in recipes:
    recipe_products = ProductInRecipe.objects.filter(recipe=recipe).values_list('product')
    priority = recipe_products.intersection(kitchen_products).count()
    recipe.priority = priority
    recipe.save()
  recipes = Recipe.objects.all().order_by('-priority')
  return recipes

def home(request):
  if request.user.is_anonymous:
    return render(request, 'home.html')
  else:
    recipes = get_suggested_recipes(request)
    context = {
      "recipes": recipes
    }
    return render(request, 'home.html', context)

