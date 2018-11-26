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

    testreport.generate_status = pi.controller._out_generate_status(request, testreport)
    try:
        rconfig = ReportConfig.objects.get(contest=pi.contest)
    except:
        rconfig = None

    return render(request, 'reports/modal.html',
                {'test': testreport, 'can_admin': can_admin,
                'isolate_meta': mark_safe(isolate_meta),
                'config': rconfig})

def info_button_view(request, testreport_id=None):
    testreport = get_object_or_404(TestReport, id=testreport_id)
    submission = testreport.submission_report.submission
    pi = submission.problem_instance
    controller = pi.controller
    can_admin = can_admin_problem_instance(request, pi)

    try:
        rconfig = ReportConfig.objects.get(contest=pi.contest)
    except: 
        rconfig = None

    visible = can_admin or request.user.is_superuser or (rconfig.stderr_visible and testreport.stderr and len(testreport.stderr) > 0)

    if not visible:
        return HttpResponse("")
    else:
        return render(request, 'reports/info.html',
                    {'test': testreport})
