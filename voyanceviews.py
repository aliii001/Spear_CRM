from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse


@login_required(login_url='login')
@allowed_users(allowed_roles=['voyance'])
def addrendezvousvoyance(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Rendezvousvoyance.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=RendezvousvoyanceForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=RendezvousvoyanceForm(request.POST)
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
			messages.success(request,'Rendez vous ajouté ')
			return redirect('addrendezvousvoyance')

	context = {'form':form,'list':listt}
	return render(request, 'voyance/addrendezvousvoyance.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['voyance'])
def updaterendezvousvoyance(request,pk):
	rv_opco = Rendezvousvoyance.objects.get(id=pk)
	form = RendezvousvoyanceForm(instance=rv_opco)
	if request.method == 'POST':
		form = RendezvousvoyanceForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('addrendezvousvoyance')
	context = {'form':form}
	return render(request, 'voyance/updaterendezvousvoyance.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['voyance'])
def deletervvoyance (request,pk):
	rv_opco = Rendezvousvoyance.objects.get(id=pk)
	rv_opco.delete()
	loggedinuser = request.user 
	useraccount=Account.objects.get(user=loggedinuser)
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	try :
		userbenefice=Rendezvousvoyance.objects.filter(user_admin=admin_id).aggregate(count=Sum('prix'))
		useraccount=Account.objects.get(user=loggedinuser)
		useraccount.user_benefice=userbenefice['count']
		useraccount.save() 
	except:
		userbenefice['count']=0
	return HttpResponse("deleted",rv_opco)

@login_required(login_url='login')
@allowed_users(allowed_roles=['voyance'])
def ignorerendezvousvoyance (request,pk):
	rv_opco = Rendezvousvoyance.objects.get(id=pk)
	rv_opco.etat=0
	rv_opco.prix=0
	rv_opco.save()
	loggedinuser = request.user 
	useraccount=Account.objects.get(user=loggedinuser)
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	try :
		userbenefice=Rendezvousvoyance.objects.filter(user_admin=admin_id).aggregate(count=Sum('prix'))
		useraccount=Account.objects.get(user=loggedinuser)
		useraccount.user_benefice=userbenefice['count']
		useraccount.save() 
	except:
		userbenefice['count']=0
	return redirect('addrendezvousvoyance')


@login_required(login_url='login') 
@allowed_users(allowed_roles=['voyance']) 
def approverendezvousvoyance (request,pk): 
	loggedinuser = request.user 
	rv_opco = Rendezvousvoyance.objects.get(id=pk) 
	if request.method == 'POST': 
		price=float(request.POST.get('price')) 
		print('MY PRICE',price) 
		rv_opco.prix=price 
		rv_opco.etat=2 
		rv_opco.save() 
		useraccount=Account.objects.get(user=loggedinuser)
		admin_id=Account.objects.get(user=loggedinuser).user_admin
		try :
			userbenefice=Rendezvousvoyance.objects.filter(user_admin=admin_id).aggregate(count=Sum('prix'))
			useraccount=Account.objects.get(user=loggedinuser)
			useraccount.user_benefice=userbenefice['count']
			useraccount.save() 
		except:
			userbenefice['count']=0

		# useraccount=Account.objects.get(user=loggedinuser) 
		# benefice=useraccount.user_benefice 
		# newbenefice=benefice+price 

		# useraccount.user_benefice=newbenefice 
		# useraccount.save() 
		return redirect('addrendezvousvoyance') 
	context={} 
		
	return render(request, 'voyance/accepterrvvoyance.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','RH','voyance'])
def listrendezvousvoyanceadmin(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Rendezvousvoyance.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'voyance/listrendezvousvoyanceadmin.html', context)