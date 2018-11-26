from __future__ import unicode_literals

from django.db import models
from staszic.rankings.models import StaszicRanking
from oioioi.contests.models import Round

class ACMRankingConfig(models.Model):
    ranking=models.OneToOneField(StaszicRanking)
    freeze_time=models.IntegerField(default=60)
    unfreeze=models.DateTimeField(blank=True, null=True)
    penalty_time=models.IntegerField(default=20)
    ignore_ce=models.BooleanField(default=True)

    @property
    def dict_config(self):
        return dict(
            freeze_time=self.freeze_time,
            penalty_time=self.penalty_time,
            ignore_ce=self.ignore_ce,
            unfreeze = self.unfreeze)
