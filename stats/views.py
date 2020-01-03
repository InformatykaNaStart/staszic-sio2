from django.shortcuts import render
from django.http import HttpResponse
from oioioi.base.permissions import is_superuser, enforce_condition
from oioioi.contests.models import Submission
import os.path
import csv
from ast import literal_eval

@enforce_condition(is_superuser)
def timing_view(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="timing.csv"'

    def imeta(tr):
        try:
            return literal_eval(tr.isolate_meta)
        except Exception:
            return {}

    fields = [
        ('submission', lambda t: t.submission_report.submission.id),
        ('problem', lambda t: t.submission_report.submission.problem_instance.short_name),
        ('contest', lambda t: t.submission_report.submission.problem_instance.contest.id),
        ('date', lambda t: t.submission_report.submission.date),
        ('test', lambda t: t.test_name),
        ('worker', lambda t: imeta(t).get('hostname')),
        ('wall', lambda t: imeta(t).get('time-wall')),
        ('instr', lambda t: imeta(t).get('instructions')),
        ('time', lambda t: imeta(t).get('time')),
        ('max-rss', lambda t: imeta(t).get('max-rss')),
    ]

    writer = csv.writer(response)
    writer.writerow([name for name, f in fields])

    submissions = Submission.objects.filter(problem_instance__contest__id__contains='wwi-2019').order_by('-date')

    counter = 0
    for sub in submissions:
        for r in sub.submissionreport_set.filter():
            for tr in r.testreport_set.filter():
                writer.writerow([f(tr) for name, f in fields])
        counter += 1
        if counter%100 == 0:
            print counter, '/', submissions.count()
    return response

@enforce_condition(is_superuser)
def submissions_view(request):
    response = HttpResponse(content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="submissions.csv"'

    fields = [
        ('id', lambda s: s.id),
        ('problem', lambda s: s.problem_instance.problem.short_name),
        ('author', lambda s: getattr(s.user, 'username', None)),
        ('date', lambda s: s.date),
        ('score', lambda s: getattr(s.score, 'value', None)),
        ('kind', lambda s: s.kind),
        
    ]

    writer = csv.writer(response)
    writer.writerow([name for name, f in fields])

    submissions = Submission.objects.filter(problem_instance__contest=request.contest).order_by('-date')

    for sub in submissions:
        writer.writerow([f(sub) for name, f in fields])

    return response

