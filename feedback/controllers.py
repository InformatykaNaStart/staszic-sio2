from oioioi.programs.controllers import ProgrammingContestController, ProgrammingProblemController

class Mixin(object):
    def judge_prepare(self, judging, name, config):
        return False

    def judge_finished(self, judging, name, code, config):
        pass
    
    def can_see_stats(self, request, judging):
        if request.user.is_superuser: return True
        return False

    def can_see_progress(self, request, judging):
        if request.user.is_superuser: return True
        return False

ProgrammingContestController.mix_in(Mixin)
ProgrammingProblemController.mix_in(Mixin)
