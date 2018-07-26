from django.shortcuts import render, get_object_or_404
from oioioi.programs.models import TestReport
def re_view(request, testreport_id=None):
    raise RuntimeError
    t = get_object_or_404(TestReport, id=testreport_id)
    return render(request, 'python/re.html', {
        'data': t.stderr,
    })
