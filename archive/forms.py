from django import forms
from django.utils.translation import ugettext_lazy as _

class OldLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'form-input', 'style':'width:100%;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-input', 'style':'width:100%;'}))
