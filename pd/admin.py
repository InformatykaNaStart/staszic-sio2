from oioioi.base import admin
from models import PersonalDataPass
from permissions import has_personal_data_pass

class PersonalDataPassAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return has_personal_data_pass(request)
    def has_add_permission(self, request, obj=None):
        return has_personal_data_pass(request)
    def has_delete_permission(self, request, obj=None):
        return has_personal_data_pass(request)

admin.site.register(PersonalDataPass, PersonalDataPassAdmin)