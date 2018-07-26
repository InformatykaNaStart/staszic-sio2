from oioioi.problems.forms import ProblemUploadForm
from django import forms

class PolygonImportForm(ProblemUploadForm):
    problem_id = forms.IntegerField(label='Polygon problem ID', required=True)

    statement_date = forms.CharField(label='Date to be used in problem statement', required=False)
    statement_contest = forms.CharField(label='Contest name to be used in statement', required=False)
