# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django import forms

from qa.models import User


class UserSingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'avatar', )
