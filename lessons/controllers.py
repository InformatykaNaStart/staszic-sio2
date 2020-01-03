from staszic.new_base.controllers import StaszicContestController
from oioioi.contests.models import SubmissionReport, submission_statuses, UserResultForProblem, Submission
from staszic.lessons.models import ExamConfig

class StaszicLessonsContestController(StaszicContestController):
    description = 'Staszic algo classes'
    visible = False

    def fill_evaluation_environ(self, environ, *args, **kwargs):
        environ['report_kinds'] = ['FULL']
        super(StaszicLessonsContestController, self).fill_evaluation_environ(environ, *args, **kwargs)

        environ['test_scorer'] = 'oioioi.programs.utils.discrete_test_scorer'
        environ['group_scorer'] = 'staszic.lessons.utils.binary_group_scorer'
        environ['score_aggregator'] = 'staszic.lessons.utils.binary_score_aggregator'

    def update_report_statuses(self, submission, qs):
        self._activate_newest_report(submission, qs, kind=['FULL', 'FAILURE'])

    def update_submission_score(self, submission):
        try:
            report = SubmissionReport.objects.get(submission=submission,
                    status='ACTIVE', kind='FULL')
            score_report = report.score_report
            submission.score = score_report.score
            submission.status = score_report.status
        except SubmissionReport.DoesNotExist:
            submission.score = None
            if SubmissionReport.objects.filter(submission=submission,
                    status='ACTIVE', kind='FAILURE'):
                submission.status = 'SE'
            else:
                submission.status = '?'
        submission.save()

    def get_visible_reports_kinds(self, request, submission):
        return ['FULL']

    def judge_prepare(self, judging, test, config):
        # returns true, if allowed to skip a test
        if test.kind == 'EXAMPLE': return False
        if judging.submission.user is None: return False
        if config['mode'] == 'off': return False
        if 'failed' not in config:
            return False
        return test.order > config['failed']

    def judge_finished(self, judging, test, code, config):
        if code != 'OK':
            if 'failed' not in config:
                config['failed'] = test.order
            config['failed'] = min(config['failed'], test.order)


    def get_status_class(self, request, submission):
        status = submission.status

        if '@' in status:
            status, _ = status.split('@')

        return status

    def get_status_display(self, request, submission):
        status = submission.status
        if '@' not in status:
            return submission.get_status_display()

        status, test = status.split('@')

        return u"{} @ test {}".format(submission_statuses.get(status, status), test)

    def filter_test_reports(self, request, report, tests):
        if request.user.is_superuser: return tests
        if report.submission.status == 'OK': return tests

        return tests.exclude(status='OK')[:1]
    
    def update_user_result_for_problem(self, result):
        result.score = None
        result.status = None
        result.submission_report = None

        submissions = Submission.objects.filter(problem_instance=result.problem_instance, user=result.user, score__isnull=False, kind='NORMAL').order_by('date')

        for sub in submissions:
            report = sub.submissionreport_set.filter(status='ACTIVE', kind='FULL').first()
            if result.score is None or sub.score > result.score:
                result.score = sub.score
                result.status = sub.status
                result.submission_report = report

class StaszicExamsContestController(StaszicLessonsContestController):
    description = 'Staszic exams'
    visible = False

    def can_see_statement(self, request, problem_instance):
        return False

    def can_see_round(self, request_or_context, round):
        context = self.make_context(request_or_context)

        if context.is_admin: return True

        exam = ExamConfig.objects.filter(round=round).first()
        if exam is not None:
            user = request_or_context.user
            if exam.user_group is None or user not in exam.user_group.user_set.all():
                return False

        return super(StaszicExamsContestController, self).can_see_round(request_or_context, round)

    def can_submit(self, request, problem_instance, check_times=True):
        if self.make_context(request).is_admin:
            return True

        if super(StaszicExamsContestController, self).can_submit(request, problem_instance, check_times):
            exam = ExamConfig.objects.filter(round=problem_instance.round).first()
            if exam is not None and problem_instance in exam.notsubmittable_problems.all():
                return False

            return True
        
        return False

    def can_see_submission_score(self,request, submission):
        if self.make_context(request).is_admin:
            return True

        exam = ExamConfig.objects.filter(round=submission.problem_instance.round).first()
        if exam is not None:
            return exam.show_scores

        return False

