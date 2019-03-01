from oioioi.oi.controllers import OIContestController
from oioioi.participants.controllers import ParticipantsController, OpenParticipantsController
from staszic.languages.models import LanguageConfig
from staszic.acl import utils as acl
from oioioi.evalmgr.tasks import find_recipe_entry
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from staszic.feedback.utils import get_stats_from_judging
from staszic.feedback.models import SmartJudgeConfig
from oioioi.contests.utils import can_admin_contest

class ParticipantsControllerWithACL(ParticipantsController):
    def can_enter_contest(self, request):
        default = super(ParticipantsControllerWithACL, self).can_enter_contest(request)
        return acl.query_acl(request, self.contest, 'access', default)

    @classmethod
    def filter_user_contests(cls, request, queryset):
        pks = []

        filtered = super(ParticipantsControllerWithACL, cls).filter_user_contests(request, queryset)

        for contest in filtered:
            if acl.query_acl(request, contest, 'access', True):
                pks.append(contest.pk)

        return queryset.filter(pk__in = pks)

class StaszicContestController(OIContestController):
    description = 'Staszic closed'
    visible = True

    def get_available_languages_dict(self, problem_instance):
        assert problem_instance is None
        config = getattr(self.contest, 'languageconfig', LanguageConfig())

        result = {}
        for lang in config.languages:
            result[lang.description] = lang.extensions

        return result

    def get_allowed_languages(self):
        return list(self.get_available_languages_dict(None).keys())

    def registration_controller(self):
        return ParticipantsControllerWithACL(self.contest)

    def can_see_problem(self, request, problem_instance):
        default = super(StaszicContestController, self).can_see_problem(request, problem_instance)
        return acl.query_acl(request, problem_instance, 'show', default)
    
    def can_submit(self, request, problem_instance, check_round_times=True):
        default = super(StaszicContestController, self).can_submit(request, problem_instance, check_round_times)
        default = default and self.can_see_problem(request, problem_instance)
        return acl.query_acl(request, problem_instance, 'submit', default)

    def fill_evaluation_environ_post_problem(self, environ, submission):
        try:
            environ['recipe'].insert(0, ('create_judgings', 'staszic.feedback.utils.create_judgings'))
            idx = find_recipe_entry(environ['recipe'], 'collect_tests')
            environ['recipe'].insert(idx+1, ('polish_tests', 'staszic.feedback.utils.put_judgings_into_tests'))
            environ['recipe'].append(('invalidate_judgings', 'staszic.feedback.utils.invalidate_judgings'))
        except:
            pass

    def judge_prepare(self, judging, test, config):
        if test.kind == 'EXAMPLE': return False
        if judging.submission.user is None: return False
        if config['mode'] == 'off': return False
        if 'failed' not in config:
            config['failed'] = []
        return test.group in config['failed']

    def judge_finished(self, judging, test, code, config):
        if code != 'OK':
            if 'failed' not in config:
                config['failed'] = []
            config['failed'].append(test.group)

    def render_submission(self, request, submission):
        now = super(StaszicContestController, self).render_submission(request, submission)
        new = mark_safe(self.render_judgings(request, submission))
        js = render_to_string('feedback/judging_js.html')
        return now + new + js

    def render_judgings(self, request, submission):
        jds = submission.judging_set.filter(active=True).order_by('-pk')
        return mark_safe('').join(self.render_judging(request, judging) for judging in jds)

    def render_judging(self, request, judging):
        return render_to_string('feedback/judging.html', dict(
            judging=judging,
            stats=get_stats_from_judging(judging.config.get('results')),
            can_see_stats=self.can_see_stats(request, judging),
            can_see_progress=self.can_see_progress(request, judging)))

    def can_see_stats(self, request, judging):
        if request.user.is_superuser: return True
        if can_admin_contest(request.user, judging.submission.problem_instance.contest): return True
        if request.user != judging.submission.user: return False
        contest = judging.submission.problem_instance.contest
        if contest is None: return False
        try:
            if judging.kind not in self.get_visible_reports_kinds(request, judging.submission): return False
            return getattr(contest, 'judgingconfig', SmartJudgeConfig()).mode in ['all']
        except:
            return False
    
    def can_see_progress(self, request, judging):
        try:
            if request.user.is_superuser: return True
            if can_admin_contest(request.user, judging.submission.problem_instance.contest): return True
            if request.user != judging.submission.user: return False
            contest = judging.submission.problem_instance.contest
            if contest is None: return False
            if judging.kind not in self.get_visible_reports_kinds(request, judging.submission): return False
            return getattr(contest, 'judgingconfig', SmartJudgeConfig()).mode in ['all', 'pro']
        except:
            return False

class StaszicOpenController(StaszicContestController):
    description = 'Staszic otwarty'
    def registration_controller(self):
        return OpenParticipantsController(self.contest)
