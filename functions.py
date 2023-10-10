from django.db.models import Count,Sum

from .models import *
from .forms import *




def total_charges(admin_id):
    total=0
    try:
        Chargefixe_sum_columns=Chargefixe.objects.filter(user_admin=admin_id).aggregate(loyer=Sum('loyer'),internet=Sum('internet'),telecom=Sum('telecom'),steg=Sum('steg'),soned=Sum('soned'),banque=Sum('banque'),retenuealasource=Sum('retenuealasource'),cnss=Sum('cnss'),comptable=Sum('comptable'))
        total_Chargefixe=(Chargefixe_sum_columns['loyer']+Chargefixe_sum_columns['internet']+Chargefixe_sum_columns['telecom']+Chargefixe_sum_columns['steg']+Chargefixe_sum_columns['soned']+Chargefixe_sum_columns['banque']+Chargefixe_sum_columns['retenuealasource']+Chargefixe_sum_columns['cnss']+Chargefixe_sum_columns['comptable'])
        

    
    except Exception: 
        total_Chargefixe =0
        
        

    try :
        Chargevariable_sum_columns=Chargevariable.objects.filter(user_admin=admin_id).aggregate(
            salaire=Sum('salaire'),credit=Sum('credit'),marketingdigitale=Sum('marketingdigitale'),
            voip=Sum('voip'),fiches=Sum('fiches'),crm=Sum('crm'),autres=Sum('autres'),
            hebergement=Sum('hebergement'),leads=Sum('leads'),voyants=Sum('voyants')
            )

        total_Chargevariable=( Chargevariable_sum_columns['salaire']+Chargevariable_sum_columns['credit']
        +Chargevariable_sum_columns['marketingdigitale']
        +Chargevariable_sum_columns['voip']+Chargevariable_sum_columns['fiches']+Chargevariable_sum_columns['crm']
        +Chargevariable_sum_columns['autres']+Chargevariable_sum_columns['hebergement']+Chargevariable_sum_columns['leads']+
        Chargevariable_sum_columns['voyants'])

    
    except Exception: 
        total_Chargevariable =0

    try :
        total_Chargeimprevisionelle=Chargeimprevisionelle.objects.filter(user_admin=admin_id).aggregate(
            chargeimp=Sum('chargeimp'))['chargeimp'] or 0


    
    except Exception:
        total_Chargeimprevisionelle =0


    total=total_Chargeimprevisionelle+total_Chargevariable+total_Chargefixe
    return total,total_Chargeimprevisionelle,total_Chargevariable,total_Chargefixe


