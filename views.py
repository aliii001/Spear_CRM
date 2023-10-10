from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import Group
from itsdangerous import exc
from formation.decorators import allowed_users, unauthenticated_user
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import date, datetime    
from django.db.models import Count,Sum
from .models import Suivi,Ventervmutellevente
from django.core.paginator import Paginator
from django.db.models import F
import decimal as d
import folium
import joblib
import geocoder
import pandas as pd
import csv
import numpy as np
from pyexcel_xlsx import get_data
from .functions import total_charges
from django.contrib.auth import get_user_model

# Create your views here.

@login_required(login_url='login')
def home(request):
	loggedinuser = request.user
	admin_id= Account.objects.get(user=loggedinuser).user_admin
	###############  BLOCK Calcul GAIN USERS  ###############################
	User = get_user_model()
	# users = User.objects.all()
	users=User.objects.filter(account__user_admin=admin_id)
	group = request.user.groups.all()[0].name
	totalgainsdeusers = 0
	gainopco=0
	gainmutuelle=0
	gainvoyance=0
	gainmutuellevente=0
	gainenergie=0
	for i in users:
		# print(vars(i))
		group = i.groups.all()[0].name
		a=Account.objects.get(user=i).user_benefice
		if a==None:
			a=0
		if group=='OPCO':
			gainopco+=a
		if group=='energie':
			a=0.75*a
			gainenergie+=a
		if group=='mutuelle':
			gainmutuelle+=a
		if group=='mutuelle_vente':
			gainmutuellevente+=a
		if group=='voyance':
			a=0.75*a
			gainvoyance+=a
		totalgainsdeusers+=a


	###############  ENDBLOCK Calcul GAIN USERS  ############################



	###############  BLOCK Calcul depences  ###############################
	totalcharges,total_Chargeimprevisionelle,total_Chargevariable,total_Chargefixe=total_charges(admin_id)
	print('CHARGES RH',totalcharges)
	gainecommerce=Categorieecommerce.objects.filter(user_admin=admin_id).aggregate(benefices=Sum('benefices')) 
	if gainecommerce['benefices']== None:
		gainecommerce['benefices']=0
	print('////////////////////',gainecommerce)
	depencesecommerce=Categorieecommerce.objects.filter(user_admin=admin_id).aggregate(depences=Sum('depences')) 
	if depencesecommerce['depences']== None:
		depencesecommerce['depences']=0
	###############  ENDBLOCK Calcul depences  ############################


	total_gains=Bilan.objects.filter(user_admin=admin_id).aggregate(count=Sum('prix_formation'))
	prix_formation_admin=Bilan.objects.filter(user_admin=admin_id).values('username').annotate(prix=F('prix_formation')*0.2)
	total_admin=prix_formation_admin.aggregate(count=Sum('prix'))
	try:
		total_admin['count']=round(total_admin['count'],2)
		prix_formation_admin=Bilan.objects.filter(user_admin=admin_id).values('username').annotate(prix=F('prix_formation')*0.2)
		total_gains=Bilan.objects.filter(user_admin=admin_id).aggregate(count=Sum('prix_formation'))
		
		total_admin=prix_formation_admin.aggregate(count=Sum('prix'))
	except:
		total_admin['count']=0
		total_gains['count']=0
		print("non 1")
	sec=Suivi.objects.filter(user_admin=admin_id).aggregate(sec_count=Sum('nbre_sec'))
	min=Suivi.objects.filter(user_admin=admin_id).aggregate(min_count=Sum('nbre_min'))
	
	try :
		a=(sec['sec_count'])>60
		diff=sec['sec_count']/60
		min['min_count']=min['min_count']+int(diff)
		sec['sec_count']=sec['sec_count']-int(diff)*60
		depences=(0.035*min['min_count'])+(sec['sec_count']*0.035/60)
		depences= round(depences,2)
		gain=int(total_admin['count'])
		#depences=1200
		pourcentage_depences=(depences/gain)*100
		pourcentage_depences=int(round(pourcentage_depences,0))
		gain_net= (round(gain-depences,2))
	
		pourcentage_gain_net= 100-pourcentage_depences
	except:
		depences=0
		pourcentage_depences=0
		gain_net=0
		pourcentage_gain_net=0

	total_users=Account.objects.filter(user_admin=admin_id).count()
	total_ventes=Bilan.objects.filter(user_admin=admin_id).count()
	
	totalsgainfinals=total_admin['count']+totalgainsdeusers
	print('aaaaaaaaaaaaaaaa',totalsgainfinals)

	#####user
	Suivis = Suivi.objects.filter(user_id=request.user.id,user_admin=admin_id)
	Bilan_user = Bilan.objects.filter(user_id=request.user.id,user_admin=admin_id)
	total_user_vente=Bilan_user.count()
	total_secondes=Suivis.aggregate(count=Sum('nbre_sec'))
	total_minutes=Suivis.aggregate(count=Sum('nbre_min'))
	total_ventes_user=Bilan_user.aggregate(count=Sum('prix_formation'))

	count_appel=Suivis.count()

	try:
		a=total_secondes['count']>60
		diff=total_secondes['count']/60

		total_minutes['count']=total_minutes['count']+int(diff)
		total_secondes['count']=total_secondes['count']-int(diff)*60
		total_ventes_user=Bilan_user.aggregate(count=Sum('prix_formation'))

	except :
		print("non")
		total_ventes_user['count']=0
		total_minutes['count']=0
		total_secondes['count']=0

	if (total_ventes_user['count']==None):
		total_ventes_user['count']=0	

	group = request.user.groups.all()[0].name

	print('GROUP user::::',group)
	print('type',type(request.user.groups.all()[0].name))


	gainsupdatedd=totalsgainfinals+gainecommerce['benefices']
	depenceupdated=depencesecommerce['depences']+totalcharges
	gainupdated=totalsgainfinals+gainecommerce['benefices']-depencesecommerce['depences']-totalcharges
	try:
		pourcentage_depencesupdated=(depenceupdated/gainsupdatedd)*100
		pourcentage_depencesupdated=int(round(pourcentage_depencesupdated,0))
	except:
		pourcentage_depencesupdated=0
	try:
		pourcentage_gain_net2= 100-pourcentage_depencesupdated
	except:
		pourcentage_gain_net2= 0
	if (pourcentage_gain_net2 < 0):
		pourcentage_gain_net2=0	

	print('aaaaaaaMMMMMMMMMMMM',gainupdated)
	print('aaaaaaaMMMMMMMMMMMM',pourcentage_gain_net2)





	############Interface Ecommerce
	nbventeecommerce=len(Venteecommerce.objects.filter(user_admin=admin_id,user_id=request.user.id).annotate(count=Count('username')))
	ecommercestat=Categorieecommerce.objects.filter(user_admin=admin_id,user_id=request.user.id).aggregate(DEPENCES=Sum('depences'),BENEFICES=Sum('benefices'),NBVENTE=Sum('Nb_Vente'))
	
	############End Interface Ecommerce

	##########Interface Energie
	refus=len(Rendezvousenergie.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=0))
	accept=len(Rendezvousenergie.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=2))
	encours=len(Rendezvousenergie.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=1))
	########## Interface OPCO

	refusopco=len(Rendezvousopco.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=0))
	acceptopco=len(Rendezvousopco.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=2))
	encoursopco=len(Rendezvousopco.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=1))
	##########End Interface OPCO

	########## Interface MUTUELLE VENTE

			# nbrvmutuellevente=Rendezvousmutuellevente.objects.count()
			# nbventemutuellevente=Ventervmutellevente.objects.count()
	nbrvmutuellevente=Rendezvousmutuellevente.objects.filter(user_id=request.user.id,user_admin=admin_id).count()
	nbventemutuellevente=Ventervmutellevente.objects.filter(user_id=request.user.id,user_admin=admin_id).count()
	totalventerevmv=Ventervmutellevente.objects.filter(user_id=request.user.id,user_admin=admin_id).aggregate(totvrv_mv=Sum('prix'))
	totalventerevmv=totalventerevmv['totvrv_mv']
	##########End Interface MUTUELLE VENTE

	########## Interface MUTUELLE

	refusmutuelle=len(Rendezvousmutuelle.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=0))
	acceptmutuelle=len(Rendezvousmutuelle.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=2))
	encoursmutuelle=len(Rendezvousmutuelle.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=1))

	##########End Interface MUTUELLE 

	########## Interface VOYANCE

	refusvoyance=len(Rendezvousvoyance.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=0))
	acceptvoyance=len(Rendezvousvoyance.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=2))
	encoursvoyance=len(Rendezvousvoyance.objects.filter(user_admin=admin_id,user_id=request.user.id,etat=1))

	##########End Interface VOYANCE 



	
	context = {'total_gains':total_gains,'total_admin':total_admin,'depences':depences,'pourcentage_depences':round(pourcentage_depences,2)
	,'gain_net':round(gain_net,2) ,'pourcentage_gain_net':round(pourcentage_gain_net,2),'total_users':total_users,'total_ventes':total_ventes
	,'total_user_vente':total_user_vente,'total_minutes':total_minutes,'total_secondes':total_secondes,'total_ventes_user':total_ventes_user
	,'count_appel':count_appel,'group':group
	,'gainopco':round(gainopco,2),'gainmutuelle':round(gainmutuelle,2),'gainenergie':round(gainenergie,2),'gainmutuellevente':round(gainmutuellevente,2)
	,'gainvoyance':round(gainvoyance,2),'totalgainsdeusers':round(totalgainsdeusers,2),'totalsgainfinals':round(totalsgainfinals,2)
	,'gainecommerce':gainecommerce['benefices'],'depencesecommerce':depencesecommerce['depences'],'totalcharges':totalcharges,
	'pourcentage_gain_net2':round(pourcentage_gain_net2,2),'gainupdated':round(gainupdated,2)
	,'nbventeecommerce':nbventeecommerce,'ecommercestat':ecommercestat,'refus':refus,'accept':accept,'encours':encours,
	'refusopco':refusopco,'acceptopco':acceptopco,'encoursopco':encoursopco,'nbrvmutuellevente':nbrvmutuellevente
	,'nbventemutuellevente':nbventemutuellevente,'refusmutuelle':refusmutuelle,'acceptmutuelle':acceptmutuelle,
	'encoursmutuelle':encoursmutuelle,'total_Chargeimprevisionelle':total_Chargeimprevisionelle,'total_Chargevariable':total_Chargevariable
	,'total_Chargefixe':total_Chargefixe,'encoursvoyance':encoursvoyance,'refusvoyance':refusvoyance,'acceptvoyance':acceptvoyance
	,'totalventerevmv':totalventerevmv}

	return render(request, 'home/index.html', context)
