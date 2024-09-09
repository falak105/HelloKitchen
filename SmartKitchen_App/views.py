from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def userreg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'userreg.html', {'form': form})

def userlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
    else:
        form = UserLoginForm()
    return render(request, 'userlogin.html', {'form': form})

# Logout View

##@login_required
###logout(request)
    #return redirect('user_login')
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

