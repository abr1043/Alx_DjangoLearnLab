# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm, ProfileForm
from .models import UserProfile

class UserLoginView(LoginView):
    template_name = "blog/login.html"

class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"

class RegisterView(View):
    """Show registration form and create user, then login."""
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "blog/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # automatically log user in after registration
            login(request, user)
            return redirect(reverse_lazy("blog:profile"))
        return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    """
    Show profile and allow update. Both User and UserProfile fields
    can be added here. This view handles POST to update profile.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("blog:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "blog/profile.html", {"form": form, "profile": profile})
