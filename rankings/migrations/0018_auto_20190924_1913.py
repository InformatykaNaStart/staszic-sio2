# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-09-24 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0017_roundrankingconfig_ignore_submissions_after'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='privacysettings',
            unique_together=set([('contest', 'user')]),
        ),
    ]