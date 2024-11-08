from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm
from .models import MessageContact
from .forms import LoginForm
from .models import Produit, Panier, LignePanier

def afficher_index(request):
    produits = Produit.objects.all()  # Récupère tous les produits
    return render(request, 'index.html', {'produits': produits})  # Passe les produits au template

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Enregistre le message de contact dans la base de données
            MessageContact.objects.create(
                nom=form.cleaned_data['nom'],
                email=form.cleaned_data['email'],
                sujet=form.cleaned_data['sujet'],
                message=form.cleaned_data['message']
            )
            # Ajouter un message de succès
            messages.success(request, "Votre message a été envoyé avec succès!")
            return redirect('contact')  # Redirige vers la page de contact pour afficher le message
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def cart_view(request):
    if request.user.is_authenticated:
        # Utilisateur connecté : Récupère les lignes du panier depuis la base de données
        panier = Panier.objects.filter(utilisateur=request.user).first()
        lignes = panier.lignes.all() if panier else []
    else:
        # Utilisateur non connecté : Récupère les produits depuis la session
        panier_session = request.session.get('panier', {})
        lignes = []
        for produit_id, details in panier_session.items():
            produit = Produit.objects.get(id=produit_id)
            lignes.append({
                'produit': produit,
                'quantite': details['quantite'],
                'prix': details['prix'],
            })

    return render(request, 'cart.html', {'lignes': lignes})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def product_details(request, id):
    produit = get_object_or_404(Produit, id=id)
    return render(request, 'product_details.html', {'produit': produit})


def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    if request.user.is_authenticated:
        # Utilisateur connecté : utilise le panier de l'utilisateur
        panier, created = Panier.objects.get_or_create(utilisateur=request.user)
        ligne, created = LignePanier.objects.get_or_create(panier=panier, produit=produit)
        
        if not created:
            ligne.quantite += 1
            ligne.save()
        
        return JsonResponse({
            'message': 'Produit ajouté',
            'new_quantity': ligne.quantite,
            'new_total': ligne.quantite * ligne.prix
        })
    else:
        # Utilisateur non connecté : utilise la session pour stocker le panier
        panier_session = request.session.get('panier', {})
        ligne = panier_session.get(str(produit_id), {'quantite': 0, 'prix': produit.prix})

        # Incrémente la quantité
        ligne['quantite'] += 1
        panier_session[str(produit_id)] = ligne
        request.session['panier'] = panier_session
        request.session.modified = True

        return JsonResponse({
            'message': 'Produit ajouté au panier',
            'new_quantity': ligne['quantite'],
            'new_total': ligne['quantite'] * ligne['prix']
        })


def diminuer_quantite(request, ligne_id):
    ligne = get_object_or_404(LignePanier, id=ligne_id)
    if ligne.quantite > 1:
        ligne.quantite -= 1
        ligne.save()
    else:
        ligne.delete()
    
    return JsonResponse({
        'message': 'Quantité réduite',
        'new_quantity': ligne.quantite if ligne.id else 0
    })


def supprimer_du_panier(request, ligne_id):
    ligne = get_object_or_404(LignePanier, id=ligne_id)
    ligne.delete()
    
    return JsonResponse({
        'message': 'Produit supprimé'
    })
