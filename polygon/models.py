from __future__ import unicode_literals

from django.db import models
from oioioi.base.fields import EnumRegistry, EnumField

import_statuses = EnumRegistry()
import_statuses.register('QU', 'Queued')
import_statuses.register('ST', 'Importing statement')
import_statuses.register('CH', 'Importing checker')
import_statuses.register('TE', 'Importing tests')
import_statuses.register('SO', 'Importing solutions')
import_statuses.register('OK', 'Done')
import_statuses.register('KO', 'Error')

class PolygonImportRequest(models.Model):
    problem_id = models.IntegerField()
    contest = models.ForeignKey('contests.Contest', null=True, blank=True)
    problem_name = models.CharField(max_length=100)
    celery_task_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = EnumField(import_statuses, default='QU')
    info = models.TextField(null=True, blank=True)
