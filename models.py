from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from sqlalchemy import null 

# Create your models here.
class Account(models.Model):
	user =models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	etat= models.IntegerField(default=0)
	user_admin=models.IntegerField(null=True)
	user_benefice=models.FloatField(default=0,null=True)
	def __str__(self):
		return str(self.user.username)
	
class Bilan(models.Model):

	CHOIX=(
			('OUI','OUI'),
			('NON','NON')
			
		)
	CATEGORY = (
			("Langues", "Langues"),
			("Bureautique", "Bureautique"),
			("Développement Web", "Développement Web"),
			("Infographie", "Infographie"),
			("Web marketing", "Web marketing"),
			("Création d'entreprise" , "Création d'entreprise"),
			("Monatage vidéo", "Monatage vidéo"),
			) 
	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	secteur_activite=models.CharField(max_length=200, null=True)
	nom_formation=models.CharField(max_length=200, null=True)
	age=models.IntegerField(null=True,default=1,validators=[MaxValueValidator(80), MinValueValidator(15)])
	nbre_heure=models.IntegerField(default=1,null=True,validators=[MinValueValidator(1)])
	prix_formation=models.FloatField(null=True,default=1,validators=[MinValueValidator(1)])
	date_debut=models.DateField(null=True)
	categorie = models.CharField(max_length=200, null=True, choices=CATEGORY)
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=True,default=1)
	username=models.CharField(max_length=200, null=True)
	user_admin=models.IntegerField(null=True,default=1)

	numdesecu = models.CharField(max_length=200, null=True, choices=CHOIX)
	centre_formation = models.CharField(max_length=200, null=True)
	heure=models.CharField(max_length=200, null=False)
	commentaire=models.CharField(max_length=200, null=False)

	def __str__(self):
		return self.nom_client

class Event(models.Model):
	title=models.CharField(max_length=200, null=False)
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	username_agent=models.CharField(max_length=200, null=True)
	start_date=models.DateField(null=False)
	end_date=models.DateField(null=False)
	color=models.CharField(max_length=200,null=True)
	user_admin=models.IntegerField(null=True,default=0)
	def __str__(self):
		return self.title
	
class Suivi(models.Model):
	user_id=models.IntegerField(null=False)
	username=models.CharField(max_length=200, null=False)
	nbre_sec=models.IntegerField(null=False,validators=[MaxValueValidator(60), MinValueValidator(0)])
	nbre_min=models.IntegerField(null=False,validators=[MaxValueValidator(180), MinValueValidator(0)])
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_admin=models.IntegerField(null=True,default=0)
	def __str__(self):
		return self.username
	
class Rendezvous(models.Model):
	AGES=(
			('de 15 à 18','de 15 à 18'),
			('de 18 à 30','de 18 à 30'),
			('de 30 à 50','de 30 à 50'),
			('50 ans et ++','50 ans et ++')
		)
	CHOIX=(
			('OUI','OUI'),
			('NON','NON')
			
		)
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	phone_number=models.IntegerField(null=False)
	date_rendez_vous=models.DateField(null=False)
	date_rendez_vous_prochain=models.DateField(null=False)
	secteur=models.CharField(max_length=200, null=True)
	objet=models.CharField(max_length=200, null=False)
	username=models.CharField(max_length=200, null=False)
	
	periode_exercise=models.CharField(max_length=200, null=False)
	trancheage = models.CharField(max_length=200, null=True, choices=AGES)
	numdesecu = models.CharField(max_length=200, null=True, choices=CHOIX)
	formationsouhaitee= models.CharField(max_length=200, null=False)
	date_appel=models.DateField(null=True)


	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	def __str__(self):
		return self.nom_agent
	
class Stockage(models.Model):
	PROFESSION=(
		('Etudiant','Etudiant'),
		('Employeur','Employeur'),
		('Employé','Employé')
	)
	nom=models.CharField(max_length=200, null=False)
	prenom=models.CharField(max_length=200, null=False)
	age=models.IntegerField(null=False,validators=[MaxValueValidator(75), MinValueValidator(15)])
	profession = models.CharField(max_length=200, null=False, choices=PROFESSION)
	secteur=models.CharField(max_length=200, null=False)
	lieu=models.CharField(max_length=200, null=False)
	formation=models.CharField(max_length=200, null=False)
	loisir=models.CharField(max_length=200, null=True, blank=True)
	def __str__(self):
		return self.nom

