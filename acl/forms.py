from django import forms
from custom import RulesetWidget
from models import ACL
from acl_hooks import ACLHookBase

class ACLForm(forms.ModelForm):
    class Meta:
        model = ACL
        fields = ['name', 'json_ruleset']
        widgets = { 'json_ruleset' : RulesetWidget() }

def generate_models():
    result = []

    ACLHookBase.load_subclasses()
    for hook_class in ACLHookBase.subclasses:
        dotted = hook_class.get_dotted()
        result.append((dotted, hook_class.description))

    return result

def generate_objects(request):
    result = []

    ACLHookBase.load_subclasses()
    for hook_class in ACLHookBase.subclasses:
        result.extend(('%s:%s' % (hook_class.get_dotted(), unicode(obj.pk)), unicode(obj)) for obj in hook_class().get_queryset(request))

    return result

def generate_actions():
    result = []

    ACLHookBase.load_subclasses()
    for hook_class in ACLHookBase.subclasses:
        dotted = hook_class.get_dotted()
        result.extend(('%s:%s' % (dotted, action_name), action_name) for action_name in hook_class.actions)

    return result

class HookAddForm(forms.Form):
    model_type = forms.ChoiceField(choices=generate_models())
    object = forms.ChoiceField()
    action = forms.ChoiceField(choices=generate_actions())

    def __init__(self, request, *args, **kwargs):
        super(HookAddForm, self).__init__(*args, **kwargs)

        self.fields['object'] = forms.ChoiceField(choices=generate_objects(request))

    class Media:
        js = ['acl/hook_form.js']
