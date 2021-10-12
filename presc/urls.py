from django.urls import path
from .views import *

urlpatterns = [
    path('', nlp, name='algo'),
    path('register/', register, name='register'),
    path('login/', login, name='login')
]
