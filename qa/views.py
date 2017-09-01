# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from forms import UserSingUpForm, UserSettingsForm, QuestionAskForm, AnswerForm
from qa.decorators import logout_required
from qa.models import Question, QuestionVotes, Answer, AnswerVotes


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


def question_vote(request, pk, value=False):
    question = get_object_or_404(Question, pk=pk)
    try:
        vote = QuestionVotes.objects.get(question=question, user=request.user)
        if vote.vote != value:
            vote.delete()
        else:
            return JsonResponse({'success': False, 'rating': question.rating})
    except ObjectDoesNotExist:
        QuestionVotes.objects.get_or_create(question=question, user=request.user, vote=value)
    question.rating += 1 if value else -1
    question.save()
    return JsonResponse({'success': True, 'rating': question.rating})


def answer_vote(request, pk, value=False):
    answer = get_object_or_404(Answer, pk=pk)
    try:
        vote = AnswerVotes.objects.get(answer=answer, user=request.user)
        if vote.vote != value:
            vote.delete()
        else:
            return JsonResponse({'success': False, 'rating': answer.rating})
    except ObjectDoesNotExist:
        AnswerVotes.objects.get_or_create(answer=answer, user=request.user, vote=value)
    answer.rating += 1 if value else -1
    answer.save()
    return JsonResponse({'success': True, 'rating': answer.rating})


@require_POST
@login_required
def question_like_json(request, pk):
    return question_vote(request, pk, True)


@require_POST
@login_required
def question_dislike_json(request, pk):
    return question_vote(request, pk, False)


@require_POST
@login_required
def answer_like_json(request, pk):
    return answer_vote(request, pk, True)


@require_POST
@login_required
def answer_dislike_json(request, pk):
    return answer_vote(request, pk, False)