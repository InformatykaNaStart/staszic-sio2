from __future__ import unicode_literals

from django.db import models
from oioioi.contests.models import Round, ProblemInstance, Submission
from django.contrib.auth.models import Group

class ExamConfig(models.Model):
    round = models.ForeignKey(Round)
    user_group = models.ForeignKey(Group, blank=True, null=True)
    notsubmittable_problems = models.ManyToManyField(ProblemInstance)
    show_scores = models.BooleanField()

    def __unicode__(self):
        return u'<ExamConfig: round={}, user_group={}, notsubmittable={}, show_scores={}>'.format(
                self.round,
                self.user_group,
                [p.short_name for p in self.notsubmittable_problems.all()],
                self.show_scores
        )

class ExamSubmissionCopy(models.Model):
    original_submission = models.ForeignKey(Submission, related_name='copies')
    copied_submission = models.ForeignKey(Submission, related_name='originals')
