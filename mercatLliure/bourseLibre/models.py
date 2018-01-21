# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.utils.timezone import now
# from django.utils.formats import localize
from address.models import AddressField
import datetime
from model_utils.managers import InheritanceManager
import django_filters
from django.urls import reverse

# from datetimewidget.widgets import DateTimeWidget

class Panier(models.Model):
    listeProduits = []
    date_creation = models.DateTimeField(verbose_name="Date de création", editable=False)
    etat = "attente"

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_creation = timezone.now()
        return super(Panier, self).save(*args, **kwargs)

    def add_produit(self, produit):
        self.listeProduits.append(produit)

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    site_web = models.URLField(blank=True)
    description = models.TextField(null=True, default="")
    competences = models.TextField(null=True, default="")
    adresse = AddressField(null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    inscrit_newsletter = models.BooleanField(default=False)
    date_registration = models.DateTimeField(verbose_name="Date de création", editable=False)
    #panier = models.OneToOneField(Panier,on_delete=models.CASCADE,)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_registration = timezone.now()
            self.panier = Panier()
        return super(Profil, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()


class ChoixProduits():
    #couleurs = {'aliment':'#D8C457','vegetal':'#4CAF47','service':'#BE373A','objet':'#5B4694'}
    couleurs = {'aliment':'#D8AD57','vegetal':'#A9CB52','service':'#DA7BE4','objet':'#80B2C0'}
    choix = {
    'aliment': {
        'souscategorie': (('légumes', 'légumes'), ('fruits', 'fruits'), ('boisson', 'boisson'), ('herbes', 'herbes'),
                          ('condiments', 'condiments'), ('viande', 'viande'), ('poisson', 'poisson'),
                          ('boulangerie', 'boulangerie'), ('patisserie', 'patisserie'), ('autre', 'autre')),
        'etat': (('fr', 'frais'), ('se', 'sec'), ('cs', 'conserve')),
        'type_prix': (('kg', 'kg'), ('un', 'unité'), ('li', 'litre')),
    },
    'vegetal': {
        'souscategorie': (('graines', 'graines'), ('fleurs', 'fleurs'), ('plantes', 'plantes')),
        'etat': (('frais', 'frais'), ('séché', 'séché')),
        'type_prix': (('kg', 'kg'), ('un', 'unité'), ('li', 'litre')),
    },
    'service': {
        'souscategorie': (('jardinier', 'jardinier'), ('informaticien', 'informaticien'), ('electricen', 'electricien'),
                          ('plombier', 'plombier'), ('mécanicien', 'mécanicien'), ('autre', 'autre')),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('nul', 'nul')),
        'type_prix': (('kg', 'kg'), ('un', 'unité'), ('li', 'litre')),
    },
    'objet': {
        'souscategorie': (
        ('materiel', 'materiel'), ('vehicule', 'vehicule'), ('multimedia', 'multimedia'), ('mobilier', 'mobilier'),
        ('autre', 'autre'),),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('mauvais', 'mauvais')),
        'type_prix': (('kg', 'kg'), ('un', 'unité'), ('li', 'litre')),
    }
}

