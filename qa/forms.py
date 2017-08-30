# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from qa.models import User, Question
from qa.widgets import ClearableImageInput


class UserSingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar', )


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'avatar', )

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget = ClearableImageInput()


class QuestionAskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags', )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = [] if not tags else [t.strip() for t in tags.split(',')]

        if len(tags) > settings.TAGS_LIMIT:
            raise ValidationError('The maximum number of tags is {}'.format(settings.TAGS_LIMIT))

        for tag in tags:
            if not re.match(r'^[\w\@\.\+\-]+$', tag):
                raise ValidationError('Tag value may contain only English letters, numbers and @/./+/-/_ characters.')

        return tags
