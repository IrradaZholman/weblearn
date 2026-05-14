from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
