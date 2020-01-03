from django.contrib import admin
from models import CConfiguration
from oioioi.contests.admin import ContestAdmin

class CConfigurationInline(admin.StackedInline):
    model = CConfiguration
    can_delete = False

class ContestAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContestAdminMixin, self).__init__(*args, **kwargs)
        self.inlines = self.inlines + [CConfigurationInline]

ContestAdmin.mix_in(ContestAdminMixin)
