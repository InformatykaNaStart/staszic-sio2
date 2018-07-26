from staszic.new_base.controllers import StaszicContestController
from oioioi.contests.models import Contest
from django.db import models

class PythonMixin(object):

    def get_available_languages(self):
        orig = super(PythonMixin, self).get_available_languages()
        return orig + ['Python']

StaszicContestController.mix_in(PythonMixin)
