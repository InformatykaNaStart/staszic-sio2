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
from oioioi.sinolpack.package import _stringify_keys
import re

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


@enforce_condition(contest_exists & can_enter_contest & is_superuser)
def reload_limits_from_config_view(request, problem_instance_id):
    pi = get_object_or_404(ProblemInstance, id=problem_instance_id)
    config = pi.problem.extraconfig.parsed_config
    tests = [t for t in pi.test_set.filter()]
    log = []
    for t in tests:
        name = t.name
        tl_dict = _stringify_keys(config['time_limits'])
        original_tl = t.time_limit
        new_tl = tl_dict.get(name, tl_dict.get(re.search('^\d+', name).group(0), None))
        if new_tl is None:
            info = 'No time limit in config. Keeping old limit (%d)' % original_tl
        elif new_tl == original_tl:
            info = 'Time limits are equal (%d)' % original_tl
        else:
            t.time_limit = new_tl
            t.save()
            info = 'Time limit changed from %s to %s' % (str(original_tl), str(new_tl))
        log.append({'test': name, 'info': info})
    return render(request, 'utils/reload_limits.html', {'log': log,
        'back': reverse('oioioiadmin:contests_probleminstance_changelist')})