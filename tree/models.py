from __future__ import unicode_literals
from oioioi.contests.models import Contest
from django.db import models

class ContestGroup(models.Model):
    name = models.CharField(max_length=100)
    parent_contest = models.ForeignKey('ContestGroup', blank=True, null=True)
    order = models.IntegerField()

    contest = models.ManyToManyField(Contest)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-order']
