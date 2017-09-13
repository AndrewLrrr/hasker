# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models import Q
from rest_framework.generics import ListAPIView

from qa.models import Question
from paginators import QuestionListPagination
from serializers import QuestionSerializer


class QuestionList(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    pagination_class = QuestionListPagination

    def get_queryset(self):
        return self.model.objects.new()


class TrendingList(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.popular()[:settings.TRENDING_QUESTIONS_LIMIT]


class SearchList(QuestionList):
    def get_queryset(self):
        search_query = self.request.GET.get('q')
        if not search_query:
            return Question.objects.none()
        query = Q(title__icontains=search_query) | Q(text__icontains=search_query)
        return Question.objects.filter(query).order_by('-rating', '-pub_date')
