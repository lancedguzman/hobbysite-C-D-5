from django.urls import path
from .views import thread_list, thread_details, thread_create, thread_update

urlpatterns = [
    path('forum/threads', thread_list, name='thread_list'),
    path('forum/thread/<int:id>', thread_details, name='thread_details'),
    path('forum/thread/add', thread_create, name='thread_create'),
    path('forum/thread/<int:id>/edit', thread_update, name='thread_update'),
]

app_name = 'forum'

