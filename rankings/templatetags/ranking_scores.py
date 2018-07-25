from django import template

register = template.Library()

@register.filter
def render_score(score):
    if score is None:
        return '-'
    else:
        return score.render_score()

@register.filter
def score_classes(score):
    if score is None:
        return ' score-null'
    else:
        return score.css_classes()

@register.filter
def call_summary(pair, arg):
    _, function = pair
    return function(arg)
