from django.shortcuts import render
from .models import Recipe, UserRating 
from django.http import JsonResponse

# Create your views here.
def recipes_view(request):
  recipes = Recipe.objects.all()
  context = {
    "recipes": recipes
  }
  return render(request, 'recipes.html', context)


def single_recipe_view(request, id):
  chosen_recipe = Recipe.objects.get(id=id)
  user = request.user
  user_rating_score = 0
  
  if UserRating.objects.filter(recipe=chosen_recipe, owner=user).exists():
    user_rating_score = UserRating.objects.get(recipe=chosen_recipe, owner=user).score
  
  context = {
      "recipe": chosen_recipe,
      "user_rating": user_rating_score, 
  }
  return render(request, 'recipe.html', context)


def user_rating_view(request, id):
    if request.method == 'POST':
        user = request.user
        current_recipe = Recipe.objects.get(id=id)
        rating_value = request.POST.get('rating_value')
        if not UserRating.objects.filter(recipe=current_recipe, owner=user):
            rating = UserRating.objects.create(recipe=current_recipe, owner=user,
                                                 score=rating_value)
            rating.save()
            current_recipe.rated_by.add(rating.owner)
        else:
          rating = UserRating.objects.get(recipe=current_recipe, owner=user)
          rating.score = rating_value
          rating.save()
        return JsonResponse({'success':'true', 'score': rating_value}, safe=False)
    return JsonResponse({'success': 'false'})
