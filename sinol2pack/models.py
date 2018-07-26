from __future__ import unicode_literals

from django.db import models
from oioioi.problems.models import Problem, make_problem_filename

class ProblemHooks(models.Model):
    problem = models.OneToOneField(Problem)
    content = models.FileField(upload_to=make_problem_filename)
