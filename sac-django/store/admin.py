from django.contrib import admin
from .models import Produit, MessageContact, Panier, LignePanier, Commande, LigneCommande
# Register your models here.
admin.site.register(Produit)
admin.site.register(MessageContact)
admin.site.register(Panier)
admin.site.register(LignePanier)
admin.site.register(Commande)
admin.site.register(LigneCommande)