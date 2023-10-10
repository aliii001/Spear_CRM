from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse


@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente'])
def addmutuellevente(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Rendezvousmutuellevente.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousmutuelleventeForm()
	print('before post')
	if request.method == 'POST':
		# heure=(request.POST.get('heure'))
		form=RendezvousmutuelleventeForm(request.POST)	
		# note=request.POST.get('slider')	
		if form.is_valid():
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			# form1.note=note
			# form1.heure=heure
			form1.save()
			messages.success(request,'Rendez vous ajouté ')
			return redirect('addmutuellevente')
	context = {'form':form,'list':listt}
	return render(request, 'mutuellevente/addmutuellevente.html', context)
           
@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente'])
def updaterendezvousmutuellevente(request,pk):
	rv_opco = Rendezvousmutuellevente.objects.get(id=pk)
	form = RendezvousmutuelleventeForm(instance=rv_opco)
	# oldnote=rv_opco.note
	if request.method == 'POST':
		form = RendezvousmutuelleventeForm(request.POST, instance=rv_opco)
		# heure=(request.POST.get('heure'))
		# note=request.POST.get('slider')	
		if form.is_valid():
			form1=form.save(commit=False)
			# form1.note=note
			# form1.heure=heure
			form1.save()
			return redirect('addmutuellevente')
	context = {'form':form}
	return render(request, 'mutuellevente/updatemutuellevente.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente'])
def deleterendezvousmutuellevente (request,pk):
	print('Hello')
	rv_opco = Rendezvousmutuellevente.objects.get(id=pk)
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	try:
		ventes=Ventervmutellevente.objects.filter(rendezvousid=rv_opco.id)
		print('ventes',ventes)
		ventes.delete()
	
	except:
		print('ventes introuvable')

	rv_opco.delete()

	
	try:
		userbenefice=Ventervmutellevente.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
		useraccount=Account.objects.get(user=loggedinuser)
		useraccount.user_benefice=userbenefice['count']
		useraccount.save() 
	
	except:
		userbenefice['count']=0

	return HttpResponse("deleted",rv_opco)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente'])
def ajouterventemutuelle(request,pk):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    group = request.user.groups.all()[0].name
    loggedinuser_id=loggedinuser.id
    nom_agent=request.user.last_name
    prenom_agent=request.user.first_name
    username=request.user.username
    rv = Rendezvousmutuellevente.objects.get(id=pk)

    nom_client=rv.nom_client
    prenom_client=rv.prenom_client
    adresse=rv.adresse
    telephone=rv.telephone
    email=rv.email

    if request.method == 'POST':
        prix=float(request.POST.get('prix'))    
        b = Ventervmutellevente(nom_agent=nom_agent,prenom_agent=prenom_agent,user_id=loggedinuser_id,user_admin=admin_id
        ,user_role=group,username=username,nom_client=nom_client,prenom_client=prenom_client,adresse=adresse,telephone=telephone
        ,email=email,prix=prix,rendezvousid=rv.id,benefice=0.12*prix)
        b.save()
        rv.etat=2
        rv.save()
        try :
            userbenefice=Ventervmutellevente.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
            useraccount=Account.objects.get(user=loggedinuser)
            useraccount.user_benefice=userbenefice['count']
            useraccount.save() 
        except:
            userbenefice['count']=0

                
                
        return redirect('addmutuellevente')

    context = {'form':'form'}
    return render(request, 'mutuellevente/ajoutervente.html', context)
	


@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente'])
def listdesventes(request):

	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username

	venteform=Ventervmutellevente.objects.filter(user_id=request.user.id,user_admin=admin_id)

	
	context = {'list':venteform}
	return render(request, 'mutuellevente/listvente.html', context)