class Chargevariable(models.Model):
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	salaire=models.FloatField(null=True,default=0)
	credit=models.FloatField(null=True,default=0)
	marketingdigitale=models.FloatField(null=True,default=0)
	voip=models.FloatField(null=True,default=0)
	fiches=models.FloatField(null=True,default=0)
	crm=models.FloatField(null=True,default=0)
	hebergement=models.FloatField(null=True,default=0)
	leads=models.FloatField(null=True,default=0)
	voyants=models.FloatField(null=True,default=0)
	autres=models.FloatField(null=True,default=0)

	
	
	def __str__(self):
		return self.nom_agent

class Chargefixe(models.Model):
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	loyer=models.FloatField(null=True,default=0)
	internet=models.FloatField(null=True,default=0)
	telecom=models.FloatField(null=True,default=0)
	steg=models.FloatField(null=True,default=0)
	soned=models.FloatField(null=True,default=0)
	banque=models.FloatField(null=True,default=0)
	retenuealasource=models.FloatField(null=True,default=0)
	cnss=models.FloatField(null=True,default=0)
	comptable=models.FloatField(null=True,default=0)

	def __str__(self):
		return self.nom_agent

class Chargeimprevisionelle(models.Model):
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(null=True,max_length=200)
	username=models.CharField(max_length=200, null=False)

	chargeimp=models.FloatField(null=True,default=0)

	def __str__(self):
		return self.nom_agent

class Rendezvousopco(models.Model):
	COMPTEOPCP=(
		('OUI','OUI'),
		('NON','NON')
	)

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)


	nom_entreprise=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	ville=models.CharField(max_length=200, null=True)
	code_postal=models.IntegerField(null=False)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	siret=models.IntegerField(null=False)
	codeape=models.CharField(max_length=200, null=True)
	secteur_activite=models.CharField(max_length=200,default='NON', null=False,choices=COMPTEOPCP)
	identifiant=models.CharField(max_length=200, null=True,blank=True)
	mdp=models.CharField(max_length=200, null=True,blank=True)
	telephone_comptable=models.IntegerField(null=True,blank=True)
	formation_souhaite=models.CharField(max_length=200,null=False)
	effectife_salarie=models.IntegerField(null=False)
	dont=models.IntegerField(null=False)
	date_rendez_vous=models.DateField(null=False)
	etat=models.IntegerField(default=1)
	heure=models.CharField(max_length=200, null=False)
	date_appel=models.DateField(null=True)
	date_rappel=models.DateField(null=True)
	benefice=models.FloatField(default=0,null=True)

	def __str__(self):
		return self.nom_agent

class Rendezvousenergie(models.Model):
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	ville=models.CharField(max_length=200, null=True)
	code_postal=models.IntegerField(null=False)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	age=models.IntegerField(null=True,default=0,validators=[MaxValueValidator(80), MinValueValidator(15)])
	Description=models.CharField(max_length=200, null=True)
	date_rendez_vous=models.DateField(null=False)
	etat=models.IntegerField(default=1)
	heure=models.CharField(max_length=200, null=False)
	date_appel=models.DateField(null=True)
	date_rappel=models.DateField(null=True)
	benefice=models.FloatField(default=0,null=True)

	def __str__(self):
		return self.nom_agent
	
class Rendezvousmutuelle(models.Model):
	CHOICES1=(
			('OUI','OUI'),
			('NON','NON')
		)
	CHOICES2=(
			('PHYSIQUE','PHYSIQUE'),
			('TELEPHONIQUE','TELEPHONIQUE')
		)

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	ville=models.CharField(max_length=200, null=True)
	code_postal=models.IntegerField(null=False)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	date_naissance=models.DateField(null=False)
	seule=models.CharField(max_length=200, null=False,choices=CHOICES1)

	Description=models.CharField(max_length=200, null=True)
	date_rendez_vous=models.DateField(null=False)
	note=models.IntegerField(null=True,default=0,validators=[MaxValueValidator(10), MinValueValidator(0)])
	etat=models.IntegerField(default=1)
	typerv=models.CharField(max_length=200, null=False,choices=CHOICES2)
	benefice=models.FloatField(default=0,null=True)

	def __str__(self):
		return self.nom_agent

