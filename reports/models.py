from __future__ import unicode_literals

from django.db import models
from oioioi.contests.models import Contest
from django.utils.module_loading import import_string
from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _

class ReportConfig(models.Model):
    contest = models.OneToOneField(Contest)
    stderr_visible = models.NullBooleanField(default=False, null=True, blank=True)
    comment_visible = models.NullBooleanField(default=False, null=True, blank=True)

    class Meta(object):
        verbose_name = 'report element visible for the participant'
        verbose_name_plural = 'report elements visible for the participant'
