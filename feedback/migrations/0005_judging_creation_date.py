# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-06-24 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20180829_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='judging',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]