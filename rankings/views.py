from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from models import StaszicRanking
from oioioi.base.permissions import make_condition, enforce_condition
from oioioi.base.menu import menu_registry
from oioioi.contests.utils import can_enter_contest, contest_exists, can_admin_contest
from django.core.urlresolvers import reverse

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
        ranking_data = ranking.type.calculate_data()
    ranking_data = ranking.type.finalize_ranking(request, ranking_data)

    rendered_ranking = ranking.renderer.render(request, ranking_data)

    rankings = StaszicRanking.objects.filter(contest = request.contest)

    return render(request, 'rankings/ranking.html', {
            'can_admin': can_admin_contest(request.user, request.contest),
            'ranking': ranking,
            'rendered_ranking': rendered_ranking,
            'rankings': rankings,
        })
