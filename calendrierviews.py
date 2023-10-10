from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse




@login_required(login_url='login')
@allowed_users(allowed_roles=['RH','OPCO','admin','evaluateur'])
def listcalendrieropco(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    listt=Rendezvousopco.objects.filter(user_admin=admin_id)
    # for i in listt:
    #     print(vars(i)) 
    context = {'listt':listt}
    return render(request, 'calendrier/listcalendrieropco.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RH','energie','admin','evaluateur'])
def listcalendrierenergetique(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    listt=Rendezvousenergie.objects.filter(user_admin=admin_id)
    context = {'listt':listt}
    return render(request, 'calendrier/listcalendrierenergie.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle','RH','admin','evaluateur'])
def listcalendriermutuelle(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    listt=Rendezvousmutuelle.objects.filter(user_admin=admin_id)
    context = {'listt':listt}
    return render(request, 'calendrier/listcalendriermutuelle.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['mutuelle_vente','RH','admin','evaluateur'])
def listcalendriermutuellevente(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    listt=Rendezvousmutuellevente.objects.filter(user_admin=admin_id)
    listt2=Rendezvousmutuelle.objects.filter(typerv='TELEPHONIQUE')


    context = {'listt':listt,'listt2':listt2}
    return render(request, 'calendrier/listcalendriermutuellevente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['voyance','RH','admin','evaluateur'])
def listcalendriervoyance(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    listt=Rendezvousvoyance.objects.filter(user_admin=admin_id)


    context = {'listt':listt}
    return render(request, 'calendrier/listcalendriervoyance.html', context)