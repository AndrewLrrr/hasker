# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from forms import UserSingUpForm


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

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('qa:index')
        return render(request, self.template, {'form': form})


class LoginView(View):
    form_class = AuthenticationForm
    template = 'qa/user_login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

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
    def post(self, request):
        logout(request)
        return redirect('qa:index')


class ProfileView(View):
    def get(self, request, username):
        return HttpResponse('profile')
