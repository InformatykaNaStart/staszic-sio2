import models
from oioioi.base.permissions import make_request_condition
from oioioi.contests.models import ContestPermission

@make_request_condition
def has_personal_data_pass(request):
    return models.PersonalDataPass.objects.filter(user=request.user).exists()

@make_request_condition
def has_contest_personal_data_access(request):
    return models.PersonalDataPass.objects.filter(user=request.user).exists() or \
        ContestPermission.objects.filter(user=request.user, contest=request.contest).exists()
