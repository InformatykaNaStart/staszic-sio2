from oioioi.base import admin
import models
from django import forms

from django.db.models import F


class ContestGroupAdminForm(forms.ModelForm):
    class Meta:
        model = models.ContestGroup
        widgets = {
            'contest': forms.CheckboxSelectMultiple,
        }
        fields = '__all__'

class ContestGroupAdmin(admin.ModelAdmin):
    form = ContestGroupAdminForm

admin.site.register(models.ContestGroup, ContestGroupAdmin)
