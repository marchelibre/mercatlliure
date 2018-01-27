from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, User
from .models import Produit, Produit_aliment, Produit_objet, Produit_service, Produit_vegetal, Adresse, Profil

#import datetime
#from datetimewidget.widgets import DateTimeWidget
#from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
#from address.forms import AddressField

# class yourForm(forms.ModelForm):
#     class Meta:
#         model = yourModel
#         widgets = {
#         #Use localization and bootstrap 3
#         'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
#         }


#validateur:
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
#
# def validate_even(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )
#
# class MyForm(forms.Form):
#     even_field = forms.IntegerField(validators=[validate_even])


fieldsCommunsProduits = ['souscategorie', 'photo', 'nom_produit', 'etat',   'description', 'date_debut', 'date_expiration',
                'unite_prix', 'prix',  'type_prix', 'stock_initial',]

# fieldsCommunsProduits = ['type_prix', 'souscategorie', 'etat']
#
class ProduitCreationForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude=('user', )
        #fields ='__all__'

        #fields = fieldsCommunsProduits

        fields = ['photo', 'nom_produit', 'description', 'date_debut', 'date_expiration',
                  'stock_initial', 'unite_prix','prix',   ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}),
            'date_expiration': forms.DateInput(attrs={'type':"date"})
        }

        # widgets = {
        #     # 'date_debut': DateTimeWidget(attrs={'id':"date_debut"}, usel10n = True, bootstrap_version=4),
        #     # 'date_expiration': DateWidget(attrs={'id':"date_expiration"}, usel10n = True, bootstrap_version=4),
        #     'date_debut' : forms.DateInput(attrs={'class' : 'date_picker'}),
        #     'date_expiration' : forms.DateInput(attrs={'class' : 'date_picker2'})
        # }
        # widgets = {
        #     'text': forms.TextInput(attrs={
        #         'id': 'post-text',
        #         'required': True,
        #         'placeholder': 'Say something...'
        #     }),
        # model = Produit
        # fields = fieldsCommuns
    # def clean_date_debut(self):
    #     data = self.cleaned_data['date_debut']
    #     # Check date is not in past.
    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid date - date_debut'))
    #
    #     # Remember to always return the cleaned data.
    #     return data
    #
    # def clean_date_expiration(self):
    #     data = self.cleaned_data['date_expiration']
    #     data_debut = self.cleaned_data['date_debut']
        # Check date is not in past.
        # if data < datetime.date.today():
        #     raise ValidationError(_('Invalid date - date_expiration'))
        # if data < data_debut:
        #     raise ValidationError(_('Invalid date - date_expiration doi etre apres la date de debut'))

        # def __init__(self, *args, **kwargs):
        #     super(FooForm, self).__init__(*args, **kwargs)
        #     if self.fields
        #     self.fields['foo'].choices = foo_choices
        #
        # foo = forms.ChoiceField(choices=(), required=True)
    # def save(self, commit=True):
    #     produit = super(ProduitCreationForm, self).save(commit=False)
    #
    #     if commit:
    #         produit.save()
    #
    #     return produit
    # date_debut = forms.DateField(widget=widgets.AdminDateWidget)
    # def __init__(self, *args, **kwargs):
    #     super(ProduitCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['date_debut'].widget = widgets.AdminDateWidget()

    # class Meta:
    #     abstract = True
        # model = Produit
        # widgets = {
        #     #Use localization and bootstrap 3
        #     'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=4)
        # }
        # fields = ['categorie', 'photo', 'nom_produit', 'description', 'date_debut', 'date_expiration', 'etat',
        #           'stock_initial', 'prix', 'unite_prix', 'type_prix', ]

class Produit_aliment_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_aliment
        fields =fieldsCommunsProduits
        #exclude = ('proprietes',)
        #fields ='__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}),
            'date_expiration': forms.DateInput(attrs={'type':"date"})
        }


class Produit_vegetal_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_vegetal
        fields =fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}),
            'date_expiration': forms.DateInput(attrs={'type':"date"})
        }
        #fields ='__all__'
       # exclude = ('proprietes',)

class Produit_service_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_service
        fields =fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}),
            'date_expiration': forms.DateInput(attrs={'type':"date"})
        }
        #fields ='__all__'
        #exclude = ('proprietes',)
        #['souscategorie', 'photo', 'nom_produit', 'description', 'date_debut', 'date_expiration',
         #         'prix', 'unite_prix', 'type_prix', ]


class Produit_objet_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_objet
        fields =fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}),
            'date_expiration': forms.DateInput(attrs={'type':"date"})
        }
        #fields ='__all__'
        #exclude = ('proprietes',)

