# coding: utf-8
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from django.template.loader import render_to_string
from utils import stacked_inline_for
from models import TableRendererConfig, SummaryRankingConfig
import math

class SummaryMixin(object):
    @classmethod
    def get_mixin_admin_inlines(cls, ranking_type):
        return [stacked_inline_for(SummaryRankingConfig, ranking_type)]

    @property
    def summary_config(self):
        return getattr(self.ranking, 'summaryrankingconfig', SummaryRankingConfig())

    def get_row_summary_config(self, data):
        best_sum = max([0]+[x['sum'] for x in data])
    
        result = []
        if self.summary_config.show_sum:
            result.append((u'∑', lambda x: x['sum']))
        if self.summary_config.show_percentage:
            result.append((u'%', lambda x: ('%.2f' % (100. * x['sum'] / best_sum))))
        if self.summary_config.show_difference:
            result.append((u'±', lambda x: x['sum'] - best_sum))

        return result

    def summarize_row(self, row):
        score_sum = sum(x.score for x in row['scores'] if x is not None)
        row['sum'] = score_sum

    def prepare_render(self, request, ranking_data):
        super(SummaryMixin, self).prepare_render(request, ranking_data)

        for row in ranking_data['data']:
            self.summarize_row(row)

        ranking_data['row_summary'] = self.get_row_summary_config(ranking_data['data'])
    
class RankingRendererBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['ranking_renderers']
    abstract = True

    def __init__(self, ranking):
        self.ranking = ranking

    @classmethod
    def get_admin_inlines(cls):
        return []

    def render(self, request, ranking_data):
        raise NotImplementedError

    def prepare_render(self, request, ranking_data):
        pass

class DebugRenderer(RankingRendererBase):
    description = 'Render debug ranking data'
    type_id = 'debug_renderer'

    def render(self, request, ranking_data):
        import pprint
        return render_to_string('rankings/debug.html', request=request, context=dict(
            rendered_ranking = pprint.pformat(ranking_data)
        ))

class TableRenderer(RankingRendererBase):
    description = 'Tradycyjny rendering w tabelce'
    type_id = 'table_renderer'

    mixins = (SummaryMixin, )

    def render(self, request, ranking_data):
        import pprint

        self.prepare_render(request, ranking_data)

        return render_to_string('rankings/table.html', request=request, context=dict(
            data = ranking_data,
            #debug = pprint.pformat(ranking_data),
            medals = self.get_medals(ranking_data)
        ))

    @classmethod
    def get_admin_inlines(cls):
        return super(TableRenderer, cls).get_admin_inlines() + [stacked_inline_for(TableRendererConfig, cls)]

    @property
    def config(self):
        return getattr(self.ranking, 'tablerendererconfig', TableRendererConfig())

    def get_medal_tresholds(self, data):
        places = len(data['data'])

        if self.config.medals == 'none': return 0, 0, 0
        if self.config.medals == 'og': return 1, 2, 3
        if self.config.medals == 'ioi':
            gold = math.ceil(places / 12.)
            silver = gold + math.ceil(places / 6.)
            bronze = silver + math.ceil(places / 4.)

            return gold, silver, bronze
        assert False

    def get_medals(self, data):
        gold, silver, bronze = self.get_medal_tresholds(data)

        result = []

        for row in data['data']:
            medal = 'medal-none'
            if row['place'] <= gold: medal = 'medal-gold'
            elif row['place'] <= silver: medal = 'medal-silver'
            elif row['place'] <= bronze: medal = 'medal-bronze'

            result.append(medal)

        return result
