from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.files import File
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from oioioi.contests.utils import contest_exists, can_enter_contest, \
    is_contest_admin, get_submission_or_error
from oioioi.base.permissions import enforce_condition
from oioioi.problems.utils import can_admin_instance_of_problem
from oioioi.contests.models import submission_statuses
from oioioi.programs.models import ProgramSubmission

import forms

@enforce_condition(~contest_exists | can_enter_contest)
def edit_view(request, submission_id):
    submission = get_submission_or_error(request, submission_id, submission_class=ProgramSubmission)
    if not can_admin_instance_of_problem(request, submission.problem):
        raise PermissionDenied
    else:
        form = forms.EditResultsForm()
        if request.method == 'POST':
            form = forms.EditResultsForm(request.POST)
            if form.is_valid():
                if submission.score is not None:
                    submission.score.value = form.cleaned_data['score']
                submission.status, submission.comment  = form.cleaned_data['status'], form.cleaned_data['comment'].strip(), 
                submission.save()
                return redirect('submission', contest_id=request.contest.id, submission_id=submission.id)
            raise PermissionDenied
        statuses = submission_statuses.entries
        return render(request, 'results_editor/edit.html', {'form': form, 'statuses': statuses, 'submission': submission})
