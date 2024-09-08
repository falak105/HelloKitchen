from django.shortcuts import render
from .models import Recipe
# Create your views here.
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def userreg(request):
    return render(request,'userreg.html')
def userlogin(request):
    return render(request,'userlogin.html')
def menu(request):
    return render(request, 'menu.html')
def service(request):
    return render(request, 'service.html')
def team(request):
    return render(request, 'team.html')
def testimonial(request):
    return render(request, 'testimonial.html')
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'kitchen_assistant/recipe_list.html', {'recipes': recipes})


