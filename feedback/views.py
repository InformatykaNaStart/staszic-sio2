from django.shortcuts import render, get_object_or_404
from models import Judging
from utils import get_stats_from_judging

def judging(request, jid):
    judging = get_object_or_404(Judging, pk=jid)
    controller = judging.submission.problem_instance.controller
    return render(request, 'feedback/judging_base.html', dict(
        judging=judging,
        can_see_stats=controller.can_see_stats(request, judging),
        can_see_progress=controller.can_see_progress(request, judging),
        stats=get_stats_from_judging(judging.config.get('results')),
        ))


