from django import forms
from models import StaszicRanking
from ranking_types import RankingTypeBase

def RankingAddFormFactory(contest):
    RankingTypeBase.load_subclasses()
    CHOICES=[('%s.%s' % (x.__module__, x.__name__), x.description) for x in RankingTypeBase.subclasses if x.is_valid_for_contest(contest.controller)]

    class RankingAddForm(forms.ModelForm):
        class Meta:
            model = StaszicRanking
            fields = ('type_name', 'name', 'renderer_name')
        type_name = forms.ChoiceField(choices=CHOICES)

    return RankingAddForm
