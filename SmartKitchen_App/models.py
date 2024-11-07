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

    Date = models.DateField()
    BreakFast = models.CharField(max_length=255)
    Lunch = models.CharField(max_length=255)
    Dinner = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Date
    
# class Response(models.Model):
#     question = models.CharField(max_length=255)
#     response = models.CharField(max_length=255)

#     def __str__(self):
#         return self.question
    
# class CustomUser(AbstractUser):
#     # Add unique related_names to avoid clashes with the auth.User model
#     groups = models.ManyToManyField(
#         Group,
#         related_name='customuser_set',  # Ensure the related name is unique
#         blank=True,
#         help_text="The groups this user belongs to.",
#         verbose_name="groups",
#     )
    
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='customuser_permissions_set',  # Ensure the related name is unique
#         blank=True,
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions",
#     )