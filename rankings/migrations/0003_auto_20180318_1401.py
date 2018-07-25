# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-18 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0002_roundrankingconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='roundrankingconfig',
            name='contest_type',
            field=models.CharField(choices=[('best', 'Best'), ('last', 'Last'), ('rlast', 'Last + revealed')], default='best', max_length=8),
        ),
        migrations.AddField(
            model_name='roundrankingconfig',
            name='round_type',
            field=models.CharField(choices=[('best', 'Best'), ('last', 'Last'), ('rlast', 'Last + revealed')], default='last', max_length=8),
        ),
        migrations.AlterField(
            model_name='roundrankingconfig',
            name='contest_coef',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='roundrankingconfig',
            name='round_coef',
            field=models.IntegerField(default=1),
        ),
    ]
