# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import QuestionListSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class QuestionList(ListAPIView):
    serializer_class = QuestionListSerializer
    model = serializer_class.Meta.model
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.model.objects.new()
