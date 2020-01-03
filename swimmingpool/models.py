from __future__ import unicode_literals
from datetime import date
from django.db import models
from django.contrib.auth.models import User

class SwimmingPoolTicket(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User)
    moment = models.DateTimeField()

    class Meta:
        unique_together = ['date', 'user']

    def position(self):
        return 1 + SwimmingPoolTicket.objects.filter(date=self.date, moment__lt=self.moment).count()

class SwimmingPoolBlacklist(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User)
    reason = models.TextField()

    class Meta:
        unique_together = ['date', 'user']
