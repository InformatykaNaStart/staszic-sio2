from oioioi.programs.controllers import ProgrammingContestController, ProgrammingProblemController

class Mixin(object):
    def judge_prepare(self, judging, name, config):
        return False

    def judge_finished(self, judging, name, code, config):
        pass

ProgrammingContestController.mix_in(Mixin)
ProgrammingProblemController.mix_in(Mixin)
