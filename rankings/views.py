
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from models import StaszicRanking, CachedRankingData, PrivacySettings
from oioioi.base.permissions import make_condition, enforce_condition, not_anonymous
from oioioi.base.menu import menu_registry
from oioioi.contests.utils import can_enter_contest, contest_exists, can_admin_contest, is_contest_admin
from django.core.urlresolvers import reverse
from staszic.new_acm.ranking_types import ACMRanking
from forms import PrivacySettingsForm
import pickle
import csv
import datetime
from datetime import timedelta
from django.http import HttpResponse
import time # debug only

@make_condition()
def has_rankings(request, *args, **kwargs):
    return StaszicRanking.objects.filter(contest = request.contest).exists()

@menu_registry.register_decorator(_("Rankings"),
        lambda request: reverse('default-ranking'),
        order=142)
@enforce_condition(has_rankings & contest_exists & can_enter_contest & not_anonymous)
def ranking_view(request, ranking_id=None):
    if ranking_id is None:
        return redirect('ranking', ranking_id=StaszicRanking.objects.filter(contest=request.contest).latest('order').pk)
    else:
        ranking = get_object_or_404(StaszicRanking, pk=ranking_id, contest=request.contest)

    ts = time.time()
    time_now = datetime.datetime.now()
    min_time = time_now - timedelta(minutes=2)
    entries = CachedRankingData.objects.filter(ranking=ranking, time__gt=min_time)
    generated_at = None
    if len(entries) > 0:
        cached_data = entries[0]
        ranking_data = pickle.loads(cached_data.data)
        generated_at = cached_data.time
    else:
        if isinstance(ranking.type, ACMRanking):
            ranking_data = ranking.type.calculate_data(request)
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

    rankings = StaszicRanking.objects.filter(contest = request.contest).order_by('-order')
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
                'timing': ranking_data['timing'],
            })
    else:
        return render(request, 'rankings/none.html', {})


@enforce_condition(contest_exists & can_enter_contest & is_contest_admin)
def cache_flush_view(request, ranking_id):
    ranking = get_object_or_404(StaszicRanking, pk=ranking_id, contest=request.contest)
    CachedRankingData.objects.filter(ranking=ranking).delete()
    return redirect('ranking', ranking_id=ranking_id)

@enforce_condition(contest_exists & can_enter_contest & is_contest_admin)
def csv_view(request, ranking_id):
    ranking = get_object_or_404(StaszicRanking, pk=ranking_id, contest=request.contest)
    if isinstance(ranking.type, ACMRanking):
        ranking_data = ranking.type.calculate_data(request)
    else:
        ranking_data = ranking.type.calculate_data()
    ranking_data = ranking.type.finalize_ranking(request, ranking_data)
    ranking.renderer.prepare_render(request, ranking_data)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ranking.csv"'\

    writer = csv.writer(response)

    def uwriterow(row):
        writer.writerow([s.encode('utf-8') if isinstance(s, unicode) else s for s in row])

    uwriterow(
        ['']*3 +
        [column.problem_instance.short_name for column in ranking_data['columns']] +
        [summary for summary, _ in ranking_data['row_summary']])
    for row in ranking_data['data']:
        uwriterow(
            [row['place'], row['user'].username, row['user'].get_full_name()] +
            [score.render_score_string() if score else ' ' for score in row['scores']] +
            [f(row) for _, f in ranking_data['row_summary']])
    return response

@enforce_condition(contest_exists & can_enter_contest & not_anonymous)
def privacy_view(request):
    settings, _ = PrivacySettings.objects.get_or_create(user=request.user, contest=request.contest)
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST)
        if form.is_valid():
            settings.hide_scores = form.cleaned_data['hide_scores']
            settings.hide_name = form.cleaned_data['hide_name']
            settings.save()
            return redirect('default-ranking')
    else:
        form = PrivacySettingsForm(instance=settings)
    return render(request, 'rankings/privacy.html', {'form': form})
