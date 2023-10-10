from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse


@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def addmutuelle(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Rendezvousmutuelle.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousmutuelleForm()
	print('before post')
	if request.method == 'POST':
		form=RendezvousmutuelleForm(request.POST)	
		note=request.POST.get('slider')	
		if form.is_valid():
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id
			form1.note=note
			form1.save()
			messages.success(request,'Rendez vous ajouté ')
			return redirect('addmutuelle')
	context = {'form':form,'list':listt}
	return render(request, 'mutuelle/addmutuelle.html', context)
           



@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def ignorerendezvousmutuelle(request,pk):
    rv_opco = Rendezvousmutuelle.objects.get(id=pk)
    rv_opco.etat=0
    print('be,eficeeee',rv_opco.benefice)
    if (rv_opco.benefice==70):
        rv_opco.benefice=0
    rv_opco.save()
    loggedinuser = request.user
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousmutuelle.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    return redirect('addmutuelle')

@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def approverendezvousmutuelle(request,pk):
    loggedinuser = request.user
    rv_opco = Rendezvousmutuelle.objects.get(id=pk)
    rv_opco.etat=2
    rv_opco.benefice=70
    rv_opco.save()

    loggedinuser = request.user
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousmutuelle.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0
    return redirect('addmutuelle')  

@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def deleterendezvousmutuelle (request,pk):
    rv_opco = Rendezvousmutuelle.objects.get(id=pk)
    loggedinuser = request.user
    useraccount=Account.objects.get(user=loggedinuser)
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    try :
        userbenefice=Rendezvousmutuelle.objects.filter(user_admin=admin_id).aggregate(count=Sum('benefice'))
        useraccount=Account.objects.get(user=loggedinuser)
        useraccount.user_benefice=userbenefice['count']
        useraccount.save() 
    except:
        userbenefice['count']=0

    rv_opco.delete()

    # return redirect('addrendezvousopco')
    return HttpResponse("deleted",rv_opco)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def updaterendezvousmutuelle(request,pk):
	rv_opco = Rendezvousmutuelle.objects.get(id=pk)
	form = RendezvousmutuelleForm(instance=rv_opco)
	oldnote=rv_opco.note
	if request.method == 'POST':
		form = RendezvousmutuelleForm(request.POST, instance=rv_opco)
		note=request.POST.get('slider')	
		if form.is_valid():
			form1=form.save(commit=False)
			form1.note=note
			form1.save()
			return redirect('addmutuelle')
	context = {'form':form,'oldnote':oldnote}
	return render(request, 'mutuelle/updaterendezvousmutuelle.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RH','evaluateur'])
def listrendezvousmutuelleadmin(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Rendezvousmutuelle.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'mutuelle/listrendezvousmutuelleadmin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle'])
def mesrendezvousmutuelle(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Rendezvousmutuelle.objects.filter(user_id=request.user.id,user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'mutuelle/mesrendezvousmutuelle.html', context)