from django.contrib import admin
from models import CConfiguration
from oioioi.contests.admin import ContestAdmin
from oioioi.contests.utils import is_contest_admin

class CConfigurationInline(admin.StackedInline):
    model = CConfiguration
    can_delete = False
    def has_change_permission(self, request, obj=None):
        return is_contest_admin(request)

class ContestAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContestAdminMixin, self).__init__(*args, **kwargs)
        self.inlines = self.inlines + [CConfigurationInline]

ContestAdmin.mix_in(ContestAdminMixin)
