from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.utils.http import urlencode
from oioioi.contests.utils import is_contest_admin, contest_exists, visible_contests, can_enter_contest
from oioioi.base.main_page import register_main_page_view
from oioioi.contests.models import Submission, ProblemInstance
from oioioi.contests.controllers import submission_template_context
from oioioi.base.permissions import enforce_condition, is_superuser, not_anonymous
from django.db.models import Q
import cStringIO
import tarfile
import mimetypes
from django.utils.safestring import mark_safe
from models import *
from oioioi.filetracker.utils import stream_file
import zipfile
from StringIO import StringIO

@enforce_condition(contest_exists & can_enter_contest)
def example_tests_view(request, pi_short):

    controller = request.contest.controller
    pi = get_object_or_404(ProblemInstance, round__contest=request.contest, short_name = pi_short)

    if not controller.can_see_problem(request, pi):
        raise PermissionDenied

    fileobj = cStringIO.StringIO()
    tar = tarfile.open('examples.tar', mode='w', fileobj=fileobj)

    def makeinfo(name, ext, size):
        info = tarfile.TarInfo('%s.%s' % (name, ext))
        info.size = size
        info.uid = 1337
        info.gid = 2102
        return info

    for test in pi.test_set.filter(kind='EXAMPLE', is_active=True).order_by('order'):
        tar.addfile(makeinfo(test.name, 'in', test.input_file.size), fileobj=test.input_file)
        tar.addfile(makeinfo(test.name, 'out', test.output_file.size), fileobj=test.output_file)

    tar.close()

    fileobj.seek(0)

    response = FileResponse(fileobj, content_type='application/x-tar')

    response['Content-Disposition'] = 'attachment; filename=%s.tar' % (pi.short_name, )

    return response

