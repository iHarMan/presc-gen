from django.urls import path
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('logout/', logout, name='logout'),
    path('home/', home, name='home'),
    path('add_drug/<int:pk>', addDrug, name='addDrug'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('login/newprescription/',newprescription,name = 'newprescription'),
    path('login/profile/',profile,name = 'profile')
    # path('myprescriptions/', viewPrescription, name='viewPrescription')
]
