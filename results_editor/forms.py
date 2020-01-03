from django import forms
from oioioi.contests.models import Submission
from django.utils.translation import ugettext_lazy as _

class EditResultsForm(forms.Form):
    score = forms.IntegerField(label=_('Score'), required=False)
    status = forms.fields_for_model(Submission)['status']
    comment = forms.CharField(label=_('Comment'),widget=forms.Textarea(attrs={'cols':'80', 'rows':'3'}),required=False)