# widgets = { 'date_debut': forms.DateTimeInput(attrs={'class': 'datetime-input'})}
class AdresseForm(forms.ModelForm):
    rue = forms.CharField(label="Adresse", required=False)
    code_postal = forms.CharField(label="Code postal*", initial="66000")
    latitude = forms.FloatField(label="Latitude", initial="42", required=False)
    longitude = forms.FloatField(label="Longitude", initial="2", required=False)
    pays = forms.CharField(label="Pays", initial="France",required=False)
    telephone = forms.FloatField(label="Téléphone", required=False)

    class Meta:
        model = Adresse
        fields = '__all__'
        exclude = ('latitude', 'longitude')
    # def save(self, *args, **kwargs):
    #     import requests
    #
    #     address = self.cleaned_data['rue'] + ", "+ self.cleaned_data['code_postal']
    #     api_key = "AIzaSyCmGcPj0ti_7aEagETrbJyHPbE3U6gVfSA"
    #     api_response = requests.get(
    #         'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    #     api_response_dict = api_response.json()
    #
    #     if api_response_dict['status'] == 'OK':
    #         self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
    #         self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']
    #     return super(AdresseForm, self).save(*args, **kwargs)

class ProfilCreationForm(forms.ModelForm):
    class Meta:
        model = Profil
        exclude = ['user', 'adresse']

    # def save(self, user, adresse):
    #     profil = super(ProfilCreationForm, self).save(commit=False)
    #     profil.user = user
    #     profil.adresse = adresse
    #     profil.save()
    #     return profil


class ProducteurCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=False)
    username = forms.CharField(label="pseudonyme")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                #  'competences', 'rue', 'code_postal', 'latitude', 'longitude', 'pays', 'telephone'
                  ]
    #

    def save(self, commit=True, is_active = False):
        user = super(ProducteurCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username =self.cleaned_data['username']
        user.set_password(self.cleaned_data['password1'])
        user.is_active = is_active
        user.is_superuser = False

        if commit:
            user.save()
        return user

    # def save(self,):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email= self.cleaned_data['email']
    #     user.username=self.cleaned_data['username']
    #     user.password= self.cleaned_data['password1']
    #     user.is_active=False
    #     user.is_superuser=False
    #
    #     adresse =  Adresse.objects.create(
    #         rue=self.cleaned_data['rue'],
    #         code_postal=self.cleaned_data['code_postal'],
    #         latitude=self.cleaned_data['latitude'],
    #         longitude=self.cleaned_data['longitude'],
    #         pays=self.cleaned_data['pays'],
    #         telephone=self.cleaned_data['telephone'])
    #
    #     user.save()
    #     adresse.save()
    #     profil = Profil.objects.create(adresse=adresse,
    #                                    description=self.cleaned_data['description'],
    #                                    competences=self.cleaned_data['competences'])
    #
    #     #profil= super(ProfilCreationForm, self).save(commit=False)
    #     profil.user=user
    #     profil.adresse=adresse
    #     profil.description=self.cleaned_data['description']
    #     profil.competences=self.cleaned_data['competences']
    #     # profil = Profil.objects.create(user=user,
    #     #                                adresse=adresse,
    #     #                                description=self.cleaned_data['description'],
    #     #                                competences=self.cleaned_data['competences'])
    #
    #     profil.save()
    #
    #     return profil


    # def save(self, commit=True):
    #     user = super(ProducteurCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.username = self.cleaned_data['username']
    #     user.description = self.cleaned_data['description']
    #     user.password = self.cleaned_data['password1']
    #
    #     if commit:
    #         user.save()
    #
    #     return user


class ProducteurChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username")
    description = forms.CharField()
    competences = forms.CharField(label="competences")
    avatar = forms.ImageField(required=False)
    inscrit_newsletter = forms.BooleanField(required=False)

    def __init__(self, *args, **kargs):
        super(ProducteurChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'description', 'competences', 'inscrit_newsletter']


class ContactForm(forms.Form):
    envoyeur = forms.EmailField(label="Votre adresse mail")
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    # renvoi = forms.BooleanField(label="recevoir une copie",
    #                             help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)
    # class UserForm(forms.ModelForm):
    #     class Meta:
    #         model = User
    #         fields = ('first_name', 'last_name', 'email')
    #
    # class ProfileForm(forms.ModelForm):
    #     class Meta:
    #         model = Profil
    #         fields = ('site_web', 'description', 'avatar', 'inscrit_newsletter')

    # class ConnexionForm(forms.Form):
    #     username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    #     password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

#
# from .models import Place
#
#
# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Place
#         exclude = ()

