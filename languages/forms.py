from django.forms import CheckboxSelectMultiple
from languages import ProgrammingLanguageBase

class LanguageSelectionWidget(CheckboxSelectMultiple):
    def __init__(self):
        ProgrammingLanguageBase.load_subclasses()
        self.languages = ProgrammingLanguageBase.subclasses
        self.languages.sort(key=lambda x: x.description)

        self.choices = [
            ('%s.%s' % (language.__module__, language.__name__), language.description) for language in self.languages
        ]

        super(LanguageSelectionWidget, self).__init__(choices=self.choices)
