# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


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


class SingupView(View):
    def get(self, request):
        return render(request, 'qa/user_singup.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'qa/user_login.html')


class LogoutView(View):
    def get(self, request):
        return HttpResponse('logout')


class ProfileView(View):
    def get(self, request, username):
        return HttpResponse('profile')
