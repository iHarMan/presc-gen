from django.contrib import admin

from .models import Profile, Drugs, Prescription
# Register your models here.

admin.site.register(Profile)
admin.site.register(Drugs)
admin.site.register(Prescription)