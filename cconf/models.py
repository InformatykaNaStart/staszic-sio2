from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from oioioi.contests.models import Contest

class CConfiguration(models.Model):
    contest = models.OneToOneField(Contest)
    compiler = models.CharField(
            max_length=128,
            choices=sorted(settings.C_COMPILERS.items()),
            default=settings.DEFAULT_C_COMPILER)
    cflags = models.CharField(
            max_length=256,
            default=settings.DEFAULT_C_FLAGS)
    cxxflags = models.CharField(
            max_length=256,
            default=settings.DEFAULT_CXX_FLAGS)

import controllers
