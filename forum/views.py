from django.shortcuts import render, get_object_or_404
from .models import post_category, post


def thread_list(request):
    posts = post.objects.all()
    return render(request, 'thread_list.html', {"posts": posts})

def thread_details(request, id):
    print(f"Looking for post with id: {id}")
    post_id = get_object_or_404(post, id=id)
    return render(request, "thread_details.html", {"post": post_id})