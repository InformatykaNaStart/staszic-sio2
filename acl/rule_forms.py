from django import forms

class EmptyForm(forms.Form):
    pass

CONSTANT_CHOICES = [
    ('f', 'False'),
    ('t', 'True')
]

class ConstantForm(forms.Form):
    outcome = forms.ChoiceField(choices=CONSTANT_CHOICES, initial='f')

STRING_OPS = [
    ('eq', '=='),
    ('ne', '!='),
    ('le', '<='),
    ('lt', '<'),
    ('ge', '>='),
    ('gt', '>'),
    ('startswith', 'starts with'),
    ('endswith', 'ends with'),
]

INTEGER_OPS = [
    ('eq', '=='),
    ('ne', '!='),
    ('le', '<='),
    ('lt', '<'),
    ('ge', '>='),
    ('gt', '>'),
    ('div', 'divisible by'),    
]

class StringCompareForm(forms.Form):
    operator = forms.ChoiceField(choices=STRING_OPS, initial='eq')
    argument = forms.CharField()

class IntegerCompareForm(forms.Form):
    operator = forms.ChoiceField(choices=INTEGER_OPS, initial='eq')
    argument = forms.IntegerField()

