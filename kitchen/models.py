from django.db import models

# Create your models here.
class Products(models.Model):
    text = models.CharField(max_length=40)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.text
