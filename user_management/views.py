from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Profile
from django.contrib import messages

@login_required
def index(request):
    """Displays the Profile Page."""
    if request.method == 'POST':
        display_name = request.POST['display-name']
        email = request.POST['email']
        profile = request.user.profile
        profile.display_name = display_name
        profile.email_address = email
        profile.save()
        return HttpResponseRedirect(reverse('user_management:index'))
    else:
        return render(request, "user_management/profile.html", {
            "profile": request.user.profile
        })

def register(request):
    """Displays the Register Page."""
    if request.method == 'GET':
        return render(request, "user_management/register.html")
    elif request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["passwordConfirm"]

        if password != confirm_password:
            messages.error(request, "Passwords don't match.")
            return HttpResponseRedirect(reverse('user_management:register'))

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return HttpResponseRedirect(reverse('user_management:register'))

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used.")
            return HttpResponseRedirect(reverse('user_management:register'))

        user = User.objects.create_user(username.lower(), email, password)
        profile = Profile.objects.create(
            user=user,
            display_name=username,
            email_address=email,
        )

        return HttpResponseRedirect(reverse('user_management:login'))
