# coding: utf-8
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from oioioi.contests.models import ProblemInstance, Round
from utils import stacked_inline_for, tabular_inline_for
from ranking_columns import ProblemInstanceColumn
from models import RoundRankingConfig, AdvancedRankingConfig, MultiroundRankingConfig, RoundInRanking
from django.contrib.admin import StackedInline
from django.db import connection

class RankingTypeBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['ranking_types']
    abstract = True

    def __init__(self, ranking):
        self.ranking = ranking
        self.contest = ranking.contest
        self.request = 23

    def get_columns(self):
        raise NotImplementedError

    @classmethod
    def get_admin_inlines(cls):
        return []

    def calculate_data(self, request = None):
        start_queries = len(connection.queries)
        data = []
        umap = {}
        if request is None:
            columns = self.get_columns()
        else:
            columns = self.get_columns(request)

        ncolumns = len(columns)

        for i, column in enumerate(columns):
            scores = column.get_scores()

            for k, v in scores.items():
                if k not in umap:
                    row = dict(user=k, scores=[None] * ncolumns)
                    umap[k] = row
                    data.append(row)
                else:
                    row = umap[k]

                row['scores'][i] = v

        ranking = dict(
                columns = columns,
                data = data,
                timing = dict(queries=len(connection.queries) - start_queries),
        )
        return ranking

    def finalize_ranking(self, request, ranking_data):
        ranking_data = self.filter_columns(request, ranking_data)
        ranking_data = self.put_keys(request, ranking_data)
        ranking_data = self.order_rows(request, ranking_data)
        ranking_data = self.put_places(request, ranking_data)

        return ranking_data

    def has_any_visible_columns(self, request):
        columns = self.get_columns()
        return any([column.can_access(request) for column in columns])


    def filter_columns(self, request, ranking_data):
        all_columns = ranking_data['columns']
        selector = [column.can_access(request) for column in all_columns]

        def select(data, selector):
            return [piece for piece, sel in zip(data, selector) if sel]

        ranking_data['columns'] = select(ranking_data['columns'], selector)

        new_scores = []
        for row in ranking_data['data']:
            row['scores'] = select(row['scores'], selector)
            if any(x is not None for x in row['scores']):
                new_scores.append(row)

        ranking_data['data'] = new_scores
        return ranking_data
    
    def put_keys(self, request, ranking_data):
        for row in ranking_data['data']:
            row['key'] = -sum(score.score for score in row['scores'] if score is not None)

        return ranking_data

    def order_rows(self, request, ranking_data):
        ranking_data['data'].sort(key=lambda x: x['key'])
        return ranking_data

    def put_places(self, request, ranking_data):
        curr_place = 0
        last_score = None
        idx = 1

        for row in ranking_data['data']:
            if row['key'] != last_score:
                curr_place = idx
            last_score = row['key']
            idx += 1

            row['place'] = curr_place
        return ranking_data

    @classmethod
    def is_valid_for_contest(self, contest_controller):
        return True

class AdvancedRanking:
    description = 'Dont-use-it ranking'
    type_id = 'hugo_ranking'

    @classmethod
    def get_admin_inlines(cls):
        x = super(AdvancedRanking, cls).get_admin_inlines()+[stacked_inline_for(AdvancedRankingConfig, cls, dict(can_delete=True, can_add=True, min_num=0, extra=0))]
        return x

    @property
    def config(self):
        return AdvancedRankingConfig()

    def get_columns(self):
        result = []
        configs = AdvancedRankingConfig.objects.filter(ranking=self.ranking)
        for config in configs:
                try:
                    round = Round.objects.get(name=config.round, contest=self.contest)
                    for problem_instance in ProblemInstance.objects.filter(round=round).order_by('short_name'):
                        params = dict(round_coef=0, contest_coef=1, contest_type='last', round_type='last', start_date=config.start_date, end_date=config.end_date)
                        params.update(config.dict_config)
                        result.append(ProblemInstanceColumn(self.ranking, problem_instance, **params))
                except IOError:
                    pass
        return result


class ContestRanking(RankingTypeBase):
    description = 'Ranking'
    type_id = 'contest_ranking'

    @classmethod
    def get_admin_inlines(cls):
        return super(ContestRanking, cls).get_admin_inlines() + [stacked_inline_for(RoundRankingConfig, cls)]

    @property
    def config(self):
        if hasattr(self.ranking, 'roundrankingconfig'):
            return self.ranking.roundrankingconfig
        return RoundRankingConfig()

    def get_columns(self):
        result = []
        r = self.config.dict_config['round'].strip()
        cfg = self.config.dict_config
        cfg.pop('round', None)
        if r == '':
            pis = ProblemInstance.objects.filter(round__contest=self.contest).order_by('round__start_date', 'short_name')
            if self.config.dict_config['trial_visibility']:
                pis.filter(round__is_trial)
            for problem_instance in pis:
                result.append(ProblemInstanceColumn(self.ranking, problem_instance, **cfg))
        else:
            for problem_instance in ProblemInstance.objects.filter(round__contest=self.contest, round__name=r).order_by('round__start_date', 'short_name'):
                result.append(ProblemInstanceColumn(self.ranking, problem_instance, **cfg))
        return result


class MultiroundRanking(RankingTypeBase):
    description = 'Multiround ranking'
    type_id = 'multiround_ranking'

    @classmethod
    def get_admin_inlines(cls):
        return super(MultiroundRanking, cls).get_admin_inlines() + [stacked_inline_for(MultiroundRankingConfig, cls), RoundInRankingInline]

    @property
    def config(self):
        if hasattr(self.ranking, 'multiroundrankingconfig'):
            return self.ranking.multiroundrankingconfig
        return MultiroundRankingConfig()

    def get_columns(self):
        result = []
        cfg = self.config.dict_config
        rounds = [r.round.id for r in RoundInRanking.objects.filter(ranking=self.ranking.id)]
        pis = ProblemInstance.objects.filter(round__contest=self.contest, round__id__in=rounds).order_by('round__start_date', 'short_name')
        for problem_instance in pis:
            result.append(ProblemInstanceColumn(self.ranking, problem_instance, **cfg))
        return result


class RoundInRankingInline(StackedInline):
    model = RoundInRanking
    ranking_type = 'multiround_ranking'
    extra = 0
    inline_classes = ('collapse open', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "round":
            kwargs["queryset"] = Round.objects.filter(contest=request.contest)
        return super(RoundInRankingInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        # Protected by parent ModelAdmin
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_fieldsets(self, request, obj=None):
        fields = ['round']
        fdsets = [(None, {'fields': fields})]
        return fdsets
