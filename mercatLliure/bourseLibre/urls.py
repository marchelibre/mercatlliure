# -*- coding: utf-8 -*-
"""bourseLibre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog__ import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog__/', include(blog_urls))
"""
from django.conf.urls import include, url
#from django.contrib import admin
from . import views
#from shop import urls as shop_urls

# On import les vues de Django, avec un nom spécifique
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# admin.autodiscover()
from django.contrib import admin
# from django_filters.views import FilterView
# from .models import Produit, ProductFilter

urlpatterns = [
    url(r'^$', views.bienvenue, name='bienvenue'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^merci', views.merci, name='merci'),
    url(r'^blog/', include('blog.urls', namespace='bourseLibre.blog')),
    # url(r'^search/', include('haystack.urls'), name='chercher_site'),
url(r'^search/', include('haystack.urls'), name='haystack_search'),
    url(r'^chercher/produit/', login_required(views.chercher, login_url='/login/'), name='chercher'),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)$', views.profil, name='profil',),
    url(r'^accounts/profile/(?P<user_username>[-A-Za-z]+)$', views.profil_nom, name='profil_nom',),
    #url(r'^accounts/profile/(<user_id>[a-zA-Z0-9.]+)', views.profil, name='profil',),
    url(r'^accounts/profile/', views.profilcourant, name='profilcourant',),
    url(r'^accounts/profile/inconnu/$', views.profilInconnu, name='profilInconnu',),
    url(r'^register/', views.register, name='register',),
    url(r'^login', auth_views.login,  name='login_user', ),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout_user', ),
    url(r'^contact', views.contact, name='contact',),
    url(r'^passwordchange', auth_views.password_change, name='password_change',),
    url(r'^produits/proposer/(?P<typeProduit>[-A-Za-z]+)/$', login_required(views.proposerProduit, login_url='/login/'), name='produit_proposer',),
    url(r'^produits/proposer/', login_required(views.proposerProduit_entree, login_url='/login/'), name='produit_proposer_entree',),
    #url(r'^shop/', include(shop_urls)), # <-- That's the important bit

# url(r'^list$', views.product_list),
#     url(r'^list2/$', FilterView.as_view(model=Produit, filterset_class=ProductFilter,)),
#     url(r'^list3/$', views.ProductList.as_view()),
#     url(r'^produits/lister/categorie/(?P<categorie>[a-z]+)$', login_required(views.ListeProduitFiltre.as_view(), login_url='/login/'),  name="produit_lister_categorie"),
#     url(r'^produits/lister/producteur/(?P<producteur>[a-z]+)$',login_required(views.ListeProduitFiltre.as_view(), login_url='/login/'), name='produit_lister_producteur'),
    url(r'^produits/lister/', login_required(views.ListeProduit.as_view(), login_url='/login/'),
        name="produit_lister"),
    url(r'^produits/detail/(?P<produit_id>[0-9]+)/$', views.detailProduit, name='produit_detail',),

    url(r'^produits/modifier/(?P<pk>[0-9]+)/$',
        login_required(views.ProduitModifier.as_view(), login_url='/login/'), name='produit_modifier', ),
    # url(r'^produits/ajouter/(?P<pk>[0-9]+)/$',
    #     login_required(views.ProduitModifier.as_view(), login_url='/login/'), name='produit_ajouterAuPanier', ),
    url(r'^produits/contacterProducteur/(?P<pk>[0-9]+)/$',
        login_required(views.ProduitModifier.as_view(), login_url='/login/'), name='produit_contacterProducteur', ),
    url(r'^produits/supprimer/(?P<pk>[0-9]+)/$',
        login_required(views.ProduitSupprimer.as_view(), login_url='/login/'), name='produit_supprimer', ),

    url(r'^panier/afficher/$',
        login_required(views.afficher_panier, login_url='/login/'), name='panier_afficher', ),

    url(r'^panier/ajouter/(?P<produit_id>[0-9]+)/(?P<quantite>[0-9]{1,3}([.]{0,1}[0-9]{0,3}))/$',
        login_required(views.ajouterAuPanier, login_url='/login/'), name='produit_ajouterAuPanier', ),
]

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns
# if settings.DEBUG:
#     # static files (img, css, javascript, etc.)
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT}))