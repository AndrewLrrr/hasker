# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.urls import reverse

from qa.models import Question, Answer, User
from qa.views import QuestionVoteView, AnswerVoteView, AnswerMarkView


def create_question(author, title='Test question', text='Test question text'):
    return Question.objects.create(title=title, text=text, author=author)


def create_answer(question, author, text='Test answer text'):
    return Answer.objects.create(text=text, question=question, author=author)


class SearchViewTests(TestCase):
    questions_data = {
        'question1': 'text1',
        'question2': 'text12',
        'question3': 'text3',
    }

    tags_data = {
        'question1': ('tag1', 'tag2',),
        'question2': ('tag3',),
        'question3': ('tag1',),
    }

    def setUp(self):
        self.factory = RequestFactory()

        question_author = User.objects.create_user(
            username='test1', email='test1@eamil.com', password='top_secret'
        )

        for title, text in self.questions_data.items():
            question = create_question(title=title, text=text, author=question_author)
            question.save(self.tags_data[title])

    def test_empty_search(self):
        response = self.client.get(reverse('qa:search') + '?q=question4')
        self.assertContains(response, 'Couldn\'t find any matching `question4`')
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_empty_search_by_tag(self):
        response = self.client.get(reverse('qa:search') + '?q=tag:tag5')
        self.assertContains(response, 'Couldn\'t find any question by tag')
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_search_by_title(self):
        response = self.client.get(reverse('qa:search') + '?q=question1')
        self.assertQuerysetEqual(response.context['questions'], ['<Question: question1>'])

    def test_search_by_text(self):
        response = self.client.get(reverse('qa:search') + '?q=text1')
        self.assertQuerysetEqual(response.context['questions'], ['<Question: question2>', '<Question: question1>'])

    def test_search_by_tag(self):
        response = self.client.get(reverse('qa:search') + '?q=tag:tag1')
        self.assertQuerysetEqual(response.context['questions'], ['<Question: question3>', '<Question: question1>'])


class AnswerMarkViewTests(TestCase):
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

    def test_unauthorized_user_can_not_mark_answer(self):
        response = self.client.post(self.answer.get_mark_url())
        self.assertEqual(response.status_code, 403)

    def test_not_question_author_can_not_mark_answer(self):
        request = self.factory.post(self.answer.get_mark_url())

        request.user = self.answer_author

        self.assertEqual(self.question.has_answer, False)
        self.assertEqual(self.answer.is_correct, False)

        response = AnswerMarkView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).has_answer, False)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).is_correct, False)

    def test_question_author_can_mark_answer(self):
        request = self.factory.post(self.answer.get_mark_url())

        request.user = self.question_author

        self.assertEqual(self.question.has_answer, False)
        self.assertEqual(self.answer.is_correct, False)

        response = AnswerMarkView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).has_answer, True)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).is_correct, True)

    def test_question_author_can_unmark_answer(self):
        request = self.factory.post(self.answer.get_mark_url())

        request.user = self.question_author

        self.assertEqual(self.question.has_answer, False)
        self.assertEqual(self.answer.is_correct, False)

        response = AnswerMarkView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).has_answer, True)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).is_correct, True)

        response = AnswerMarkView.as_view()(request, self.answer.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Question.objects.get(pk=self.question.pk).has_answer, False)
        self.assertEqual(Answer.objects.get(pk=self.answer.pk).is_correct, False)


class VoteViewsTests(TestCase):
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
