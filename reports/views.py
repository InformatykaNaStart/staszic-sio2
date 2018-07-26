from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from oioioi.base.permissions import not_anonymous, make_condition, enforce_condition
from oioioi.base.menu import menu_registry
from oioioi.contests.utils import visible_contests, can_enter_contest, \
        can_see_personal_data, is_contest_admin, has_any_submittable_problem, \
        visible_rounds, visible_problem_instances, contest_exists, \
        is_contest_observer, get_submission_or_error, can_admin_contest
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, Http404, HttpResponse
from oioioi.programs.models import TestReport
from oioioi.problems.utils import can_admin_problem_instance
from django.utils.safestring import mark_safe
from ast import literal_eval
from models import ReportConfig

def report_modal_view(request, testreport_id=None):
    testreport = get_object_or_404(TestReport, id=testreport_id)
    submission = testreport.submission_report.submission
    pi = submission.problem_instance
    controller = pi.controller
    can_admin = can_admin_problem_instance(request, pi)
    isolate_meta = render(request, 'reports/isolate_meta.html', {'data': literal_eval(testreport.isolate_meta).items()}).content

    rconfig = ReportConfig.objects.get(contest=pi.contest)

    return render(request, 'reports/modal.html',
                {'test': testreport, 'can_admin': can_admin,
                'isolate_meta': mark_safe(isolate_meta),
                'config': rconfig})


