# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Question, Answer


class QuestionAskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = [] if not tags else [t.strip() for t in tags.split(',')]

        if len(tags) > settings.TAGS_LIMIT:
            raise ValidationError('The maximum number of tags is {}'.format(settings.TAGS_LIMIT))

        for tag in tags:
            if not re.match(r'^[\w\@\.\+\-]+$', tag):
                raise ValidationError('Tag value may contain only English letters, numbers and @/./+/-/_ characters.')

        return tags


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        labels = {
            'text': _('Your answer'),
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }
