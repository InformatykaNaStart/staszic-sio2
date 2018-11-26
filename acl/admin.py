from oioioi.base import admin
from models import ACL, ACLHook
from oioioi.contests.admin import contest_site
from oioioi.contests.menu import contest_admin_menu_registry
from django.core.urlresolvers import reverse
from forms import ACLForm, HookAddForm
from django.conf.urls import url
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string

class ACLHookInline(admin.TabularInline):
    model = ACLHook
    extra = 0
    readonly_fields = ['model', 'get_object', 'action']
    fields = ['model', 'get_object', 'action']
    
    def has_add_permission(self, request, obj=None):
        return False

    def get_object(self, obj):
        return obj.get_object()

class ACLAdmin(admin.ModelAdmin):
    form = ACLForm
    inlines = [ACLHookInline]
    def get_queryset(self, request):
        qs = super(ACLAdmin, self).get_queryset(request)
        return qs.filter(contest=request.contest)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.contest = request.contest

        super(ACLAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        urls = super(ACLAdmin, self).get_urls()

        custom_urls = [
            url(r'^(?P<acl_id>\d+)/hook/$', self.admin_site.admin_view(self.hook_view), name='acl_hook')
        ]
        
        return custom_urls + urls

    def hook_view(self, request, acl_id):
        acl = get_object_or_404(ACL, pk=acl_id)

        if request.method == 'POST':
            form = HookAddForm(request, request.POST)
            if form.is_valid():
                data = form.cleaned_data
                model_name = data['model_type']
                _, object_pk = data['object'].split(':')
                _, action = data['action'].split(':')

                model_obj = import_string(model_name)
                model = ContentType.objects.get_for_model(model_obj.model)

                ACLHook.objects.create(model=model, object_id=object_pk, action=action, acl=acl)
                messages.success(request, 'Successfully hooked acl')
                return redirect(reverse('oioioiadmin:acl_acl_change', args=[acl.pk]))
            else:
                messages.error(request, 'Please, correct below errors')

        else:
            form = HookAddForm(request)

        context = dict(
            self.admin_site.each_context(request),
            acl=acl,
            form=form
        )

        return render(request, 'admin/acl/add_hook.html', context)


contest_site.contest_register(ACL, ACLAdmin)

contest_admin_menu_registry.register('acl_change',
        'Access Control',
        lambda request: reverse('oioioiadmin:acl_acl_changelist'),
        order = 461)
