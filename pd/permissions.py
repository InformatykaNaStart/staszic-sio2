import models
from oioioi.base.permissions import make_request_condition

@make_request_condition
def has_personal_data_pass(request):
    return models.PersonalDataPass.objects.filter(user=request.user).exists()