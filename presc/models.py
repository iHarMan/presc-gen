from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user.username)
	
class Patient(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	doctor = models.ManyToManyField(Doctor, null=True, blank=True)

	def __str__(self) -> str:
		return str(self.user.username)

# yeh hai sab din ka collection
class Prescription(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.TextField(default="")

# yeh hai ek din ka prescription
class Drugs(models.Model):
	name = models.TextField(default="", max_length=1024)
	uses = models.TextField(default="")
	sideEffects = models.TextField(default="")
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
	
