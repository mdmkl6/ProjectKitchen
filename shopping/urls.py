from django.urls import path
from . import views


urlpatterns = [
   
    path('shopping/', views.shopping_view, name='shopping'),
    path('add_to_buy', views.addToBuy, name='add_to_buy'),
    path('done', views.done, name='done'),
    path('autocomplete_shopping_list', views.autocomplete_shopping_list, 
         name='autocomplete_shopping_list'),
]