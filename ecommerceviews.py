from formation.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count,Sum
from django.contrib import messages

from .models import *
from .forms import *
from django.http.response import HttpResponse


@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def addventeecommerce(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    group = request.user.groups.all()[0].name
    loggedinuser_id=loggedinuser.id
    nom_agent=request.user.last_name
    prenom_agent=request.user.first_name
    username=request.user.username

    listt=Venteecommerce.objects.filter(user_id=request.user.id,user_admin=admin_id)

    form=VenteecommerceForm()

    if request.method == 'POST':
        form=VenteecommerceForm(request.POST)
        if form.is_valid():
            form1=form.save(commit=False)
            form1.nom_agent=nom_agent
            form1.prenom_agent=prenom_agent
            form1.user_role=group
            form1.user_admin=admin_id
            form1.username=username
            form1.user_id=loggedinuser_id
            form1.save()
  
        return redirect('addventeecommerce')

    context = {'form':VenteecommerceForm,'list':listt}
    return render(request, 'ecommerce/addventeecommerce.html', context)
	

@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def updateventeecommerce(request,pk):
	rv_opco = Venteecommerce.objects.get(id=pk)
	form = VenteecommerceForm(instance=rv_opco)
	if request.method == 'POST':
		form = VenteecommerceForm(request.POST, instance=rv_opco)
		if form.is_valid():
			form.save()
			return redirect('addventeecommerce')
	context = {'form':form}
	return render(request, 'ecommerce/updatecomvente.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def deleteventeecommerce (request,pk):
	rv_opco = Venteecommerce.objects.get(id=pk)
	rv_opco.delete()
	return HttpResponse("deleted",rv_opco)



@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def addproduct(request):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    group = request.user.groups.all()[0].name
    loggedinuser_id=loggedinuser.id
    nom_agent=request.user.last_name
    prenom_agent=request.user.first_name
    username=request.user.username

    listt=Produitecommerce.objects.filter(user_id=request.user.id,user_admin=admin_id)

    form=ProduitecommerceForm()

    if request.method == 'POST':
        form=ProduitecommerceForm(request.POST)
        if form.is_valid():
            form1=form.save(commit=False)
            form1.nom_agent=nom_agent
            form1.prenom_agent=prenom_agent
            form1.user_role=group
            form1.user_admin=admin_id
            form1.username=username
            form1.user_id=loggedinuser_id
            form1.save()
  
        return redirect('addproduct')

    context = {'form':ProduitecommerceForm,'list':listt}
    return render(request, 'ecommerce/addproduct.html', context)
	

@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def deleteproduct (request,pk):
    rv_opco = Produitecommerce.objects.get(id=pk)
    try:
        categories=Categorieecommerce.objects.filter(produitid=rv_opco.id)
        print('categories',categories)
        categories.delete()
    except:
        print('categorie introuvable')
    
    rv_opco.delete()
    return HttpResponse("deleted",rv_opco)



@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def addcategorie(request,pk):
    loggedinuser = request.user
    admin_id=Account.objects.get(user=loggedinuser).user_admin
    group = request.user.groups.all()[0].name
    loggedinuser_id=loggedinuser.id
    nom_agent=request.user.last_name
    prenom_agent=request.user.first_name
    username=request.user.username

    # listt=Produitecommerce.objects.filter(user_id=request.user.id,user_admin=admin_id)
    produit = Produitecommerce.objects.get(id=pk)
    form=CategorieecommerceForm()

    if request.method == 'POST':
        form=CategorieecommerceForm(request.POST)
        prixunite_achat=float(request.POST.get('prixunite_achat'))	
        prixunite_vente=float(request.POST.get('prixunite_vente'))	
        quantite=int(request.POST.get('quantite'))	
        if form.is_valid():
            form1=form.save(commit=False)
            form1.produitid=produit.id
            form1.nom_agent=nom_agent
            form1.prenom_agent=prenom_agent
            form1.user_role=group
            form1.user_admin=admin_id
            form1.username=username
            form1.user_id=loggedinuser_id
            form1.quantite=quantite
            form1.prixunite_achat=prixunite_achat
            form1.prixunite_vente=prixunite_vente
            form1.depences=(quantite)*(prixunite_achat)
            form1.save()
            messages.success(request,'Catégorie ajouté ')

  
        return redirect('addproduct')

    context = {'form':CategorieecommerceForm}
    return render(request, 'ecommerce/addcategorie.html', context)
	
@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def listcategorieparproduit(request,pk):
    produit = Produitecommerce.objects.get(id=pk)
    categories = Categorieecommerce.objects.filter(produitid=produit.id)
    context = {'list':categories,'name':produit.nomproduit}
    return render(request, 'ecommerce/listcategorieparproduit.html', context)



# from pprint import pprint

@login_required(login_url='login')
@allowed_users(allowed_roles=['E_commerce'])
def modfiercategorie(request,pk):
    loggedinuser = request.user
    loggedinuser_id=loggedinuser.id
    categorie = Categorieecommerce.objects.get(id=pk)
    form=CategorieecommerceForm(instance=categorie)
    # pprint(vars(categorie)) 
    oldquantite=categorie.quantite
    olddepences=categorie.depences
    oldbenefices=categorie.benefices
    oldprixunite_achat=categorie.prixunite_achat
    oldprixunite_vente=categorie.prixunite_vente
    if request.method == 'POST':
        form=CategorieecommerceForm(request.POST,instance=categorie)
        newqantite=int(request.POST.get('newqantite'))	
        prixunite_vente=float(request.POST.get('prixunite_vente'))	
        prixunite_achat=float(request.POST.get('prixunite_achat'))	
        if form.is_valid():
            if newqantite>oldquantite:
                form1=form.save(commit=False)
                difference=newqantite-oldquantite
                print("diff",difference)
                newdepences=olddepences+(difference*oldprixunite_achat)
                form1.depences=newdepences
                form1.quantite=newqantite
                form1.prixunite_vente=prixunite_vente
                form1.prixunite_achat=prixunite_achat
                form1.save()
                return redirect('listcategorieparproduit',pk=categorie.produitid)
            
            elif newqantite<oldquantite:
                form1=form.save(commit=False)
                difference=oldquantite-newqantite
                newbenefices=oldbenefices+(difference*oldprixunite_vente)
                form1.benefices=newbenefices
                form1.quantite=newqantite
                form1.prixunite_vente=prixunite_vente
                form1.prixunite_achat=prixunite_achat
                form1.Nb_Vente+=oldquantite-newqantite
                print('nbvente',form1.Nb_Vente)
                form1.save()
                return redirect('listcategorieparproduit',pk=categorie.produitid)

            else :
                form1=form.save(commit=False)
                form1.prixunite_vente=prixunite_vente
                form1.quantite=newqantite
                form1.prixunite_achat=prixunite_achat
                form1.save()
                return redirect('listcategorieparproduit',pk=categorie.produitid)



    context = {'list':'categories','name':'nomproduit','form':form,'oldquantite':oldquantite,'olddepences':olddepences,
    'oldbenefices':oldbenefices,'oldprixunite_achat':oldprixunite_achat,'oldprixunite_vente':oldprixunite_vente}
    return render(request, 'ecommerce/modfiercategorie.html', context)
