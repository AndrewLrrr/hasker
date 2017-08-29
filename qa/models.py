# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from qa.fields import ContentTypeRestrictedFileField

# TODO: Спросить у Станислава, есть ли возможность сгенерировать составной первичный ключ

USER_AVATAR_MAX_SIZE_IN_MB = 1

USER_AVATAR_ALLOWED_CONTENT_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/pjpeg',
    'image/png',
)


def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join('uploads', filename)


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
    avatar = ContentTypeRestrictedFileField(
        _('Avatar'),
        content_types=USER_AVATAR_ALLOWED_CONTENT_TYPES,
        max_upload_size=(USER_AVATAR_MAX_SIZE_IN_MB * 1024 * 1024),
        upload_to=unique_filename,
        blank=True,
        null=True
    )

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else staticfiles_storage.url('qa/img/avatar.png')


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
