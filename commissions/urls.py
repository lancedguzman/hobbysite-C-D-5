from django.urls import path
from . import views

app_name = "commissions"

urlpatterns = [
    path('list/', views.commissions_list, name='commissions_list'),
    path('add/', views.commission_create, name='commission_create'),
    path('detail/<int:id>/', views.commission_detail, name='commission'),
    path('<int:pk>/edit/', views.commission_update, name='commission_update'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]