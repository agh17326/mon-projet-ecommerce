
from django.urls import path
from . import views

urlpatterns = [
    path('', views.afficher_index, name='index'),
    path('contact/', views.contact_view, name='contact'), 
    path('cart/', views.cart_view, name='cart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('diminuer_quantite/<int:ligne_id>/', views.diminuer_quantite, name='diminuer_quantite'),
    path('supprimer_du_panier/<int:ligne_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
]




