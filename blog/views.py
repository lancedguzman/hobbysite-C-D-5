from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleCategory
from .forms import ArticleForm, CommentForm
from django.urls import reverse

def list_view(request):
    categories = ArticleCategory.objects.order_by('name').prefetch_related('article_set')

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        author_articles = Article.objects.filter(author=request.user.profile).order_by('-created_on')
        other_articles = Article.objects.exclude(author=request.user.profile).order_by('-created_on')
    else:
        author_articles = []
        other_articles = Article.objects.all().order_by('-created_on')

    context = {
        'author_articles': author_articles,
        'other_articles': other_articles,
        'categories': categories,
    }

    return render(request, 'article_list.html', context)

def detail_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comment_set.select_related('author').order_by('-created_on')
    related_articles = Article.objects.filter(author=article.author).exclude(id=article.id)[:2]

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user.profile
            comment.save()
            return redirect('blog:detail_view', article_id=article.id)
    else:
        comment_form = CommentForm()

    can_edit = request.user.is_authenticated and request.user.profile == article.author

    context = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'comment_form': comment_form,
        'can_edit': can_edit,
    }

    return render(request, 'article_content.html', context)

@login_required
def create_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect(reverse('blog:list_view'))
    else:
        form = ArticleForm()
    return render(request, "create_article.html", {"form": form})

@login_required
def update_view(request, article_id): 
    article = get_object_or_404(Article, id=article_id)

    if not hasattr(request.user, 'profile') or request.user.profile != article.author:
        return redirect(reverse('blog:detail_view', args=[article.id]))

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:detail_view', args=[article.id]))
    else:
        form = ArticleForm(instance=article)

    return render(request, 'update_article.html', { 
        'form': form,
        'article': article,
    })