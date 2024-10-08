from django.urls import path
from .views import  home,about,contact,userlogin,userreg,menu,service,team,testimonial,recipe_list,chatbox

urlpatterns = [
    
    path('', home, name='index'),
    path('userlogin/ ',userlogin, name='userlogin'),
    path('userreg/',userreg, name='userreg'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('menu/',menu, name='menu'),
    path('service/',service, name='service'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('chatbox/',chatbox, name='chatbox'),
]