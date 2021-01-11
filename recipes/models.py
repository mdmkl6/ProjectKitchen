from django.db import models
from products.models import Product

# Create your models here.
class Recipe(models.Model):
  title = models.TextField()
  directions = models.TextField()
  def __str__(self):
    return self.title

class ProductInRecipe(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  quantity = models.TextField()
  unit = models.TextField(null=True)
  def __str__(self):
    return self.product.name
  
