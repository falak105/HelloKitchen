from .models import healthAnalysis  # Ensure correct model import
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
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
from SmartKitchen_App.models import *
from django.db.models import Count, Avg


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

        # Check if the user exists
        user_exists = User.objects.filter(username=username).exists()
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            # Redirect based on user type
            return redirect('admindashboard' if user.is_superuser else 'index')

        else:
            if not user_exists:
                msg = "User does not exist. Please register first."
            else:
                msg = "Incorrect password. Please try again."

            return render(request, 'userlogin.html', {'msg': msg})

    return render(request, "userlogin.html")


def userreg(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if username is provided
        if not username:
            msg = "Username cannot be empty."
            return render(request, 'userreg.html', {'msg': msg})

        # Check if passwords match
        if password != confirm_password:
            msg = "Passwords do not match. Please try again."
            return render(request, 'userreg.html', {'msg': msg})

        # Check if the username already exists
        if not User.objects.filter(username=username).exists():
            # Create the user with the hashed password
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            return redirect('login')  # Redirects to the login URL name
        else:
            msg = "Username already exists. Try again!"
            return render(request, 'userreg.html', {'msg': msg})

    return render(request, "userreg.html")


def userlogout(request):
    logout(request)
    return redirect('userlogin')


# def admindashboard(request):
#     # Count total recipes
#     total_recipes = recipe.objects.count()  # Correct model reference

#     # Count active users
#     active_users = User.objects.filter(is_active=True).count()

#     # Count new recipes this week
#     start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
#     new_recipes_this_week = recipe.objects.filter(
#         created_at__gte=start_of_week).count()  # Correct model reference

#     # Prepare context for rendering
#     context = {
#         'total_recipes': total_recipes,
#         'active_users': active_users,
#         'new_recipes_this_week': new_recipes_this_week,
#     }

#     # Only one return statement needed
#     return render(request, 'admin/admindashboard.html', context)


def admindashboard(request):
    # Total number of recipes
    total_recipes = recipe.objects.count()

    # Number of active users
    active_users = User.objects.filter(is_active=True).count()

    # New recipes added this week
    start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
    new_recipes_this_week = recipe.objects.filter(created_at__gte=start_of_week).count()

    # Average number of recipes per user
    if active_users > 0:
        avg_recipes_per_user = total_recipes / active_users
    else:
        avg_recipes_per_user = 0

    # Most popular recipe based on count
    most_popular_recipe = recipe.objects.values('r_name').annotate(count=Count('id')).order_by('-count').first()
    most_popular_recipe_name = most_popular_recipe['r_name'] if most_popular_recipe else 'N/A'

    # Recipe count by category
    category_data = recipe.objects.values('category').annotate(count=Count('id')).order_by('-count')

    # New recipes added in each of the last 4 weeks
    last_4_weeks = []
    for i in range(4):
        start_date = timezone.now() - timedelta(weeks=i+1)
        end_date = timezone.now() - timedelta(weeks=i)
        week_recipes = recipe.objects.filter(created_at__range=[start_date, end_date]).count()
        last_4_weeks.append(week_recipes)

    context = {
        'total_recipes': total_recipes,
        'active_users': active_users,
        'new_recipes_this_week': new_recipes_this_week,
        'avg_recipes_per_user': round(avg_recipes_per_user, 2),
        'most_popular_recipe': most_popular_recipe_name,
        'category_data': category_data,
        'last_4_weeks': last_4_weeks,
    }

    return render(request, 'admin/admindashboard.html', context)


def view_recipe(request, recipe_id):
    recipe = recipe.objects.get(id=recipe_id)

    # Log the recipe view
    if request.user.is_authenticated:
        RecipeView.objects.create(
            user=request.user, recipe=recipe, viewed_at=timezone.now())

    # Render recipe detail page (replace 'recipe_detail.html' with your template)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def userdashboard(request):
    user = request.user  # Get the currently logged-in user

    # Count total recipes saved by the user
    total_recipes = recipe.objects.all().count()

    # Count planned meals by the user
    planned_meals = MealPlan.objects.all().count()
    # MealPlan.objects.filter(user=user).count()
    # Fetch the most recent 5 recipes viewed by the user
    # Fetch the most recent 5 recipes viewed by the user
    recent_recipe_views = RecipeView.objects.filter(user=user).order_by('-viewed_at')[:5]
    recent_recipes = [view.recipe for view in recent_recipe_views]  # Get the recipe from the views
    print(recent_recipe_views)

    # Count shopping list items by the user
    # shopping_list_items = ShoppingList.objects.filter(user=user).count()

    context = {
        'total_recipes': total_recipes,
        'planned_meals': planned_meals,
        'recent_recipes': recent_recipes,
        # 'shopping_list_items': shopping_list_items,
        'recent_recipe_views': recent_recipe_views,
    }

    return render(request, 'user_dashboard.html', context)

    # If GET request, render meal plan form
    # Ensure you have a template for this
    return render(request, 'service.html')


def menu(request):
    recipes = recipe.objects.all()

    if request.method == 'POST':
        # Get the recipe ID from the form data
        recipe_id = request.POST.get('recipe_id')
        if recipe_id:
            try:
                # Get the selected recipe by its ID
                selected_recipe = recipe.objects.get(id=recipe_id)

                # Store the selected recipe ID in the session
                request.session['last_recipe'] = selected_recipe.id
                # Optional: Store the last used recipe in the user's profile or perform other actions

                # Add a success message to inform the user
                messages.success(
                    request, f'{selected_recipe.r_name} has been saved as your last recipe!')
            except recipe.DoesNotExist:
                # Add an error message if the recipe ID does not exist
                messages.error(request, 'Recipe not found!')

    # Render the page with recipes and any messages
    return render(request, 'menu.html', {'recipes': recipes})


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
            messages.error(
                request, 'All fields are required. Please fill in all fields.')

    # Render the recipe creation form
    return render(request, 'admin/recipe.html')

def view_recipe(request, recipe_id):
    recipe = recipe.objects.get(id=recipe_id)
    
    # Log the recipe view by the current user
    RecipeView.objects.create(user=request.user, recipe=recipe)
    
    # Your code to display the recipe
    context = {
        'recipe': recipe
    }
    
    return render(request, 'recipe_detail.html', context)

def health_analysis(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        level = request.POST.get('level')
        health_issue = request.POST.get('health_issues')
        other_health_issue = request.POST.get(
            'other_health_issue') if health_issue == 'Other' else None

        # Ensure all required fields are provided
        if weight and height and level and health_issue:
            # Save data to the database
            healthAnalysis.objects.create(
                weight=weight,
                height=height,
                level=level,
                health_issue=health_issue,
                other_health_issue=other_health_issue
            )

            # Redirect to the health analysis report after saving
            return redirect('health_analysis_report')
        else:
            # If any fields are missing, return to form with an error
            return render(request, 'index.html', {'error': 'Please fill out all required fields.'})

    # Render the form page for GET request
    return render(request, 'index.html')


def health_analysis_report(request):
    # Get the latest health analysis data for the user
    health_analysis = healthAnalysis.objects.filter().last()

    if health_analysis is None:
        # Return an appropriate response if no health data is found
        return HttpResponse("No health data available for analysis.")

    # Calculate BMI (Body Mass Index)
    height_in_meters = health_analysis.height / 100
    bmi = health_analysis.weight / (height_in_meters ** 2)
    bmi_status = (
        "Underweight" if bmi < 18.5 else
        "Normal weight" if bmi < 25 else
        "Overweight" if bmi < 30 else
        "Obese"
    )

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

    # Collect recommendations for each health issue
    all_recommendations = []
    for issue, rec in recommendations.items():
        rec['issue'] = issue
        all_recommendations.append(rec)

    # Prepare data for the graph
    total_food_recommended = sum(len(rec.get('food', []))
                                 for rec in all_recommendations)
    total_food_to_avoid = sum(len(rec.get('avoid', []))
                              for rec in all_recommendations)

    # Render the health report
    return render(request, 'health.html', {
        'health_analysis': health_analysis,
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
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            speech_text = body_data.get('speech', '').strip().lower()
            print(f"User input: {speech_text}")

            # Attempt to find recipes containing the provided name
            matching_recipes = recipe.objects.filter(
                r_name__icontains=speech_text)
            print(f"Matching recipes count: {matching_recipes.count()}")

            if matching_recipes.exists():
                recipe_instance = matching_recipes.first()
                print(f"Found recipe: {recipe_instance.r_name}")
                response_text = {
                    'name': recipe_instance.r_name,
                    'category': recipe_instance.category,
                    'ingredients': recipe_instance.ingridents,
                    'instructions': recipe_instance.instructions,
                    'prep_time': recipe_instance.prep_time,
                    'cooking_time': recipe_instance.cooking_time,
                }
                print(response_text)
            else:
                response_text = "Sorry, I couldn't find a recipe with that name."
                print("No matching recipes found.")

            return JsonResponse({'response': response_text})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def usermanagement(request):
    users = User.objects.all()  # Fetch all users (or filter as needed)
    return render(request, 'admin/usermanagement.html', {'users': users})

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


def MealPlans(request):
    if request.method == 'POST':
        BreakFast = request.POST.get('Breakfast')
        Lunch = request.POST.get('Lunch')
        Dinner = request.POST.get('Dinner')
        Date = request.POST.get(
            'Date') if MealPlan == 'Other' else None

        MealPlan.objects.create(
            Breakfast=BreakFast,  # Use lowercase breakfast
            Lunch=Lunch,
            Dinner=Dinner,
            Date=Date
        )

        # Redirect to the index page or a success message
        # Assuming 'index' is the URL name for the home page
        return redirect('user_dashboard')
