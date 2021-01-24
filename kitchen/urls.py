
from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('add', views.add_products, name='add'),
    path('finished/<kitchen_id>', views.finished_products, name='finished'),
    path('change_amount/<product_id>', views.change_amount, name='change_amount'),    
    path('deletefinished', views.delete_finished, name='deletefinished'),
    path('deleteall', views.delete_all, name='deleteall'),
    path('autocomplete_kitchen', views.autocomplete_kitchen, name='autocomplete_kitchen'),
    
  ]
  