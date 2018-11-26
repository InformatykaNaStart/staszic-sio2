from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from rule_forms import EmptyForm, ConstantForm, StringCompareForm
from django.forms import ChoiceField
from django.utils.module_loading import import_string

class ACLRuleBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['acl_rules']
    abstract = True
    instances = dict()

    def get_forms(self):
        raise NotImplementedError

    def evaluate(self, request, data):
        raise NotImplementedError

    def get_name(self):
        return '%s.%s' % (self.__class__.__module__, self.__class__.__name__)

    def get_config(self):
        forms = self.get_forms()
        
        fields = []
        for form in forms:
            for name, field in form.fields.items():
                fields.append(dict(name=name, type=field.__class__.__name__, custom=self.get_custom_for_field(field), default=field.initial))

        return dict(name=self.get_name(), fields=fields, description=self.description)

    def get_custom_for_field(self, field):
        if isinstance(field, ChoiceField):
            return dict(choices = field.choices)

        return dict()

    @classmethod
    def make_all_config(cls):
        result = dict()

        cls.load_subclasses()
        for subclass in cls.subclasses:
            name = subclass().get_name()
            config = subclass().get_config()

            result[name] = config

        return result

    @classmethod
    def instance_of(cls, name):
        if name in cls.instances: return cls.instances[name]

        instance = import_string(name)()

        cls.instances[name] = instance

        return instance


class ACLConstantRule(ACLRuleBase):
    abstract = True
    constant = None

    def get_forms(self):
        return []

    def evaluate(self, request, data):
        assert self.constant is not None
        return self.constant

class ACLFalseRule(ACLConstantRule):
    description = 'Always false'
    constant = False

class ACLTrueRule(ACLConstantRule):
    description = 'Always true'
    constant = True

class ACLSpecifiedRule(ACLRuleBase):
    description = 'Constant'

    def get_forms(self):
        return [ConstantForm()]
    
    def evaluate(self, request, data):
        return data['outcome'] == 't'

class ACLStringRule(ACLRuleBase):
    abstract = True
    ACTIONS = {
        'eq': lambda x,y: x == y,
        'ne': lambda x,y: x != y,
        'le': lambda x,y: x <= y,
        'lt': lambda x,y: x < y,
        'ge': lambda x,y: x >= y,
        'gt': lambda x,y: x > y,
        'startswith': lambda x,y: x.startswith(y),
        'endswith': lambda x,y: x.endswith(y),
    }

    def get_forms(self):
        return [self.get_arg_form(), StringCompareForm()]

    def get_arg_form(self):
        raise NotImplementedError

    def get_value(self, request, data):
        raise NotImplementedError

    def evaluate(self, request, data):
        value = self.get_value(request, data)
        action = data['operator']
        argument = data['argument']

        return self.ACTIONS[action](value, argument)

class ACLUsernameRule(ACLStringRule):
    description = 'Username'
    
    def get_arg_form(self):
        return EmptyForm()

    def get_value(self, request, data):
        if not request.user.is_authenticated: return ''
        return request.user.username
