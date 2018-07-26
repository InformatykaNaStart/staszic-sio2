from oioioi.oi.controllers import OIContestController
from oioioi.participants.controllers import ParticipantsController
from staszic.languages.models import LanguageConfig

class StaszicContestController(OIContestController):
    description = 'Staszic closed'
    visible = True

    def get_available_languages_dict(self, problem_instance):
        assert problem_instance is None
        config = getattr(self.contest, 'languageconfig', LanguageConfig())

        result = {}
        for lang in config.languages:
            result[lang.description] = lang.extensions

        return result

    def get_allowed_languages(self):
        return list(self.get_available_languages_dict(None).keys())

    def registration_controller(self):
        return ParticipantsController(self.contest)

