from django.shortcuts import render
from django.conf import settings
import xmlrpclib
from django.http import HttpResponse
from oioioi.base.permissions import enforce_condition, is_superuser

server = xmlrpclib.ServerProxy(settings.SIOWORKERSD_URL, allow_none=True)

@enforce_condition(is_superuser)
def get_queue_ajax(request):
    qs = server.get_queue()
    return render(request, 'queue/queue.txt', {'qs': qs})


#system_admin_menu_registry.register('workers_queue_admin',
#        _("What is happening right now?"), lambda request:
#        reverse('show_queue'),
#        order=100)
