from email.policy import default
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=200, default="")
	email = models.TextField(default="")
	type = models.CharField(max_length=1, choices=(('p', 'Patient'), ('d', 'Doctor')))
	def __str__(self):
		return str(self.user.username) + "'s profile"

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


