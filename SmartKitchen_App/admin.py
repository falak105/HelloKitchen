from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Ingredient, Recipe, MealPlan

admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(MealPlan)
