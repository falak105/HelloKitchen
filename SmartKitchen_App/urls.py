from django.urls import path
from .views import  *
from django.contrib.auth import views as auth_views
from django.contrib import admin
from SmartKitchen_App import views


urlpatterns = [
    
    path('', home, name='index'),
    path('userlogin/ ',userlogin, name='userlogin'),
    path('userlogout/ ',userlogout, name='userlogout'),
    path('userreg/',userreg, name='userreg'),
    path('login/', auth_views.LoginView.as_view(template_name='userlogin.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('userdashboard/',userdashboard, name='user_dashboard'),
    path('admindashboard/',admindashboard, name='admindashboard'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('userlogin/',userlogin, name='login'),
    path('userreg/',userreg, name='reg'),
    path('menu/',menu, name='menu'),
    path('service/',service, name='service'),
    path('recipe/', Recipe, name='recipe'),
    path('dashboard/',dashboard, name='dashboard'),
    path('vassi/',vassi, name='voiceassistant'),
    path('health_analysis/',health_analysis, name='health_analysis'),
    path('health/', health_analysis_report, name='health_analysis_report'),
    path('admin/', admin.site.urls),
    path('query/', views.get_response, name='get_response'),  # Add this line

    # path('notifications/',notf, name='notf'),
    # path('profile/',profile,name='profile'),
]