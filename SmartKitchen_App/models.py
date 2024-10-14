from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    r_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    ingridents = models.CharField(max_length=255)
    instructions = models.CharField(max_length=255)
    prep_time = models.IntegerField()
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.r_name
