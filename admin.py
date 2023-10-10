from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import Account 


# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete=False
    verbose_name_plural= 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines =(AccountInline, )

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)
admin.site.register(Account)
admin.site.register(Bilan)
admin.site.register(Event)
admin.site.register(Suivi)
admin.site.register(Rendezvous)
admin.site.register(Stockage)
admin.site.register(Chargevariable)
admin.site.register(Chargefixe)
admin.site.register(Chargeimprevisionelle)
admin.site.register(Rendezvousopco)
admin.site.register(Rendezvousenergie)
admin.site.register(Rendezvousmutuelle)
admin.site.register(Stockagerendezvousmutuelle)
admin.site.register(Rendezvousmutuellevente)
admin.site.register(Ventervmutellevente)
admin.site.register(Venteecommerce)
admin.site.register(Suivicpf)
admin.site.register(Mutuellesante)
admin.site.register(Suiviopco)
admin.site.register(Suivienergitique)
admin.site.register(Suivivoyance)
admin.site.register(Produitecommerce)
admin.site.register(Categorieecommerce)
admin.site.register(Rendezvousvoyance)










