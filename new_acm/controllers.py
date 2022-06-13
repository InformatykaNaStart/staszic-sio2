from django.contrib.auth.models import User, AnonymousUser
from staszic.new_base.controllers import StaszicContestController
from oioioi.acm.score import format_time, BinaryScore, ACMScore
from oioioi.contests.utils import rounds_times
from oioioi.contests.models import SubmissionReport, Submission, \
        ProblemInstance, UserResultForProblem

IGNORED_STATUSES = ['CE', 'SE', '?']
class StaszicACM(StaszicContestController):
    description = "Staszic ACM"
    visible = True

    #def judge_prepare(self, judging, test, config):
    #    #if judging.submission.user is None: return False
    #    if config['mode'] == 'off': return False
    #    if 'first_failed' not in config:
    #        config['first_failed'] = 999
    #    return test.order > config['first_failed']

    #def judge_finished(self, judging, test, code, config):
    #    if code != 'OK':
    #        if 'first_failed' not in config:
    #            config['first_failed'] = test.order
    #        config['first_failed'] = min(config['first_failed'], test.order)

    def can_print_files(self, request):
        return True


    def fill_evaluation_environ(self, environ, submission):
        environ['group_scorer'] = 'oioioi.acm.utils.acm_group_scorer'
        environ['test_scorer'] = 'oioioi.acm.utils.acm_test_scorer'
        environ['score_aggregator'] = 'oioioi.acm.utils.acm_score_aggregator'
        pi = submission.problem_instance
        if pi.contest.pk == 'wwi-2021-acm' and pi.short_name == 'd':
            if Submission.objects.filter(problem_instance=pi, user=submission.user, date__lt=submission.date).count() < 5:
                environ['score_aggregator'] = 'staszic.new_acm.utils.fail_acm_score_aggregator'
                

        environ['report_kinds'] = ['FULL']

        super(StaszicACM, self). \
                fill_evaluation_environ(environ, submission)

    def update_report_statuses(self, submission, queryset):
        self._activate_newest_report(submission, queryset,
            kind=['FULL', 'FAILURE'])

    def update_submission_score(self, submission):
        try:
            report = SubmissionReport.objects.get(submission=submission,
                    status='ACTIVE', kind='FULL')
            score_report = report.score_report
            if score_report.status in IGNORED_STATUSES:
                submission.score = None
            else:
                submission.score = BinaryScore(score_report.status == 'OK')
            submission.status = score_report.status
        except SubmissionReport.DoesNotExist:
            submission.score = None
            if SubmissionReport.objects.filter(submission=submission,
                    status='ACTIVE', kind='FAILURE'):
                submission.status = 'SE'
            else:
                submission.status = '?'
        submission.save()

    def get_submission_relative_time(self, submission):
        # FIXME: SIO-1387 RoundTimes shouldn't require request
        # Workaround by mock Request object
        class DummyRequest(object):
            def __init__(self, contest, user):
                self.contest = contest
                self.user = user or AnonymousUser()

        rtimes = rounds_times(DummyRequest(self.contest, submission.user or
                                           AnonymousUser()))
        round_start = rtimes[submission.problem_instance.round].get_start()
        submission_time = submission.date - round_start
        # Python2.6 does not support submission_time.total_seconds()
        seconds = submission_time.days * 24 * 3600 + submission_time.seconds
        return max(0, seconds)

    def _fill_user_result_for_problem(self, result, pi_submissions):
        if pi_submissions:
            for penalties_count, submission in enumerate(pi_submissions, 1):
                if submission.status == 'IGN':
                    # We have found IGNORED submission before accepted one.
                    # This means, that some other
                    # submission is no longer accepted
                    self.update_submission_score(submission)
                if submission.status == 'OK':
                    # ``submission`` and ``penalties_count`` variables preserve
                    #  their last value after the loop
                    break

            solved = int(submission.status == 'OK')
            score = ACMScore(
                problems_solved=solved,
                penalties_count=(penalties_count - solved),
                time_passed=self.get_submission_relative_time(submission)
            )
            result.score = score
            result.status = submission.status
            return submission

        else:
            result.score = None
            result.status = None
            return None

    def update_user_result_for_problem(self, result):
        submissions = Submission.objects \
                .filter(problem_instance=result.problem_instance,
                    user=result.user, kind='NORMAL') \
                .exclude(status__in=IGNORED_STATUSES) \
                .order_by('date')

        last_submission = self._fill_user_result_for_problem(
                result, submissions)
        if last_submission:
            result.submission_report = last_submission \
                    .submissionreport_set.get(status='ACTIVE', kind='FULL')

            if last_submission.status == 'OK':
                # FIXME: May not ignore submissions with admin-hacked same-date
                submissions.filter(date__gt=last_submission.date) \
                        .update(status='IGN', score=None)
        else:
            result.submission_report = None

    def results_visible(self, request, submission):
        return False

    def get_visible_reports_kinds(self, request, submission):
        if submission.status == 'CE':
            return ['FULL']
        else:
            return []

    def can_see_submission_score(self, request, submission):
        return True

    def can_see_submission_status(self, request, submission):
        return True

    def render_submission_date(self, submission):
        return format_time(self.get_submission_relative_time(submission))

#    def ranking_controller(self):
#        return ACMRankingController(self.contest)

    def can_see_round(self, request_or_context, round):
        context = self.make_context(request_or_context)
        if context.is_admin:
            return True
        rtimes = self.get_round_times(request_or_context, round)
        return not rtimes.is_future(context.timestamp)
