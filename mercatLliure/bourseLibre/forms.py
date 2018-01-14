from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, User
from .models import Produit, Produit_aliment, Produit_objet, Produit_service, Produit_vegetal
import datetime
#from datetimewidget.widgets import DateTimeWidget

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


fieldsCommunsProduits = ['souscategorie', 'photo', 'nom_produit', 'description', 'date_debut', 'date_expiration',
                'etat', 'stock_initial', 'prix', 'unite_prix', 'type_prix', ]

# fieldsCommunsProduits = ['type_prix', 'souscategorie', 'etat']
#
class ProduitCreationForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude=('user', )
        #fields ='__all__'

        #fields = fieldsCommunsProduits

        fields = ['photo', 'nom_produit', 'description', 'date_debut', 'date_expiration',
                  'stock_initial', 'prix', 'unite_prix',  ]
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


class Produit_vegetal_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_vegetal
        fields =fieldsCommunsProduits
        #fields ='__all__'
       # exclude = ('proprietes',)

class Produit_service_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_service
        fields =fieldsCommunsProduits
        #fields ='__all__'
        #exclude = ('proprietes',)
        #['souscategorie', 'photo', 'nom_produit', 'description', 'date_debut', 'date_expiration',
         #         'prix', 'unite_prix', 'type_prix', ]


class Produit_objet_CreationForm(forms.ModelForm):
    class Meta:
        model = Produit_objet
        fields =fieldsCommunsProduits
        #fields ='__all__'
        #exclude = ('proprietes',)

# widgets = { 'date_debut': forms.DateTimeInput(attrs={'class': 'datetime-input'})}

class ProducteurCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    competences = forms.CharField(label="competences", widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    avatar = forms.ImageField(required=False)
    inscrit_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'description', 'competences', 'inscrit_newsletter']
    #

    def save(self, commit=True):
        user = super(ProducteurCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.description = self.cleaned_data['description']
        user.password = self.cleaned_data['password1']

        if commit:
            user.save()

        return user


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
