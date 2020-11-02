from django.core.urlresolvers import reverse
from models import Link
from oioioi.base import admin
from oioioi.contests.admin import contest_site
from oioioi.contests.menu import contest_admin_menu_registry
from django.utils.translation import ugettext_lazy as _

class LinkAdmin(admin.ModelAdmin):
    exclude = ['contest', 'magic']
    readonly_fields = ['link']
    list_display = ['link', 'expiration_date', 'comment', 'active']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.contest = request.contest
        super(LinkAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(LinkAdmin, self).get_queryset(request)
        return qs.filter(contest=request.contest)


contest_site.contest_register(Link, LinkAdmin)

contest_admin_menu_registry.register('link_change',
                                     _('Join links'),
                                     lambda request: reverse('oioioiadmin:linkjoin_link_changelist'),
                                     order=30)
