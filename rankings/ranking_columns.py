import math
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from staszic.rankings.ranking_scores import SingleScore, CombinedScore
from django.template import Engine, Context
from oioioi.contests.views import problem_statement_view
from django.core.urlresolvers import reverse
from oioioi.contests.utils import is_contest_admin

class RankingColumnBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['ranking_columns']
    abstract = True

    def __init__(self, ranking):
        self.ranking = ranking
        self.contest = ranking.contest

    def render_header(self):
        raise NotImplementedError

    def get_scores(self):
        raise NotImplementedError

    def can_access(self, request):
        return False

class ProblemInstanceColumn(RankingColumnBase):
    description = 'Problem instance'

    header_template = Engine.get_default().from_string('<span title="{{ full_name }}"><a href="{{ pi_link }}">{{ short_name }}</a></span>')

    def __init__(self, ranking, problem_instance, round_coef, round_type, contest_coef, contest_type, visibility_type, trial_visibility, start_date=None, end_date=None, order='max', ignore_submissions_after=None):
        super(ProblemInstanceColumn, self).__init__(ranking)
        self.problem_instance = problem_instance

        self.round_config = dict(type=round_type, coef=round_coef, start_date=start_date, end_date=end_date, order=order)
        self.contest_config = dict(type=contest_type, coef=contest_coef)
        self.visible_after = self.when_visible(problem_instance.round, visibility_type)
        self.ignore_submissions_after = ignore_submissions_after

    def when_visible(self, round, type):
        if type == 'always':
            return round.start_date
        if type == 'end':
            return round.end_date
        if type == 'results':
            return round.results_date
        if type == 'none':
            return None

    def can_access(self, request):
        if request.user.is_superuser or is_contest_admin(request): return True
        if self.visible_after is None: return False
        return request.timestamp >= self.visible_after

    def render_header(self):
        return self.header_template.render(Context(dict(
            short_name = self.problem_instance.short_name,
            full_name = self.problem_instance.problem.name,
            pi_link = reverse('problem_statement', kwargs={'problem_instance': self.problem_instance.short_name})
        )))

    def get_scores(self):
        submissions = self.problem_instance.submission_set.filter(kind='NORMAL')
        if self.ignore_submissions_after: submissions = submissions.filter(date__lte=self.ignore_submissions_after)
        submissions = submissions.exclude(score=None).order_by('-date').select_related()
        
        start_date = self.problem_instance.round.start_date
        end_date = self.problem_instance.round.end_date

        round_scores = self.get_round_scores(submissions, self.round_config['type'], self.round_config['order'], lambda x: (end_date and start_date <= x.date <= end_date) or (not end_date and start_date <= x.date))
        contest_scores = self.get_round_scores(submissions, self.contest_config['type'], self.round_config['order'], lambda x: start_date <= x.date)

        #start_date = self.round_config['start_date']
        #end_date = self.round_config['end_date']

        #round_scores = self.get_round_scores(submissions, self.round_config['type'], lambda x: ( ((not start_date) or start_date <= x.date) and ((not end_date) or x.date <= end_date)))
        #contest_scores = self.get_round_scores(submissions, self.contest_config['type'], lambda x: ( ((not start_date) or start_date <= x.date) and ((not end_date) or x.date <= end_date)))

        return self.combine_scores(
                ('contest', round_scores, self.round_config['coef']),
                ('alltime', contest_scores, self.contest_config['coef'])
            )

    def get_round_scores(self, qs, type, order, filter):
        result = dict()
        #raise RuntimeError([(x.date, filter(x)) for x in qs])
        for sub in qs:
            if filter(sub):
                self.put_score(result, type, order, self.score_for_sub(sub))
        
        return result

    def score_for_sub(self, sub):
        if sub.problem_instance.score_weight is None:
            return SingleScore(sub.user, sub, sub.score.value)
        else:
            return SingleScore(sub.user, sub, round(sub.score.value*sub.problem_instance.score_weight, 2))

    def put_score(self, container, type, order, score):
        if self.better_score(container.get(score.user, None), type, order, score):
            container[score.user] = score

    def better_score(self, orig, type, order, new):
        if orig is None: return True
        if type == 'last': return False
        if type == 'best': return self.in_order(order, new.score, orig.score)
        if type == 'rlast': return self.in_order(order, new.score, orig.score) and new.submission.is_revealed

        assert False

    def in_order(self, order, new, orig):
        if order == 'max':
            return new > orig
        else:
            return new < orig

    def combine_scores(self, *args):
        result = dict()

        args = filter(lambda x: x[2] != 0, args)
        
        if len(args) == 1:
            (_, scores, _), = args
            return scores

        for name, scores, coef in args:
            for user, score in scores.items():
               result[user] = self.combine(result.get(user, None), name, score, coef)

        return result

    def combine(self, orig, name, new, coef):
        if orig is None: return CombinedScore.single(name, new, coef)
        else: return orig.combine_with(name, new, coef)

    def __repr__(self):
        return u'<ProblemInstanceColumn pi={}>'.format(self.problem_instance)

