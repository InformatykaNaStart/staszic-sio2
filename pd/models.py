from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class PersonalDataPass(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + self.user.username + ')'
    class Meta:
        verbose_name_plural = "Personal Data Passes"