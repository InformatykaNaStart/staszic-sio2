from models import ACLHook, ACLOutcome
from django.contrib.contenttypes.models import ContentType

def query_acl(request, object, action, default):
    if request.user.is_superuser: return default
    acl = ACLHook.objects.filter(model=ContentType.objects.get_for_model(object), object_id=object.pk, action=action).first()

    if acl is None: return default

    outcome = acl.acl.evaluate(request)

    if outcome == ACLOutcome.ACCEPT: return True
    if outcome == ACLOutcome.REJECT: return False
    if outcome == ACLOutcome.DEFAULT: return default

    raise RuntimeError('ACL {} errored'.format(acl.pk))
