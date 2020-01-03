from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import date
from django.contrib.auth.models import User

class SwimmingPoolBlacklistForm(forms.Form):
    date = forms.DateField(initial=date.today)
    user = forms.ModelChoiceField(queryset=User.objects)
    reason = forms.CharField(widget=forms.Textarea, required=False)
