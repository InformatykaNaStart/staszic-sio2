from django import forms

class ChangeStatementForm(forms.Form):
    problem = forms.ModelChoiceField(queryset=None)
    new_statement = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')

        super(ChangeStatementForm, self).__init__(*args, **kwargs)
        
        self.fields['problem'].queryset = request.contest.probleminstance_set.all()

class ChangeSubLimitForm(forms.Form):
    new_limit = forms.IntegerField()

