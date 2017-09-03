# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from forms import UserSingUpForm, UserSettingsForm, QuestionAskForm, AnswerForm
from qa.decorators import logout_required
from qa.models import Question, Answer, User, Tag


class PaginationMixin(object):
    def paginate(self, request, items_per_page=20, pagination_limit=100):
        try:
            limit = int(request.GET.get('limit', items_per_page))
        except ValueError:
            limit = items_per_page
        if limit > pagination_limit:
            limit = items_per_page
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            raise Http404
        paginator = Paginator(self.get_query_set(), limit)
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        if len(get_params) > 0:
            paginator.url = '{}?{}&page='.format(self.get_url(), urllib.urlencode(get_params.items()))
        else:
            paginator.url = '{}?page='.format(self.get_url())
        try:
            page = paginator.page(page)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return paginator, page


class IndexView(PaginationMixin, View):
    template = 'qa/question_list.html'

    def get(self, request):
        paginator, page = self.paginate(request, settings.QUESTIONS_PER_PAGE)
        return render(request, self.template, {
            'questions': page.object_list,
            'paginator': paginator,
            'page': page,
        })

    def get_query_set(self):
        return Question.objects.popular() if self.request.GET.get('sort') else Question.objects.new()

    def get_url(self):
        return reverse('qa:index')


class SearchView(PaginationMixin, View):
    template = 'qa/question_search.html'
    search_query = None

    def get(self, request):
        self.search_query = request.GET.get('q')[:255]
        paginator, page = self.paginate(request, settings.QUESTIONS_PER_PAGE)
        return render(request, self.template, {
            'questions': page.object_list,
            'paginator': paginator,
            'page': page,
        })

    def get_query_set(self):
        if not self.search_query:
            return Question.objects.none()
        if self.search_query.startswith('tag:'):
            try:
                tag = get_object_or_404(Tag, name=self.search_query[len('tag:'):])
            except Http404:
                return Question.objects.none()
            return tag.question_tags.popular()
        query = Q(title__icontains=self.search_query) | Q(text__icontains=self.search_query)
        return Question.objects.filter(query).order_by('-rating', '-pub_date')

    def get_url(self):
        return reverse('qa:search')


class TagView(View):
    def get(self, request, slug):
        return HttpResponse('tag')


class QuestionView(PaginationMixin, View):
    form_class = AnswerForm
    template = 'qa/question_detail.html'
    question = None
    form = None

    def do_response(self, request):
        paginator, page = self.paginate(request, settings.ANSWERS_PER_PAGE)
        return render(request, self.template, {
            'question': self.question,
            'form': self.form,
            'answers': page.object_list,
            'paginator': paginator,
            'page': page,
        })

    def get(self, request, slug):
        self.form = self.form_class(None)
        self.question = get_object_or_404(Question, slug=slug)
        return self.do_response(request)

    @method_decorator(login_required)
    def post(self, request, slug):
        self.form = self.form_class(request.POST)
        self.question = get_object_or_404(Question, slug=slug)
        if self.form.is_valid():
            answer = self.form.save(commit=False)
            answer.question = self.question
            answer.author = request.user
            answer.save()
            return redirect(self.question.get_url())
        return self.do_response(request)

    def get_query_set(self):
        return self.question.answer_set.popular()

    def get_url(self):
        return self.question.get_url()


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


class AnswerMarkView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        return JsonResponse({'success': answer.mark(request.user)})


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


class ProfileView(View):
    template = 'qa/user_profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, self.template, {'user': user})
