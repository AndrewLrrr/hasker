# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .fields import ContentTypeRestrictedFileField


def unique_filename(instance, filename):
    chunk_size = 65536
    hasher = hashlib.md5()
    instance.avatar.open()
    buf = instance.avatar.read(chunk_size)
    while len(buf) > 0:
        hasher.update(buf)
        buf = instance.avatar.read(chunk_size)
    _, ext = os.path.splitext(filename)
    filename = '{}{}'.format(hasher.hexdigest(), ext)
    return os.path.join('uploads', filename)


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
        null=True,
    )

    def get_url(self):
        return reverse('accounts:profile', kwargs={'username': self.username})

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else staticfiles_storage.url('img/avatar.png')
