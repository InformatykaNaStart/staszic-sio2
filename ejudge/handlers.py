from oioioi.programs.models import ProgramSubmission, CompilationReport, GroupReport, TestReport
from oioioi.contests.models import SubmissionReport, FailureReport, ScoreReport
from oioioi.contests.scores import IntegerScore
from collections import defaultdict
import random

from api import api_pb2 as pb

def GetSubmission(request):
    submissions = ProgramSubmission.objects.filter(
        problem_instance__contest__pk=request.contest,
        problem_instance__short_name__in=request.problems,
        status='?').order_by('pk')

    if not submissions.exists():
        return pb.GetSubmissionResponse()

    users = {}

    for sub in submissions:
        if sub.user.pk not in users:
            users[sub.user.pk] = sub

    submission = random.choice(users.values())
    
    if submission is not None:
        source_file = submission.source_file
        source_file.open()
        source_code = source_file.read()
        source_file.close()

        return pb.GetSubmissionResponse(
            id=submission.pk,
            problem=submission.problem_instance.short_name,
            language=submission.extension,
            source_code=source_code
            )
    else:
        return pb.GetSubmissionResponse()

def HandleFailure(report, text):
    report.kind = 'FAILURE'
    report.save()

    failure = FailureReport.objects.create(
        submission_report=report,
        message=text,
        json_environ='{"recipe":[]}')


def HandleCompilation(report, status, compilation_output):
    creport = CompilationReport.objects.create(
        submission_report=report,
        status=status,
        compiler_output = compilation_output)

def HandleTests(report, request):
    group_map = defaultdict(lambda: [])
    for rtest in request.tests:
        group_map[rtest.group_name].append(rtest)

    for rgroup in request.groups:
        greport = GroupReport.objects.create(
            submission_report = report,
            group = rgroup.name,
            score = IntegerScore(rgroup.score),
            max_score = IntegerScore(rgroup.max_score),
            status = pb.Status.Name(rgroup.status))

        for rtest in group_map[rgroup.name]:
            TestReport.objects.create(
                submission_report = report,
                status = pb.Status.Name(rtest.status),
                comment = rtest.comment,
                score = IntegerScore(rtest.score),
                time_used = rtest.time_used,
                test_name = rtest.name,
                test_group = rtest.group_name,
                test_time_limit = rtest.time_limit,
                test_max_score = rtest.max_score)

def PostResults(request):
    submission = ProgramSubmission.objects.get(pk=request.submission_id)
    submission.submissionreport_set.filter(status='ACTIVE').update(status='SUPERSEDED')

    report = SubmissionReport.objects.create(submission=submission, status='ACTIVE', kind='FULL')

    if request.failure_text:
        HandleFailure(report, request.failure_text)
        submission.score = None
        submission.max_score = None
        submission.status = 'SE'
        submission.comment = ''
    else:
        score_report = ScoreReport.objects.create(submission_report=report)
        if request.status == pb.Status.CE:
            HandleCompilation(report, 'CE', request.compiler_output)
        else:
            HandleCompilation(report, 'OK', request.compiler_output)

        if request.has_score:
            score_report.score = IntegerScore(request.score)
        if request.has_max_score:
            score_report.max_score = IntegerScore(request.max_score)

        HandleTests(report, request)

        score_report.status = pb.Status.Name(request.status)
        score_report.comment = request.comment
        score_report.save()

        submission.comment = score_report.comment
        submission.score = score_report.score
        submission.max_score = score_report.max_score
        submission.status = score_report.status

    submission.save()

    if submission.user:
        submission.problem_instance.controller.update_user_results(submission.user, submission.problem_instance)
    return pb.PostResultsResponse()
