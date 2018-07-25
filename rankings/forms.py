from django import forms
from models import StaszicRanking

class RankingAddForm(forms.ModelForm):
    class Meta:
        model = StaszicRanking
        fields = ('type_name', 'name', 'renderer_name')
