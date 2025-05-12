from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, ThreadCategory, Comment
from .forms import CommentForm, ThreadForm

def thread_list(request):
    user_threads = Thread.objects.none()
    remaining_threads = Thread.objects.all()
    categories = ThreadCategory.objects.all()

    if (request.user.is_authenticated) and hasattr(request.user, 'profile'):
        user_profile = request.user.profile
        user_threads = Thread.objects.filter(author=user_profile)
        remaining_threads = Thread.objects.exclude(author=user_profile)

    categorized_threads = {}
    for category in categories:
        categorized_threads[category] = remaining_threads.filter(category=category)

    content = {'user_threads': user_threads, 'categorized_threads': categorized_threads}

    return render(request, 'thread_list.html', content)

def thread_details(request, id):
    post_id = get_object_or_404(Thread, id=id)
    more_threads = Thread.objects.filter(category=post_id.category)
    comments = Comment.objects.filter(thread=post_id)
            
    content = {'thread': post_id, 'comments': comments, 'more_threads': more_threads}

    if request.method == 'POST':
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            form = CommentForm(request.POST)
            content += form
            if form.is_valid():
                comment = form.save(commit = False)
                comment.author = request.user.profile
                comment.thread = post_id
                comment.save()
                return redirect('thread_details', id=post_id.id)

    return render(request, "thread_details.html", content)

@login_required
def thread_create(request):
    if not hasattr(request.user, 'profile'):
        return redirect('thread_list')

    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit = False)
            thread.author = request.user.profile
            thread.save()
            return redirect('thread_details', id=thread.id)
    else:
            form = ThreadForm()

    return render(request, 'thread_form.html', {'form': form})

@login_required
def thread_update(request, id):
    thread = get_object_or_404(Thread, id=id)

    if not hasattr(request.user, 'profile') or thread.author != request.user.profile:
        return redirect('thread_details', id=id)

    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_details', id=thread.id)
    else:
            form = ThreadForm(instance=thread)

    return render(request, 'thread_form.html', {'form': form})
