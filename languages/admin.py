from django.contrib import admin
from models import LanguageConfig
from forms import LanguageSelectionWidget
from oioioi.contests.admin import ContestAdmin
from oioioi.contests.utils import is_contest_admin

class LanguageConfigInline(admin.StackedInline):
    model = LanguageConfig
    fields = ['languages_desc']
    can_delete = False
    def has_change_permission(self, request, obj=None):
        return is_contest_admin(request)

class ContestAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContestAdminMixin, self). \
                __init__(*args, **kwargs)
        self.inlines = self.inlines + [LanguageConfigInline]

ContestAdmin.mix_in(ContestAdminMixin)
