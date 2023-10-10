from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse

@login_required(login_url='login')
@allowed_users(allowed_roles=['energie'])
def addrendezenergie(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Rendezvousenergie.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousenergieForm()
	print('before post')
	if request.method == 'POST':
		heure=(request.POST.get('heure'))
		form=RendezvousenergieForm(request.POST)
		if form.is_valid():
			print("valid",form.is_valid)
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			form1.heure=heure
			

			print('MY form',form1)
			form1.save()
			messages.success(request,'Rendez vous ajouté ')
			return redirect('addrendezenergie')

	context = {'form':form,'list':listt}
	return render(request, 'energie/addrendezenergie.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['energie'])
def ignorerendezvousenergie (request,pk):
    rv_opco = Rendezvousenergie.objects.get(id=pk)
    rv_opco.etat=0
    benefice=rv_opco.benefice
    print('////////////',benefice)
    if (benefice==300):
        rv_opco.benefice=0
    rv_opco.save()
    loggedinuser = request.user
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousenergie.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0

    return redirect('addrendezenergie')

@login_required(login_url='login')
@allowed_users(allowed_roles=['energie'])
def approverendezvousenergie (request,pk):
    loggedinuser = request.user
    rv_opco = Rendezvousenergie.objects.get(id=pk)
    rv_opco.etat=2
    rv_opco.benefice=300
    rv_opco.save()
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousenergie.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0

    return redirect('addrendezenergie')     


@login_required(login_url='login')
@allowed_users(allowed_roles=['energie'])
def deleterendezvousenergie (request,pk):
    rv_opco = Rendezvousenergie.objects.get(id=pk)
    loggedinuser = request.user
    rv_opco.delete()

    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousenergie.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    # return redirect('addrendezvousopco')
    return HttpResponse("deleted",rv_opco)

@login_required(login_url='login')
@allowed_users(allowed_roles=['energie'])
def updaterendezvousenergie(request,pk):
	rv_opco = Rendezvousenergie.objects.get(id=pk)
	form = RendezvousenergieForm(instance=rv_opco)
	if request.method == 'POST':
		heure=(request.POST.get('heure'))	
		print('new heure',heure)
		print('type',type(heure))
		form = RendezvousenergieForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form1=form.save(commit=False)
			form1.heure=heure
			form1.save()
			return redirect('addrendezenergie')
	context = {'form':form,'heure':rv_opco.heure}
	return render(request, 'energie/updaterendezvousenergie.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RH','evaluateur','energie'])
def listrendezvousenergieadmin(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Rendezvousenergie.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'energie/listrendezvousenergieadmin.html', context)