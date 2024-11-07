from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from google.cloud import translate_v2 as translate 


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
                return redirect('admindashboard')
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


def admindashboard(request):
    # Count total recipes
    total_recipes = recipe.objects.count()  # Correct model reference

    # Count active users
    active_users = User.objects.filter(is_active=True).count()

    # Count new recipes this week
    start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
    new_recipes_this_week = recipe.objects.filter(
        created_at__gte=start_of_week).count()  # Correct model reference

    # Prepare context for rendering
    context = {
        'total_recipes': total_recipes,
        'active_users': active_users,
        'new_recipes_this_week': new_recipes_this_week,
    }

    # Only one return statement needed
    return render(request, 'admin/admindashboard.html', context)


def userdashboard(request):
    user = request.user  # Get the currently logged-in user

    # Count total recipes saved by the user
    total_recipes = recipe.objects.count()

    # Count planned meals by the user
    planned_meals = MealPlan.objects.count()

    # Count shopping list items by the user
    # shopping_list_items = ShoppingList.objects.filter(user=user).count()

    context = {
        'total_recipes': total_recipes,
        'planned_meals': planned_meals,
        # 'shopping_list_items': shopping_list_items,
    }

    return render(request, 'user_dashboard.html', context)


def menu(request):
    recipes=recipe.objects.all()
    return render(request, 'menu.html',{'recipes': recipes})


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def create_recipe(request):  # Keep your function name as is
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
                new_recipe = recipe.objects.create(  # Correctly reference the Recipe model
                    r_name=recipe_name,
                    category=recipe_category,
                    ingridents=ingredients,
                    instructions=instructions,
                    prep_time=int(prep_time),
                    cooking_time=int(cook_time)
                )
                messages.success(request, 'Recipe created successfully!')
                return redirect('recipe_list')  # Adjust this as needed
            except Exception as e:
                messages.error(request, f'Error saving recipe: {str(e)}')
        else:
            messages.error(request, 'All fields are required. Please fill in all fields.')

    # Render the recipe creation form
    return render(request, 'admin/recipe.html')


def health_analysis(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        health_issue = request.POST.get('health_issues')
        other_health_issue = request.POST.get(
            'other_health_issue') if health_issue == 'Other' else None

        # Save data to the database
        HealthAnalysis.objects.create(
            weight=weight,
            height=height,
            health_issue=health_issue,
            other_health_issue=other_health_issue
        )
        # Redirect to the index page or a success message
        # Assuming 'index' is the URL name for the home page
        return redirect('user_dashboard')


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
    total_food_recommended = sum(
        [len(rec.get('food', [])) for rec in all_recommendations])
    total_food_to_avoid = sum([len(rec.get('avoid', []))
                              for rec in all_recommendations])

    # Render the health report
    return render(request, 'health.html', {
        'health_analysis': health_analysis,
        # Round BMI to two decimal places for better readability
        'bmi': round(bmi, 2),
        'bmi_status': bmi_status,
        'recommendations': all_recommendations,
        'total_food_recommended': total_food_recommended,
        'total_food_to_avoid': total_food_to_avoid,
    })


def vassi(request):
    return render(request, 'voiceassistant.html')
# def dashboard(request):
#     return render(request, 'user/index.html')
# def notf(request):
#     return render(request, 'user/notifications.html')
# def profile(request):
#     return render(request, 'user/user.html')

# handle to speech queries


# @csrf_exempt
# def query(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body_data = json.loads(body_unicode)
#         speech_text = body_data.get('speech', '')

#         # Basic dataset response
#         dataset = {
#             "hello": "Hi there! How can I help you today?",
#             "weather": "The weather is sunny and warm today.",
#             "your name": "I am your personal voice assistant.",
#             "time": "I am not sure about the exact time, but you can always check your watch.",
#             "breakfast": "paalappam with creamy nutfinished duck curry",
#             "lunch": "hot rice with chicken currry and meen curry with aviyal and yellow moru with some hot sambar combo also haing some payar curry and achar!!",
#             "dinner": "take some morinja hot porotta and take some piece of pork or beaf curry and have it like yum yum!!",
#             "duck": "cut the duck into small pieces and maranite with the appropriate masala you like and wait for hrs to settle the maranite into the duck, later take it into hot boiling oil and put some onions and tomatos into it, then put some water and wait.. it will be cooked! later take out the curry from beaker and have it yummy yummy!",
#             "എടാ": "enthada kuttah..!!",
#             "കോഴിക്കറി": "ചിക്കൻ ചെറിയ കഷണങ്ങളായി മുറിച്ച് മസാലപ്പൊടി ഉപയോഗിച്ച് മാരിനേറ്റ് ചെയ്ത് 1 മണിക്കൂർ കാത്തിരിക്കുക, എന്നിട്ട് തിളപ്പിച്ച എണ്ണയിൽ ചട്ടിയിൽ ഇട്ടു 7-8 മിനിറ്റ് ഫ്രൈ ചെയ്യുക",
#             "मुर्गी करी": "चिकन को छोटे-छोटे टुकड़ों में काट लें, मसाला पाउडर के साथ मैरीनेट करें और 1 घंटे तक इंतजार करें, फिर इसे उबलते तेल में एक पैन में डालें और 7-8 मिनट तक भूनें।",
#         }

#         response_text = dataset.get(speech_text.lower(), "Sorry, I didn't understand that.")

#         return JsonResponse({'response': response_text})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def query(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        speech_text = body_data.get('speech', '').strip().lower()
        print(f"User input: {speech_text}")

        # Attempt to find recipes containing the provided name in the speech_text
        matching_recipes = recipe.objects.filter(r_name__icontains=speech_text)
        print(f"Matching recipes: {matching_recipes}")
        
        if matching_recipes.exists():
            # Get the first matching recipe for simplicity (or modify to return multiple if needed)
            recipe_instance = matching_recipes.first()
            
            # Prepare the response with the recipe details
            response_text = {
                'name': recipe_instance.r_name,
                'category': recipe_instance.category,
                'ingredients': recipe_instance.ingridents,
                'instructions': recipe_instance.instructions,
                'prep_time': recipe_instance.prep_time,
                'cooking_time': recipe_instance.cooking_time,
            }
        else:
            # If no matching recipes are found, send a default message
            response_text = "Sorry, I couldn't find a recipe with that name."

        return JsonResponse({'response': response_text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def usermanagement(request):
    return render(request, 'usermanagement.html')

# Display all users


def user_list(request):
    users = User.objects.all()
    return render(request, 'usermanagement.html', {'users': users})

# Add a new user


def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'usermanagement.html', {'form': form})

# Edit an existing user


def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'usermanagement.html', {'form': form})

# Delete a user


def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'usermanagement.html', {'user': user})

def MealPlan(request):
    if request.method == 'POST':
        BreakFast = request.POST.get('Breakfast')
        Lunch = request.POST.get('Lunch')
        Dinner = request.POST.get('Dinner')
        Date = request.POST.get(
            'Date') if MealPlan == 'Other' else None

        # Save data to the database
        MealPlan.objects.create(
            BreakFast=BreakFast,
            Lunch=Lunch,
            Dinner=Dinner,
            Date=Date
        )
        # Redirect to the index page or a success message
        # Assuming 'index' is the URL name for the home page
        return redirect('user_dashboard')