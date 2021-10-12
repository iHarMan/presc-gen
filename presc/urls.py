from django.urls import path
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login')
]
