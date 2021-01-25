from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Case
from django.db.models import When
from kitchen.models import Products
from recipes.models import Recipe, UserRating
from recipes.models import ProductInRecipe
import pandas as pd
from math import sqrt


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


def pearson_correlation(user_ratings_data, common_ratings):
    common_ratings = common_ratings.sort_values(by='recipe_id')
    user_ratings_data = user_ratings_data.sort_values(by='recipe_id')
    num_of_ratings = len(common_ratings)
    temp_df = user_ratings_data[user_ratings_data['recipe_id'].isin(common_ratings['recipe_id'].tolist())]
    temp_rating_list = temp_df['score'].tolist()
    temp_group_list = common_ratings['score'].tolist()
    sum_xx = sum([i**2 for i in temp_rating_list]) - pow(sum(temp_rating_list),2)/num_of_ratings
    sum_yy = sum([i**2 for i in temp_group_list]) - pow(sum(temp_group_list),2)/num_of_ratings
    sum_xy = sum( i*j for i, j in zip(temp_rating_list, temp_group_list)) \
            - sum(temp_rating_list)*sum(temp_group_list)/num_of_ratings

    if sum_xx != 0 and sum_yy != 0:
        return sum_xy/sqrt(sum_xx*sum_yy)
    else:
        return 0

 
def pearson_correlation_dataframe(user_ratings_data, common_ratings_data):
    common_rating_groups = sorted(common_ratings_data.groupby(['owner_id']), 
                                  key=lambda x: len(x[1]), reverse=True)
    pearson_correlation_dict = {}
    
    for owner_id, group in common_rating_groups:
        pearson_correlation_dict[owner_id] = pearson_correlation(user_ratings_data, group)
    
    pearson_df = pd.DataFrame.from_dict(pearson_correlation_dict, orient='index')
    pearson_df.columns = ['similarity_index']
    pearson_df['owner_id'] = pearson_df.index
    pearson_df.index = range(len(pearson_df))
    return pearson_df
        

def recommender(request):
    user = request.user
    user_ratings = UserRating.objects.filter(owner=user)
    other_ratings = UserRating.objects.exclude(owner=user)
    recommended_recipes = {}
    
    if user_ratings and other_ratings:
        user_df = pd.DataFrame(user_ratings.values('owner_id', 'recipe_id', 'score'))
        others_df = pd.DataFrame(other_ratings.values('owner_id', 'recipe_id', 'score'))
        
        common_ratings = others_df[others_df['recipe_id'].isin(user_df['recipe_id'].tolist())]
                
        similarity_df = pearson_correlation_dataframe(user_df, common_ratings)
        
        top_similar_users = similarity_df.sort_values(by='similarity_index', ascending=False)
        top_similar_users_rating = top_similar_users.merge(others_df, left_on='owner_id', right_on='owner_id')
        top_similar_users_rating['weighted_rating'] = top_similar_users_rating['similarity_index']*top_similar_users_rating['score']
        top_similar_users_rating = top_similar_users_rating.groupby('recipe_id').sum()[['similarity_index','weighted_rating']]
        top_similar_users_rating.columns = ['sum_similarity_index', 'sum_weigthed_rating']
        recommendation_df = pd.DataFrame()
        recommendation_df['weighted average recommendation score'] = top_similar_users_rating['sum_weigthed_rating']/ \
                                                                    top_similar_users_rating['sum_similarity_index']
        recommendation_df['recipe_id'] = top_similar_users_rating.index
        recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', 
                                                          ascending=False)[:10]
        
        recommended_recipes_id = recommendation_df['recipe_id'].tolist()
        recommended_recipes = Recipe.objects.filter(id__in=recommended_recipes_id)

    else:
        recommended_recipes = Recipe.objects.order_by('?')[:10]
    
    return recommended_recipes


def home(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    else:
        recipes = get_suggested_recipes(request)
        recommended_recipes = recommender(request)
        
        context = {
            "recipes": recipes,
            "recommended_recipes": recommended_recipes,
        }
    return render(request, 'home.html', context)

