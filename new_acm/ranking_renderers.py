# coding: utf-8
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from django.template.loader import render_to_string
from oioioi.contests.utils import can_enter_contest, contest_exists, can_admin_contest
from staszic.rankings.ranking_renderers import SummaryMixin, TableRenderer
import math

class ACMSummaryMixin(object):
    @classmethod
    def get_mixin_admin_inlines(cls, ranking_type):
        return []

    def summarize_row(self, row):
        row['scoresum'] = sum([x.score for x in row['scores'] if x is not None])
        row['timesum'] = sum([x.acmtime for x in row['scores'] if x is not None and x.score != 0])
        row['timesum'] += sum([(x.ntries-1)*20 for x in row['scores'] if x is not None and x.score != 0])

    def get_row_summary_config(self, data):
        result = []
        result.append((u'✔', lambda x: x['scoresum']))
        result.append((u'🕑', lambda x: x['timesum']))
        return result
        
class ACMRenderer(TableRenderer):
    description = 'Rendering dla ACM'
    type_id = 'acm_renderer'
    mixins = (ACMSummaryMixin, )

    def render(self, request, ranking_data):
        import pprint

        self.prepare_render(request, ranking_data)

        return render_to_string('new_acm/acm.html', request=request, context=dict(
            data = ranking_data,
            medals = self.get_medals(ranking_data),
            frozen = ranking_data['ranking'].is_frozen(request.timestamp),
            can_admin = can_admin_contest(request.user, request.contest)
        ))


