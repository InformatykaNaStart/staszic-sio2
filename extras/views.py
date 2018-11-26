# coding: utf-8
from django.shortcuts import render
from oioioi.contests.menu import contest_admin_menu_registry
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from oioioi.base.permissions import enforce_condition, is_superuser
from forms import ChangeSubLimitForm, ChangeStatementForm
from django.core.exceptions import MultipleObjectsReturned
from django.utils.http import urlencode

@contest_admin_menu_registry.register_decorator('Staszic extras',
    lambda request: reverse('staszic-extras', kwargs=dict(contest_id=request.contest.id)),
    order=240)
@enforce_condition(is_superuser)
def staszic_extras(request):
    change_statement_form = ChangeStatementForm(request=request)
    context = dict(
        change_statement_form=change_statement_form,
        change_limit_form = ChangeSubLimitForm(),
    )

    return render(request, 'extras/extras.html', context)

@enforce_condition(is_superuser)
def doesnt_need(request):
    request.contest.probleminstance_set.update(needs_rejudge=False)
    messages.success(request, "Done.")
    return redirect(reverse('staszic-extras'))

@enforce_condition(is_superuser)
def change_statement(request):
    form = ChangeStatementForm(request.POST, request.FILES, request=request)
    
    if form.is_valid():
        data = form.cleaned_data
        pi = data['problem']
        st = data['new_statement']

        try:
            stmt = pi.problem.statements.get()

            stmt.content = st
            stmt.save()
            messages.success(request, 'Zmieniono treść zadania :)')
            get_data = dict(
                category='p_%d' % (pi.pk,),
                topic=u'Zmiana treści zadania',
                content=u'Treść zadania "%s" została zmieniona. Zmiana dotyczy !!!TU UZUPEŁNIĆ!!!\nNowa treść jest dostępna z dziale Zadania.' % (pi.problem.name, )
            )
            return redirect('%s?%s' %(reverse('add_contest_message'), urlencode(get_data)))
        except MultipleObjectsReturned:
            messages.error(request, 'W tym zadaniu jest wiele treści. Poddaję się.')

    else:
        messages.error(request, 'Wypełnij, proszę, formularz z należytą starannością.')
    return redirect(reverse('staszic-extras'))

@enforce_condition(is_superuser)
def change_sub_limit(request):
    form = ChangeSubLimitForm(request.POST)
    
    if form.is_valid():
        data = form.cleaned_data
        nl = data['new_limit']

        c = request.contest
        c.default_submission_limit = nl
        c.save()
        c.probleminstance_set.update(submissions_limit = nl)
        
        messages.success(request, 'Zmieniono limit zgłoszeń.')
        return redirect(reverse('staszic-extras'))

    else:
        messages.error(request, 'Wypełnij, proszę, formularz z należytą starannością.')
    return redirect(reverse('staszic-extras'))

