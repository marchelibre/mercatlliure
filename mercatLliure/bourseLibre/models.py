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

from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
import decimal


class ChoixProduits():
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
        'souscategorie': ('jardinier', 'informaticien', 'electricen', 'plombier', 'mécanicien', 'autre'),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('nul', 'nul')),
        'type_prix': (('h', 'heure'), ('un', 'unité')),
    },
    'objet': {
        'souscategorie': ('materiel','vehicule', 'multimedia', 'mobilier','autre'),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('mauvais', 'mauvais')),
        'type_prix': typePrixUnite,
    }
    }

def get_categorie_from_subcat(subcat):
    for typeProduit, dico in ChoixProduits.choix.items():
        if subcat in dico['souscategorie']:
            return typeProduit
    return "Categorie inconnue (souscategorie : " + str(subcat) +")"



class Profil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    site_web = models.URLField(blank=True)
    description = models.TextField(null=True, default="")
    competences = models.TextField(null=True, default="")
    adresse = AddressField(null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    inscrit_newsletter = models.BooleanField(default=False)
    date_registration = models.DateTimeField(verbose_name="Date de création", editable=False)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_registration = now()
        return super(Profil, self).save(*args, **kwargs)

    def get_nom_class(self):
        return "Profil"

    def get_absolute_url(self):
        return reverse('profil', kwargs={'user_id':self.id})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)
        Panier.objects.create(user=Profil.objects.get(user=instance))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()



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

    CHOIX_CATEGORIE = (('aliment', 'aliment'),('vegetal', 'vegetal'), ('service', 'service'), ('objet', 'objet'))
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
        choices=((ChoixProduits.couleurs['aliment'],ChoixProduits.couleurs['aliment']),),
        default=ChoixProduits.couleurs['aliment']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in ChoixProduits.choix[type]['souscategorie']),
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
        choices=((ChoixProduits.couleurs['vegetal'],ChoixProduits.couleurs['vegetal']),),
        default=ChoixProduits.couleurs['vegetal']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in ChoixProduits.choix[type]['souscategorie']),
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
        choices=((ChoixProduits.couleurs['service'],ChoixProduits.couleurs['service']),),
        default=ChoixProduits.couleurs['service']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in ChoixProduits.choix[type]['souscategorie']),
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
        choices=((ChoixProduits.couleurs['objet'],ChoixProduits.couleurs['objet']),),
        default=ChoixProduits.couleurs['objet']
    )
    souscategorie = models.CharField(
        max_length=20,
        choices=((cat,cat) for cat in ChoixProduits.choix[type]['souscategorie']),
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
