from django.contrib import admin
from models import SmartJudgeConfig, JudgingConfig
from oioioi.contests.admin import ContestAdmin

# Register your models here.

class SmartJudgeConfigInline(admin.StackedInline):
    model = SmartJudgeConfig
    fields = ['mode']
    can_delete = False

class JudgingConfigInline(admin.StackedInline):
    model = JudgingConfig
    fields = ['mode']
    can_delete = False

class ContestAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContestAdminMixin, self). \
                __init__(*args, **kwargs)
        self.inlines = self.inlines + [SmartJudgeConfigInline, JudgingConfigInline]

ContestAdmin.mix_in(ContestAdminMixin)
