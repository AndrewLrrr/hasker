# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from qa.models import Answer, Question, Tag
from paginators import QuestionListPagination, AnswerListPagination
from serializers import QuestionSerializer, AnswerSerializer, VoteSerializer


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
        search_query = self.request.GET.get('q')[:255]
        if not search_query:
            return Question.objects.none()
        query = Q(title__icontains=search_query) | Q(text__icontains=search_query)
        return Question.objects.filter(query).order_by('-rating', '-pub_date')


class AnswerList(ListAPIView):
    serializer_class = AnswerSerializer
    model = serializer_class.Meta.model
    pagination_class = AnswerListPagination

    def get_queryset(self):
        try:
            question = Question.objects.get(id=self.kwargs.get('pk'))
        except Question.DoesNotExist:
            raise NotFound()
        return question.answer_set.popular()


class TagSearchList(QuestionList):
    def get_queryset(self):
        try:
            tag = Tag.objects.get(id=self.kwargs.get('pk'))
        except Tag.DoesNotExist:
            raise NotFound()
        return tag.question_tags.popular()


class VoteView(APIView):
    serializer_class = VoteSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, pk):
        value = True if request.data.get('value') == 'true' else False
        try:
            entity = self.get_model().objects.get(id=pk)
        except self.get_model().DoesNotExist:
            raise NotFound()
        entity.vote(request.user, value)
        return Response({'rating': entity.rating}, status=status.HTTP_201_CREATED)

    def get_model(self):
        raise NotImplementedError('Model needs to be defined by sub-class')


class QuestionVote(VoteView):
    def get_model(self):
        return Question


class AnswerVote(VoteView):
    def get_model(self):
        return Answer
