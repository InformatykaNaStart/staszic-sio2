# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from oioioi.base.permissions import enforce_condition, not_anonymous
from oioioi.contests.utils import can_enter_contest, contest_exists
from models import VirtualContest, VirtualContestEntry
from utils import get_current_virtual_contest, contest_has_vcontests
from oioioi.base.menu import menu_registry
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from datetime import timedelta
from django.contrib import messages

@menu_registry.register_decorator(
    "Virtual contests",
    lambda request: reverse('virtual-contests'),
    order=110
    )

@enforce_condition(contest_exists & can_enter_contest & not_anonymous & contest_has_vcontests)
def virtual(request):
    current_contest_entry = get_current_virtual_contest(request)
    controller = request.contest.controller

    if current_contest_entry is not None:
        return render(request, 'virtual/active.html', dict(
            vc=current_contest_entry.contest,
            actions=sorted(controller.get_virtual_contest_actions(request, current_contest_entry.contest)),
            vce=current_contest_entry))

    else:
        vcs = VirtualContest.objects.filter(round__contest=request.contest)

        if not vcs.exists():
            return render(request, 'virtual/no-contests.html')

        vc_infos = []

        for vc in vcs:
            vc_infos.append(dict(
                vc=vc,
                actions=sorted(controller.get_virtual_contest_actions(request, vc))
            ))


        return render(request, 'virtual/list.html', dict(
            vcs=vc_infos
        ))

@enforce_condition(contest_exists & can_enter_contest & contest_has_vcontests & not_anonymous)
def info(request, vcontest_id):
    controller = request.contest.controller
    contest = get_object_or_404(VirtualContest, pk=vcontest_id, round__contest=request.contest)

    pinfos = [controller.get_virtual_problem_info(pi) for pi in contest.round.probleminstance_set.order_by('short_name')]

    total_score = sum(x['max_score'] for x in pinfos)

    return render(request, 'virtual/info.html', dict(
        vcontest = contest,
        problems = pinfos,
        total_score = total_score
    ))

@enforce_condition(contest_exists & can_enter_contest & not_anonymous & contest_has_vcontests)
def start(request, vcontest_id):
    controller = request.contest.controller
    contest = get_object_or_404(VirtualContest, pk=vcontest_id, round__contest=request.contest)

    if not controller.can_start_contest(request, contest):
        messages.error(request, 'Niestety, nie możesz, z jakichś przyczyn rozpocząć tego konkursu.')
        return redirect('virtual-info', vcontest_id=contest.id)

    VirtualContestEntry.objects.create(contest=contest, user=request.user, start_date = request.timestamp, end_date=request.timestamp + timedelta(minutes=contest.duration))

    messages.success(request, 'Udało się rozpocząć konkurs. Powodzenia!')
    return redirect('problems_list')


@enforce_condition(contest_exists & can_enter_contest & not_anonymous & contest_has_vcontests)
def finish(request, vcontest_id):
    controller = request.contest.controller
    contest = get_object_or_404(VirtualContest, pk=vcontest_id, round__contest=request.contest)

    if not controller.can_finish_contest(request, contest):
        messages.error(request, 'Niestety, nie możesz, z jakichś przyczyn zakończyć tego konkursu.')
        return redirect('virtual-info', vcontest_id=contest.id)

    VirtualContestEntry.objects.filter(contest=contest, user=request.user).update(end_date=request.timestamp)

    messages.success(request, 'Udało się zakończyć konkurs. Dziękujemy za wspólną zabawę!')
    return redirect('virtual-info', vcontest_id=contest.id)
