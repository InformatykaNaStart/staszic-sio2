from django.shortcuts import render, get_object_or_404, redirect
from models import Link, LinkClickHistory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import models
from oioioi.participants.models import Participant
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

@login_required
def linkjoin_view(request, magic):

    history, created = LinkClickHistory.objects.get_or_create(user=request.user)
    if history.last_click and timezone.now() - history.last_click < timedelta(seconds=10):
        raise PermissionDenied(_('Please wait a few moments and try again.'))
    else:
        history.last_click = timezone.now()
        history.save()

    link = get_object_or_404(Link, magic=magic)
    if link.expiration_date < timezone.now():
        raise PermissionDenied(_('This link has expired.'))
    contest = link.contest
    if Participant.objects.filter(contest=contest, user=request.user):
        messages.info(request, _('You are already registered to this contest.'))
    else:
        Participant(contest=contest, user=request.user).save()
        messages.success(request, _('You were successfully registered to the contest.'))
    return redirect('contest_dashboard', contest_id=link.contest.id)
