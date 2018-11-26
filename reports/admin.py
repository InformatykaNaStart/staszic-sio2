from django.contrib import admin
from models import ReportConfig
from oioioi.contests.admin import ContestAdmin

class ReportConfigInline(admin.StackedInline):
    model = ReportConfig
    can_delete = False
    extra = 1

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(ReportConfigInline, self) \
            .formfield_for_foreignkey(db_field, request, **kwargs)



class ContestAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContestAdminMixin, self). \
                __init__(*args, **kwargs)
        self.inlines = self.inlines + [ReportConfigInline]

ContestAdmin.mix_in(ContestAdminMixin)

