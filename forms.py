from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account, Bilan, Chargefixe, Chargeimprevisionelle, Chargevariable, Event, Rendezvous, Rendezvousenergie, Rendezvousmutuelle, Rendezvousmutuellevente, Rendezvousopco, Stockagerendezvousmutuelle, Suivi
from django.db import models
#from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.contrib.admin.widgets import AdminTimeWidget

from .models import Stockage,Venteecommerce,Suivicpf,Mutuellesante,Suiviopco,Suivienergitique,Suivivoyance,Produitecommerce,Categorieecommerce,Rendezvousvoyance

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']
	
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class AccountForm(ModelForm):
	class Meta:
		model=Account
		fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'

class BilanForm(ModelForm):
	class Meta:
		model = Bilan
		fields = ['nom_client','prenom_client','age','secteur_activite','nom_formation','nbre_heure','prix_formation','date_debut'
		,'categorie','numdesecu','centre_formation','commentaire']
		widgets = {'date_debut': DateInput(),}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
		
valid_time_formats = ['%P', '%H:%M%A', '%H:%M %A', '%H:%M%a', '%H:%M %a']
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['title','start_date','end_date']
		widgets = {'start_date': DateInput(),
					'end_date': DateInput(),
				
		}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
		
class SuiviForm(ModelForm):
	class Meta:
		model=Suivi
		fields = ['nbre_sec','nbre_min']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			
class UserUpdateForm(ModelForm):
	class Meta:
		model=User
		fields = ['email','first_name','last_name']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	
class RendezvousForm(ModelForm):
	class Meta:
		model=Rendezvous
		fields = ['nom_client','prenom_client','phone_number','date_rendez_vous','date_rendez_vous_prochain','secteur','objet'
		,'periode_exercise','trancheage','numdesecu','formationsouhaitee','date_appel']
		widgets = {'date_rendez_vous': DateInput(),
					'date_rendez_vous_prochain': DateInput(),
					'date_appel': DateInput()}
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	
class StockageForm(ModelForm):

	class Meta:
		model=Stockage
		fields="__all__"
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class ChargevariableForm(ModelForm):
	class Meta:
		model=Chargevariable
		fields = ['salaire','credit','marketingdigitale','voip','fiches','crm','hebergement','leads','voyants','autres']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class ChargefixeForm(ModelForm):
	class Meta:
		model=Chargefixe
		fields = ['loyer','internet','telecom','steg','soned','banque','retenuealasource','cnss','comptable']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class ChargeimprevisionelleForm(ModelForm):
	class Meta:
		model=Chargeimprevisionelle
		fields = ['chargeimp']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	
class RendezvousopcoForm(ModelForm):
	class Meta:
		model = Rendezvousopco
		fields = ['nom_entreprise','adresse','ville','code_postal','telephone','email','siret','codeape','secteur_activite'
		,'telephone_comptable','formation_souhaite','effectife_salarie','dont','date_rendez_vous'
		,'date_appel','date_rappel']
		widgets = {'date_rendez_vous': DateInput(),
		'date_appel': DateInput(),
		'date_rappel': DateInput()}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class RendezvousenergieForm(ModelForm):
	class Meta:
		model = Rendezvousenergie
		fields = ['nom_client','prenom_client','ville','code_postal','telephone','email','adresse','age','Description','date_rendez_vous'
		,'date_appel','date_rappel']
		widgets = {'date_rendez_vous': DateInput(),
		'date_appel': DateInput(),
		'date_rappel': DateInput()}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class RendezvousmutuelleForm(ModelForm):
	class Meta:
		model = Rendezvousmutuelle
		fields = ['nom_client','prenom_client','adresse','ville','code_postal','telephone','email','date_naissance','seule','Description','date_rendez_vous','typerv']
		widgets = {'date_rendez_vous': DateInput(),
		'date_naissance': DateInput(),}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class RendezvousmutuelleventeForm(ModelForm):
	class Meta:
		model = Rendezvousmutuellevente
		fields = ['nom_client','prenom_client','adresse','localite','code_postal','telephone','email','mutuellevendue','formule',
		'cotisation','ancienne','date_vente','date_effet','nomcommercial','date_naissance','description']
		widgets = {'date_vente': DateInput(),
		'date_effet': DateInput(),
		'date_naissance':DateInput()}
		

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class VenteecommerceForm(ModelForm):
	class Meta:
		model = Venteecommerce
		fields = ['nom_client','prenom_client','adresse','telephone','email','date_rendez_vous','prix','codepostal','ville','nomproduit',
		'nomcategorie','quantite','trancheage','colonne']
		widgets = {'date_rendez_vous': DateInput(),
		'date_naissance': DateInput(),}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class SuivicpfForm(ModelForm):
	class Meta:
		model = Suivicpf
		fields = ['nbappel','nbfiche','nbminute','dmc','nrp','nbhorscibleage','nbhorsciblebudget',
		'nbpasinteresse','nbpasinteressecilble','nbrefuscategorique','nbrepondeur','nbvente','nbrendezvous','nbrappel']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class MutuellesanteForm(ModelForm):
	class Meta:
		model = Mutuellesante
		fields = ['nbappel','nbfiche','nbminute','dmc','nrp','nbhorscibleage','nbpersonneengage','nbmutuelleentreprise',
		'nbpasinteresse','nbpasinteressecilble','nbrefuscategorique','nbrepondeur','nbvente','nbrendezvous','nbrappel']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
		
class SuiviopcoForm(ModelForm):
	class Meta:
		model = Suiviopco
		fields = ['nbappel','nbfiche','nbminute','dmc','nrp','nbhroscibleregime',
		'nbpasinteresse','nbpasinteressecilble','nbrefuscategorique','nbrepondeur','nbvente','nbrendezvous','nbrappel']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class SuivienergitiqueForm(ModelForm):
	class Meta:
		model = Suivienergitique
		fields = ['nbappel','nbfiche','nbminute','dmc','nrp','nbhroscibletechnique',
		'nbpasinteresse','nbpasinteressecilble','nbrefuscategorique','nbrepondeur','nbvente','nbrendezvous','nbrappel']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class SuivivoyanceForm(ModelForm):
	class Meta:
		model = Suivivoyance
		fields = ['nbappel','nbfiche','nbminute','dmc','nrp','nbhroscible',
		'nbpasinteresse','nbpasinteressecilble','nbrefuscategorique','nbrepondeur','nbvente','nbrendezvous','nbrappel']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class ProduitecommerceForm(ModelForm):
	class Meta:
		model = Produitecommerce
		fields = ['nomproduit']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

class CategorieecommerceForm(ModelForm):
	class Meta:
		model = Categorieecommerce
		fields = ['nomcategorie']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
		
class RendezvousvoyanceForm(ModelForm):
	class Meta:
		model = Rendezvousvoyance
		fields = ['nom_client','prenom_client','ville','code_postal','telephone','email','adresse','age','date_rendez_vous',
		'nom_voyant','description']
		widgets = {'date_rendez_vous': DateInput(),}

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'