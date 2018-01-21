# -*- coding: utf-8 -*-
'''
Created on 25 mai 2017

@author: tchenrezi
'''
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect  # render_to_response,
from .forms import ProduitCreationForm, Produit_aliment_CreationForm, Produit_vegetal_CreationForm, Produit_objet_CreationForm, \
    Produit_service_CreationForm, ProducteurCreationForm, ContactForm
from .models import Profil, Produit, ChoixProduits, ProductFilter#, Produit_aliment, Produit_service, Produit_objet, Produit_vegetal
# from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import mail_admins
# from itertools import chain


def bienvenue(request):
    return render(request, 'bienvenue.html')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/login/')
def proposerProduit(request, typeProduit):
    try:
        bgcolor = ChoixProduits.couleurs[typeProduit]
    except:
        bgcolor = None

    #produit_form = ProduitCreationForm(request.POST or None, request.FILES or None)
    if typeProduit == 'aliment':
        type_form = Produit_aliment_CreationForm(request.POST or None, request.FILES or None)
    elif typeProduit == 'vegetal':
        type_form = Produit_vegetal_CreationForm(request.POST or None, request.FILES or None)
    elif typeProduit == 'service':
        type_form = Produit_service_CreationForm(request.POST or None, request.FILES or None)
    elif typeProduit == 'objet':
        type_form = Produit_objet_CreationForm(request.POST or None, request.FILES or None)
    else:
        raise Exception('Type de produit inconnu (aliment, vegetal, service ou  objet)')
    # if produit_form.is_valid() and type_form.is_valid():
    if  type_form.is_valid():
       # produit = produit_form.save(commit=False)
        produit = type_form.save(commit=False)
        produit.user = Profil.objects.get(pk=request.user.id)
        produit.categorie = typeProduit
        if produit.photo:
            produit.photo = request.FILES['photo']
            file_type = produit.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'produit': produit, 'form': produit_form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'bourseLibre/produit_proposer.html', context)

        produit.save()
        # type = type_form.save(commit=False)
        # type.proprietes = produit
        # type.save()
        return HttpResponseRedirect('/produits/detail/' + str(produit.id))
    return render(request, 'bourseLibre/produit_proposer.html', {"form": type_form, "bgcolor": bgcolor, "typeProduit":typeProduit})

class ProduitModifier(UpdateView):
    model = Produit
    template_name_suffix = '_modifier'
    fields = ['date_debut','date_expiration','nom_produit', 'description', 'prix', 'unite_prix', 'categorie', 'photo', 'estUneOffre',]# 'souscategorie','etat','type_prix']

class ProduitSupprimer(DeleteView):
    model = Produit
    success_url = reverse_lazy('produit_lister')

@login_required(login_url='/login/')
def proposerProduit_entree(request):
    return render(request, 'bourseLibre/produit_proposer_entree.html',  {"couleurs":ChoixProduits.couleurs})


# @login_required
# def supprimerProduit(request, produit_id):
#     produit = Produit.objects.get(pk=produit_id)
#     produit.delete()
#     produit = Produit.objects.filter(user=request.user)
#     return render(request, 'indexProduits.html', {'produit': produit})

@login_required
def detailProduit(request, produit_id):
    prod = Produit.objects.get_subclass(pk=produit_id)
    return render(request, 'bourseLibre/produit_detail.html', {'produit': prod})


def merci(request, template_name='merci.html'):
    return render(request, template_name)


# @login_required
# def index(request):
#         produits = Produit.objects.filter(user=request.user)
#         query = request.GET.get("q")
#         if query:
#             produits = produits.filter(
#                 Q(album_title__icontains=query) | 
#                 Q(artist__icontains=query)
#             ).distinct()
#             return render(request, 'index.html', {
#                 'produits': produits,
#             })
#         else:
#             return render(request, 'index.html', {'produits': produits})

def profilcourant(request, ):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, 'profil.html', {'user': user})


