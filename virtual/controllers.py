
# coding: utf-8
from oioioi.programs.controllers import ProgrammingContestController
from oioioi.contests.utils import RoundTimes
from models import VirtualContestEntry
from utils import get_current_virtual_contest
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from oioioi.base.permissions import enforce_condition, not_anonymous
import datetime

class HiddenRoundTimes(RoundTimes):
    def is_past(self, dt):
        return False
    
    def is_future(self, dt):
        return True

    def is_hidden(self):
        return True

class VirtualContestsController(ProgrammingContestController):
    description = 'Virtual contests container'
    visible = True

    def get_round_times(self, request, round):
        if request is None:
            return HiddenRoundTimes(None, None, round.contest, None, None, 0)
        else:
            try:
                vce = VirtualContestEntry.objects.filter(
                        user=request.user,
                        contest__round=round).first()
            except:
                return HiddenRoundTimes(None, None, round.contest, None, None, 0)
            if vce is None:
                return HiddenRoundTimes(None, None, round.contest, None, None, 0)

            else:
                current_vce = get_current_virtual_contest(request)
                if current_vce is not None:
                    if current_vce.contest.round == round:
                        return RoundTimes(vce.start_date, vce.end_date, round.contest, vce.end_date, vce.end_date, 0)
                    else:
                        return HiddenRoundTimes(None, None, round.contest, None, None, 0)
                else:
                        return RoundTimes(vce.start_date, None, round.contest, vce.end_date, vce.end_date, 0)

    def get_virtual_problem_info(self, pi):
        return dict(
            problem=pi,
            max_score=self.get_max_score(pi),
        )

    def can_start_contest(self, request, vcontest):
        started_already = VirtualContestEntry.objects.filter(user=request.user, contest=vcontest).exists()
        return get_current_virtual_contest(request) is None and not started_already

    def can_finish_contest(self, request, vcontest):
        vce = vcontest.virtualcontestentry_set.filter(user = request.user).first()

        if vce is None: return False
        return vce.end_date > request.timestamp

    def start_contest_action(self, request, vcontest):
        return mark_safe('<a class="btn btn-success" href="{}">Zacznij</a>'.format(
                reverse('virtual-start', args=[vcontest.id])
            ))
    
    def info_contest_action(self, request, vcontest):
        return mark_safe('<a class="btn btn-info" href="{}">Info</a>'.format(
                reverse('virtual-info', args=[vcontest.id])
            ))

    def finish_contest_action(self, request, vcontest):
        return mark_safe('<a class="btn btn-danger" href="{}">Zakończ</a>'.format(
                reverse('virtual-finish', args=[vcontest.id])
            ))

    def get_virtual_contest_actions(self, request, vcontest):
        result = []

        result.append((5, self.info_contest_action(request, vcontest)))

        if self.can_start_contest(request, vcontest):
            result.append((10, self.start_contest_action(request, vcontest)))

        if self.can_finish_contest(request, vcontest):
            result.append((15, self.finish_contest_action(request, vcontest)))

        return result
