# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework.generics import ListAPIView

from paginators import QuestionsSetPagination
from serializers import QuestionSerializer


class QuestionList(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    pagination_class = QuestionsSetPagination

    def get_queryset(self):
        return self.model.objects.new()


class TrendingList(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.popular()[:settings.TRENDING_QUESTIONS_LIMIT]
