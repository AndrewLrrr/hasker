# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

import itertools
from urllib import urlencode

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from qa.fields import ContentTypeRestrictedFileField


def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join('uploads', filename)


class VoteMixin(object):
    def vote(self, user, value=False):
        try:
            vote = self.get_vote(user)
            if vote.vote != value:
                vote.delete()
            else:
                return False
        except ObjectDoesNotExist:
            self.create_vote(user, value)
        self.rating += 1 if value else -1
        self.save()
        return True


class SlugifyMixin(object):
    def slugify(self, string):
        max_length = self.get_slug_max_length()
        slug = orig = slugify(string)[:max_length]
        for x in itertools.count(1):
            if not self.is_slug_exists():
                break
            slug = '{}-{}'.format(orig[:max_length - len(str(x)) - 1], x)
        return slug


class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-pub_date')

    def popular(self):
        return self.all().order_by('-rating', '-pub_date')


class AnswerManager(models.Manager):
    def popular(self):
        return self.all().order_by('-rating', '-pub_date')


class User(AbstractUser):
    username = models.CharField(
        _('Login'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _('A user with that login already exists.'),
        },
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    avatar = ContentTypeRestrictedFileField(
        _('Avatar'),
        content_types=settings.USER_AVATAR_ALLOWED_CONTENT_TYPES,
        max_upload_size=(settings.USER_AVATAR_MAX_SIZE_IN_MB * 1024 * 1024),
        upload_to=unique_filename,
        blank=True,
        null=True
    )

    def get_url(self):
        return reverse('qa:profile', kwargs={'username': self.username})

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else staticfiles_storage.url('qa/img/avatar.png')


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=True)

    def get_url(self):
        return '{}?{}'.format(reverse('qa:search'), urlencode({'q': 'tag:' + self.name}))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Question(VoteMixin, SlugifyMixin, models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    has_answer = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='question_tags')
    votes = models.ManyToManyField(User, through='QuestionVotes', related_name='question_votes')

    objects = QuestionManager()

    def get_url(self):
        return reverse('qa:question', kwargs={'slug': self.slug})

    def get_vote_url(self):
        return reverse('qa:question_vote', kwargs={'pk': self.pk})

    def get_vote(self, user):
        return QuestionVotes.objects.get(question=self, user=user)

    def create_vote(self, user, value):
        return QuestionVotes.objects.get_or_create(question=self, user=user, vote=value)

    def get_slug_max_length(self):
        return self._meta.get_field('slug').max_length

    def is_slug_exists(self):
        return Question.objects.filter(slug=self.slug).exists()

    def save(self, tags=(), *args, **kwargs):
        if not self.pk:
            self.slug = self.slugify(self.title)
        super(Question, self).save(*args, **kwargs)
        tag_objects = []
        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(name=tag)
            tag_objects.append(tag_object)
        self.tags.add(*tag_objects)

    def __str__(self):
        return self.title


class Answer(VoteMixin, models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    votes = models.ManyToManyField(User, through='AnswerVotes', related_name='answer_votes')

    objects = AnswerManager()

    def mark(self, user):
        question = self.question
        if question.author != user:
            return False
        if self.is_correct:
            self.is_correct = False
            question.has_answer = False
        else:
            if question.has_answer:
                incorrect_answer = question.answer_set.get(is_correct=True)
                incorrect_answer.is_correct = False
                incorrect_answer.save()
            else:
                question.has_answer = True
            self.is_correct = True
        question.save()
        self.save()
        return True

    def get_vote_url(self):
        return reverse('qa:answer_vote', kwargs={'pk': self.pk})

    def get_mark_url(self):
        return reverse('qa:answer_mark', kwargs={'pk': self.pk})

    def get_vote(self, user):
        return AnswerVotes.objects.get(answer=self, user=user)

    def create_vote(self, user, value):
        return AnswerVotes.objects.get_or_create(answer=self, user=user, vote=value)


class Vote(models.Model):
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AnswerVotes(Vote):
    answer = models.ForeignKey(Answer)

    class Meta:
        unique_together = (('user', 'answer'),)


class QuestionVotes(Vote):
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = (('user', 'question'),)
