from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from .models import Patient, Doctor
from nltk import word_tokenize
import pandas as pd


	

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

def register(request):
	if request.method == 'GET':
		return render(request, 'presc/register.html')
	else:
		return render(request, 'presc/index.html')
