from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse





@login_required(login_url='login')
@allowed_users(allowed_roles=['OPCO'])
def addrendezvousopco(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Rendezvousopco.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousopcoForm()
	print('before post')
	if request.method == 'POST':
		heure=(request.POST.get('heure'))
		form=RendezvousopcoForm(request.POST)

		identifiant=request.POST.get('identifiant')
		password=request.POST.get('pass')
		print('aaaaaaaaaaa',identifiant)
		if form.is_valid():
			print("valid",form.is_valid)
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			form1.identifiant=identifiant
			form1.mdp=password
			form1.heure=heure
			print('MY form',form1)
			form1.save()
			messages.success(request,'Rendez vous ajouté ')
			return redirect('addrendezvousopco')

	context = {'form':form,'list':listt}
	return render(request, 'opco/addrendezvousopco.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['OPCO'])
def ignorerendezvousopco (request,pk):
    rv_opco = Rendezvousopco.objects.get(id=pk)
    rv_opco.etat=0
    rv_opco.save()
    if (rv_opco.benefice==65):
        rv_opco.benefice=0
    rv_opco.save()
    loggedinuser = request.user
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousopco.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    return redirect('addrendezvousopco')

@login_required(login_url='login')
@allowed_users(allowed_roles=['OPCO'])
def approverendezvousopco (request,pk):
    loggedinuser = request.user
    rv_opco = Rendezvousopco.objects.get(id=pk)
    rv_opco.etat=2
    rv_opco.benefice=65
    rv_opco.save()
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin

    try :
        userbenefice=Rendezvousopco.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    

    return redirect('addrendezvousopco')


@login_required(login_url='login')
@allowed_users(allowed_roles=['OPCO'])
def deleterendezvousopco (request,pk):
    loggedinuser = request.user
    rv_opco = Rendezvousopco.objects.get(id=pk)
    rv_opco.delete()
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin

    try :
        userbenefice=Rendezvousopco.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    
    return HttpResponse("deleted",rv_opco)

@login_required(login_url='login')
@allowed_users(allowed_roles=['OPCO'])
def updaterendezvousopco(request,pk):
	rv_opco = Rendezvousopco.objects.get(id=pk)
	form = RendezvousopcoForm(instance=rv_opco)
	if request.method == 'POST':
		heure=(request.POST.get('heure'))
		form = RendezvousopcoForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form1=form.save(commit=False)
			form1.heure=heure
			form1.save()
			return redirect('addrendezvousopco')
	context = {'form':form,'heure':rv_opco.heure}
	return render(request, 'opco/updaterendezvousopco.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RH','evaluateur','OPCO'])
def listrendezvousopcoadmin(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Rendezvousopco.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'opco/listrendezvousopcoadmin.html', context)
