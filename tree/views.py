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
import re

@register_main_page_view(order=90)
def contests_tree_view(request):
    contests = sorted(visible_contests(request), key=lambda x: x.creation_date)[::-1]
    if settings.STASZIC_CONTEST_MODE and not request.user.is_superuser:
        contests = [contest for contest in contests if re.match(settings.STASZIC_CONTEST_MODE, contest.pk)]

    groups = {}
    for contest in contests:
        for cgroup in contest.contestgroup_set.all():
            if cgroup not in groups:
                groups[cgroup] = [contest]
            else:
                groups[cgroup].append(contest)
            groups[cgroup] = sorted(groups[cgroup], key=lambda contest: contest.id)
    to_show = sorted(groups.items(), key=lambda x: -x[0].order)

    return render(request, 'tree/tree.html',
            {'to_show': to_show})
