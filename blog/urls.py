from django.urls import path
from .views import list_view, detail_view, create_view, update_view

urlpatterns = [
    path('articles/', list_view, name='list_view'),
    path('article/<int:article_id>/', detail_view, name='detail_view'),
    path('article/create/', create_view, name='create_view'),
    path('article/<int:article_id>/edit/', update_view, name='update_view')
] 

app_name = 'blog'