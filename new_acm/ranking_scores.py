# coding: utf-8
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from django.template import Context, Engine
from django.utils.safestring import mark_safe
from oioioi.programs.models import Submission

class RankingScoreBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['ranking_scores']
    abstract = True

    def __init__(self, user, score):
        self.user = user
        self.score = score

    def render_score(self):
        return self.score

    def css_classes(self):
        return ''

def fancy_score(score):
    if isinstance(score, int):
        return score
    if score.is_integer(): return int(score)
    else: return score


class ACMScore(RankingScoreBase):
    score_template_active = Engine.get_default().from_string(
        """
            {% if frozen == 1 %}<span style="color:#4286f4">
            {% elif score == 0 %}<span style="color:#c11c1c">
            {% elif ifs %}<span style="color:#08630d; font-weight:900;">
            {% else %}<span style="color:#188917">
            {%endif%}
                {% if frozen == 1 %}
                    ?
                {% elif score == 0 %}
                    --
                {% else %}
                    {{acmtime}}
                {% endif %}
        <br/>
        <small>tries: {{ntries}}</small>
        </span>
        """
    )
    score_template_inactive = score_template_active #Engine.get_default().from_string('{{ score }} ({{ acmtime }} {{ntries}}</small>')

    def __init__(self, user, submission, score, acmtime, ranking, request):
        super(ACMScore, self).__init__(user, score)
        if ranking.is_frozen(submission.date) and request.timestamp < ranking.config.dict_config['unfreeze']:
             self.frozen = True
        else:
            self.frozen = False

        self.submission = submission
        self.ntries = Submission.objects.filter(problem_instance=submission.problem_instance, user=submission.user).exclude(status='CE').exclude(status='IGN').count()
        self.fsub = None
        subs = Submission.objects.filter(problem_instance=submission.problem_instance, status='OK', kind='NORMAL').order_by('date')
        if len(subs) > 0:
            self.fsub = subs[0]
        self.acmtime = acmtime
        self.ranking = ranking
        if self.frozen:
            self.acmtime = 0
            self.score = 0

    def render_score_from(self, template):
        return template.render(Context(dict(submission=self.submission, score=fancy_score(self.score), acmtime=self.acmtime, ntries=self.ntries, ranking=self.ranking, frozen=self.frozen, ifs=(self.fsub==self.submission))))

    def render_score(self):
        return self.render_score_from(self.score_template_inactive)

    def render_score_active(self):
        return self.render_score_from(self.score_template_active)

    def render_score_string(self):
        return '{} {} {}'.format(self.score, self.ntries, self.acmtime)

    def __repr__(self):
        return u'<ACMScore user={} score={} submission={} acmtime={}>'.format(self.user, self.score, self.submission.pk)

