from django.shortcuts import render
from oioioi.contests.menu import contest_admin_menu_registry
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from oioioi.base.permissions import enforce_condition, is_superuser

@contest_admin_menu_registry.register_decorator('Staszic extras',
    lambda request: reverse('staszic-extras', kwargs=dict(contest_id=request.contest.id)),
    order=240)
@enforce_condition(is_superuser)
def staszic_extras(request):
    return render(request, 'extras/extras.html')

@enforce_condition(is_superuser)
def doesnt_need(request):
    request.contest.probleminstance_set.update(needs_rejudge=False)
    messages.success(request, "Done.")
    return redirect(reverse('staszic-extras'))