class Stockagerendezvousmutuelle(models.Model):



	nom_client=models.CharField(max_length=200, null=False)
	prenom_client=models.CharField(max_length=200, null=False)
	adresse=models.CharField(max_length=200, null=False)
	ville=models.CharField(max_length=200, null=False)
	code_postal=models.IntegerField(null=False)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	date_naissance=models.DateField(null=False)
	commentaire=models.CharField(null=True,max_length=200)

	typerv=models.CharField(max_length=200, null=False)

	def __str__(self):
		return self.nom_client

class Rendezvousmutuellevente(models.Model):
	CHOICES1=(
			('OUI','OUI'),
			('NON','NON')
		)
	CHOICES2=(
			('PHYSIQUE','PHYSIQUE'),
			('TELEPHONIQUE','TELEPHONIQUE')
		)

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	localite=models.CharField(max_length=200, null=True)
	code_postal=models.IntegerField(null=False)
	mutuellevendue=models.CharField(max_length=200, null=True)	
	formule=models.CharField(max_length=200, null=True)
	cotisation=models.FloatField(default=0, null=False)
	ancienne=models.CharField(max_length=200, null=True)
	date_vente=models.DateField(null=True)
	date_effet=models.DateField(null=True)
	nomcommercial=models.CharField(max_length=200, null=True)	

	date_naissance=models.DateField(null=True)
	description=models.CharField(max_length=200, null=True)	


	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	etat=models.IntegerField(default=1)



	def __str__(self):
		return self.nom_agent

