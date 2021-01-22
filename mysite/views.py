from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Case
from django.db.models import When
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
  ordered_tuples = ProductInRecipe.objects.filter(product__in=kitchen_products).values('recipe').annotate(priority=Count('recipe')).order_by('-priority')
  recipe_pks = [x['recipe'] for x in ordered_tuples]
  preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recipe_pks)])
  ordered_recipes = Recipe.objects.filter(pk__in=recipe_pks).order_by(preserved_order)
  return ordered_recipes

def home(request):
  if request.user.is_anonymous:
    return render(request, 'home.html')
  else:
    recipes = get_suggested_recipes(request)
    context = {
      "recipes": recipes
    }
    return render(request, 'home.html', context)

