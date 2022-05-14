from django.db import models

class SimpleModel(models.Model):
    name = models.CharField(max_length=200)
    occupation = models.TextField()


# Create your models here.
