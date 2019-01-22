from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from oioioi.contests.models import ProblemInstance, Submission
def submission_limit(pi):
    return pi.submissions_limit

def submissions(request, pi):
    try:
        return Submission.objects.filter(kind='NORMAL', user=request.user, problem_instance=pi).count()
    except:
        return 0

def limits_view(request, pid):
    pi = get_object_or_404(ProblemInstance, id=pid)
    users = submissions(request, pi)
    total = submission_limit(pi)
    if users <= total*0.5: 
        mode='success'
    elif users <= total*0.75:
        mode='warning'
    else:
        mode='danger'
    pattern = '<span class="label label-%s">%d / %d</span>'
    return HttpResponse(pattern%(mode, submissions(request, pi), submission_limit(pi)))
