# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User#, AbstractUser
#from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.utils.timezone import now
# from django.utils.formats import localize
#from address.models import AddressField
import datetime
from model_utils.managers import InheritanceManager
import django_filters
from django.urls import reverse, reverse_lazy

from django.template.defaultfilters import slugify

from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
import decimal

import requests

# from location_field.models import spatial

#from django.contrib.gis.db import models as models_gis
# from django.contrib.gis.geos import Point
#from geoposition.fields import GeopositionField

#from django.contrib.gis.db.models import GeoManager

class Choix():
    #couleurs = {'aliment':'#D8C457','vegetal':'#4CAF47','service':'#BE373A','objet':'#5B4694'}
    couleurs = {'aliment':'#D8AD57','vegetal':'#A9CB52','service':'#E66562','objet':'#80B2C0'}
    typePrixUnite =  (('kg', 'kg'), ('100g', '100g'), ('10g', '10g'),('g', 'g'),  ('un', 'unité'), ('li', 'litre'))

    choix = {
    'aliment': {
        'souscategorie': ('légumes', 'fruits', 'champignons', 'boisson', 'herbes','condiments', 'viande','poisson','boulangerie','patisserie', 'autre'),
        'etat': (('fr', 'frais'), ('se', 'sec'), ('cs', 'conserve')),
        'type_prix': typePrixUnite,
    },
    'vegetal': {
        'souscategorie': ('graines', 'fleurs', 'plantes','autre'),
        'etat': (('frais', 'frais'), ('séché', 'séché')),
        'type_prix': typePrixUnite,
    },
    'service': {
        'souscategorie': ('jardinier', 'informaticien', 'electricien', 'plombier', 'mécanicien', 'autre'),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('nul', 'nul')),
        'type_prix': (('h', 'heure'), ('un', 'unité')),
    },
    'objet': {
        'souscategorie': ('materiel','vehicule', 'multimedia', 'mobilier','autre'),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('mauvais', 'mauvais')),
        'type_prix': typePrixUnite,
    },
    'monnaies': (('don', 'don'), ('soudaqui', 'soudaqui'), ('heuresT', 'heuresT'), ('troc', 'troc')),

    }

def get_categorie_from_subcat(subcat):
    for typeProduit, dico in Choix.choix.items():
        if subcat in dico['souscategorie']:
            return typeProduit
    return "Categorie inconnue (souscategorie : " + str(subcat) +")"

