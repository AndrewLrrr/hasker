# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from forms import UserSingUpForm, UserSettingsForm, QuestionAskForm, AnswerForm
from qa.decorators import logout_required
from qa.models import Question, Answer


class IndexView(View):
    def get(self, request):
        message = 'Hello ' + request.user.username + '!' if request.user.is_authenticated() else 'Nobody'
        return HttpResponse(message)


class PopularView(View):
    def get(self, request):
        return HttpResponse('popular')


class TagView(View):
    def get(self, request, slug):
        return HttpResponse('tag')


class SearchView(View):
    def get(self, request):
        return HttpResponse('search')


class QuestionView(View):
    form_class = AnswerForm
    template = 'qa/question_detail.html'

    def get(self, request, slug):
        form = self.form_class(None)
        question = get_object_or_404(Question, slug=slug)
        return render(request, self.template, {'question': question, 'form': form})

    @method_decorator(login_required)
    def post(self, request, slug):
        form = self.form_class(request.POST)
        question = get_object_or_404(Question, slug=slug)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(question.get_url())
        return render(request, self.template, {'question': question, 'form': form})


class AskView(View):
    form_class = QuestionAskForm
    template = 'qa/question_form.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            tags = form.cleaned_data['tags']
            question.author = request.user
            question.save(tags=tags)
            return redirect(question.get_url())
        return render(request, self.template, {'form': form})


class SingUpView(View):
    form_class = UserSingUpForm
    template = 'qa/user_singup.html'

    @method_decorator(logout_required('qa:index'))
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    @method_decorator(logout_required('qa:index'))
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


class SettingsView(View):
    form_class = UserSettingsForm
    template = 'qa/user_settings.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = self.form_class(instance=request.user)
        return render(request, self.template, {'form': form, 'user': user})

    @method_decorator(login_required)
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
            return redirect('qa:settings')
        return render(request, self.template, {'form': form, 'user': user})


class VoteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        value = True if request.POST.get('value') == 'true' else False
        entity = get_object_or_404(self.get_model(), pk=pk)
        entity.vote(request.user, value)
        return JsonResponse({'rating': entity.rating})

    def get_model(self):
        raise NotImplementedError('Model needs to be defined by sub-class')


class QuestionVoteView(VoteView):
    def get_model(self):
        return Question


class AnswerVoteView(VoteView):
    def get_model(self):
        return Answer

