from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User


class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'

    redirect_authenticated_user = True

    # КУДА ПЕРЕНАПРАВЛЯТЬ ПОСЛЕ ВХОДА
    def get_success_url(self):

        user = self.request.user

        # ЕСЛИ АДМИН
        if user.is_superuser:
            return '/admin/'

        # ЕСЛИ ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ
        return '/'


def register(request):

    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            # ПОСЛЕ РЕГИСТРАЦИИ
            if user.is_superuser:
                return redirect('/admin/')

            return redirect('main:home')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
