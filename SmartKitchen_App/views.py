from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import*
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
    
def health_analysis(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        health_issue = request.POST.get('health_issues')
        other_health_issue = request.POST.get('other_health_issue') if health_issue == 'Other' else None

        # Save data to the database
        HealthAnalysis.objects.create(
            weight=weight,
            height=height,
            health_issue=health_issue,
            other_health_issue=other_health_issue
        )
        # Redirect to the index page or a success message
        return redirect('user_dashboard')  # Assuming 'index' is the URL name for the home page
    

from django.shortcuts import render
from django.http import HttpResponse

def health_analysis_report(request):
    # Get the latest health analysis data for the user
    health_analysis = HealthAnalysis.objects.filter().last()

    # Check if health_analysis is None
    if health_analysis is None:
        # Return an appropriate response if no health data is found
        return HttpResponse("No health data available for analysis.")

    # Calculate BMI (Body Mass Index) = weight (kg) / (height (m))^2
    height_in_meters = health_analysis.height / 100
    bmi = health_analysis.weight / (height_in_meters ** 2)
    bmi_status = "Underweight" if bmi < 18.5 else "Normal weight" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"

    # Basic recommendations based on health issue
    recommendations = {
        'Diabetes': {
            'food': ['Leafy Greens', 'Whole Grains', 'Fish', 'Nuts'],
            'avoid': ['Sugary Drinks', 'White Bread', 'Processed Foods'],
            'tips': 'Monitor blood sugar levels regularly and maintain a balanced diet.',
        },
        'Hypertension': {
            'food': ['Bananas', 'Leafy Greens', 'Oatmeal', 'Garlic'],
            'avoid': ['Salt', 'Alcohol', 'Caffeine'],
            'tips': 'Regular exercise and reducing sodium intake can help manage blood pressure.',
        },
        'Obesity': {
            'food': ['Lean Proteins', 'Vegetables', 'Fruits', 'Whole Grains'],
            'avoid': ['Sugary Snacks', 'Fast Food', 'Soda'],
            'tips': 'Incorporate regular physical activity and avoid calorie-dense foods.',
        },
        'High Cholesterol': {
            'food': ['Oats', 'Barley', 'Nuts', 'Fatty Fish'],
            'avoid': ['Red Meat', 'Full-fat Dairy', 'Fried Foods'],
            'tips': 'Include soluble fiber in the diet and exercise regularly to improve cholesterol levels.',
        },
        'Sugar': {
            'food': ['Whole Grains', 'Nuts', 'Legumes', 'Non-Starchy Veggies'],
            'avoid': ['Refined Sugar', 'White Flour', 'Fruit Juice'],
            'tips': 'Limit intake of added sugars and focus on low glycemic index foods.',
        },
    }

    # Collect recommendations for all health issues
    all_recommendations = []
    for issue, rec in recommendations.items():
        rec['issue'] = issue
        all_recommendations.append(rec)

    # Prepare data for the graph
    total_food_recommended = sum([len(rec.get('food', [])) for rec in all_recommendations])
    total_food_to_avoid = sum([len(rec.get('avoid', [])) for rec in all_recommendations])

    # Render the health report
    return render(request, 'health.html', {
        'health_analysis': health_analysis,
        'bmi': round(bmi, 2),  # Round BMI to two decimal places for better readability
        'bmi_status': bmi_status,
        'recommendations': all_recommendations,
        'total_food_recommended': total_food_recommended,
        'total_food_to_avoid': total_food_to_avoid,
    })


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