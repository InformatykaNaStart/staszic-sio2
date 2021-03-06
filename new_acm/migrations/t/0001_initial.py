# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-27 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0004_auto_20180824_1612'),
        ('rankings', '0006_auto_20180825_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='ACMRankingConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freeze_time', models.IntegerField(default=60)),
                ('penalty_time', models.IntegerField(default=20)),
                ('ignore_ce', models.BooleanField(default=True)),
                ('ranking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rankings.StaszicRanking')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Round')),
            ],
        ),
    ]
