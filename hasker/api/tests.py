# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from api.serializers import QuestionSerializer, AnswerSerializer
from accounts.models import User
from qa.models import Question, Answer, Tag


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
        questions = Question.objects.all().order_by('-pub_date')[:settings.QUESTIONS_PER_PAGE]
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
        questions = Question.objects.all().order_by('-rating', '-pub_date')[:settings.TRENDING_QUESTIONS_LIMIT]
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
        questions = Question.objects \
            .filter(text__icontains='text1') \
            .order_by('-rating', '-pub_date')[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_title(self):
        response = self.client.get(reverse('api:search') + '?q=question1')
        questions = Question.objects \
            .filter(title__icontains='question1') \
            .order_by('-rating', '-pub_date')[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnswerListTest(TestCase):
    questions_data = {
        'question1': {'text': 'text1', 'rating': 3, 'days': 0},
        'question2': {'text': 'text2', 'rating': 3, 'days': 1},
        'question3': {'text': 'text3', 'rating': 2, 'days': 2},
    }

    answers_data = {
        'answer1': {'question': 'question1', 'rating': 2, 'days': 0},
        'answer2': {'question': 'question1', 'rating': 1, 'days': 1},
        'answer3': {'question': 'question2', 'rating': 2, 'days': 1},
        'answer4': {'question': 'question2', 'rating': 3, 'days': 0},
        'answer5': {'question': 'question3', 'rating': 0, 'days': 1},
        'answer6': {'question': 'question3', 'rating': 2, 'days': 0},
    }

    def setUp(self):
        question_list = {}

        question_author = User.objects.create_user(
            username='test', email='test@eamil.com', password='top_secret'
        )

        answer_author = User.objects.create_user(
            username='test2', email='test2@eamil.com', password='top_secret'
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
            question_list[title] = question

        for text, data in self.answers_data.items():
            pub_date = timezone.now() + datetime.timedelta(days=data['days'])
            question = question_list[data['question']]
            answer = Answer.objects.create(
                text=text,
                rating=data['rating'],
                author=answer_author,
                question=question,
            )
            answer.pub_date = pub_date
            answer.save()

    def test_get_question_answers(self):
        question_id = 1
        response = self.client.get(reverse('api:answers', kwargs={'pk': question_id}))
        question = Question.objects.get(pk=question_id)
        answers = question.answer_set.all().order_by('-rating', '-pub_date')[:settings.ANSWERS_PER_PAGE]
        serializer = AnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404_for_not_exist_question(self):
        response = self.client.get(reverse('api:answers', kwargs={'pk': 15}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagSearchListTest(TestCase):
    questions_data = {
        'question1': {'text': 'text1', 'rating': 3, 'days': 0},
        'question2': {'text': 'text2', 'rating': 3, 'days': 1},
        'question3': {'text': 'text3', 'rating': 2, 'days': 2},
    }

    tags_data = {
        'question1': ('tag1', 'tag2',),
        'question2': ('tag3',),
        'question3': ('tag1',),
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
            question.save(self.tags_data[title])

    def test_get_questions_by_tag(self):
        tag = Tag.objects.get(name='tag1')
        response = self.client.get(reverse('api:tags_questions', kwargs={'pk': tag.pk}))
        questions = tag.question_tags.all().order_by('-rating', '-pub_date')[:settings.QUESTIONS_PER_PAGE]
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404_for_not_exist_question(self):
        response = self.client.get(reverse('api:tags_questions', kwargs={'pk': 15}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
