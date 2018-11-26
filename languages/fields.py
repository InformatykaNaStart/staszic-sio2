from django.db import models
from django import forms
from languages import ProgrammingLanguageBase
from django.forms import CheckboxSelectMultiple
from django.core.exceptions import ValidationError

class LanguageSelectionField(models.CharField):
    def __init__(self, *args, **kwargs):
        ProgrammingLanguageBase.load_subclasses()
        languages = ProgrammingLanguageBase.subclasses

        languages.sort(key=lambda x: x.description)

        choices = list( ('%s.%s' % (lang.__module__, lang.__name__), lang.description) for lang in languages )
        self.languages = set(x for x,y in choices)
        
        kwargs['choices'] = choices
        kwargs['max_length'] = 1024

        super(LanguageSelectionField, self).__init__(self, *args, **kwargs)

    def from_db_value(self, value, *args, **kwargs):
        if value is None: return []
        return value.split(',')

    def to_python(self, value):
        if value is None: return []
        return value

    def get_prep_value(self, value):
        if value is None: return ''
        return ','.join(value)

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': forms.TypedMultipleChoiceField, 'widget': CheckboxSelectMultiple() }
        kwargs.update(defaults)

        return super(LanguageSelectionField, self).formfield(**kwargs)
    
    def validate(self, value, model_instance):
        for lang in value:
            if lang not in self.languages:
                raise ValidationError('Do not cheat, please')

    def deconstruct(self):
        return (None, 'staszic.languages.fields.LanguageSelectionField', [], {})
