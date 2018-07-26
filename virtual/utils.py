from models import VirtualContestEntry
from oioioi.base.permissions import make_request_condition

def get_current_virtual_contest(request):
    vce = VirtualContestEntry.objects.filter(
        user=request.user,
        start_date__lte=request.timestamp,
        end_date__gt=request.timestamp).first()

    return vce

@make_request_condition
def contest_has_vcontests(request):
    from controllers import VirtualContestsController
    return request.contest is not None and isinstance(request.contest.controller, VirtualContestsController)
