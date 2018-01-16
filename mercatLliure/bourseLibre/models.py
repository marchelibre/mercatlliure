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
        return "utilisateur:" + self.user.username

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
    couleurs = {'aliment':'#5f99de','vegetal':'#41b746','service':'#a68335','objet':'#c3bb4b'}
    choix = {
    'aliment': {
        'souscategorie': (('légumes', 'légumes'), ('fruits', 'fruits'), ('boisson', 'boisson'), ('herbes', 'herbes'),
                          ('condiments', 'condiments'), ('viande', 'viande'), ('poisson', 'poissson'),
                          ('boulangerie', 'boulangerie'), ('patisserie', 'patisserie'), ('autre', 'autre')),
        'etat': (('fr', 'frais'), ('se', 'sec'), ('cs', 'conserve')),
        'type_prix': (('kg', '/kg'), ('un', '/unité'), ('li', '/litre')),
    },
    'vegetal': {
        'souscategorie': (('graines', 'graines'), ('fleurs', 'fleurs'), ('plantes', 'plantes')),
        'etat': (('frais', 'frais'), ('séché', 'séché')),
        'type_prix': (('kg', '/kg'), ('un', '/unité'), ('li', '/litre')),
    },
    'service': {
        'souscategorie': (('jardinier', 'jardinier'), ('informaticien', 'informaticien'), ('electricen', 'electricien'),
                          ('plombier', 'plombier'), ('mécanicien', 'mécanicien'), ('autre', 'autre')),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('nul', 'nul')),
        'type_prix': (('kg', '/kg'), ('un', '/unité'), ('li', '/litre')),
    },
    'objet': {
        'souscategorie': (
        ('materiel', 'materiel'), ('vehicule', 'vehicule'), ('multimedia', 'multimedia'), ('mobilier', 'mobilier'),
        ('autre', 'autre'),),
        'etat': (('excellent', 'excellent'), ('bon', 'bon'), ('moyen', 'moyen'), ('mauvais', 'mauvais')),
        'type_prix': (('kg', '/kg'), ('un', '/unité'), ('li', '/litre')),
    }
}

#from polymorphic.models import PolymorphicModel

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
    prix = models.DecimalField(max_digits=5, decimal_places=2, default=1, validators=[MinValueValidator(0), ])
    unite_prix = models.CharField(
        max_length=6,
        choices=(('lliure', 'lliure'), ('eugros', 'eugros'), ('heures', 'heures'), ('troc', 'troc')),
        default='lliure', verbose_name="monnaie"
    )

    categorie = models.CharField(max_length=20,
                                 choices=(('aliment', 'aliment'),('vegetal', 'vegetal'), ('service', 'service'),
                                          ('objet', 'objet')),
                                 default='aliment')
    photo = models.ImageField(blank=True, upload_to="imagesProduits/")
    objects = InheritanceManager()
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

        return super(Produit, self).save(*args, **kwargs)

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
