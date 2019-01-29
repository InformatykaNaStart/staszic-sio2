from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from models import StaszicRanking, CachedRankingData
from oioioi.base.permissions import make_condition, enforce_condition
from oioioi.base.menu import menu_registry
from oioioi.contests.utils import can_enter_contest, contest_exists, can_admin_contest
from django.core.urlresolvers import reverse
import pickle
import datetime
from datetime import timedelta
import time # debug only

@make_condition()
def has_rankings(request, *args, **kwargs):
    return StaszicRanking.objects.filter(contest = request.contest).exists()

@menu_registry.register_decorator(_("Rankings"),
        lambda request: reverse('default-ranking'),
        order=142)
@enforce_condition(has_rankings & contest_exists & can_enter_contest)
def ranking_view(request, ranking_id=None):
    if ranking_id is None:
        ranking = StaszicRanking.objects.filter(contest=request.contest).earliest('pk')
    else:
        ranking = get_object_or_404(StaszicRanking, pk=ranking_id, contest=request.contest)


    if 'ACM' in str(ranking.type):
        ranking_data = ranking.type.calculate_data(request)
    else:
        ts = time.time()
        time_now = datetime.datetime.now()
        min_time = time_now - timedelta(minutes=2)
        entries = CachedRankingData.objects.filter(ranking=ranking, time__gt=min_time)
        generated_at = time
        if len(entries) > 0:
            cached_data = entries[0]
            ranking_data = pickle.loads(cached_data.data)
            generated_at = cached_data.time
        else:
            ranking_data = ranking.type.calculate_data()
            CachedRankingData.objects.filter(ranking=ranking).delete()
            entry = CachedRankingData(ranking=ranking, time=time_now, data=pickle.dumps(ranking_data))
            entry.save()
        ranking_data['timing']['generate'] = time.time() - ts

    ts = time.time()
    ranking_data = ranking.type.finalize_ranking(request, ranking_data)
    ranking_data['timing']['finalize'] = time.time() - ts

    rendered_ranking = ranking.renderer.render(request, ranking_data)

    rankings = StaszicRanking.objects.filter(contest = request.contest)
    visible_rankings = []
    for r in rankings:
        if r.type.has_any_visible_columns(request):
            visible_rankings.append(r)

    if len(visible_rankings) > 0:
        return render(request, 'rankings/ranking.html', {
                'can_admin': can_admin_contest(request.user, request.contest),
                'ranking': ranking,
                'rendered_ranking': rendered_ranking,
                'rankings': visible_rankings,
                'generated_at': generated_at,
                'timing': ranking_data['timing']
            })
    else:
        return render(request, 'rankings/none.html', {})
