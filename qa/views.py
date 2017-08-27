# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from forms import UserSingUpForm


class IndexView(View):
    def get(self, request):
        return HttpResponse('index')


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
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect('qa:index')
        return render(request, self.template, {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'qa/user_login.html')


class LogoutView(View):
    def get(self, request):
        return HttpResponse('logout')


class ProfileView(View):
    def get(self, request, username):
        return HttpResponse('profile')
