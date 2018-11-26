from __future__ import unicode_literals

from django.db import models
from oioioi.contests.models import Contest
from django.utils.module_loading import import_string
from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _

def mkrc(sender, instance, created, **kwargs):
    if created:
        ReportConfig.objects.create(contest=instance)

models.signals.post_save.connect(mkrc, sender=Contest, weak=False,
                          dispatch_uid='models.mkrc')

class ReportConfig(models.Model):
    contest = models.OneToOneField(Contest)
    stderr_visible = models.BooleanField(default=False, blank=True)
    comment_visible = models.BooleanField(default=True, blank=True)

    class Meta(object):
        verbose_name = 'report elements visible for the participant'
        verbose_name_plural = 'report elements visible for the participant'
