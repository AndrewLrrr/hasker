# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from forms import UserSingUpForm, UserProfileForm
from qa.decorators import logout_required


class IndexView(View):
    def get(self, request):
        message = 'Hello ' + request.user.username + '!' if request.user.is_authenticated() else 'Nobody'
        return HttpResponse(message)


class PopularView(View):
    def get(self, request):
        return HttpResponse('popular')


class AskView(View):
    def get(self, request):
        return HttpResponse('ask')


class QuestionView(View):
    def get(self, request, slug):
        return HttpResponse('question')


class TagView(View):
    def get(self, request, slug):
        return HttpResponse('tag')


class SearchView(View):
    def get(self, request):
        return HttpResponse('search')


class SingUpView(View):
    form_class = UserSingUpForm
    template = 'qa/user_singup.html'
    redirect = 'qa:index'

    @method_decorator(logout_required('qa:index'))
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(logout_required('qa:index'))
    def post(self, request):
        if request.user.is_authenticated():
            return redirect('qa:index')
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('qa:index')
        return render(request, self.template, {'form': form})


class LoginView(View):
    form_class = AuthenticationForm
    template = 'qa/user_login.html'

    @method_decorator(logout_required('qa:index'))
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(logout_required('qa:index'))
    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            login(request, user)
            return redirect('qa:index')
        return render(request, self.template, {'form': form})


class LogoutView(View):
    @method_decorator(login_required)
    def post(self, request):
        logout(request)
        return redirect('qa:index')


class ProfileView(View):
    form_class = UserProfileForm
    template = 'qa/user_profile.html'

    @method_decorator(login_required)
    def get(self, request, username):
        user = request.user
        if user.username != username:
            return redirect('qa:profile', username=user.username)
        form = self.form_class(initial={'email': user.email})
        return render(request, self.template, {'form': form, 'user': user})

    @method_decorator(login_required)
    def post(self, request, username):
        user = request.user
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                user.avatar = avatar
            user.save()
            return redirect('qa:profile', username=username)
        return render(request, self.template, {'form': form, 'user': user})
