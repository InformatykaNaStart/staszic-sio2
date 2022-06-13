from __future__ import unicode_literals
from oioioi.contests.models import Contest
from django.db import models
from django.core.exceptions import ValidationError
from django import forms

class ContestGroup(models.Model):
    name = models.CharField(max_length=100)
    parent_contest = models.ForeignKey('ContestGroup', blank=True, null=True)
    order = models.IntegerField()

    contest = models.ManyToManyField(Contest, blank=True)

    def path(self):
        if self.parent_contest:
            pp = self.parent_contest.path()
        else:
            pp = []
        pp.append(self)
        return pp

    def __unicode__(self):
        return ' / '.join([g.name for g in self.path()])

    def clean(self):
        if self.parent_contest == self:
            raise ValidationError("A contest group can't be its own parent")
        visited = set()
        at = self
        while at:
            visited.add(str(at))
            at = at.parent_contest
            if str(at) in visited:
                raise ValidationError("Cycle in the tree!")

    class Meta:
        ordering = ['-order']
