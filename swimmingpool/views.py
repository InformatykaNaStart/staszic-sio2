# -*- coding: utf-8 -*-
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from oioioi.base.permissions import not_anonymous, make_condition, enforce_condition, is_superuser
from django.contrib import messages
from oioioi.base.menu import menu_registry, account_menu_registry
#from django.contrib.auth import AnonymousUser
from oioioi.contests.utils import can_enter_contest, contest_exists #, is_superuser
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, Http404, HttpResponse, HttpResponseNotFound
from oioioi.base.menu import menu_registry
from models import *
from forms import *
from oioioi.filetracker.utils import stream_file
import zipfile
from StringIO import StringIO
import mimetypes
from django.utils.safestring import mark_safe
from models import SwimmingPoolTicket, SwimmingPoolBlacklist
from datetime import timedelta


#@menu_registry.register_decorator("CTF", lambda request: reverse('ctf_view'), order=1)
def ctf_view(request):
    return redirect('http://10.0.13.37')
#    #return render(request, 'ctf/info.html', {})

#@menu_registry.register_decorator(_("Zapisy na basen"),
#        lambda request: reverse('staszic-pool-info'),
#        order=0)

@enforce_condition(not_anonymous)
def pool_info(request):
    #return HttpResponseNotFound()
    day = get_pool_day(request.timestamp)
    ticket = SwimmingPoolTicket.objects.filter(date=day, user=request.user).first()
    tickets = SwimmingPoolTicket.objects.filter(date=day).order_by('moment')
    blist = SwimmingPoolBlacklist.objects.filter(date=day).order_by('user__last_name')
    return render(request, 'swimmingpool/pool_info.html', dict(day=day, ticket=ticket, list=tickets, blist=blist, bl_form=SwimmingPoolBlacklistForm()))

def get_pool_day(timestamp):
    return (timestamp + timedelta(hours=8)).date()

@enforce_condition(not_anonymous)
@transaction.atomic
def pool_sign(request):
    day = get_pool_day(request.timestamp)
    ticket = SwimmingPoolTicket.objects.filter(date=day, user=request.user).first()
    blacklist = SwimmingPoolBlacklist.objects.filter(date=day, user=request.user).first()

    if ticket:
        messages.error(request, u'Jesteś już zapisany.')
        return redirect(reverse('staszic-pool-info'))
    elif blacklist:
        messages.error(request, u'Jesteś na czarnej liście! Powód: {}'.format(blacklist.reason))
        return redirect(reverse('staszic-pool-info'))
    else:
        SwimmingPoolTicket.objects.create(date=day, user=request.user, moment=request.timestamp)
        messages.success(request, u'Zostałeś pomyślnie zapisany')
        return redirect(reverse('staszic-pool-info'))

@enforce_condition(not_anonymous)
@transaction.atomic
def pool_unsign(request):
    day = get_pool_day(request.timestamp)
    ticket = SwimmingPoolTicket.objects.filter(date=day, user=request.user).first()

    if ticket:
        ticket.delete()
        messages.success(request, u'Zostałeś wypisany :(')
        return redirect(reverse('staszic-pool-info'))
    else:
        messages.error(request, u'Nie jesteś jeszcze zapisany.')
        return redirect(reverse('staszic-pool-info'))


@enforce_condition(is_superuser)
def pool_bl_ins(request):
    form = SwimmingPoolBlacklistForm(request.POST)
    
    if form.is_valid():
        data = form.cleaned_data

        SwimmingPoolBlacklist.objects.create(date=data['date'], user=data['user'], reason=data['reason'])
         
        messages.success(request, u'Zablokowano pływaka')
        return redirect(reverse('staszic-pool-info'))

    else:
        messages.error(request, 'Wypełnij, proszę, formularz z należytą starannością.')
    return redirect(reverse('staszic-pool-info'))

@enforce_condition(is_superuser)
def pool_bl_del(request, id):
    bl = SwimmingPoolBlacklist.objects.get(pk=id)
    bl.delete()
    messages.success(request, u'Odblokowano pływaka')
    return redirect(reverse('staszic-pool-info'))
