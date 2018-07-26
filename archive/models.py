from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from oioioi.base.fields import DottedNameField
from django.utils.module_loading import import_string
from oioioi.contests.models import submission_statuses
from oioioi.base.fields import EnumRegistry, EnumField
from oioioi.filetracker.fields import FileField
import os.path

def make_problem_filename(instance, filename):
    return 'oldproblems/%d/%s' % (instance.problem_id, os.path.basename(filename))

def make_submission_filename(instance, filename):
    return 'oldsubmissions/%s/%s' % (instance.problem_instance.contest.short_name, os.path.basename(filename))

class StaszicOldUser(models.Model):
    parent = models.ForeignKey(User, default=None, blank=True, null=True)
    username = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    is_superuser = models.BooleanField(default=False)

class StaszicOldContest(models.Model):
    short_name = models.CharField(max_length=512, default=None, blank=True, null=True)
    name = models.CharField(max_length=512)
    sio2dead = models.BooleanField(default=False)

class StaszicOldContestAdminPermission(models.Model):
    contest = models.ForeignKey(StaszicOldContest)
    user = models.ForeignKey(StaszicOldUser)

class StaszicOldProblem(models.Model):
    problem_id = models.IntegerField(default=0)
    short_name = models.CharField(max_length=64)
    name = models.CharField(max_length=512)
    package = models.FileField(upload_to=make_problem_filename, default=None, blank=True, null=True)
    statement = models.FileField(upload_to=make_problem_filename, default=None, blank=True, null=True)
    sio2dead = models.BooleanField(default=False)

class StaszicOldProblemInstance(models.Model):
    problem = models.ForeignKey(StaszicOldProblem, default=None, blank=True, null=True)
    contest = models.ForeignKey(StaszicOldContest, default=None, blank=True, null=True)
    round = models.CharField(max_length=512)

class StaszicOldSubmission(models.Model):
    submission_id = models.IntegerField(default=0)
    author = models.ForeignKey(StaszicOldUser, default=None, blank=True, null=True)
    score = models.IntegerField(blank=True,null=True)
    status = EnumField(submission_statuses)
    problem_instance = models.ForeignKey(StaszicOldProblemInstance, default=None, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    source = FileField(upload_to=make_submission_filename, default=None, blank=True, null=True)
