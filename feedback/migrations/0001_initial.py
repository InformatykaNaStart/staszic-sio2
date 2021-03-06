# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-18 20:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0002_auto_20180816_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Judging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=32)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Submission')),
            ],
        ),
        migrations.CreateModel(
            name='SmartJudgeConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('off', 'Always judge all tests'), ('on', "Do not judge tests that don't affect score"), ('aft', "Do not judge tests that don't affect score; judge them after presenting the report")], default='aft', max_length=3)),
                ('contest', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
            ],
            options={
                'verbose_name': 'SmartJudge\u2122',
                'verbose_name_plural': 'SmartJudge\u2122',
            },
        ),
    ]
