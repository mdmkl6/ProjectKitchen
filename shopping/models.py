from django.db import models

# Create your models here.
class ToBuy(models.Model):
    text = models.CharField(max_length=40)
    

    def __str__(self):
        return self.text
