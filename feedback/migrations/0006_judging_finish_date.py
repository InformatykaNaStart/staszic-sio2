# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-06-24 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_judging_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='judging',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
