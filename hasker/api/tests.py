# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from hasker.api.serializers import QuestionSerializer
from accounts.models import User
from qa.models import Question


class QuestionListTest(TestCase):
    questions_data = {
        'question1': {'text': 'text1', 'rating': 3, 'days': 0},
        'question2': {'text': 'text2', 'rating': 3, 'days': 1},
        'question3': {'text': 'text3', 'rating': 2, 'days': 2},
        'question4': {'text': 'text4', 'rating': 1, 'days': 3},
        'question5': {'text': 'text5', 'rating': 0, 'days': 3},
    }

    def setUp(self):
        question_author = User.objects.create_user(
            username='test', email='test@eamil.com', password='top_secret'
        )

        for title, data in self.questions_data.items():
            pub_date = timezone.now() + datetime.timedelta(days=data['days'])
            question = Question.objects.create(
                title=title,
                text=data['text'],
                rating=data['rating'],
                author=question_author,
            )
            question.pub_date = pub_date
            question.save()

    def test_get_new_questions(self):
        response = self.client.get(reverse('api:questions'))
        questions = Question.objects.new()[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrendingListTest(TestCase):
    questions_data = {
        'question1': {'text': 'text1', 'rating': 3, 'days': 0},
        'question2': {'text': 'text2', 'rating': 3, 'days': 1},
        'question3': {'text': 'text3', 'rating': 2, 'days': 2},
        'question4': {'text': 'text4', 'rating': 1, 'days': 3},
        'question5': {'text': 'text5', 'rating': 0, 'days': 3},
    }

    def setUp(self):
        question_author = User.objects.create_user(
            username='test', email='test@eamil.com', password='top_secret'
        )

        for title, data in self.questions_data.items():
            pub_date = timezone.now() + datetime.timedelta(days=data['days'])
            question = Question.objects.create(
                title=title,
                text=data['text'],
                rating=data['rating'],
                author=question_author,
            )
            question.pub_date = pub_date
            question.save()

    def test_get_trending_questions(self):
        response = self.client.get(reverse('api:trending'))
        questions = Question.objects.popular()[:settings.TRENDING_QUESTIONS_LIMIT]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchListTest(TestCase):
    questions_data = {
        'question1': {'text': 'text1', 'rating': 3, 'days': 0},
        'question12': {'text': 'text12', 'rating': 3, 'days': 1},
        'question3': {'text': 'text3', 'rating': 2, 'days': 2},
        'question4': {'text': 'text4', 'rating': 1, 'days': 3},
        'question5': {'text': 'text5', 'rating': 0, 'days': 3},
    }

    def setUp(self):
        question_author = User.objects.create_user(
            username='test', email='test@eamil.com', password='top_secret'
        )

        for title, data in self.questions_data.items():
            pub_date = timezone.now() + datetime.timedelta(days=data['days'])
            question = Question.objects.create(
                title=title,
                text=data['text'],
                rating=data['rating'],
                author=question_author,
            )
            question.pub_date = pub_date
            question.save()

    def test_search_by_text(self):
        response = self.client.get(reverse('api:search') + '?q=text1')
        questions = Question.objects.filter(text__icontains='text1').order_by('-rating', '-pub_date')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_title(self):
        response = self.client.get(reverse('api:search') + '?q=question1')
        questions = Question.objects.filter(title__icontains='question1').order_by('-rating', '-pub_date')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
