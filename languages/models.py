from __future__ import unicode_literals

from django.db import models
from oioioi.contests.models import Contest
from django.utils.module_loading import import_string
from fields import LanguageSelectionField

DEFAULT_LANGUAGES='staszic.languages.languages.CProgrammingLanguage,staszic.languages.languages.CppProgrammingLanguage'

class LanguageConfig(models.Model):
    problem_instance = models.OneToOneField(Contest)
    languages_desc = LanguageSelectionField(max_length=1024, default=DEFAULT_LANGUAGES)

    @property
    def languages(self):
        modules = self.languages_desc
        result = []
        for module in modules:
            if module == '': continue
            language = import_string(module)
            result.append(language())

        return result

    class Meta(object):
        verbose_name = 'language config'
        verbose_name_plural = 'language configs'