LATITUDE_DEFAUT = '42.6976'
LONGITUDE_DEFAUT = '2.8954'
#from django.contrib.gis.db import models as models_gis
class Adresse(models.Model):
    rue = models.CharField(max_length=200, blank=True, null=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True, default="66000")
    latitude = models.FloatField(blank=True, null=True, default=LATITUDE_DEFAUT)
    longitude = models.FloatField(blank=True, null=True, default=LONGITUDE_DEFAUT)
    pays = models.CharField(max_length=12, blank=True, null=True, default="France")
    telephone = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.set_latlon_from_adresse()
        return super(Adresse, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('profil_courant')

    def set_latlon_from_adresse(self):
        address = ''
        if self.rue:
            address += self.rue + ", "
        address += self.code_postal + ", " + self.pays
        api_key = "AIzaSyCmGcPj0ti_7aEagETrbJyHPbE3U6gVfSA"
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

        if api_response_dict['status'] == 'OK':
            self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']




    def get_latitude(self):
        if not self.latitude:
            return LATITUDE_DEFAUT
        return str(self.latitude).replace(",",".")

    def get_longitude(self):
        if not self.longitude:
            return LONGITUDE_DEFAUT
        return str(self.longitude).replace(",",".")


# class Profil(AbstractBaseUser):
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    site_web = models.URLField(blank=True)
    description = models.TextField(null=True, default="")
    competences = models.TextField(null=True, default="")
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/", default='avatar/avatar-defaut2.jpg')
    inscrit_newsletter = models.BooleanField(default=False)
    date_registration = models.DateTimeField(verbose_name="Date de création", editable=False)

    # position = models_gis.PointField()
    # code_postal = models_gis.CharField(max_length=5)
    # #objects = GeoManager()
    # lon = models.FloatField()
    # lat = models.FloatField()

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_registration = now()
        if not self.adresse:
            self.adresse = Adresse.objects.create()
        return super(Profil, self).save(*args, **kwargs)

    def get_nom_class(self):
        return "Profil"

    def get_absolute_url(self):
        return reverse('profil_courant')#, kwargs={'user_id':self.id})
#
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        adresse = Adresse.objects.create()
        Profil.objects.create(user=instance, adresse=adresse)
        Panier.objects.create(user=Profil.objects.get(user=instance))


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profil.save()



class Produit(models.Model):  # , BaseProduct):
    user = models.ForeignKey(Profil, on_delete=models.CASCADE,)
    date_creation = models.DateTimeField(verbose_name="Date de parution", editable=False)
    date_debut = models.DateField(default=now, verbose_name="Débute le : (jj/mm/an)", null=True, blank=True)
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    date_expiration = models.DateField(verbose_name="Expire le : (jj/mm/an)", blank=True, null=True, default=proposed_renewal_date, )
    nom_produit = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100)

    stock_initial = models.FloatField(verbose_name="Quantité disponible", default=1, max_length=250,
                                      validators=[MinValueValidator(1), ])
    stock_courant = models.FloatField(default=1, max_length=250, validators=[MinValueValidator(0), ])
    prix = models.DecimalField(max_digits=4, decimal_places=2, default=1, validators=[MinValueValidator(0), ])
    unite_prix = models.CharField(
        max_length=8,
        choices = Choix.choix['monnaies'],
        default='lliure', verbose_name="monnaie"
    )

    CHOIX_CATEGORIE = (('aliment', 'aliment'),('vegetal', 'végétal'), ('service', 'service'), ('objet', 'objet'))
    categorie = models.CharField(max_length=20,
                                 choices=CHOIX_CATEGORIE,
                                 default='aliment')
    photo = models.ImageField(blank=True, upload_to="imagesProduits/")


    estUneOffre = models.BooleanField(default=True, verbose_name='Offre ? (ou demande)')

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
            self.date_creation = now()
            self.stock_courant = self.stock_initial

        return super(Produit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('produit_detail', kwargs={'produit_id':self.id})

    def get_type_prix(self):
        return Produit.objects.get_subclass(id=self.id).type_prix

    def get_unite_prix(self):
        if self.unite_prix == "don":
            return self.unite_prix
        else:
            return Produit.objects.get_subclass(id=self.id).get_unite_prix()
            # return prod.get_unite_prix()

    def get_prix(self):
        if self.unite_prix == "don":
            return 0
        else:
            return self.prix

    def get_nom_class(self):
        return "Produit"

    def get_souscategorie(self):
        return"standard"



class Produit_aliment(Produit):  # , BaseProduct):
    type = 'aliment'
    couleur = models.CharField(
        max_length=20,
        choices=((Choix.couleurs['aliment'], Choix.couleurs['aliment']),),
        default=Choix.couleurs['aliment']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in Choix.choix[type]['souscategorie']),
        default=Choix.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['etat'],
        default=Choix.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['type_prix'],
        default=Choix.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    def get_unite_prix(self):
        if self.unite_prix == "don":
            return self.unite_prix
        else:
            return self.unite_prix + "/" + self.type_prix

    def get_prixEtUnite(self):
        if self.unite_prix == "don":
            return 'gratuit'
        return str(self.get_prix()) + " " + self.get_unite_prix()

    def get_souscategorie(self):
        return"aliment"

class Produit_vegetal(Produit):  # , BaseProduct):
    type = 'vegetal'
    couleur = models.CharField(
        max_length=20,
        choices=((Choix.couleurs['vegetal'], Choix.couleurs['vegetal']),),
        default=Choix.couleurs['vegetal']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in Choix.choix[type]['souscategorie']),
        default=Choix.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['etat'],
        default=Choix.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['type_prix'],
        default=Choix.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    def get_unite_prix(self):
        if self.unite_prix == "don":
            return self.unite_prix
        else:
            return self.unite_prix + "/" + self.type_prix

    def get_prixEtUnite(self):
        if self.unite_prix == "don":
            return 'gratuit'
        return str(self.get_prix()) + " " + self.get_unite_prix()

    def get_souscategorie(self):
        return"vegetal"

class Produit_service(Produit):  # , BaseProduct):
    type = 'service'
    couleur = models.CharField(
        max_length=20,
        choices=((Choix.couleurs['service'], Choix.couleurs['service']),),
        default=Choix.couleurs['service']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in Choix.choix[type]['souscategorie']),
        default=Choix.choix["service"]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=Choix.choix["service"]['etat'],
        default=Choix.choix["service"]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=Choix.choix["service"]['type_prix'],
        default=Choix.choix["service"]['type_prix'][0][0], verbose_name="par"
    )
    def get_unite_prix(self):
        if self.unite_prix == "don":
            return self.unite_prix
        else:
            return self.unite_prix + "/" + self.type_prix

    def get_prixEtUnite(self):
        if self.unite_prix == "don":
            return 'gratuit'
        return str(self.get_prix()) + " " + self.get_unite_prix()

    def get_souscategorie(self):
        return "service"

