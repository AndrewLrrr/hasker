# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User
from .decorators import logout_required
from .forms import UserSingUpForm, UserSettingsForm


class SingUpView(View):
    form_class = UserSingUpForm
    template = 'accounts/user_singup.html'

    @method_decorator(logout_required(settings.BASE_REDIRECT))
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(logout_required(settings.BASE_REDIRECT))
    @transaction.atomic
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.BASE_REDIRECT)
        return render(request, self.template, {'form': form})


class LoginView(View):
    form_class = AuthenticationForm
    template = 'accounts/user_login.html'

    @method_decorator(logout_required(settings.BASE_REDIRECT))
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(logout_required(settings.BASE_REDIRECT))
    @transaction.atomic
    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            login(request, user)
            return redirect(settings.BASE_REDIRECT)
        return render(request, self.template, {'form': form})


class LogoutView(View):
    @method_decorator(login_required)
    def post(self, request):
        logout(request)
        return redirect(settings.BASE_REDIRECT)


class SettingsView(View):
    form_class = UserSettingsForm
    template = 'accounts/user_settings.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = self.form_class(instance=request.user)
        return render(request, self.template, {'form': form, 'user': user})

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request):
        user = request.user
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                user.avatar = avatar
            user.save()
            messages.info(request, 'The changes have been saved!')
            return redirect('accounts:settings')
        return render(request, self.template, {'form': form, 'user': user})


class ProfileView(View):
    template = 'accounts/user_profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, self.template, {'user': user})
