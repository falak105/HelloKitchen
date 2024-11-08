from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, Group, Permission

class recipe(models.Model):
    r_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    ingridents = models.CharField(max_length=255)
    instructions = models.CharField(max_length=255)
    prep_time = models.IntegerField()
    cooking_time = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.r_name
    
class RecipeView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} viewed {self.recipe.r_name} on {self.viewed_at}"
    
class healthAnalysis(models.Model):
    HEALTH_ISSUES = [
        ('Diabetes', 'Diabetes'),
        ('Hypertension', 'Hypertension'),
        ('Obesity', 'Obesity'),
        ('High Cholesterol', 'High Cholesterol'),
        ('Sugar', 'High Sugar'),
        ('Other', 'Other'),
    ]

    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Weight in kg
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Height in cm
    level = models.IntegerField(null=False, default=0)
    health_issue = models.CharField(max_length=50, choices=HEALTH_ISSUES)
    
    other_health_issue = models.CharField(max_length=255, blank=True, null=True)  # Optional field for "Other" selection

    def __str__(self):
        return f"Health Analysis - Weight: {self.weight}kg, Height: {self.height}cm"
    
class MealPlan(models.Model):
    Meal_Plan=[
        ('Date','Dates'),
        ('BreakFast','BreakFast'),
        ('Lunch'),('Lunch'),
        ('Dinner'),('Dinner'),
    
    ]

    
    Dish = models.CharField(max_length=255)
    Set_your_reminder =[
        ('Before 1hr of food','Before 1hr of food'),
        ('Before 45 mins of food','Before 45 mins of food'),
        ('Before 30 mins of food','Before 30 mins of food'),
        ('Before 15 mins of food','Before 15 mins of food'),
        ('Before 5 mins of food','Before 5 mins of food')
    ]

    def __str__(self):
        return self.Date
    

