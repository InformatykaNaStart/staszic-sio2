# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from oioioi.contests.models import Contest, submission_statuses, Submission
from django.contrib.postgres.fields import JSONField

# Create your models here.

SMARTJUDGE_MODES = [
    ('off', 'Always judge all tests'),
    ('on', "Do not judge tests that don't affect score"),
#    ('aft', "Do not judge tests that don't affect score; judge them after presenting the report"),
]

JUDGING_MODES = [
    ('off', 'Do not show judgings table'),
    ('pro', 'Show judging progress table'),
    ('all', 'Show judging progress and results table'),
]

submission_statuses.register('NJ', _("Not judged"))

class SmartJudgeConfig(models.Model):
    contest = models.OneToOneField(Contest)
    mode = models.CharField(max_length=3, choices=SMARTJUDGE_MODES, default='on')

    class Meta:
        verbose_name = 'SmartJudge™'
        verbose_name_plural = verbose_name

class JudgingConfig(models.Model):
    contest = models.OneToOneField(Contest)
    mode = models.CharField(max_length=3, choices=JUDGING_MODES, default='pro')

    class Meta:
        verbose_name = 'SmartJudge™ Judging table'
        verbose_name_plural = verbose_name

class Judging(models.Model):
    submission = models.ForeignKey(Submission)
    kind = models.CharField(max_length=32)
    config = JSONField(default=dict)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '<Judging pk=%d submission=%d kind=%s config=%s>' % (self.pk, self.submission.pk, self.kind, self.config)
