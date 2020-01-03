from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from oioioi.base.permissions import not_anonymous, make_condition, enforce_condition
from oioioi.base.menu import menu_registry, account_menu_registry
#from django.contrib.auth import AnonymousUser
from oioioi.contests.utils import can_enter_contest, contest_exists #, is_superuser
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, Http404, HttpResponse
from oioioi.base.menu import menu_registry
from models import *
from forms import *
from oioioi.filetracker.utils import stream_file
import zipfile
from StringIO import StringIO
import mimetypes
from django.utils.safestring import mark_safe

mpremoi = [] #['Kubin', 'u65848', 'szymekjakubicz', 'eratchia']


@account_menu_registry.register_decorator(_("Archive"),
        lambda request: reverse('archive-home'), order=0)

#@menu_registry.register_decorator(_("Archive"),
#        lambda request: reverse('archive-home'),
#        order=0, condition=not_anonymous)


def is_oldcontest_admin(request, who, contest):
    if request.user.is_superuser:
        return True
    permissions = [p.contest.short_name for p in StaszicOldContestAdminPermission.objects.filter(user=who)]
    if getattr(who, 'is_superuser', False):
        permissions = [c.short_name for c in StaszicOldContest.objects.filter()]
    if contest.short_name in permissions: return True
    else: return False


def is_oldcontest_participant(request, who, contest):
    if request.user.username in mpremoi: return True
    if is_oldcontest_admin(request, who, contest): return True
    if len(StaszicOldSubmission.objects.filter(author=who, problem_instance__contest=contest)) > 0: return True
    return False


def is_oldproblem_admin(request, who, problem):
    if request.user.is_superuser:
        return True
    for pi in StaszicOldProblemInstance.objects.filter(problem=problem):
        if pi.contest and is_oldcontest_admin(request, who, pi.contest): return True
    return False
    
    
def can_see_oldproblem(request, who, problem):
    if is_oldproblem_admin(request, who, problem):
        return True
    for pi in StaszicOldProblemInstance.objects.filter(problem=problem):
        if pi.contest and is_oldcontest_participant(request, who, pi.contest): return True
    return False


def getperms(request, who):
    r = []
    for c in StaszicOldContest.objects.filter():
        if is_oldcontest_admin(request, who, c):
            r.append(c.short_name)
    return r
    
    
def home_view(request):
            
    form = OldLoginForm()
    modal = False
    
    if request.method == 'POST':
        form = OldLoginForm(request.POST)
        if form.is_valid():
            u = StaszicOldUser.objects.filter(username=form.cleaned_data['username']);
            if len(u) == 0:
                form.add_error(None, 'No such user.')
                modal = True
            else:
                if not check_password(form.cleaned_data['password'], u[0].password):
                    form.add_error(None, 'Authentication error.')
                    modal = True
                else:
                    for ux in StaszicOldUser.objects.filter(parent=request.user):
                        ux.parent = None
                        ux.save()
                    u[0].parent = request.user
                    u[0].save()
    
    who = StaszicOldUser.objects.filter(parent=request.user)
    if len(who) == 0:
        who = None
    else:
        who = who[0]
        
    contests = []
        
    all_contests = StaszicOldContest.objects.filter(sio2dead=False)
    
    for c in all_contests:
        if is_oldcontest_participant(request, who, c):
            contests.append(c)

    old_contests = StaszicOldContest.objects.filter(sio2dead=True)
    permissions = getperms(request, who)

    return render(request, 'archive/contests.html', {
        'contests': contests,
        'who': who,
        'form': form,
        'modal': modal,
        'sio2dead_contests': old_contests,
        'perms': permissions,
        })


def submissions_view(request, contest_id=None):
    if contest_id is None:
        return home_view(request)
        
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    contest = get_object_or_404(StaszicOldContest, short_name=contest_id)
    submissions = StaszicOldSubmission.objects.filter(author=who,problem_instance__contest=contest).order_by('-date')
    return render(request, 'archive/submissions.html', {
        'submissions': submissions,
        'old_contest': contest
        })


def all_submissions_view(request, contest_id=None):
    if contest_id is None:
        return home_view(request)
        
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    contest = get_object_or_404(StaszicOldContest, short_name=contest_id)    
    
    if not is_oldcontest_admin(request, who, contest):
        return HttpResponseForbidden()
        
    submissions = StaszicOldSubmission.objects.filter(problem_instance__contest=contest,author__isnull=False).order_by('-date')
    return render(request, 'archive/submissions.html', {
        'submissions': submissions,
        'old_contest': contest,
        'all_submissions': True
        })

def download_source_code_view(request, submission_id):
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    submission = get_object_or_404(StaszicOldSubmission, submission_id=submission_id)
    if is_oldcontest_admin(request, who, submission.problem_instance.contest) or who == submission.author:
        if hasattr(submission.source, "file"):
            return stream_file(submission.source, submission.source.name)
        else:
            raise Http404()
    else:
        return HttpResponseForbidden()

def problems_view(request, contest_id=None):
    if contest_id is None:
        return home_view(request)
        
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    contest = get_object_or_404(StaszicOldContest, short_name=contest_id)
    if not is_oldcontest_participant(request, who, contest):
        return HttpResponseForbidden()    
    problems = StaszicOldProblemInstance.objects.filter(contest=contest).order_by('round')
    
    return render(request, 'archive/problems.html', {
        'problems': problems,
        'old_contest': contest,
        'is_admin': is_oldcontest_admin(request, who, contest)
        })


def problems_sio2dead_view(request, contest_id=None):
    if contest_id is None:
        return home_view(request)
        
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    contest = get_object_or_404(StaszicOldContest, short_name=contest_id)
    problems = StaszicOldProblemInstance.objects.filter(contest=contest)
    
    return render(request, 'archive/problems.html', {
        'problems': problems,
        'old_contest': contest,
        'is_admin': True
        })


def problem_package_name(problem):
    name = problem.package.name
    name = name[name.find('.'):]
    name = problem.short_name + name
    return name


def download_package_view(request, pid):
    p = get_object_or_404(StaszicOldProblem, problem_id=pid)
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    
    if not is_oldproblem_admin(request, who, p):
        return HttpResponseForbidden()
        
    return stream_file(p.package, problem_package_name(p))
    

def problem_statement_name(problem):
    name = problem.statement.name
    name = name[name.find('.'):]
    name = problem.short_name + 'zad' + name
    return name
    
    
def zip_view(request, contest, pid, path):
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    p = get_object_or_404(StaszicOldProblem, problem_id=pid)
    if not can_see_oldproblem(request, who, p):
        return HttpResponseForbidden()

    fp = StringIO(p.statement.read())
    zip = zipfile.ZipFile(fp)
    try:
        info = zip.getinfo(path)
    except KeyError:
        raise Http404(path)

    content_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    response = HttpResponse(zip.read(path), content_type=content_type)
    response['Content-Length'] = info.file_size
    return response   


def statement_view(request, contest, pid):
    who = get_object_or_404(StaszicOldUser, parent=request.user)
    p = get_object_or_404(StaszicOldProblem, problem_id=pid)   
    if not can_see_oldproblem(request, who, p):
        return HttpResponseForbidden()
            
    c = get_object_or_404(StaszicOldContest, short_name=contest)
    
    if p.statement.name.endswith('.zip'):          
        resp = zip_view(request, contest, pid, 'index.html')
        return render(request, 'archive/html_statement.html', {
            'content': mark_safe(resp.content),
            'old_contest': c,
            'problem': p
            })
    else:
        return stream_file(p.statement, problem_statement_name(p))
    
