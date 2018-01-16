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

urlpatterns = [
    url(r'^$', views.bienvenue, name='bienvenue'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^merci', views.merci, name='merci'),
    url(r'^blog/', include('blog.urls', namespace='bourseLibre.blog')),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)$', views.profil, name='profil',),
    #url(r'^accounts/profile/(<user_id>[a-zA-Z0-9.]+)', views.profil, name='profil',),
    url(r'^accounts/profile/', views.profilcourant, name='profilcourant',),
    url(r'^accounts/profile/inconnu/$', views.profilInconnu, name='profilInconnu',),
    url(r'^register/', views.register, name='register',),
    url(r'^login', auth_views.login,  name='login_user', ),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout_user', ),
    url(r'^contact', views.contact, name='contact',),
    url(r'^passwordchange', auth_views.password_change, name='password_change',),
    url(r'^produits/proposerProduit/(?P<typeProduit>[-A-Za-z]+)/$', views.proposerProduit, name='proposerProduit',),
    url(r'^produits/proposerProduit/', views.proposerProduit_entree, name='proposerProduit_entree',),
    #url(r'^shop/', include(shop_urls)), # <-- That's the important bit
    url(r'^produits/listerProduits/$', login_required(views.ListeProduit.as_view(), login_url='/login/'),
        name="afficheProduitsDispo"),

    url(r'^produits/listerProduits/categorie/(?P<categorie>[a-z]+)$', login_required(views.ListeProduitFiltre.as_view(), login_url='/login/'),  name="afficheProduitsDispo_categorie"),
    url(r'^produits/listerProduits/producteur/(?P<producteur>[a-z]+)$',login_required(views.ListeProduitFiltre.as_view(), login_url='/login/'), name='afficheProduitsDispo_producteur'),
    url(r'^produits/detailProduit/(?P<produit_id>[0-9]+)/$', views.detailProduit, name='detailProduit',),
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