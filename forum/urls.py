from django.urls import path
from .views import thread_list, thread_details, thread_create, thread_update

urlpatterns = [
    path('threads', thread_list, name='thread_list'),
    path('thread/<int:id>', thread_details, name='thread_details'),
    path('thread/add', thread_create, name='thread_create'),
    path('thread/<int:id>/edit', thread_update, name='thread_update'),
]

app_name = 'forum'