@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)
			
			#print("mon etat",etat)
			#if user is not None and etat==1:
			if username =="" and password =="" :
				messages.info(request, 'Enter valid Credentials')
			elif username =="" :
				messages.info(request, 'Enter valid username')
			elif password=="" :
				messages.info(request, 'Enter valid password')
			elif user is not None :
				useraccount=Account.objects.get(user=user)
				etat=Account.objects.get(user=user).etat
				if etat==0:
					messages.info(request, 'wait for acceptance')
				elif etat==1:
					login(request, user)
					return redirect('home')
			else:
				messages.info(request, 'Username or password incorrect')
	

	context = {'orders':'orders' }
	

	return render(request, 'home/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user =form.save()
			account = Account.objects.create(user=user,etat=0)
			username = form.cleaned_data.get('username')
			group=Group.objects.get(name='user')
			user.groups.add(group)
			
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
			

	context = {'form':form}
	return render(request, 'home/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def model(request):
	age=0
	domaine =""
	formation=""
	for_adequate= ""
	list_age={1:'31-50',2:'51-56'}
	list_domaine={1:'Agro-alimentaire',2:'Artisan',3:'Automobile',4:'Aéronautique',5:'Banque/Finance/Assurance',6:'Chimie/Biologie'
	,7:'Commerce',8:'Conseils et Communication',9:'Design et décoration',10:'Droit et justice',11:'Electrique',12:'Electronique et robotique',
	13:'Energie',14:'Enseignement',15:'Informatique',16:'Intelligence artificielle',17:'Journalisme et communication',18:'Marketing et publicité',
	19:'Mathématiques',20:'Mécanique',21:'Multimédia',22:'Métiers animaliers',23:'Ouvrier',24:'Science vie et terre',
	25:'Sciences humaines et sociales',26:'Sciences physiques',27:'Secteur santé',28:'Spectacle/métier de la scène/cinéma',29:'Sport',30:'Tourisme',
	31:'Transport et logistique',32:'Travailler avec les enfants',33:'Travailleur indépendant'
	,34:'Télécommunications',35:'Urbanisme',36:'Ventes et achats',37:'Edition et métiers du livre'}
	data={'31-50': [0],'51-56':[0],'Agro-alimentaire': [0],'Artisan': [0],'Automobile': [0],'Aéronautique': [0],'Banque/Finance/Assurance': [0]
	,'Chimie/Biologie': [0],'Commerce': [0],'Conseils et Communication': [0],'Design et décoration': [0],'Droit et justice': [0],
	'Electrique': [0],'Electronique et robotique': [0]
	,'Energie': [0],'Enseignement': [0],'Informatique': [0],'Intelligence artificielle': [0],'Journalisme et communication': [0]
	,'Marketing et publicité': [0],'Mathématiques': [0],'Mécanique': [0],'Multimédia': [0],'Métiers animaliers': [0]
	,'Ouvrier': [0],'Science vie et terre': [0],'Sciences humaines et sociales': [0],'Sciences physiques': [0],'Secteur santé': [0]
	,'Spectacle/métier de la scène/cinéma': [0],'Sport': [0],'Tourisme': [0],'Transport et logistique': [0],'Travailler avec les enfants': [0]
	,'Travailleur indépendant': [0],'Télécommunications': [0],'Urbanisme': [0],'Ventes et achats': [0],'Edition et métiers du livre': [0]
	
	}
	df = pd.DataFrame(data) 
	model=joblib.load("Model.sav")
	if request.method=="POST":
		age=request.POST.get('age')	
		domaine=request.POST.get('domaine')
		if (int(domaine)!=0) and (int(age)!=0):
			df[list_domaine.get(int(domaine))]=1
			df[list_age.get(int(age))]=1
			formation=model.predict(df.values)
		elif (int(domaine)==0) and (int(age)==0):
			formation=model.predict(df.values)
		elif (int(domaine)==0) and (int(age)!=0):
			df[list_age.get(int(age))]=1
			formation=model.predict(df.values)
		elif (int(domaine)!=0) and (int(age)==0):
			df[list_domaine.get(int(domaine))]=1
			formation=model.predict(df.values)
		a=int(formation)
		if a==0:
			for_adequate="Bureautiques"
		elif a==1:
			for_adequate="Création d'entreprise"
		elif a==2:
			for_adequate="Développement web ou infographie"
		elif a==3:
			for_adequate="Développement web ou infographie ou création entreprise"
		elif a==4:
			for_adequate="Langues"
		elif a==5:
			for_adequate="Langues ou montage vidéo"
		elif a==6: 
			for_adequate="Langues ou web marketing ou montage vidéo"
		elif a==7:
			for_adequate="Web marketing ou création entreprise"

		
		

		



	context = {'formation':for_adequate }

	return render(request, 'home/model.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allUsers(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	users=User.objects.filter(is_superuser=0,account__user_admin=admin_id)
	print(vars(users))



	context = {'users':users}
	return render(request, 'home/allUsers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def approveordeleteuser(request,pk):
	
	user = User.objects.get(id=pk)
	useraccount=Account.objects.get(user=user)
	etat=Account.objects.get(user=user).etat
	if request.method=="POST":
		if request.POST['status']=="Accept":
			useraccount.etat=1
			useraccount.save()
			return redirect('allUsers')
		else:
			user.delete()
			return redirect('allUsers')

	context = {'users':'users'}
	return render(request, 'home/allUsers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def createBilan(request):
	form = BilanForm()
	loggedinuser_id = request.user.id
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	print('Admin ID',admin_id)

	if request.method == 'POST':
		heure=(request.POST.get('heure'))
		form = BilanForm(request.POST)
		if form.is_valid():
			
			bilan=form.save(commit=False)
			bilan.user_id=loggedinuser_id
			bilan.nom_agent=request.user.last_name
			bilan.prenom_agent=request.user.first_name
			bilan.username=request.user.username
			bilan.user_admin=admin_id
			bilan.heure=heure
			bilan.save()
			messages.success(request,'Bilan ajouté avec succès')
			return redirect('home')


	context = {'form':form}
	return render(request, 'home/bilan.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin','RH'])
def listBilan(request):
	loggedinuser_id = request.user.id
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	bilans = Bilan.objects.filter(user_id=loggedinuser_id,user_admin=admin_id)
	total = bilans.count()
	if total ==None:
		total=0
	context = {'bilans':bilans,'total':total}
	return render(request, 'home/listBilan.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listBilanAdmin(request):
	loggedinuser_id = request.user.id
	bilans = Bilan.objects.filter(user_admin=loggedinuser_id)
	total = bilans.count()
	data=Bilan.objects.filter(user_admin=loggedinuser_id).values('username').annotate(count=Count('user_id')).order_by('-count')
	data2=Bilan.objects.filter(user_admin=loggedinuser_id).values('username').annotate(count=Sum('prix_formation')).order_by('-count')
	data3=Bilan.objects.filter(user_admin=loggedinuser_id).values('categorie').annotate(count=Count('categorie'))
	total_ventes=Bilan.objects.aggregate(count=Sum('prix_formation'))
	if total_ventes['count']==None:
		total_ventes['count']=0
	context = {'bilans':bilans,'total':total,'data':data,'data2':data2,'total_ventes':total_ventes,'data3':data3}
	return render(request, 'home/listBilanAdmin.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def updateBilan(request,pk):
	bilan = Bilan.objects.get(id=pk)
	form = BilanForm(instance=bilan)
	if request.method == 'POST':
		heure=(request.POST.get('heure'))
		form = BilanForm(request.POST, instance=bilan)
		if form.is_valid():
			form1=form.save(commit=False)
			form1.heure=heure
			form1.save()
			return redirect('listBilan')
	context = {'form':form,'heure':bilan.heure}
	return render(request, 'home/bilan.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def deleteBilan(request, pk):
	bilan = Bilan.objects.get(id=pk)
	bilan.delete()
	return HttpResponse("deleted",bilan)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteBilanAdmin(request, pk):
	bilan = Bilan.objects.get(id=pk)
	bilan.delete()
	return HttpResponse("deleted",bilan)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteuser (request,pk):
	user = User.objects.get(id=pk)
	user.delete()
	return HttpResponse("deleted",user)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def acceptuser (request,pk):
	user = User.objects.get(id=pk)
	useraccount=Account.objects.get(user=user)
	useraccount.etat=1
	useraccount.save()
	return redirect('allUsers')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def alleventsPage(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	form = EventForm()
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event=form.save(commit=False)
			event.user_admin=admin_id
			event.nom_agent=loggedinuser.last_name
			event.prenom_agent=loggedinuser.first_name
			event.username_agent=loggedinuser.username
			start_date=event.start_date
			end_date=event.end_date
			date_now  =  datetime.today().date()
			if date_now>start_date and date_now<end_date:
				event.color="#14c1c4"
				event.save()
				return redirect('alleventsPage')
			elif date_now>start_date and date_now>end_date:
				event.color="#40b351"
				event.save()
				return redirect('alleventsPage')
			else:
				event.color="#e83410"
				event.save()
				return redirect('alleventsPage')
			
	events = Event.objects.filter(user_admin=admin_id)
	rendezvous =Rendezvous.objects.filter(user_admin=admin_id)
	for i in events :
		start_date=i.start_date
		end_date=i.end_date
		date_now  =  datetime.today().date()
		if date_now>start_date and date_now<end_date: #bde w mawfesh
			i.color="#14c1c4"
			i.save()
		elif date_now>start_date and date_now>end_date:  # bde w wfe 
			i.color="#40b351"
			i.save()
		else: # mazel mabdesh 
			i.color="#e83410"
			i.save()


	context = {'events':events,'form':form,'rendezvous':rendezvous}
	return render(request, 'home/allevents.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def delete_event(request):
	id = request.GET.get('id')
	event =Event.objects.get(id=id)
	
	if request.method == 'GET':
		event.delete()
		return redirect('alleventsPage')  
	return JsonResponse("data to delete",safe=False)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','user'])
def update_event(request):
	
	
	if request.method=="POST":
		title=request.form['title']
		start=request.form['start']
		end=request.form['end']
		id=request.form['id']
		event = Event.objects.get(id=id)
		form = EventForm(instance=event)
		form.title=title
		form.start_date=start
		form.end_date=end
		form.id=id
		if form.is_valid():
			form.save()
	return JsonResponse("data to update",safe=False) 



@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def createSuivi(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	Suivis = Suivi.objects.filter(user_id=request.user.id)
	total=Suivis.count()
	total_secondes=Suivis.aggregate(count=Sum('nbre_sec'))
	total_minutes=Suivis.aggregate(count=Sum('nbre_min'))

	try:
		a=total_secondes['count']>60
		diff=total_secondes['count']/60
		total_minutes['count']=total_minutes['count']+int(diff)
		total_secondes['count']=total_secondes['count']-int(diff)*60
	except :
		print("erreur")
	if total_secondes['count']==None:
		total_secondes['count']=0
	if total_minutes['count']==None:
		total_minutes['count']=0
	form = SuiviForm()
	loggedinuser_id = request.user.id
	loggedinuser_username = request.user.username
	loggedinuser_nom = request.user.last_name
	loggedinuser_prenom = request.user.first_name
	if request.method == 'POST':
		form = SuiviForm(request.POST)
		if form.is_valid():
			Suivii=form.save(commit=False)
			Suivii.user_id=loggedinuser_id
			Suivii.username=loggedinuser_username
			Suivii.nom_agent=loggedinuser_nom
			Suivii.prenom_agent=loggedinuser_prenom
			Suivii.user_admin=admin_id
			Suivii.save()
			messages.success(request,'Suivi added sucessfully')
			return redirect('createSuivi')


	context = {'form':form,'Suivis':Suivis,'total':total,'total_secondes':total_secondes,'total_minutes':total_minutes}
	return render(request, 'home/Suivi.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def SuiviAdmin(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	list_nbre_sec=[]
	list_nbre_min=[]
	list_depences=[]
	list_depences1=[]
	list_names=[]
	list_argent=[]
	list_verification=[]
	list_depences_total=[]
	r = []

	a=Suivi.objects.filter(user_admin=admin_id)
	nbre_sec_user=Suivi.objects.filter(user_admin=admin_id).values('username').annotate(count_sec=Sum('nbre_sec'),minute=Sum('nbre_min')).order_by('username')
	print("Suivi",nbre_sec_user)

	for i in nbre_sec_user:
		if(i['count_sec']>60):
			diff=i['count_sec']/60
			i['minute']=i['minute']+int(diff)
			i['count_sec']=i['count_sec']-int(diff)*60
			
			

	prix_formation_user1=Bilan.objects.filter(user_admin=admin_id).values('username').annotate(prix=F('prix_formation')*0.2).order_by('username')
	prix_formation_user=prix_formation_user1.values('username').annotate(count=Sum('prix')).order_by('username')
	print("Prix formation",prix_formation_user1)
	print("Prix formation avec reduction",prix_formation_user)
	for i in nbre_sec_user:
		for j in prix_formation_user:
			if i['username']==j['username']:
				#r = i.copy()
				#r.update(j)
				#print("OUSSAMA",r)
				r.append({**i,**j})
				#r.append(i|j)
				#print("My type",type(r))
				#print("New query set",r)
			else :
				#r.append(i)
				#print("appendddd",r)
				print("Empty")
	print( "finallll ",r)
	print('Type de R',type(r))
	
	

	prix_de_minute=0
	if request.method == 'POST':
		prix_de_minute=float(request.POST['prix_seconde'])
		if prix_de_minute <=0:
			prix_de_minute=0
	for i in r:
		print(i)
		list_argent.append(i['count'])	
	for i in r:
		list_nbre_sec.append(i['count_sec'])
		list_nbre_min.append(i['minute'])
		list_names.append(i['username'])
	for i in list_nbre_min:
		a=i*float(prix_de_minute)
		list_depences.append(a)
	for i in list_nbre_sec:
		a=i*float(prix_de_minute)/60
		list_depences1.append(a)
	
	for i in range(len(list_depences)):
		list_verification.append(list_argent[i]-(list_depences[i]+list_depences1[i]))
	list_depences_total=[x + y for x, y in zip(list_depences, list_depences1)]
	
	

	

	data=[]
	for n,m, j,s,t,e in zip(list_names,list_nbre_min , list_nbre_sec, list_argent,list_depences_total,list_verification):
		dataa = { 'username': n, 'minutes':m , 'secondes': j, 'argent': s ,'depences':t,'differnce':round(e,2)}
		data.append(dataa)
	

	context = {'form':'form','data':data}
	return render(request, 'home/SuiviAdmin.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def modifiersuivi(request,pk):
	suivi = Suivi.objects.get(id=pk)
	form = SuiviForm(instance=suivi)
	if request.method == 'POST':
		form = SuiviForm(request.POST, instance=suivi)
		if form.is_valid():
			form.save()
			return redirect('createSuivi')
	context = {'form':form}
	return render(request, 'home/updatesuivi.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def deleteSuivi(request, pk):
	suivi = Suivi.objects.get(id=pk)
	suivi.delete()
	return HttpResponse("deleted",suivi)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def profileUser(request):
	user=request.user
	if request.method == 'POST':
		form = UserUpdateForm(request.POST,instance=user)
		if form.is_valid():
			form.save()
			messages.success(request,'Sucessfully updated')
			return redirect('profileUser')
	else :
		form = UserUpdateForm(instance=user)

	context = {'form':form}
	return render(request, 'home/profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def rendezvous(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	username=request.user.username
	listt=Rendezvous.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousForm()
	if request.method == 'POST':
		form=RendezvousForm(request.POST)
		if form.is_valid():
			form1=form.save(commit=False)
			form1.nom_agent=request.user.last_name
			form1.prenom_agent=request.user.first_name
			form1.user_id=request.user.id
			form1.user_admin=admin_id
			form1.username=username
			form1.save()
			messages.success(request,'Rendez vous ajouté ')
			return redirect('Rendezvous')

	context = {'form':form,'list':listt}
	return render(request, 'home/rendezvous.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def deleterendezvous(request, pk):
	rendezvous = Rendezvous.objects.get(id=pk)
	rendezvous.delete()
	return HttpResponse("deleted",rendezvous)
	#return redirect('listBilan')

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def updateRendezvous(request,pk):
	myform = Rendezvous.objects.get(id=pk)
	form = RendezvousForm(instance=myform)
	if request.method == 'POST':
		form = RendezvousForm(request.POST, instance=myform)
		if form.is_valid():
			form.save()
			return redirect('Rendezvous')
	context = {'form':form}
	return render(request, 'home/modifierrendezvous.html', context)


def stockagedata(request):
	form=StockageForm()

	if request.method == 'POST':
		form=StockageForm(request.POST)
		if form.is_valid():
			form.save()
			messages.info(request, 'Merci')

	context = {'form':form}
	return render(request, 'home/formulaire_stockage.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def maps(request):
	m=folium.Map(location = [48.856578, 2.351828], zoom_start = 5)
	df2 = pd.DataFrame()
	list_indice=[]
	list_numero=[]
	list_mobile=[]
	list_nom=[]
	list_genre=[]
	list_ville=[]
	list_prenom=[]
	data=[]
	address =" "
	df=pd.read_excel("dash_map.xlsx")
	if request.method == "POST":
		# import geocoder
		# g = geocoder.ip('me')
		# print("CURRENT LOCATION",g.latlng)
		address=request.POST.get('address')
		location=geocoder.osm(address)
		print('longeur',len(location))
		print('adresse/////////:',location)
		lat=location.lat
		lng=location.lng
		print('lat and lng',lat,lng)
		country=location.country
		if lat==None or lng==None:
			messages.info(request, 'Localisation introuvable')
		else:
			folium.Marker([lat,lng],tooltip="click for more",popup=country).add_to(m)
			for i,j in enumerate(df['ville']):
				address=address.lower()
				j=j.lower()
				if address in j:
					list_indice.append(i)
			desired_indices = [i for i in range (len(df.index)) if i  in list_indice]
			df2 = df.iloc[desired_indices]
			for i in df2.index: 
				list_mobile.append(df2["mobile"][i])
				list_nom.append(df2["nom"][i])
				list_prenom.append(df2["prenom"][i])
				list_genre.append(df2["genre"][i])
				list_ville.append(df2["ville"][i])	
			for n,r,j,s,t in zip(list_mobile,list_nom , list_prenom, list_genre,list_ville):
				dataa = { 'mobile': n, 'nom':r , 'prenom': j, 'genre': s ,'ville':t}
				data.append(dataa)

	m=m._repr_html_()
	
	a=len(data)

	context = {'m':m,'data':data,'a':a,'address':address}
	return render(request, 'home/maps.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def dashboard(request):

	return render(request, 'home/dashboard.html')



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def database_tocsv(request):
	data = Stockage.objects.all()
	context={'data':data}
	return render(request, 'home/datatocsv.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def download_csv(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Nom', 'Prenom', 'Age', 'Téléphone','Profession','Secteur','Lieu','Formation','Loisir'])
	for data in Stockage.objects.all().values_list('nom', 'prenom', 'age', 'telphone','profession','secteur','lieu','formation','loisir'):
		writer.writerow(data)
        
	response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
	return response

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rolebyuser(request,pk):
	user = User.objects.get(id=pk)

	role= user.groups.all()
	#query_set = Group.objects.filter(id = pk)
	groups=Group.objects.all()
	groups=groups.exclude(name='admin')
	print("ALL groups",groups)

	if request.method == 'POST':
		newrole=request.POST.get('group')
		newGroup=Group.objects.get(name=newrole)
		user.groups.remove(role[0])
		user.groups.add(newGroup)



	context = {'role':role[0],'user':user,'groups':groups}
	return render(request, 'home/roledeuser.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RH'])
def allrendezvous(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rendezvous=Rendezvous.objects.filter(user_admin=admin_id)

	context={'rendezvous':rendezvous}
	return render(request, 'home/allrendezvous.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleterendezvous(request, pk):
	rendezvous=Rendezvous.objects.get(id=pk)
	rendezvous.delete()
	return HttpResponse("deleted",rendezvous)







@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def addchargevariable(request):

	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	print('hi')
	listt=Chargevariable.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=ChargevariableForm()
	if request.method == 'POST':
		print('post')
		form=ChargevariableForm(request.POST)
		print("ddd",form)
		print('amannnn',form.is_valid())
		if form.is_valid():
			print("valid",form.is_valid)
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			print('MY form',form1)
			form1.save()
			messages.success(request,'Charge variable ajouté ')
			return redirect('addchargevariable')

	context = {'form':form,'list':listt}
	return render(request, 'home/addchargevariable.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def addchargefixe(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Chargefixe.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=ChargefixeForm()
	if request.method == 'POST':
		print('post')
		form=ChargefixeForm(request.POST)
		print("ddd",form)
		print('amannnn',form.is_valid())
		if form.is_valid():
			print("valid",form.is_valid)
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			print('MY form',form1)
			form1.save()
			messages.success(request,'Charge fixe ajouté ')
			return redirect('addchargefixe')

	context = {'form':form,'list':listt}
	return render(request, 'home/addchargefixe.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def addchargeimprevisionelle(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Chargeimprevisionelle.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=ChargeimprevisionelleForm()
	if request.method == 'POST':
		print('post')
		form=ChargeimprevisionelleForm(request.POST)

		if form.is_valid():
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			print('MY form',form1)
			form1.save()
			messages.success(request,'Charge imprevisionelle ajouté ')
			return redirect('addchargeimprevisionelle')

	context = {'form':form,'list':listt}
	return render(request, 'home/addchargeimprevisionelle.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def deletechargevariable(request, pk):
	charge = Chargevariable.objects.get(id=pk)
	charge.delete()
	return HttpResponse("deleted",charge)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def deletechargefixe(request, pk):
	charge = Chargefixe.objects.get(id=pk)
	charge.delete()
	return HttpResponse("deleted",charge)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def deletechargeimprevisionelle(request, pk):
	charge = Chargeimprevisionelle.objects.get(id=pk)
	charge.delete()
	return HttpResponse("deleted",charge)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def updatechargevariable(request,pk):
	charge = Chargevariable.objects.get(id=pk)
	form = ChargevariableForm(instance=charge)
	if request.method == 'POST':
		form = ChargevariableForm(request.POST, instance=charge)
		if form.is_valid():
			form.save()
			return redirect('addchargevariable')
	context = {'form':form}
	return render(request, 'home/updatechargevariable.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def updatechargefixe(request,pk):
	charge = Chargefixe.objects.get(id=pk)
	form = ChargefixeForm(instance=charge)
	if request.method == 'POST':
		form = ChargefixeForm(request.POST, instance=charge)
		if form.is_valid():
			form.save()
			return redirect('addchargefixe')
	context = {'form':form}
	return render(request, 'home/updatechargefixe.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def updatechargeimprevisionelle(request,pk):
	charge = Chargeimprevisionelle.objects.get(id=pk)
	form = ChargeimprevisionelleForm(instance=charge)
	if request.method == 'POST':
		form = ChargeimprevisionelleForm(request.POST, instance=charge)
		if form.is_valid():
			form.save()
			return redirect('addchargeimprevisionelle')
	context = {'form':form}
	return render(request, 'home/updatechargeimprevisionelle.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listechargefixe(request):
	loggedinuser = request.user.id
	# admin_id=Account.objects.get(user=loggedinuser).user_admin
	listt=Chargefixe.objects.filter(user_admin=loggedinuser)
	context={'list':listt}
	return render(request, 'home/listechargefixe.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listechargeimprevisionelle(request):
	loggedinuser = request.user.id
	# admin_id=Account.objects.get(user=loggedinuser).user_admin
	listt=Chargeimprevisionelle.objects.filter(user_admin=loggedinuser)
	context={'list':listt}
	return render(request, 'home/listechargeimprevisionelle.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listechargevariable(request):
	loggedinuser = request.user.id
	# admin_id=Account.objects.get(user=loggedinuser).user_admin
	listt=Chargevariable.objects.filter(user_admin=loggedinuser)
	context={'list':listt}
	return render(request, 'home/listechargevariable.html', context)
	

def stockagemutuelle(request):
	print('INIT')
	if request.method == 'POST':
		nom = request.POST.get('nom')
		prenom =request.POST.get('prenom')
		adresse =request.POST.get('adresse')
		ville =request.POST.get('ville')
		codepostal =request.POST.get('codepostal')
		phone =request.POST.get('phone')
		date =request.POST.get('date')
		etat =request.POST.get('etat')
		email =request.POST.get('email')
		commentaire=request.POST.get('commentaire')
		s_date=datetime.strptime(str(date), "%Y-%m-%d").date()
		b = Stockagerendezvousmutuelle(commentaire=commentaire,email=email,nom_client=nom,prenom_client=prenom,adresse=adresse,ville=ville,code_postal=codepostal,telephone=phone,date_naissance=s_date,typerv=etat)
		b.save()
		messages.info(request, 'votre formulaire a été enregistré avec succès')
	context = {'form':'form'}
	return render(request, 'stockage/Rendezvous.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def facturerv(request):
	context = {'form':'form'}
	return render(request, 'home/facturerv.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['RH'])
def facturevente(request):

	context = {'form':'form'}
	return render(request, 'home/facturevente.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','E_commerce','RH','evaluateur'])
def stat_ecommerce(request):
	loggedinuser = request.user
	admin_id= Account.objects.get(user=loggedinuser).user_admin
	nbvente=Venteecommerce.objects.filter(user_admin=admin_id).annotate(count=Count('username'))
	# benefices=Categorieecommerce.objects.filter(user_admin=admin_id).values('produitid',beneficess=Sum('benefices')).annotate(byid=Count('produitid'))
	categories=Categorieecommerce.objects.filter(user_admin=admin_id).values('produitid').annotate(DEPENCES=Sum('depences'),BENEFICES=Sum('benefices'),NBVENTE=Sum('Nb_Vente'))
	produit=Produitecommerce.objects.filter(user_admin=admin_id).values('id','nomproduit')
	nbvente=Categorieecommerce.objects.filter(user_admin=admin_id).values('produitid','nomcategorie').annotate(nbvente=Sum('Nb_Vente'))
	categoriess=Categorieecommerce.objects.filter(user_admin=admin_id)

	r=[]
	for i in produit:
		for j in categories:
			if i['id']==j['produitid']:
				r.append({**i,**j})
			else :
				print("Empty")
	
	# print("NOMBR:::",nbvente)

	nbre_vente=0
	for i in nbvente:
		nbre_vente+=i['nbvente']

	print(categoriess)
	# nomcategorie  depences   benefices

	context = {'data':r,'nbvente':nbre_vente,'nbvente_par_categorie':nbvente,'categoriess':categoriess}

	return render(request, 'home/stateecommerce.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','energie','RH'])
def stat_energie(request):
	loggedinuser = request.user
	admin_id= Account.objects.get(user=loggedinuser).user_admin
	refus=len(Rendezvousenergie.objects.filter(user_admin=admin_id,etat=0))
	accept=len(Rendezvousenergie.objects.filter(user_admin=admin_id,etat=2))
	encours=len(Rendezvousenergie.objects.filter(user_admin=admin_id,etat=1))
	nblist=[]
	nblist.append(refus)
	nblist.append(accept)
	nblist.append(encours)
	listnom=['Nbre de RV refusé','Nbre de RV validé','Pas encore']
	context = {'data':nblist,'listnom':listnom}

	return render(request, 'home/statenergie.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','OPCO','RH'])
def stat_opco(request):
	loggedinuser = request.user
	admin_id= Account.objects.get(user=loggedinuser).user_admin
	refus=len(Rendezvousopco.objects.filter(user_admin=admin_id,etat=0))
	accept=len(Rendezvousopco.objects.filter(user_admin=admin_id,etat=2))
	encours=len(Rendezvousopco.objects.filter(user_admin=admin_id,etat=1))
	nblist = [refus, accept, encours]
	listnom=['Nbre de RV refusé','Nbre de RV validé','Pas encore']
	context = {'data':nblist,'listnom':listnom}

	return render(request, 'home/statopco.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def stat_rv_par_role(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	list_rvopco=Rendezvousopco.objects.filter(user_admin=admin_id).values('username').annotate(rv_opco_count=Count('username')).order_by()
	list_rvenergie=Rendezvousenergie.objects.filter(user_admin=admin_id).values('username').annotate(rv_energie_count=Count('username')).order_by()
	list_rvmutuelle=Rendezvousmutuelle.objects.filter(user_admin=admin_id).values('username').annotate(rv_mutuelle_count=Count('username')).order_by()
	list_rv_mv=Rendezvousmutuellevente.objects.filter(user_admin=admin_id).values('username').annotate(rv_mutuellevente_count=Count('username')).order_by()
	list_rvvoyance=Rendezvousvoyance.objects.filter(user_admin=admin_id).values('username').annotate(rv_voyance_count=Count('username')).order_by()
	list_rvcpf=Rendezvous.objects.filter(user_admin=admin_id).values('username').annotate(rv_cpf_count=Count('username')).order_by()

	
	vente_cpf=Bilan.objects.filter(user_admin=admin_id).values('username').annotate(prix=Sum(F('prix_formation')),prix_spear=Sum(F('prix_formation')*0.2),vente_cpf_count=Count('username'))
	vente_mutuelle_vente=Ventervmutellevente.objects.filter(user_admin=admin_id).values('username').annotate(prix=Sum(F('prix')),vente_ecommerce_count=Count('username'))

	
	# print('Liste des ventes cpf',vente_cpf)
	print('Liste des ventes mutuelle',vente_mutuelle_vente)


	context={'list_rvopco':list_rvopco,'list_rvenergie':list_rvenergie,'list_rvmutuelle':list_rvmutuelle,'list_rv_mv':list_rv_mv
		,'list_rvvoyance':list_rvvoyance,'list_rvcpf':list_rvcpf,'vente_cpf':vente_cpf,'vente_mutuelle_vente':vente_mutuelle_vente}
	return render(request, 'home/stat_rv_par_role.html', context)