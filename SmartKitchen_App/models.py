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
    
class HealthAnalysis(models.Model):
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
    health_issue = models.CharField(max_length=50, choices=HEALTH_ISSUES)
    other_health_issue = models.CharField(max_length=255, blank=True, null=True)  # Optional field for "Other" selection

    def __str__(self):
        return f"Health Analysis - Weight: {self.weight}kg, Height: {self.height}cm"