def profil(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return render(request, 'profil.html', {'user': user})
    except User.DoesNotExist:
        return render(request, 'profilInconnu.html', {'userid': user_id})

def profilInconnu(request):
    return render(request, 'profilInconnu.html')


def register(request):
    form = ProducteurCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user = form.save(commit=True)
        return render(request, 'userenattente.html')
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password1']
    #         user = authenticate(username=username,password=password)
    #         if user is not None:
    #             if user.is_active:
    #                 user.backend = 'django.contrib.auth.backends.ModelBackend'
    #                 login(request, user)
    #                 produits = Produit.objects.all()
    #                 return render(request, 'index.html', {'produits': produits})

    return render(request, 'register.html', {"form": form})

class ListeProduit(ListView):
    model = Produit
    context_object_name = "produits_list"
    template_name = "produit_list.html"
    paginate_by = 18

    def get_queryset(self):
        qs = Produit.objects.select_subclasses()
        params = dict(self.request.GET.items())
        if "producteur" in params:
            qs = qs.filter(user__user__username=params['producteur'])
        if "categorie" in params:
            qs = qs.filter(categorie=params['categorie'])
        if "prixmax" in params:
            qs = qs.filter(prix__lt=params['prixmax'])
        if "prixmin" in params:
            qs = qs.filter(prix__gtt=params['prixmin'])
        if "monnaie" in params:
            qs = qs.filter(unite_prix=params['monnaie'])
        if "gratuit" in params:
            qs = qs.filter(unite_prix='don')

        return qs.order_by('categorie','user')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        listee = Profil.objects.values_list('user__username', flat=True).distinct()
        context['producteur_list'] = listee
        return context

# from django_filters import rest_framework as filters
# from rest_framework import generics
# from .models import ProduitSerializer
#
# class ProductList(generics.ListAPIView):
#     queryset = Produit.objects.all().select_subclasses()
#     filter_backends = (filters.DjangoFilterBackend,)
#     serializer_class = ProduitSerializer
#
# def product_list(request):
#     f = ProductFilter(request.GET, queryset=Produit.objects.all().select_subclasses())
#     return render(request, 'templateList.html', {'filter': f})

    # res = [Produit_aliment.objects.all(), Produit_vegetal.objects.all(), Produit_service.objects.all(), Produit_objet.objects.all()]
    # queryset = list(chain(*res))
    #queryset = qs=[Produit_aliment.objects.all(), Produit_vegetal.objects.all(), Produit_service.objects.all(), Produit_objet.objects.all())


    # def get_queryset(self):
    #     filter_val = self.request.GET.get('filter', 'give-default-value')
    #     order = self.request.GET.get('orderby', 'give-default-value')
    #     new_context = Update.objects.filter(
    #         state=filter_val,
    #     ).order_by(order)
    #     return new_context

    #
    # def get_context_data(self, **kwargs):
    #     context = super(MyView, self).get_context_data(**kwargs)
    #     context['filter'] = self.request.GET.get('filter', 'give-default-value')
    #     context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
    #     return context

# class ListeProduitFiltre(ListView):
#     model = Produit
#     context_object_name = "produits_list"
#     template_name = "produit_list.html"
#     paginate_by = 18
#
#     def get_queryset(self):
#         qs = Produit.objects.select_subclasses()
#         params = dict(self.request.GET.items())
#         if "filtrer_producteur" in params:
#             qs = qs.filter(user__user__username=self.request.GET.get('filtrer_producteur') )
#
#         if "categorie" in self.kwargs:
#            # return list(chain(*([Produit_aliment.objects.filter(proprietes__categorie=self.kwargs["categorie"]), Produit_vegetal.objects.filter(proprietes__categorie=self.kwargs["categorie"]), Produit_service.objects.filter(proprietes__categorie=self.kwargs["categorie"]), Produit_objet.objects.filter(proprietes__categorie=self.kwargs["categorie"])])))
#             return qs.filter(categorie=self.kwargs["categorie"]).select_subclasses()
#         elif "producteur" in self.kwargs:
#            # return list(chain(*([Produit_aliment.objects.filter(proprietes__user__user__username=self.kwargs["producteur"]), Produit_vegetal.objects.filter(proprietes__user__user__username=self.kwargs["producteur"]), Produit_service.objects.filter(proprietes__user__user__username=self.kwargs["producteur"]), Produit_objet.objects.filter(proprietes__user__user__username=self.kwargs["producteur"])])))
#             return qs.filter(user__user__username=self.kwargs["producteur"]).select_subclasses()
#         else:
#             return qs
#             #return list(chain(*([Produit_aliment.objects.all(), Produit_vegetal.objects.all(), Produit_service.objects.all(), Produit_objet.objects.all()])))
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the publisher
#         if "categorie" in self.kwargs:
#             context['typeFiltre'] = "categorie"
#             context['filtre'] = self.kwargs["categorie"]
#         elif "producteur" in self.kwargs:
#             context['typeFiltre'] = "producteur"
#             context['filtre'] = self.kwargs['producteur']
#         return context
#
#
# class ListeProduitCategorie(ListView):
#     model = Produit
#     context_object_name = "produits_list"
#     template_name = "produit_list.html"
#     paginate_by = 18
#
#     def get_queryset(self):
#         return Produit.objects.filter(categorie=self.kwargs["categorie"])
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the publisher
#         context['typeFiltre'] = "categorie"
#         context['filtre'] = self.kwargs["categorie"]
#         print(context)
#         return context
#
# class ListeProduitProducteur(ListView):
#     model = Produit
#     context_object_name = "produits_list"
#     template_name = "produit_list.html"
#     paginate_by = 18
#
#     def get_queryset(self):
#         return Produit.objects.filter(user__username=self.kwargs["producteur"])
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the publisher
#         context['typeFiltre'] = "producteur"
#         context['filtre'] = context['user.username']
#         return context

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message'] + '(par : ' + form.cleaned_data['envoyeur'] + ')'
        #         envoyeur = form.cleaned_data['envoyeur']
        mail_admins(sujet, message)

        #         try:
        #             f.save()
        #             print("success")
        #             messages.add_message(request, messages.SUCCESS, 'Feedback sent!')
        #         except:
        #             print("failed")
        #             messages.add_message(request, messages.INFO, 'Unable to send feedback. Try agian')

        #         send_mail( sujet,message, envoyeur, to=['labourselibre@gmail.com'], fail_silently=False,)
        #         if renvoi:
        #             mess = "message envoyé a la bourse libre : \\n"
        #             send_mail( sujet,mess + message, envoyeur, to=[envoyeur], fail_silently=False,)

    return render(request, 'contact.html', {'form': form})
