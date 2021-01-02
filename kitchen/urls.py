
from django.urls import path
from . import views

urlpatterns = [
   
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('add', views.addProducts, name='add'),
    path('finished/<kitchen_id>', views.finishedProducts, name='finished'),
    path('deletefinished', views.deleteFinished, name='deletefinished'),
    path('deleteall', views.deleteAll, name='deleteall'),
    path('autocomplete_kitchen', views.autocomplete_kitchen, name='autocomplete_kitchen')
  ]