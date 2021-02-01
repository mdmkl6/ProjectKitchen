from django.urls import path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('shopping/', views.shopping_view, name='shopping'),
    path('add_to_buy', views.add_to_buy, name='add_to_buy'),
    path('done', views.done, name='done'),
    path('autocomplete_shopping_list', views.autocomplete_shopping_list, 
         name='autocomplete_shopping_list'),
]