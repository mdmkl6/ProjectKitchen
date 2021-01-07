from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    text = models.CharField(max_length=40)
    finished = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount =  models.CharField(max_length = 20, default = "0")
    
    def __str__(self):
        return self.text
