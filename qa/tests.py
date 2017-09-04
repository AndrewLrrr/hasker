# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory

from qa.models import Question, Answer, User
from qa.views import QuestionVoteView, AnswerVoteView


def create_question(author, title='Test question', text='Test question text'):
    return Question.objects.create(title=title, text=text, author=author)


def create_answer(question, author, text='Test answer text'):
    return Answer.objects.create(text=text, question=question, author=author)


class VoteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.question_author = User.objects.create_user(
            username='test1', email='test1@eamil.com', password='top_secret'
        )
        self.answer_author = User.objects.create_user(
            username='test2', email='test2@eamil.com', password='top_secret'
        )
        self.question = create_question(author=self.question_author)
        self.answer = create_answer(author=self.answer_author, question=self.question)

    def test_unauthorized_user_can_not_vote_for_question(self):
        response = self.client.post(self.question.get_vote_url())
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_can_not_for_vote_for_answer(self):
        response = self.client.post(self.answer.get_vote_url())
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_can_do_only_one_question_vote_up(self):
        request = self.factory.post(self.question.get_vote_url(), {'value': 'true'})

        request.user = self.answer_author

        self.assertEqual(self.question.rating, 0)

        response = QuestionVoteView.as_view()(request, self.question.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, 1)

        response = QuestionVoteView.as_view()(request, self.question.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, 1)

    def test_authorized_user_can_do_only_one_question_vote_down(self):
        request = self.factory.post(self.question.get_vote_url(), {'value': 'false'})

        request.user = self.answer_author

        self.assertEqual(self.question.rating, 0)

        response = QuestionVoteView.as_view()(request, self.question.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, -1)

        response = QuestionVoteView.as_view()(request, self.question.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, -1)

    def test_authorized_user_can_do_question_vote_toggle(self):
        request_up = self.factory.post(self.question.get_vote_url(), {'value': 'true'})
        request_down = self.factory.post(self.question.get_vote_url(), {'value': 'false'})

        request_up.user = self.answer_author
        request_down.user = self.answer_author

        self.assertEqual(self.question.rating, 0)

        QuestionVoteView.as_view()(request_up, self.question.pk)
        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, 1)

        QuestionVoteView.as_view()(request_down, self.question.pk)
        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, 0)

        QuestionVoteView.as_view()(request_down, self.question.pk)
        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, -1)

        QuestionVoteView.as_view()(request_up, self.question.pk)
        self.assertEqual(Question.objects.get(pk=self.question.pk).rating, 0)

    def test_authorized_user_can_do_only_one_answer_vote_up(self):
        request = self.factory.post(self.answer.get_vote_url(), {'value': 'true'})

        request.user = self.question_author

        self.assertEqual(self.answer.rating, 0)

        response = AnswerVoteView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, 1)

        response = AnswerVoteView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, 1)

    def test_authorized_user_can_do_only_one_answer_vote_down(self):
        request = self.factory.post(self.answer.get_vote_url(), {'value': 'false'})

        request.user = self.question_author

        self.assertEqual(self.answer.rating, 0)

        response = AnswerVoteView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, -1)

        response = AnswerVoteView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, -1)

    def test_authorized_user_can_do_answer_vote_toggle(self):
        request_up = self.factory.post(self.answer.get_vote_url(), {'value': 'true'})
        request_down = self.factory.post(self.answer.get_vote_url(), {'value': 'false'})

        request_up.user = self.question_author
        request_down.user = self.question_author

        self.assertEqual(self.answer.rating, 0)

        AnswerVoteView.as_view()(request_up, self.answer.pk)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, 1)

        AnswerVoteView.as_view()(request_down, self.answer.pk)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, 0)

        AnswerVoteView.as_view()(request_down, self.answer.pk)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, -1)

        AnswerVoteView.as_view()(request_up, self.answer.pk)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).rating, 0)
