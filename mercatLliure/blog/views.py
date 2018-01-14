# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
# from django.db.models import Q
from .models import Article, Commentaire
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

def accueil(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all()  # Nous sélectionnons tous nos articles
    return render(request, 'blog/accueil.html', {'derniers_articles': articles})


@login_required(login_url='/login/')
def ajouterNouveauPost(request):
#     if not request.user.is_authenticated():
#         return render(request, 'login.html')
#     else:
        form = ArticleForm(request.POST or None)
        if form.is_valid():
            article = form.save(request.user.profil)
            return render(request, 'blog/lireArticle.html', {'article': article})
        return render(request, 'blog/ajouterPost.html', { "form": form, })

    
    
# def index(request):
#     all_posts = Post.objects.all().order_by('-date')
#     template_data = {'posts' : all_posts}
#  
#     return render_to_response('index.html', template_data)

# def lire(request,slug):
#     
#     article = get_object_or_404(Article, slug=slug)
#     return render(request, 'blog/lire.html', {'article':article})


def lireArticle(request, slug):
    article = get_object_or_404(Article, slug=slug)
#     try:
    commentaires = Commentaire.objects.filter(article=article)
    #print ('zzzzz' + commentaires)
#     except:
#         commentaires = None
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        request.session["nom"] = comment.nom
        request.session["email"] = comment.email
        request.session["siteweb"] = comment.siteweb
        return redirect(request.path)
    
    form.initial['nom'] = request.session.get('nom')
    form.initial['email'] = request.session.get('email')
    form.initial['siteweb'] = request.session.get('siteweb')
    return render(request, 'blog/lireArticle.html', { 'article': article, 'form': form, 'commentaires':commentaires},)


class ListeArticles(ListView):
    model = Article
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"
    paginate_by = 5