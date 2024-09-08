from django.urls import path
from .views import  home,about,contact,userlogin,userreg,menu,service,team,testimonial,recipe_list

urlpatterns = [
    path('', home, name='index'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('userlogin/',userlogin, name='userlogin'),
    path('userreg/',userreg, name='userreg'),
    path('menu/',menu, name='menu'),
    path('service/',service, name='service'),
    path('recipes/', recipe_list, name='recipe_list'),
]