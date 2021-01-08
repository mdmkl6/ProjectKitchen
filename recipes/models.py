from django.db import models
import json


# Create your models here.
class Recipe(models.Model):
  title = models.TextField()
  directions = models.TextField()
  units = models.TextField()
  quantities = models.TextField()
  ingredients = models.TextField()
  
  def __str__(self):
    return self.title
  
  def get_dict(self):
    elements_list = []
    units = self.units.split(",")
    quantities = self.quantities.split(",")
    ingredients = self.ingredients.split(",")
    for i in range(19):
       if ingredients[i] != " ": 
        elements_list.append({"quantity": quantities[i], "unit": units[i], "ingredient": ingredients[i]})
    data_dict = {"id": self.id, "title": self.title, "directions": self.directions, "elements": elements_list}
    return data_dict


  
