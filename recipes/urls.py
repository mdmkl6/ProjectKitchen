
from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipes_view, name='recipes'),
    path('<int:id>/', views.single_recipe_view, name="recipe"), 
  ]
