from __future__ import unicode_literals

from django.contrib.auth.models import User
from oioioi.contests.models import Round
from django.db import models

class VirtualContest(models.Model):
    round = models.OneToOneField(Round)
    duration = models.IntegerField(help_text='duration in minutes')
    
    difficulty = models.IntegerField()
    description = models.TextField()

    def __unicode__(self):
        return self.round.name

class VirtualContestEntry(models.Model):
    contest = models.ForeignKey(VirtualContest)
    user = models.ForeignKey(User)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
