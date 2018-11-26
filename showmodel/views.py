import difflib
import zipfile
import os
import shutil
import tempfile
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.files import File
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
# pylint: disable=no-name-in-module
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

from oioioi.programs.models import ProgramSubmission, TestReport, Test, \
        OutputChecker, SubmissionReport, UserOutGenStatus, ModelSolution
from oioioi.programs.utils import decode_str, \
        get_submission_source_file_or_error
from oioioi.contests.utils import contest_exists, can_enter_contest, \
        is_contest_admin, get_submission_or_error
from oioioi.base.permissions import enforce_condition
from oioioi.base.utils import strip_num_or_hash
from oioioi.filetracker.utils import stream_file
from oioioi.problems.models import Problem

def get_model(problem):
    pid = problem.short_name
    a = ModelSolution.objects.filter(problem=problem, name__contains=pid+'.')
    if len(a) == 0:
        a = ModelSolution.objects.filter(problem=problem, name__contains=pid+'1.')
    return a[0].source_file

@enforce_condition(~contest_exists | can_enter_contest)
def showmodel_view(request, problem_id, submission_id):
    problem = Problem.objects.get(id=problem_id)
    submission = get_object_or_404(ProgramSubmission, id=submission_id)
    pi = submission.problem_instance
    if pi.contest and (not request.contest or request.contest.id != pi.contest.id):
        raise PermissionDenied
    if not pi.controller.can_see_source(request, submission):
        raise PermissionDenied
    if submission.score != 100 or not submission.problem_instance.show_model:
        raise PermissionDenied
    source_file = get_model(problem)
    raw_source, decode_error = decode_str(source_file.read())
    filename = source_file.file.name
    is_source_safe = False
    try:
        lexer = guess_lexer_for_filename(
            filename,
            raw_source
        )
        formatter = HtmlFormatter(linenos=True, line_number_chars=3,
                            cssclass='syntax-highlight')
        formatted_source = highlight(raw_source, lexer, formatter)
        formatted_source_css = HtmlFormatter() \
                .get_style_defs('.syntax-highlight')
        is_source_safe = True
    except ClassNotFound:
        formatted_source = raw_source
        formatted_source_css = ''
    return TemplateResponse(request, 'showmodel/source.html', {
        'source': formatted_source,
        'css': formatted_source_css,
        'is_source_safe': is_source_safe,
        'decode_error': decode_error,
        'problem': problem
    })

