from django.db import models

# Create your models here.
class Recipe(models.Model):
  def __str__(self):
    return self.title
  title = models.TextField()
  directions = models.TextField()
  units = models.TextField()
  quantities = models.TextField()
  ingredients = models.TextField()

  
