import math
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from staszic.rankings.ranking_scores import SingleScore, CombinedScore
from django.template import Engine, Context
from oioioi.contests.views import problem_statement_view
from django.core.urlresolvers import reverse
from staszic.rankings.ranking_columns import ProblemInstanceColumn
from ranking_scores import ACMScore


class ACMColumn(ProblemInstanceColumn):
    description = 'ACM Problem Instance'
    
    def __init__(self, ranking, request, problem_instance, ignore_ce=True, penalty_time=20*60, freeze_time=0, unfreeze=None):
        super(ACMColumn, self).__init__(ranking, problem_instance, 1, 'last', 0, 'last', 'always', False)
        self.ignore_ce = ignore_ce
        self.ranking = ranking.type
        self.request = request

    def score_for_sub(self, sub):
        reltime = int(sub.problem_instance.contest.controller.get_submission_relative_time(sub)/60)
        return ACMScore(sub.user, sub, sub.score.to_int(), reltime, self.ranking, self.request)

