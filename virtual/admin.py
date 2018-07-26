from django.contrib import admin
from models import VirtualContest, VirtualContestEntry
from oioioi.base import admin
from oioioi.contests.admin import contest_site
from oioioi.contests.menu import contest_admin_menu_registry
from django.core.urlresolvers import reverse
from utils import contest_has_vcontests

class EntryInline(admin.TabularInline):
    model = VirtualContestEntry

class VirtualContestAdmin(admin.ModelAdmin):
    inlines = [EntryInline]
    readonly_fields = ['round']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'round':
            kwargs['queryset'] = request.contest.round_set.filter(virtualcontest=None)
        return super(VirtualContestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

contest_site.contest_register(VirtualContest, VirtualContestAdmin)

contest_admin_menu_registry.register('virtual_contest_change',
        'Virtual Contests',
        lambda request: reverse('oioioiadmin:virtual_virtualcontest_changelist'),
        order=470,
        condition=contest_has_vcontests)
