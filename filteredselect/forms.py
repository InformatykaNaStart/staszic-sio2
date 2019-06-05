from django.forms.widgets import Select
from django.template.loader import render_to_string

class FilteredSelect(Select):
    def render(self, name, value, attrs=None, choices=()):
        return render_to_string('filteredselect/select.html', context={
            'choices': [choice for choice in self.choices if isinstance(choice[0], int) > 0],
            'name': name
        })
