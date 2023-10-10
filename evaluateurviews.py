from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse



@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def ajoutersuivicpf(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Suivicpf.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=SuivicpfForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=SuivicpfForm(request.POST)
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
			messages.success(request,'Suivi cpf ajouté ')
			return redirect('ajoutersuivicpf')

	context = {'form':form,'list':listt}
	return render(request, 'evaluateur/ajoutersuivi.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def deletesuivicpf(request,pk):
	rv_opco = Suivicpf.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def modifiersuivicpf(request,pk):
	rv_opco = Suivicpf.objects.get(id=pk)
	form = SuivicpfForm(instance=rv_opco)
	if request.method == 'POST':
		form = SuivicpfForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('ajoutersuivicpf')
	context = {'form':form}
	return render(request, 'evaluateur/modifiersuivicpf.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def listsuivicpf(request):
	rv_opco = Suivicpf.objects.all()
	context = {'list':rv_opco}
	return render(request, 'evaluateur/listsuivicpf.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def ajoutersuivimutuelle(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Mutuellesante.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=MutuellesanteForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=MutuellesanteForm(request.POST)
		if form.is_valid():
			print("valid",form.is_valid)
			form1=form.save(commit=False)
			form1.nom_agent=nom_agent
			form1.prenom_agent=prenom_agent
			form1.user_role=group
			form1.user_admin=admin_id
			form1.username=username
			form1.user_id=loggedinuser_id

			form1.save()
			messages.success(request,'Suivi mutuelle santé ajouté ')
			return redirect('ajoutersuivimutuelle')

	context = {'form':form,'list':listt}
	return render(request, 'evaluateur/ajoutersuivimutuelle.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def modifiersuivimutuelle(request,pk):
	rv_opco = Mutuellesante.objects.get(id=pk)
	form = MutuellesanteForm(instance=rv_opco)
	if request.method == 'POST':
		form = MutuellesanteForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('ajoutersuivimutuelle')
	context = {'form':form}
	return render(request, 'evaluateur/modifiersuivimutuelle.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def deletesuivimutuellesante(request,pk):
	rv_opco = Mutuellesante.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def listsuivimutellesante(request):
	rv_opco = Mutuellesante.objects.all()
	context = {'list':rv_opco}
	return render(request, 'evaluateur/listsuivimutuellesante.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def ajoutersuiviopco(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Suiviopco.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=SuiviopcoForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=SuiviopcoForm(request.POST)
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
			messages.success(request,'Suivi opco ajouté ')
			return redirect('ajoutersuiviopco')

	context = {'form':form,'list':listt}
	return render(request, 'evaluateur/ajoutersuiviopco.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def modifiersuiviopco(request,pk):
	rv_opco = Suiviopco.objects.get(id=pk)
	form = SuiviopcoForm(instance=rv_opco)
	if request.method == 'POST':
		form = SuiviopcoForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('ajoutersuiviopco')
	context = {'form':form}
	return render(request, 'evaluateur/modifiersuiviopco.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def deletesuiviopco(request,pk):
	rv_opco = Suiviopco.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def listsuiviopco(request):
	rv_opco = Suiviopco.objects.all()
	context = {'list':rv_opco}
	return render(request, 'evaluateur/listsuiviopco.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def ajoutersuivien(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Suivienergitique.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=SuivienergitiqueForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=SuivienergitiqueForm(request.POST)
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
			messages.success(request,'Suivi énergétique ajouté ')
			return redirect('ajoutersuivien')

	context = {'form':form,'list':listt}
	return render(request, 'evaluateur/ajoutersuivien.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def modifiersuivien(request,pk):
	rv_opco = Suivienergitique.objects.get(id=pk)
	form = SuivienergitiqueForm(instance=rv_opco)
	if request.method == 'POST':
		form = SuivienergitiqueForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('ajoutersuivien')
	context = {'form':form}
	return render(request, 'evaluateur/modifiersuivien.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def deletesuivien(request,pk):
	rv_opco = Suivienergitique.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def listsuivien(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Suivienergitique.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'evaluateur/listsuivien.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def ajoutersuivivoyance(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	group = request.user.groups.all()[0].name
	loggedinuser_id=loggedinuser.id
	nom_agent=request.user.last_name
	prenom_agent=request.user.first_name
	username=request.user.username
	listt=Suivivoyance.objects.filter(user_id=request.user.id,user_admin=admin_id)
	form=SuivivoyanceForm()
	print('before post')
	if request.method == 'POST':
		print('post')
		form=SuivivoyanceForm(request.POST)
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
			messages.success(request,'Suivi voyance ajouté ')
			return redirect('ajoutersuivivoyance')

	context = {'form':form,'list':listt}
	return render(request, 'evaluateur/ajoutersuivivoyance.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def deletesuivivoyance(request,pk):
	rv_opco = Suivivoyance.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)


@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def modifiersuivivoyance(request,pk):
	rv_opco = Suivivoyance.objects.get(id=pk)
	form = SuivivoyanceForm(instance=rv_opco)
	if request.method == 'POST':
		form = SuivivoyanceForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('ajoutersuivivoyance')
	context = {'form':form}
	return render(request, 'evaluateur/modifiersuivivoyance.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','evaluateur'])
def listsuivivoyance(request):
	loggedinuser = request.user
	admin_id=Account.objects.get(user=loggedinuser).user_admin
	rv_opco = Suivivoyance.objects.filter(user_admin=admin_id)
	context = {'list':rv_opco}
	return render(request, 'evaluateur/listsuivivoyance.html', context)