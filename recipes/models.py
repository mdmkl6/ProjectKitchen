from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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


class UserRating(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	score = models.IntegerField(default=0,
								validators=[MaxValueValidator(5),
											MinValueValidator(0),
											])
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.owner.username} rating {self.score} for {self.recipe.title}'

	
