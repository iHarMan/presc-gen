from datetime import datetime,timedelta,date
from datetime import date
from dbm import dumb
import email
import re
import string
import random
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Prescription, Profile, Drugs
from django.contrib.auth.models import User
from nltk import word_tokenize
import pandas as pd

dic = {}
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
def yp(request):
	#patients prescription
	Prescription = {
	'patients_name':dic['username'],
	'med':'crocine',
	'dosage':2
	}
	return render(request , 'presc/yp.html',{'p':Prescription})

def vp(request):
	# drug_date = Drugs.objects.get(date = date).filter(user = dic['username'])
	# return render(request, "presc/vp.html",{d : drug_date});
	a=[date.today(), date.today() + timedelta(days=1), date.today() - timedelta(days=1)]
	a.sort(reverse=True)
	return render(request,"presc/vp.html",{'pres':a})

def landing(request):
	return render(request, "presc/index.html")
	
def profile(request):
	dic_temp = {};
	dic_temp['username'] = dic['username']
	dic_temp['type'] = dic['type']
	dic_temp['email'] = dic['email']
	return render(request,'presc/profile.html' , dic_temp);

def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		global dic;
		dic['email'] = email
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
		global dic
		dic['username'] = request.POST.get('username')
		dic['type'] = request.POST.get('type')

		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username)
		if re.fullmatch(EMAIL_REGEX, username):
			user = User.objects.get(email=username)
			username = user.username
			dic['username'] = username
			print(username)

			# except:
			# 	messages.error(request, "Invalid Credentials")
			# 	return redirect('login')

		user = auth.authenticate(request, username=username, password=password)
		print(username)
		if user is not None:
			auth.login(request, user)
			return redirect(home, type=dic['type'], username=dic['username'])
			# return render(request,'presc/home.html', dic)
		messages.error(request, 'Invalid credentials.')
		return redirect('login')
	return render(request, 'presc/login.html')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect('login')
	else:
		return redirect('login')

def check_prescription(request):
	email = request.POST.get('email')
	try:
		user = User.objects.get(email=email)
		profile = Profile.objects.get(user=user)
		s = str(date.today())
		presc = Prescription.objects.create(userId=user, name=s)
		return redirect('/add_drug/'+str(presc.pk))
	except User.DoesNotExist:
		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
		dummyPass = "Pass123@@"
		user = User.objects.create(email=email, username=res, password=dummyPass)
		user.set_password(dummyPass)
		user.save()
		profile = Profile.objects.create(user=user, type='p', username=user.username, email=user.email)
		s = str(date.today())
		presc = Prescription.objects.create(userId=user, name=s)
		return redirect('/add_drug/'+str(presc.pk))


def home(request, type=None, username=None):
	if request.user.is_authenticated:
		if request.method == 'GET':
			prescriptions = Prescription.objects.filter(userId=request.user)
			datas = []
			for pres in prescriptions:
				print(pres.pk)
				datas.append({
					'pk':pres.pk,
					'name':pres.name
				})
			return render(request, 'presc/home.html', context={'datas':datas, 'type':type, 'username':username})
		else:
			return render(request, 'presc/home.html')
	else:
		return redirect('login')

def newprescription(request):
	#adding new prescription
	#1.check for exsisting Patients
	#2.redirect to voice wala
	return HttpResponse("helloo")

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
				# print(drug)
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
