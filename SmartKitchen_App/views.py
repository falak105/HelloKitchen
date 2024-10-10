from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import Response
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def dashboard(request):
    return render(request, 'user/index.html')


def userlogin(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(home)
        if user is None:
            msg = "Please check the credentials carefully!"
            return redirect('index')
    return render(request,"userlogin.html")

def userreg(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username is provided
        if not username:
            msg = "Username cannot be empty."
            return render(request, 'userreg.html', {'msg': msg})
        if not User.objects.filter(username=username).exists():
            # Create the user with all required fields, including the password
            user = User.objects.create(username=username, email=email)
            user.set_password(password)  # Hash the password before saving the user
            user.save()
            return render(request, 'userlogin.html')
        else: 
            msg = "Username already exists. Try again!"
            return render(request, 'userreg.html', {'msg': msg})

    return render(request, "userreg.html")

def userlogout(request):
    logout(request)
    return redirect('userlogin')

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
def vassi(request):
    return render(request,'voiceassistant.html')
# def dashboard(request):
#     return render(request, 'user/index.html')
# def notf(request):
#     return render(request, 'user/notifications.html')
# def profile(request):
#     return render(request, 'user/user.html')

# handle to speech queries
@csrf_exempt  # Temporarily disable CSRF for simplicity
def get_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            speech_text = data.get('speech', '')

            # Query the database to find a matching question
            response = Response.objects.filter(question__icontains=speech_text).first()

            if response:
                return JsonResponse({'response': response.response})
            else:
                return JsonResponse({'response': "Sorry, I don't have an answer for that."})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)