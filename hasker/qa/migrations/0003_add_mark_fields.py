# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_rename_votes_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='has_answer',
            field=models.BooleanField(default=False),
        ),
    ]
