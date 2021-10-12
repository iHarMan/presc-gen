from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	userID = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=200, default="")
	email = models.TextField(default="")
	type = models.CharField(max_length=1, choices=(('p', 'Patient'), ('d', 'Doctor')))
	def __str__(self):
		return str(self.userID.username) + str(self.pk)
