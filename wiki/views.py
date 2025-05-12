from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import *
from .forms import *


def articles_list(request):
    user_articles = []
    other_articles = Article.objects.all()

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            user_articles = Article.objects.filter(author=profile)
            other_articles = Article.objects.exclude(author=profile)
        except Profile.DoesNotExist:
            pass

    categorized_articles = defaultdict(list)
    for article in other_articles:
        categorized_articles[article.article_category].append(article)

    ctx = {
        'user_articles': user_articles,
        'categorized_articles': dict(categorized_articles)
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