class Ventervmutellevente(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	prix=models.FloatField(default=0,null=True)
	rendezvousid=models.IntegerField(default=0,null=True)
	benefice=models.FloatField(default=0,null=True)

	def __str__(self):
		return self.nom_agent
	
class Venteecommerce(models.Model):

	AGES=(
			('de 15 à 18','de 15 à 18'),
			('de 18 à 30','de 18 à 30'),
			('de 30 à 50','de 30 à 50'),
			('50 ans et ++','50 ans et ++')
		)
	CHOIXX=(
			('Particulier','Particulier'),
			('Professionnel','Professionnel')
		)

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	date_rendez_vous=models.DateField(null=False)
	prix=models.FloatField(default=0,null=True)

	codepostal=models.CharField(max_length=200, null=True)
	ville=models.CharField(max_length=200, null=True)
	nomproduit=models.CharField(max_length=200, null=True)
	nomcategorie=models.CharField(max_length=200, null=True)
	quantite=models.CharField(max_length=200, null=True)
	trancheage = models.CharField(max_length=200, null=True, choices=AGES)
	colonne = models.CharField(max_length=200, null=False, choices=CHOIXX)

	def __str__(self):
		return self.nom_agent

class Suivicpf(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nbappel=models.IntegerField(null=False)
	nbfiche=models.IntegerField(null=False)
	nbminute=models.IntegerField(null=False)
	dmc=models.FloatField(null=False)
	nrp=models.IntegerField(null=False)
	nbhorscibleage=models.IntegerField(null=False)
	nbhorsciblebudget=models.IntegerField(null=False)
	nbpasinteresse=models.IntegerField(null=False)
	nbpasinteressecilble=models.IntegerField(null=False)
	nbrefuscategorique=models.IntegerField(null=False)
	nbrepondeur=models.IntegerField(null=False)
	nbvente=models.IntegerField(null=False)
	nbrendezvous=models.IntegerField(null=False)
	nbrappel=models.IntegerField(null=False)


	def __str__(self):
		return self.nom_agent

class Mutuellesante(models.Model):
	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nbappel=models.IntegerField(null=False)
	nbfiche=models.IntegerField(null=False)
	nbminute=models.IntegerField(null=False)
	dmc=models.FloatField(null=False)
	nrp=models.IntegerField(null=False)
	nbhorscibleage=models.IntegerField(null=False)
	nbmutuelleentreprise=models.IntegerField(null=False)
	nbpersonneengage=models.IntegerField(null=False)
	nbpasinteresse=models.IntegerField(null=False)
	nbpasinteressecilble=models.IntegerField(null=False)
	nbrefuscategorique=models.IntegerField(null=False)
	nbrepondeur=models.IntegerField(null=False)
	nbvente=models.IntegerField(null=False)
	nbrendezvous=models.IntegerField(null=False)
	nbrappel=models.IntegerField(null=False)

	



	def __str__(self):
		return self.nom_agent

class Suiviopco(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nbappel=models.IntegerField(null=False)
	nbfiche=models.IntegerField(null=False)
	nbminute=models.IntegerField(null=False)
	dmc=models.FloatField(null=False)
	nrp=models.IntegerField(null=False)
	nbhroscibleregime=models.IntegerField(null=False)
	nbpasinteresse=models.IntegerField(null=False)
	nbpasinteressecilble=models.IntegerField(null=False)
	nbrefuscategorique=models.IntegerField(null=False)
	nbrepondeur=models.IntegerField(null=False)
	nbvente=models.IntegerField(null=False)
	nbrendezvous=models.IntegerField(null=False)
	nbrappel=models.IntegerField(null=False)


	def __str__(self):
		return self.nom_agent

class Suivienergitique(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nbappel=models.IntegerField(null=False)
	nbfiche=models.IntegerField(null=False)
	nbminute=models.IntegerField(null=False)
	dmc=models.FloatField(null=False)
	nrp=models.IntegerField(null=False)
	nbhroscibletechnique=models.IntegerField(null=False)
	nbpasinteresse=models.IntegerField(null=False)
	nbpasinteressecilble=models.IntegerField(null=False)
	nbrefuscategorique=models.IntegerField(null=False)
	nbrepondeur=models.IntegerField(null=False)
	nbvente=models.IntegerField(null=False)
	nbrendezvous=models.IntegerField(null=False)
	nbrappel=models.IntegerField(null=False)


	def __str__(self):
		return self.nom_agent

class Suivivoyance(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nbappel=models.IntegerField(null=False)
	nbfiche=models.IntegerField(null=False)
	nbminute=models.IntegerField(null=False)
	dmc=models.FloatField(null=False)
	nrp=models.IntegerField(null=False)
	nbhroscible=models.IntegerField(null=False)
	nbpasinteresse=models.IntegerField(null=False)
	nbpasinteressecilble=models.IntegerField(null=False)
	nbrefuscategorique=models.IntegerField(null=False)
	nbrepondeur=models.IntegerField(null=False)
	nbvente=models.IntegerField(null=False)
	nbrendezvous=models.IntegerField(null=False)
	nbrappel=models.IntegerField(null=False)


	def __str__(self):
		return self.nom_agent

class Produitecommerce(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nomproduit=models.CharField(max_length=200,null=True)


	def __str__(self):
		return self.nomproduit

class Categorieecommerce(models.Model):

	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	produitid=models.IntegerField(null=False)
	nomcategorie=models.CharField(max_length=200,null=False)
	quantite=models.IntegerField(null=False)
	prixunite_achat=models.FloatField(null=False)
	prixunite_vente=models.FloatField(null=False)
	depences=models.FloatField(null=False)
	benefices=models.FloatField(null=True,default=0)
	Nb_Vente=models.IntegerField(null=False,default=0)

	def __str__(self):
		return self.nomcategorie

class Rendezvousvoyance(models.Model):


	nom_agent=models.CharField(max_length=200, null=True)
	prenom_agent=models.CharField(max_length=200, null=True)
	user_id=models.IntegerField(null=False)
	user_admin=models.IntegerField(null=True,default=0)
	user_role=models.CharField(max_length=200,null=True)
	username=models.CharField(max_length=200, null=False)

	nom_client=models.CharField(max_length=200, null=True)
	prenom_client=models.CharField(max_length=200, null=True)
	adresse=models.CharField(max_length=200, null=True)
	ville=models.CharField(max_length=200, null=True)
	code_postal=models.IntegerField(null=False)
	telephone=models.IntegerField(null=False)
	email = models.EmailField(max_length=200)
	age = models.IntegerField(null=False)
	nom_voyant=models.CharField(max_length=200, null=True)
	prix = models.FloatField(max_length=200,null=True,default=0)
	description=models.CharField(max_length=200, null=False)
	date_rendez_vous=models.DateField(null=False)
	etat=models.IntegerField(default=1)

	def __str__(self):
		return self.nom_agent
