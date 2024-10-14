from django.contrib import admin

from .models import *

admin.site.register(Recipe)
admin.site.register(HealthAnalysis)
admin.site.register(MealPlan)
admin.site.register(Response)

