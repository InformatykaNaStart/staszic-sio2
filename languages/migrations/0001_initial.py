# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-16 19:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0002_auto_20180816_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('languages_desc', models.CharField(default='staszic.languages.languages.CProgrammingLanguage,staszic.languages.languages.CppProgrammingLanguage', max_length=1024)),
                ('problem_instance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
            ],
            options={
                'verbose_name': 'language config',
                'verbose_name_plural': 'language configs',
            },
        ),
    ]
