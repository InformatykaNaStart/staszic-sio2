from staszic.new_base.controllers import StaszicContestController

class NasmMixin(object):
    def get_allowed_languages(self):
        orig = super(NasmMixin, self).get_allowed_languages()
        return orig + ['NASM']

StaszicContestController.mix_in(NasmMixin)