class Produit_objet(Produit):  # , BaseProduct):
    type = 'objet'
    couleur = models.CharField(
        max_length=20,
        choices=((Choix.couleurs['objet'], Choix.couleurs['objet']),),
        default=Choix.couleurs['objet']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in Choix.choix[type]['souscategorie']),
        default=Choix.choix[type]['souscategorie'][0][0]
    )
    etat = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['etat'],
        default=Choix.choix[type]['etat'][0][0]
    )
    type_prix = models.CharField(
        max_length=20,
        choices=Choix.choix[type]['type_prix'],
        default=Choix.choix[type]['type_prix'][0][0], verbose_name="par"
    )
    def get_unite_prix(self):
        if self.unite_prix == "don":
            return self.unite_prix
        else:
            return self.unite_prix + "/" + self.type_prix

    def get_prixEtUnite(self):
        if self.unite_prix == "don":
            return 'gratuit'
        return str(self.get_prix()) + " " + self.get_unite_prix()

    def get_souscategorie(self):
        return "objet"

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

# from rest_framework import serializers
# class ProduitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Produit
#         fields = ('categorie','nom_produit','description','prix')


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




class Panier(models.Model):
    date_creation = models.DateTimeField(verbose_name=_('date de création '), editable=False)
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    etat = models.CharField(
        max_length=8,
        choices=(('a', 'en cours'),('ok', 'validé'), ('t', 'terminé'), ('c', 'annulé')),
        default='a', verbose_name="état"
    )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_creation = now()
        return super(Panier, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('panier')
        verbose_name_plural = _('paniers')
        ordering = ('-date_creation',)

    def __unicode__(self):
        #return unicode(self.date_creation)
        return self.date_creation

    def __iter__(self):
        for item in self.item_set.all():
            yield item

    def get_nom_class(self):
        return "Panier"


    def add(self, produit, unit_price, quantite=1):
        try:
            item = Item.objects.get(
                panier=self,
                produit=produit,
            )
        except Item.DoesNotExist:
            item = Item()
            item.panier = self
            item.produit = produit
            item.quantite = quantite
            item.save()
        else: #ItemAlreadyExists
            item.quantite += decimal.Decimal(quantite).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)
            item.save()

    def remove(self, produit):
        try:
            item = Item.objects.get(
                panier=self,
                produit=produit,
            )
        except Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, produit, quantite):
        try:
            item = Item.objects.get(
                panier=self,
                produit=produit,
            )
        except Item.DoesNotExist:
            raise ItemDoesNotExist
        else: #ItemAlreadyExists
            if quantite == 0:
                item.delete()
            else:
                item.quantite =  decimal.Decimal(quantite).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)
                item.save()

    def total_quantite(self):
        result = 0
        for item in self.item_set.all():
            result += 1 * item.quantite
        return result

    def total_prix(self):
        result = 0
        for item in self.item_set.all():
            result += item.total_prix
        return result

    def clear(self):
        for item in self.item_set.all():
            item.delete()

    total_prix = property(total_prix)
    total_quantite = property(total_quantite)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        # if 'produit' in kwargs:
        #     kwargs['produit'] = Produit.objects.get(type(kwargs['produit'])).select_subclasses()
        #     kwargs['object_id'] = kwargs['produit'].pk
        #     del(kwargs['produit'])
        return super(ItemManager, self).get(*args, **kwargs)



class Item(models.Model):
    panier = models.ForeignKey(Panier, verbose_name=_('panier'), on_delete=models.CASCADE)
    quantite = models.DecimalField(verbose_name=_('quantite'),decimal_places=3,max_digits=6)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('panier',)

    def __unicode__(self):
        return u'%s units of %s' % (self.quantite, self.produit.nom_produit)

    def total_prix(self):
        if self.produit.unite_prix == 'don':
            return 0
        return self.quantite * self.produit.get_prix()
    total_prix = property(total_prix)

#
# class Place(models_gis.Model):
#     ville = models_gis.CharField(max_length=255)
#     #location = spatial.LocationField(based_fields=['ville'], zoom=7, default=Point(1.0, 1.0))
#     location = spatial.PlainLocationField(based_fields=['ville'], zoom=7)
#     objects = models_gis.GeoManager()