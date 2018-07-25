# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-18 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoundRankingConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_coef', models.IntegerField()),
                ('contest_coef', models.IntegerField()),
                ('ranking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rankings.StaszicRanking')),
            ],
        ),
    ]
