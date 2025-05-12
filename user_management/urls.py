from django.urls import path
from .views import profile, register
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        success_url='/user/password_reset/done/'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/user/password_reset/complete/'),name='password_reset_confirm'),
    path('password_reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]