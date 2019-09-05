from __future__ import unicode_literals

from django.db import models
from oioioi.problems.models import Problem, make_problem_filename

HOOK_TYPES = (
    ('compile', 'Haczyk kompilacji'),
    ('run', 'Haczyk uruchomienia')
        )

class ProblemHooks(models.Model):
    problem = models.OneToOneField(Problem)
    content = models.FileField(upload_to=make_problem_filename)
    type    = models.TextField(max_length=8, choices=HOOK_TYPES)