#from polymorphic.models import PolymorphicModel
from django.template.defaultfilters import slugify
# from shop.models import BaseProduct
class Produit(models.Model):  # , BaseProduct):
    user = models.ForeignKey(Profil, on_delete=models.CASCADE,)
    date_creation = models.DateTimeField(verbose_name="Date de parution", editable=False)
    date_debut = models.DateField(default=now, verbose_name="Date de debut")
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    date_expiration = models.DateField(verbose_name='date_expiration', default=proposed_renewal_date, )
    nom_produit = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    stock_initial = models.FloatField(verbose_name="Quantité disponible", default=1, max_length=250,
                                      validators=[MinValueValidator(1), ])
    stock_courant = models.FloatField(default=1, max_length=250, validators=[MinValueValidator(0), ])
    prix = models.DecimalField(max_digits=4, decimal_places=2, default=1, validators=[MinValueValidator(0), ])
    unite_prix = models.CharField(
        max_length=8,
        choices=(('don', 'don'),('soudaqui', 'soudaqui'), ('eugros', 'eugros'), ('heures', 'heures'), ('troc', 'troc')),
        default='lliure', verbose_name="monnaie"
    )

    CHOIX_CATEGORIE = (('aliment', 'aliment'),('vegetal', 'végétal'), ('service', 'service'),
                                          ('objet', 'objet'))
    categorie = models.CharField(max_length=20,
                                 choices=CHOIX_CATEGORIE,
                                 default='aliment')
    photo = models.ImageField(blank=True, upload_to="imagesProduits/")

    estUneOffre = models.BooleanField(default=True)

    objects = InheritanceManager()

    @property
    def slug(self):
        return slugify(self.nom_produit)

    # detail_categorie = None
    # type = "defaut"

    # etat = models.CharField(max_length=20)
    # type_prix = models.CharField(max_length=20)

    # class Meta:
    #      abstract = True

    def __str__(self):
        return self.nom_produit

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_creation = timezone.now()
            self.stock_courant = self.stock_initial

        return super(Produit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('produit_detail', kwargs={'produit_id':self.id})


from rest_framework import serializers
class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ('categorie','nom_produit','description','prix')


class ProductFilter(django_filters.FilterSet):
    #nom_produit = django_filters.CharFilter(lookup_expr='iexact')
    # date_creation = django_filters.DateFromToRangeFilter(name='date_creation',)
    # date_debut = django_filters.DateFromToRangeFilter(name='date_debut')
    # date_expiration = django_filters.DateFromToRangeFilter(name='date_expiration')
    categorie = django_filters.ChoiceFilter(label='categorie', lookup_expr='exact', )
    user__user__username = django_filters.ModelChoiceFilter(label='producteur', queryset=Profil.objects.all())
    nom_produit = django_filters.CharFilter(label='titre', lookup_expr='contains')
    description = django_filters.CharFilter(label='description', lookup_expr='contains')
    prixmin = django_filters.NumberFilter(label='prix min', lookup_expr='gt', name="prix")
    prixmax = django_filters.NumberFilter(label='prix max', lookup_expr='lt', name="prix")
    # date_debut = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}), label='date de début')
    date_debut = django_filters.TimeRangeFilter(label='date de début')
    # date_debut = django_filters.DateFilter(label='date de début')


    class Meta:
        model = Produit
        fields = ['categorie', 'user__user__username', 'nom_produit', "description", "prixmin","prixmax","date_debut"]
        # fields = {
        #      'categorie':['exact'],
        #     'nom_produit':['contains'],
        #     'description':['contains'],
        #     # 'date_creation': ['exact'],
        #     # 'date_debut': ['exact'],
        #     # 'date_expiration': ['exact'],
        #      'prix':['gte','lte'],
        # }
        exclude=('photo',)




class Produit_aliment(Produit):  # , BaseProduct):
    #proprietes = models.OneToOneField(Produit,on_delete=models.CASCADE, parent_link=True, )
    type = 'aliment'
    # categorie = models.CharField(max_length=20,
    #                              choices=(('aliment', 'aliment'),),
    #                              default='aliment')
    couleur = models.CharField(
        max_length=20,
        choices=((ChoixProduits.couleurs['aliment'],ChoixProduits.couleurs['aliment']),),
        default=ChoixProduits.couleurs['aliment']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['souscategorie'],
        default=ChoixProduits.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['etat'],
        default=ChoixProduits.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['type_prix'],
        default=ChoixProduits.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.date_creation = timezone.now()
    #     return super(Produit_aliment, self).save(*args, **kwargs)


class Produit_vegetal(Produit):  # , BaseProduct):
    #proprietes = models.OneToOneField(Produit,on_delete=models.CASCADE, parent_link=True )
    type = 'vegetal'
    # categorie = models.CharField(max_length=20,
    #                              choices=(('vegetal', 'vegetal'),),
    #                              default='vegetal')
    couleur = models.CharField(
        max_length=20,
        choices=((ChoixProduits.couleurs['vegetal'],ChoixProduits.couleurs['vegetal']),),
        default=ChoixProduits.couleurs['vegetal']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['souscategorie'],
        default=ChoixProduits.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['etat'],
        default=ChoixProduits.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['type_prix'],
        default=ChoixProduits.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.date_creation = timezone.now()
    #     return super(Produit_vegetaux, self).save(*args, **kwargs)


class Produit_service(Produit):  # , BaseProduct):
    #proprietes = models.OneToOneField(Produit,on_delete=models.CASCADE, parent_link=True)
    type = 'service'
    # categorie = models.CharField(max_length=20,
    #                              choices=(('service', 'service'),),
    #                              default='service')
    couleur = models.CharField(
        max_length=20,
        choices=((ChoixProduits.couleurs['service'],ChoixProduits.couleurs['service']),),
        default=ChoixProduits.couleurs['service']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix["service"]['souscategorie'],
        default=ChoixProduits.choix["service"]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix["service"]['etat'],
        default=ChoixProduits.choix["service"]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix["service"]['type_prix'],
        default=ChoixProduits.choix["service"]['type_prix'][0][0], verbose_name="par"
    )
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.date_creation = timezone.now()
    #     return super(Produit_services, self).save(*args, **kwargs)


class Produit_objet(Produit):  # , BaseProduct):
    #proprietes = models.OneToOneField(Produit,on_delete=models.CASCADE, parent_link=True)
    type = 'objet'
    # categorie = models.CharField(max_length=20,
    #                              choices=(('objet', 'objet'),),
    #                              default='objet')
    couleur = models.CharField(
        max_length=20,
        choices=((ChoixProduits.couleurs['objet'],ChoixProduits.couleurs['objet']),),
        default=ChoixProduits.couleurs['objet']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['souscategorie'],
        default=ChoixProduits.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['etat'],
        default=ChoixProduits.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=ChoixProduits.choix[type]['type_prix'],
        default=ChoixProduits.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.date_creation = timezone.now()
    #     return super(Produit_objets, self).save(*args, **kwargs)
