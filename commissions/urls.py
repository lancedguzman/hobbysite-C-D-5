from django.urls import path
from . import views

# Namespace for reverse() or {% url %} calls
app_name = "commissions"

urlpatterns = [
    # List all commissions
    path('list/', views.commissions_list, name='commissions_list'),

    # Create a new commission
    path('create/', views.commission_create, name='commission_create'),

    # View details of a specific commission
    path('detail/<int:id>/', views.commission_detail, name='commission'),

    # Update a commission
    path('update/<int:pk>/', views.commission_update, name='commission_update'),

    # View and manage a specific job's applicants
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]
