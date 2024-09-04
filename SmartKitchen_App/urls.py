from django.urls import path
from .views import  home,about,contact,booking,menu,service,team,testimonial

urlpatterns = [
    path('', home, name='index'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('booking/',booking, name='booking'),
    path('menu/',menu, name='menu'),
    path('service/',service, name='service'),
    path('team/',team, name= 'team'),
    path('testimonial/',testimonial, name= 'testimonial')
]