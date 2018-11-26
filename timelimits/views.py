from django.shortcuts import render, redirect
from forms import SetTLSForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from collections import defaultdict
from django.shortcuts import get_object_or_404
from oioioi.contests.models import Submission
# Create your views here.

def show_form(request, sid):
    form = SetTLSForm()
    return render(request, 'timelimits/form.html', dict(
        submission_id = sid,
        form = form
    ))

def get_key(test, equal_groups):
    if equal_groups: return test.group
    else: return test.name

def roundf(f, r):
    f = int(f)
    r = int(r)

    return (f + r - 1) // r * r

def set_timelimits(request, sid):
    assert request.method == 'POST'
    submission = get_object_or_404(Submission, pk=sid)

    form = SetTLSForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Form was not valid')
    else:
        multiplier = form.cleaned_data['multiplier']
        rounding = form.cleaned_data['rounding']
        equal_groups = form.cleaned_data['equal_groups']

        new_limits = defaultdict(lambda: 1000 * rounding)

        for report in submission.submissionreport_set.filter(status='ACTIVE'):
            for test in report.testreport_set.all():
                if test.test is None: continue
                key = get_key(test.test, equal_groups)
                new_limits[key] = max(new_limits[key], roundf(test.time_used * multiplier, rounding * 1000))

        for t in submission.problem_instance.test_set.all():
            t.time_limit = new_limits[get_key(t, equal_groups)]
            t.save()

        messages.success(request, 'Set time limits')

    return redirect(reverse('submission', args=[sid]))
