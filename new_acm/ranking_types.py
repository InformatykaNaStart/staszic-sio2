from staszic.rankings.ranking_types import RankingTypeBase
from staszic.rankings.utils import stacked_inline_for
from models import ACMRankingConfig
from staszic.new_acm.ranking_columns import ACMColumn
from staszic.rankings.ranking_columns import ProblemInstanceColumn
from oioioi.contests.models import ProblemInstance, Round
from datetime import datetime, timedelta

class ACMRanking(RankingTypeBase):
    description = 'ACM Ranking'
    type_id = 'acm_ranking'

    @classmethod
    def get_admin_inlines(cls):
        return [stacked_inline_for(ACMRankingConfig, cls)]

    def is_frozen(self, t):
        rounds = Round.objects.filter(contest=self.contest).order_by('end_date')
        return (t > self.freeze_time and t < rounds[0].end_date)

    @property
    def config(self):
        if hasattr(self.ranking, 'acmrankingconfig'):
            return self.ranking.acmrankingconfig
        return ACMRankingConfig()

    def get_columns(self, request):
        result = []
        pis = ProblemInstance.objects.filter(round__contest=self.contest).order_by('round__start_date', 'short_name')
        for problem_instance in pis:
            result.append(ACMColumn(self.ranking, request, problem_instance, **self.config.dict_config))
        return result

    def put_keys(self, request, ranking_data):
        for row in ranking_data['data']:
            ss = sum([x.score for x in row['scores'] if x is not None])
            ts = sum([x.acmtime for x in row['scores'] if x is not None and x.score != 0])
            ts += sum([(x.ntries-1)*20 for x in row['scores'] if x is not None and x.score != 0])
            row['key'] = -(ss*1000000-ts)
        return ranking_data

    def calculate_data(self, request):
        res = super(ACMRanking, self).calculate_data(request)
        res['ranking'] = self
        return res

    def has_any_visible_columns(self, request):
        return True

    @property
    def freeze_time(self):
        rounds = Round.objects.filter(contest=self.contest).order_by('end_date')
        return rounds[0].end_date - timedelta(minutes=self.config.dict_config['freeze_time'])


    def setrequest(self, request):
        self.request = request
