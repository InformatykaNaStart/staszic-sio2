from __future__ import unicode_literals

from django.db import models
from oioioi.base.fields import DottedNameField
from django.utils.module_loading import import_string
from oioioi.contests.models import Round
from utils import stacked_inline_for
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class StaszicRanking(models.Model):
    name = models.CharField(max_length=255)
    type_name = DottedNameField('staszic.rankings.ranking_types.RankingTypeBase')
    renderer_name = DottedNameField('staszic.rankings.ranking_renderers.RankingRendererBase')
    contest = models.ForeignKey('contests.Contest')

    order = models.IntegerField(null=True, blank=True, default=0)

    last_calculation = models.DateTimeField(null=True, blank=True)
    serialized_data = models.TextField()

    @property
    def type(self):
        return import_string(self.type_name)(self)

    @property
    def renderer(self):
        return import_string(self.renderer_name)(self)

SUBMISSION_TYPES = [
    ('best', 'Best'),
    ('last', 'Last'),
    ('rlast', 'Last + revealed'),
]

COLUMN_VISIBILITY_TYPES = [
    ('never',  'Never visible'),
    ('end',    'Visible after the round ends'),
    ('results','Visible as the round results become visible'),
    ('always', 'Visible after the round starts')
]

ORDER_TYPES = [
    ('max', 'maximum score'),
    ('min', 'minimum score'),
]

class RoundRankingConfig(models.Model):
    ranking = models.OneToOneField(StaszicRanking)

    round = models.CharField(verbose_name='Round name (empty for all rounds)', max_length=256, blank=True, default='')
    round_coef = models.IntegerField(default=1, verbose_name="Contest coefficient")
    round_type = models.CharField(max_length=8, choices=SUBMISSION_TYPES, default='last', verbose_name='Contest scoring type')
    contest_coef = models.IntegerField(default=0, verbose_name='All-time coefficient')
    contest_type = models.CharField(max_length=8, choices=SUBMISSION_TYPES, verbose_name='All-time scoring type', default='best')

    order = models.CharField(max_length=3, choices=ORDER_TYPES, verbose_name='Best solution', default='max')
    column_visibility = models.CharField(max_length=8, choices=COLUMN_VISIBILITY_TYPES, default='end')
    trial_visibility = models.BooleanField(default=False, verbose_name='Trial round visibility')

    ignore_submissions_after = models.DateTimeField(verbose_name='Ignore submissions after', null=True, blank=True)

    @property
    def dict_config(self):
        return dict(
            round = self.round,
            round_coef = self.round_coef,
            round_type = self.round_type,
            contest_coef = self.contest_coef,
            contest_type = self.contest_type,
            visibility_type = self.column_visibility,
            trial_visibility = self.trial_visibility,
            order = self.order,
            ignore_submissions_after = self.ignore_submissions_after,
            )


class MultiroundRankingConfig(models.Model):
    ranking = models.OneToOneField(StaszicRanking)

    round_coef = models.IntegerField(default=1, verbose_name="Contest coefficient")
    round_type = models.CharField(max_length=8, choices=SUBMISSION_TYPES, default='last', verbose_name='Contest scoring type')
    contest_coef = models.IntegerField(default=0, verbose_name='All-time coefficient')
    contest_type = models.CharField(max_length=8, choices=SUBMISSION_TYPES, verbose_name='All-time scoring type', default='best')

    column_visibility = models.CharField(max_length=8, choices=COLUMN_VISIBILITY_TYPES, default='end')
    ignore_submissions_after = models.DateTimeField(verbose_name='Ignore submissions after', null=True, blank=True)

    @property
    def dict_config(self):
        return dict(
            round_coef = self.round_coef,
            round_type = self.round_type,
            contest_coef = self.contest_coef,
            contest_type = self.contest_type,
            visibility_type = self.column_visibility,
            ignore_submissions_after = self.ignore_submissions_after,
            trial_visibility=True,
            )


class AdvancedRankingConfig(models.Model):
    ranking = models.ForeignKey(StaszicRanking)
    round = models.CharField(verbose_name='Round name', max_length=256)
    start_date = models.DateTimeField(verbose_name='Ignore submissions before')
    end_date = models.DateTimeField(verbose_name='Ignore submissions after')
    column_visibility = models.CharField(max_length=8, choices=COLUMN_VISIBILITY_TYPES, default='end')
    
    @property
    def dict_config(self):
        return dict(
            visibility_type = self.column_visibility,
            )

class SummaryRankingConfig(models.Model):
    ranking = models.OneToOneField(StaszicRanking)

    show_sum = models.BooleanField(default = True)
    show_percentage = models.BooleanField(default = False)
    show_difference = models.BooleanField(default = False)

MEDALS_CHOICES = [
    ('none', 'No medals'),
    ('ioi', 'IOI - 1/12 golds, 1/6 silver, 1/4 bronze'),
    ('og', '1 gold, 1 silver, 1 bronze')
]

class TableRendererConfig(models.Model):
    ranking = models.OneToOneField(StaszicRanking)

    medals = models.CharField(max_length=8, choices=MEDALS_CHOICES, default='none')


class RoundInRanking(models.Model):
    ranking = models.ForeignKey(StaszicRanking)
    round = models.ForeignKey(Round)


class CachedRankingData(models.Model):
    time = models.DateTimeField()
    data = models.BinaryField()
    ranking = models.ForeignKey(StaszicRanking)

class PrivacySettings(models.Model):
    contest = models.ForeignKey('contests.Contest')
    user = models.ForeignKey(User)
    hide_scores = models.BooleanField(default=False, verbose_name=_('Hide scores'))
    hide_name = models.BooleanField(default=False, verbose_name=_('Hide name'))
    class Meta:
        unique_together=[['contest', 'user']]
