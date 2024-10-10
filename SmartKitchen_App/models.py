from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cooking_level = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()

    def __str__(self):
        return self.name

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    meal_plan_id = models.AutoField(primary_key=True)
    date = models.DateField()
    recipes = models.ManyToManyField(Recipe)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Meal Plan for {self.user.name} on {self.date}"

class member(models.Model):
  Mname = models.CharField(max_length=255)
  date = models.DateField()
  weight = models.IntegerField()
  calories = models.IntegerField()


class Response(models.Model):
    question = models.CharField(max_length=255)
    response = models.CharField(max_length=255)

    def __str__(self):
        return self.question
