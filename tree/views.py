from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from oioioi.base.permissions import not_anonymous, make_condition, enforce_condition
from oioioi.base.menu import menu_registry, account_menu_registry
from oioioi.contests.utils import can_enter_contest, contest_exists, visible_contests
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, Http404, HttpResponse
from oioioi.base.menu import menu_registry
from oioioi.base.main_page import register_main_page_view
from django.conf import settings
from models import ContestGroup

import re


def get_visible_contests(request):
    contests = sorted(visible_contests(request), key=lambda x: x.creation_date)[::-1]
    if settings.STASZIC_CONTEST_MODE and not request.user.is_superuser:
        contests = [contest for contest in contests if re.match(settings.STASZIC_CONTEST_MODE, contest.pk)]
        r
    return contests

def make_contests_map(contests):
    contests_map = {}
    for contest in contests:
        for cgroup in contest.contestgroup_set.all():
            if cgroup not in contests_map:
                contests_map[cgroup] = [contest]
            else:
                contests_map[cgroup].append(contest)
    for group in contests_map:
        contests_map[group] = sorted(contests_map[group], key=lambda contest: contest.id)
    return contests_map

def make_tree(contests_map, group=None, indent=-1):
    def nonempty_subgroups(g):
        result = [g] if g in contests_map else []
        for sg in ContestGroup.objects.filter(parent_contest=g):
            result += nonempty_subgroups(sg)
        return result

    result = []

    subgroups = ContestGroup.objects.filter(parent_contest=group)
    subgroups = sorted(subgroups, key=lambda x: -x.order)

    if len(nonempty_subgroups(group)) == 1:
        # There is only one non-empty subgroup, so we steal it contests and become a leaf.
        result.append((indent, group, contests_map[nonempty_subgroups(group)[0]]))
    else:
        my_contests = contests_map.get(group, []) 
        if my_contests:
            result.append((indent, group, my_contests))
    
        for subgroup in subgroups:
            subgroup_result = make_tree(contests_map, subgroup, indent+1)
            if subgroup_result:
                result += subgroup_result
       
    return result


@register_main_page_view(order=90)
def contests_tree_view(request): 

    tree = make_tree(make_contests_map(get_visible_contests(request)))
    return render(request, 'tree/tree.html',
            {'tree': tree})
