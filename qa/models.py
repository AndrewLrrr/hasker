# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# TODO: Спросить у Станислава, есть ли возможность сгенерировать составной первичный ключ


class User(AbstractUser):
    username = models.CharField(
        _('Login'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that login already exists."),
        },
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    avatar = models.FileField(_('Avatar'), blank=True, null=True)

    def get_url(self):
        return reverse('qa:profile', kwargs={'username': self.username})


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='question_tags')
    votes = models.ManyToManyField(User, through='QuestionVote', related_name='question_votes')

    def get_url(self):
        return reverse('qa:question', kwargs={'slug': self.slug})


class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    tags = models.ManyToManyField(Tag, related_name='answer_tags')
    votes = models.ManyToManyField(User, through='AnswerVote', related_name='answer_votes')


class Vote(models.Model):
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def is_liked(self):
        return self.vote is True

    def is_disliked(self):
        return self.vote is False


class AnswerVote(Vote):
    answer = models.ForeignKey(Answer)

    class Meta:
        unique_together = (('user', 'answer'),)


class QuestionVote(Vote):
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = (('user', 'question'),)
