from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'

    redirect_authenticated_user = True

    def get_success_url(self):

        user = self.request.user

        if user.is_superuser:
            return '/admin/'

        return '/'


def register(request):

    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            return redirect('main:home')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ВЫХОД ИЗ АККАУНТА
def logout_view(request):

    logout(request)

    return redirect('/')
