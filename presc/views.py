from datetime import datetime
from datetime import date
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Prescription, Profile, Drugs
from django.contrib.auth.models import User
from nltk import word_tokenize
import pandas as pd

def landing(request):
	return render(request, "presc/index.html")

def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		type = str(request.POST.get('type'))

		if User.objects.filter(username=username).exists():
			messages.error(request, 'The username already exists')
			return render(request, 'presc/register.html')

		if User.objects.filter(email=email).exists():
			messages.error(request, 'The email already exists')
			return render(request, 'presc/register.html')
		
		newUser = User.objects.create_user(username=username, email=email, password=password)
		profile = Profile(user=newUser, username=username, email=email, type=type)
		newUser.save()
		profile.save()
		messages.success(request, 'Your account has been created.')
		return redirect('login')
	return render(request, 'presc/register.html')


def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		messages.error(request, 'Invalid credentials.')
		return redirect('login')
	return render(request, 'presc/login.html')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect('login')
	else:
		return redirect('login')

def home(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			prescriptions = Prescription.objects.filter(userId=request.user)
			datas = []
			for pres in prescriptions:
				datas.append({
					'pk':pres.pk,
					'name':pres.name
				})
			return render(request, 'presc/home.html', context={'datas':datas})
		else:
			return render(request, 'presc/home.html')
	else:
		return redirect('login')

def addDrug(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			sent = request.POST.get("sent")
			data1 = pd.read_csv("data.csv")
			print(sent)
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
							SideEffects = list(dt["SideEffects"])[0]
							try:
								prescription = Prescription.objects.get(pk=pk)
								drugs = Drugs.objects.create(prescription=prescription, name=str(Name), uses=str(Uses), sideEffects=str(SideEffects))
								drugs.save()
							except:
								s = str(date.today())
								temp = Prescription.objects.create(userId=request.user, name=s)
								drugs = Drugs.objects.create(prescription=temp, name=str(Name), uses=str(Uses), sideEffects=str(SideEffects))
								drugs.save()
								

			t = Prescription.objects.get(pk=pk)
			for drug in Drugs.objects.all().filter(prescription=t):
				print(drug)
				data = {}
				data['Name'] = drug.name
				data['Uses'] = drug.uses
				data['Effects'] = drug.sideEffects
				datas.append(data)

			return render(request, 'presc/table.html', context={'datas': datas})
		else:
			return render(request, 'presc/addDrug.html')
	else:
		return redirect('login')
	
