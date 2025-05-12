from django.urls import path
from .views import thread_list, thread_details

urlpatterns = [
    path('forum/threads', thread_list, name='thread_list'),
    path('forum/thread/<int:id>', thread_details, name='thread_details')
]

