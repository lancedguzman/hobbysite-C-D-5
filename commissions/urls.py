from django.urls import path
from . import views


# Namespace for the app; Allows reversing URLs using 'commissions:<name>'
app_name = "commissions"


urlpatterns = [
    # URL pattern for the list of commissions
    path('list/', views.commissions_list, name='commissions_list'),
    
    
    # URL pattern for the details of a specific commission
    path('detail/<int:id>/', views.commission, name='commission'),
]