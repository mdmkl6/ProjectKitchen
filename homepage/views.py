from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Case
from django.db.models import When
from kitchen.models import ProductInKitchen
from recipes.models import Recipe, UserRating
from recipes.models import ProductInRecipe
import numpy as np


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
    return render(request, 'registration/signup.html', {'form': form})


def get_suggested_recipes(request):
    user = request.user
    kitchen_products = ProductInKitchen.objects.filter(owner=user).values_list('product')
    ordered_tuples = ProductInRecipe.objects.filter(product__in=kitchen_products).values('recipe').annotate(priority=Count('recipe')).order_by('-priority')
    recipe_pks = [x['recipe'] for x in ordered_tuples]
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recipe_pks)])
    ordered_recipes = Recipe.objects.filter(pk__in=recipe_pks).order_by(preserved_order)[:10]
    return ordered_recipes


def pearson_correlation(user_ratings_data, common_ratings):
    temp_common_ratings =  user_ratings_data[np.in1d(user_ratings_data[:,1], common_ratings[:,1])]
    temp_user_ratings = temp_common_ratings[:,2]
    other_user_ratings = common_ratings[:,2]
    
    sum_xx = np.sum(np.square(temp_user_ratings - np.mean(temp_user_ratings)))
    sum_yy = np.sum(np.square(other_user_ratings - np.mean(other_user_ratings)))
    sum_xy = np.sum((temp_user_ratings - np.mean(temp_user_ratings))*(other_user_ratings-np.mean(other_user_ratings)))
    
    if sum_xx != 0 and sum_yy != 0:
        return sum_xy/np.sqrt(sum_xx*sum_yy)
    else:
        return 0

 
def find_similar_users(user_ratings_data, common_ratings_data):

    common_rating_users = np.split(common_ratings_data, np.unique(common_ratings_data[:,0], 
                                                                   return_index=True)[1][1:])
    similarities = np.array(list(map(lambda other_ratings: pearson_correlation(user_ratings_data, other_ratings), 
                             common_rating_users))).astype('object')
    unique_ids = np.unique(common_ratings_data[:,0]).astype('object')
    user_similaries = np.column_stack((unique_ids, similarities))
    user_similaries = user_similaries[user_similaries[:,1].argsort()[::-1]][:20]
    
    return user_similaries[user_similaries[:,0].argsort()]


def create_ratings_array_with_similarity_index(ratings_data, similar_users):
    ratings_data = ratings_data[np.in1d(ratings_data[:,0], similar_users[:,0])]
    ratings_data = np.split(ratings_data, np.unique(ratings_data[:,0], return_index=True)[1][1:])
    return np.concatenate((list(map(lambda similarity, user_data: np.column_stack((user_data, np.repeat(similarity, len(user_data)))), 
                                  similar_users[:,1], ratings_data))))    


def calculate_weighted_ratings(recipes_ratings_data):
    recipes_ratings_data = np.split(recipes_ratings_data, np.unique(recipes_ratings_data[:,0], return_index=True)[1][1:])
        
    weighted_ratings = np.empty((0,2), object)
    for group in recipes_ratings_data:
        if abs(np.sum(group[:,2])) > 0.5:
            recipe_id = group[0][0]
            temp_arr = np.array([recipe_id, np.sum(group[:,1])/np.sum(group[:,2])])
            weighted_ratings = np.vstack((weighted_ratings, temp_arr))
                
    return weighted_ratings[weighted_ratings[:,1].argsort()[::-1]][:10]
    
    
def recommender(request):
    user = request.user
    user_ratings = user.ratings.order_by('owner_id', 'recipe_id')
    other_ratings = UserRating.objects.exclude(owner=user).order_by('owner_id', 'recipe_id')
    common_ratings = other_ratings.filter(recipe__in=user.rated_recipes.all()).order_by('owner_id', 'recipe_id')
    
    if user_ratings and other_ratings and common_ratings:
        uncommon_ratings = other_ratings.exclude(recipe__in=user.rated_recipes.all()).order_by('owner_id', 'recipe_id')
        user_ratings_data = np.array(user_ratings.values_list('owner_id', 'recipe_id', 'score'))
        common_ratings_data = np.array(common_ratings.values_list('owner_id', 'recipe_id', 'score'))
        top_similar_users = find_similar_users(user_ratings_data, common_ratings_data)
        
        other_ratings_data = np.array(uncommon_ratings.values_list('owner_id', 'recipe_id', 'score')).astype('object')

        top_recipes = create_ratings_array_with_similarity_index(other_ratings_data, top_similar_users)
        top_recipes = top_recipes[top_recipes[:,1].argsort()][:,1:]
        top_recipes[:,1] *= top_recipes[:,2]
        
        weighted_ratings = calculate_weighted_ratings(top_recipes)
        recommended_recipe_ids = list(weighted_ratings[:,0])
        
        if recommended_recipe_ids:
            return Recipe.objects.filter(id__in=recommended_recipe_ids)
        else:
            return Recipe.objects.order_by('?')[:10]
    else:
        return Recipe.objects.order_by('?')[:10]
    

def home(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    else:
        suggested_recipes = get_suggested_recipes(request)
        recommended_recipes = recommender(request)
        
        context = {
            "suggested_recipes": suggested_recipes,
            "recommended_recipes": recommended_recipes,
        }
    return render(request, 'home.html', context)


