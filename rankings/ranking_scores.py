# coding: utf-8
from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from django.template import Context, Engine
from django.utils.safestring import mark_safe

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


class SingleScore(RankingScoreBase):
    score_template_active = Engine.get_default().from_string('<a href="{% url "submission" submission.pk %}">{{ score }}</a>')
    score_template_inactive = Engine.get_default().from_string('{{ score }}')

    def __init__(self, user, submission, score):
        super(SingleScore, self).__init__(user, score)
        self.submission = submission

    def render_score_from(self, template):
        return template.render(Context(dict(submission=self.submission, score=fancy_score(self.score))))

    def render_score(self):
        return self.render_score_from(self.score_template_inactive)

    def render_score_active(self):
        return self.render_score_from(self.score_template_active)


    def __repr__(self):
        return u'<SingleScore user={} score={} submission={}>'.format(self.user, self.score, self.submission.pk)

class CombinedScoreMixin(object):
    def is_combined(self):
        return False
    
RankingScoreBase.mix_in(CombinedScoreMixin)

class CombinedScore(RankingScoreBase):
    @classmethod
    def make(cls, *scores):
        curr = None
        for name, score, coef in scores:
            if curr is None:
                curr = CombinedScore.single(name, score, coef)
            else:
                curr = curr.combine_with(name, score, coef)

        return curr

    @classmethod
    def single(cls, name, score, coef):
        return CombinedScore(score.user, score.score * coef, [(name, score, coef)])

    def __init__(self, user, score, subscores):
        super(CombinedScore, self).__init__(user, score)
        self.subscores = subscores

    def combine_with(self, name, other, coef):
        return CombinedScore(self.user, self.score + other.score * coef, self.subscores + [(name, other, coef)])

    def is_combined(self):
        return True
    
    def __repr__(self):
        return u'<CombinedScore user={} score={} scores=[{}]>'.format(self.user, self.score, u'; '.join(u'{}*{} [{}]'.format(coef, score, name) for name, score, coef in self.subscores))

    template = Engine.get_default().from_string('<div class="combined">{{ score }}<span class="combined-tooltip">{{ tooltip }}</span></div>')

    def render_score(self):
        tooltip=u'<br>'.join(u'{}: {}×{:3} = {:3}'.format(name,coef, score.score, coef * score.score)
            for name, score, coef in self.subscores
        )
        return self.template.render(Context(dict(score=self.score, tooltip=mark_safe(tooltip))))

    render_score_active = render_score
