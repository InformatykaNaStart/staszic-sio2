from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from forms import RankingAddFormFactory
from models import StaszicRanking
from oioioi.base import admin
from oioioi.contests.admin import contest_site
from oioioi.contests.menu import contest_admin_menu_registry
from ranking_types import RankingTypeBase
from ranking_renderers import RankingRendererBase

# Register your models here.

class RankingAdmin(admin.ModelAdmin):
    readonly_fields = ['type_name', 'renderer_name', 'last_calculation', 'serialized_data']
    exclude = ['contest']
    list_display = ['name', 'type_name', 'order']
        
    def get_inlines():
        def get_class_inlines(cls):
            cls.load_subclasses()
            inlines = []

            for subclass in cls.subclasses:
                inlines.extend(subclass.get_admin_inlines())
                for mixin in subclass.mixins:
                    inlines.extend(mixin.get_mixin_admin_inlines(subclass))

            return inlines
        return get_class_inlines(RankingTypeBase) + get_class_inlines(RankingRendererBase)

    inlines = get_inlines()

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        type_classes = (obj.type.type_id, obj.renderer.type_id)
        return [inline(self.model, self.admin_site) for inline in self.inlines if inline.ranking_type in type_classes]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}

        if obj is None:
            defaults['form'] = RankingAddFormFactory(request.contest)
            defaults['fields'] = ['name', 'type_name', 'renderer_name']
        defaults.update(kwargs)

        return super(RankingAdmin, self).get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.contest = request.contest
        super(RankingAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(RankingAdmin, self).get_queryset(request)
        return qs.filter(contest = request.contest)

contest_site.contest_register(StaszicRanking, RankingAdmin)

contest_admin_menu_registry.register('ranking_change',
        'Rankings',
        lambda request: reverse('oioioiadmin:rankings_staszicranking_changelist'),
        order=460)
