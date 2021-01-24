from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class ToBuy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.TextField(default=0)
    unit = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  
    def __str__(self):
        return self.product.name
