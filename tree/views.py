from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from oioioi.base.permissions import not_anonymous, make_condition, enforce_condition
from oioioi.base.menu import menu_registry, account_menu_registry
from oioioi.contests.utils import can_enter_contest, contest_exists, visible_contests
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, Http404, HttpResponse
from oioioi.base.menu import menu_registry

def contests_tree_view(request):
    contests = sorted(visible_contests(request), key=lambda x: x.creation_date)[::-1]

    groups = {}
    for contest in contests:
        for cgroup in contest.contestgroup_set.all():
            if cgroup not in groups:
                groups[cgroup] = [contest]
            else:
                groups[cgroup].append(contest)

    to_show = sorted(groups.items(), key=lambda x: -x[0].order)

    return render(request, 'tree/tree.html',
            {'to_show': to_show})
