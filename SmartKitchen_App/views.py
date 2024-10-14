from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


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
            # Check if the user is a super admin (superuser)
            if user.is_superuser:
                # Redirect to super admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('index')  # Redirect to user home
        else:
            msg = "Please check the credentials carefully!"
            return render(request, 'userlogin.html', {'msg': msg})

    return render(request, "userlogin.html")


def userreg(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username is provided
        if not username:
            msg = "Username cannot be empty."
            return render(request, 'userreg.html', {'msg': msg})

        # Check if the username already exists
        if not User.objects.filter(username=username).exists():
            # Create the user with all required fields, including the password
            user = User.objects.create(username=username, email=email)
            # Hash the password before saving the user
            user.set_password(password)
            user.save()
            return render(request, 'userlogin.html')
        else:
            msg = "Username already exists. Try again!"
            return render(request, 'userreg.html', {'msg': msg})

    return render(request, "userreg.html")


def userlogout(request):
    logout(request)
    return redirect('userlogin')


def userdashboard(request):
    return render(request, 'user_dashboard.html')


def adminashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def menu(request):
    return render(request, 'menu.html')


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def create_recipe(request):
    if request.method == 'POST':
        recipe_name = request.POST.get('name')
        recipe_category = request.POST.get('category')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')

         # Validate if all required fields are present
        if recipe_name and recipe_category and ingredients and instructions and prep_time and cook_time:
            try:
                # Save data to the Recipe model
                add_recipe = Recipe.objects.create(
                    r_name=recipe_name,
                    category=recipe_category,
                    ingridents=ingredients,  # Ensure spelling is consistent
                    instructions=instructions,
                    prep_time=int(prep_time),  # Convert to integer
                    cooking_time=int(cook_time)
                )
                add_recipe.save()

                # Redirect to a success page after saving
                return redirect('recipe')

            except Exception as e:
                # Return an error response if something goes wrong
                return JsonResponse({'error': str(e)}, status=500)

        else:
            # If any field is missing, return an error message
            return JsonResponse({'error': 'All fields are required.'}, status=400)

    # Get the total count of recipes
    total_recipes = Recipe.objects.count()

    # Handle GET requests and display the form
    return render(request, 'admin/recipe.html', {'total_recipes': total_recipes})
    

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