from django.urls import path
from .views import  home,about,contact,userlogin,userreg,menu,service,team,testimonial,recipe_list,dashboard,userlogout,vassi
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', home, name='index'),
    path('userlogin/ ',userlogin, name='userlogin'),
    path('userlogout/ ',userlogout, name='userlogout'),
    path('userreg/',userreg, name='userreg'),
    path('login/', auth_views.LoginView.as_view(template_name='userlogin.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('userlogin/',userlogin, name='login'),
    path('userreg/',userreg, name='reg'),
    path('menu/',menu, name='menu'),
    path('service/',service, name='service'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('dashboard/',dashboard, name='dashboard'),
    path('vassi/',vassi, name='voiceassistant'),
    # path('notifications/',notf, name='notf'),
    # path('profile/',profile,name='profile'),
]