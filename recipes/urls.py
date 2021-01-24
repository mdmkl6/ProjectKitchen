
from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipes_view, name='recipes'),
    path('<int:id>/', views.single_recipe_view, name="recipe"),
    path('<int:id>/rate/', views.user_rating_view, name="user_rating"), 
  ]
