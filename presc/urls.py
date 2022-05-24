from django.urls import path
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('logout/', logout, name='logout'),
    path('home/<str:type>/<str:username>', home, name='home'),
    path('add_drug/<int:pk>', addDrug, name='addDrug'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('check_prescription/', check_prescription, name='check_prescription'),
    path('login/newprescription/',newprescription,name = 'newprescription'),
    path('home/p/profile/',profile,name = 'profile'),
    path('home/d/profile/',profile_d,name = 'profile_d'),
    path('home/d/patients/', lp, name='patients'),
    path('home/p/view_presc/', vp , name = 'view_all_presc'),
    path('profile/<str:username>/', generic_profile_view, name='generic-profile-view'),
    path('home/p/view_presc/your_presc/<int:pk>', yp , name = 'your_presc'),
    path('prescription_history/<str:username>', presc_his, name='presc-his'),

    # path('myprescriptions/', viewPrescription, name='viewPrescription')
]
