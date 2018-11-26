from django import forms

class SetTLSForm(forms.Form):
    multiplier = forms.FloatField(initial=5.0)
    rounding = forms.FloatField(initial=0.5)
    equal_groups = forms.BooleanField(initial=True, required=False)
