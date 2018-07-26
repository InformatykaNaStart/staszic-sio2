from django.contrib import admin

from models import ProblemHooks

class HooksInline(admin.StackedInline):
    model = ProblemHooks
    can_delete = False
    extra = 0
    max_num = 0

    def has_add_permission(self, requets):
        return False

class HooksMixin(object):
    def __init__(self, *args, **kwargs):
        super(HooksMixin, self).__init__(*args, **kwargs)
        self.inlines = self.inlines + [HooksInline]
