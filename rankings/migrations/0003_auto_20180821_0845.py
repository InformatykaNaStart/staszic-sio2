# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-21 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0002_roundrankingconfig_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roundrankingconfig',
            name='round',
            field=models.CharField(blank=True, max_length=256, verbose_name='Round name (empty for all rounds)'),
        ),
    ]