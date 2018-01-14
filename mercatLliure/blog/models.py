from django.db import models
from bourseLibre.models import Profil

# from django.contrib.auth.forms import User

# Create your models here.
# class Post(models.Model):
#     title = models.CharField(max_length=64)
#     date = models.DateTimeField()
#     author = models.ForeignKey(User)
#     body = models.TextField()
#  
#     def __str__(self):
#         return "%s (%s)" % (self.title, self.author.name)
#     
    
class Article(models.Model):
    categorie = models.CharField(max_length=30,         
        choices=(('Histoire', 'Histoire'), ('Bon plan', 'Bon plan'), ('Descriptif', 'Descriptif'), ('autre','autre'),),
        default='Histoire', verbose_name="categorie")
    titre = models.CharField(max_length=100)
    auteur = models.ForeignKey(Profil)
    slug = models.SlugField(max_length=100)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    
    class Meta:
        ordering = ('date', )
        
    def __str__(self):
        return self.titre
    
#     @models.permalink
#     def get_url(self):
#         return ('blog_post_detail', (), 
#                 {
#                     'slug' :self.slug,
#                 })

class Commentaire(models.Model):
    nom = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    siteweb = models.URLField(max_length=200, null=True, blank=True)
    commentaire = models.TextField()
    article = models.ForeignKey(Article)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.commentaire