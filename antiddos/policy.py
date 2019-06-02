from oioioi.evalmgr.models import QueuedJob
from django.conf import settings

def queued_submissions_of(user):
    return QueuedJob.objects.filter(state='WAITING',submission__user=user).count()

def get_queued_submissions_limit():
    return getattr(settings, 'MAX_QUEUED_SUBMISSIONS_PER_USER', 10**3)

def can_submit(user):
    if user.is_superuser: return True
    return queued_submissions_of(user) < get_queued_submissions_limit()
