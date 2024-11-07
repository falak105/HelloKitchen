from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

admin.site.register(recipe)
admin.site.register(healthAnalysis)
admin.site.register(MealPlan)



# class CustomUserAdmin(UserAdmin):
#     # Fields to display in the admin list view
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
#     # Add a search bar to search users by username, email, etc.
#     search_fields = ('username', 'email', 'first_name', 'last_name')

#     # Sections for the user edit form
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )

# # Unregister the default UserAdmin and register the custom one
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)