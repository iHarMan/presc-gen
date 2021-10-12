from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.models import User
from nltk import word_tokenize
import pandas as pd

def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		type = request.POST.get('type')

		if User.objects.filter(username=username).exists():
			messages.error(request, 'The username already exists')
			return render(request, 'presc/register.html')

		if User.objects.filter(email=email).exists():
			messages.error(request, 'The email already exists')
			return render(request, 'presc/register.html')
		
		newUser = User.objects.create_user(username=username, email=email, password=password)
		profile = Profile(user=newUser, type=type)
		profile.save()
		newUser.save()
		messages.success(request, 'Your account has been created.')
		return redirect('login')
	else:
		return render(request,  'presc/register.html')

def login(request):
	return render(request, 'presc/login.html')

def nlp(request):
	if request.method == 'POST':
		sent = request.POST.get("sent")
		data1 = pd.read_csv("data.csv")
		a = word_tokenize(sent)
		print(data1.dtypes)
		print("GIVEN SENTENCE :: " , sent)
		datas = []
		for  i in data1["MedicineName"]:
			for  j in a:
					if(j.lower() == i.lower().split()[0]):
						a.remove(j)
						dt = data1.loc[data1["MedicineName"] == i, {"MedicineName","Uses","HowToUse","SideEffects","AlternateMedicines"}]
						Uses = list(dt["Uses"])[0]
						Name = i
						How = list(dt["HowToUse"])[0]
						SideEffects = list(dt["SideEffects"])[0]
						datas.append({
							'Name': Name,
							'Uses': Uses,
							'How': How,
							'Effects': SideEffects
						})
						print(datas)
		return render(request, 'presc/table.html', context={'datas': datas})
	else:
		return render(request, 'presc/index.html')


