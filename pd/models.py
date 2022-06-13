from __future__ import unicode_literals
from django.contrib.auth.models import User
from oioioi.contests.models import Contest
from django.db import models

class PersonalDataPass(models.Model):
    user = models.OneToOneField(User)
    #wildcard = models.BooleanField(default=False)
    #contest = models.ManyToManyField(Contest, null=True, blank=True)
    def __unicode__(self):
        r = self.user.first_name + ' ' + self.user.last_name + ' (' + self.user.username + ')'
        return r
    class Meta:
        verbose_name_plural = "Personal Data Passes"
