from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import *
from .forms import *


def articles_list(request):
    categories = ArticleCategory.objects.order_by('name').prefetch_related('article_set')
    user_articles = []
    other_articles = Article.objects.all()

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_articles = Article.objects.filter(author=request.user.profile).order_by('-created_on')
        other_articles = Article.objects.exclude(author=request.user.profile).order_by('-created_on')
    else:
        user_articles = []
        other_articles = Article.objects.all().order_by('-created on')


    ctx = {
        'user_articles': user_articles,
        'other_articles' : other_articles,
        'categories' : categories
    }

    return render(request, 'articles.html', ctx)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article).order_by('-created_on')
    related_articles = Article.objects.filter(article_category=article.article_category).exclude(pk=article.pk)[:2]
    form = CommentForm()

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = request.user.profile
                comment.save()
                return redirect('wiki:article_detail', pk=article.pk)
        else:
            form = CommentForm()

    
    ctx = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'form': form,
    }

    return render(request, 'article_detail.html', ctx)


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect('wiki:article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return render(request, 'article_create.html', {'form': form})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('wiki:article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'article_update.html', {'form': form})
