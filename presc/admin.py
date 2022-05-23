from django.contrib import admin

from .models import Drugs, Prescription, Doctor, Patient
# Register your models here.

admin.site.register(Drugs)
admin.site.register(Prescription)
admin.site.register(Doctor)
admin.site.register(Patient)