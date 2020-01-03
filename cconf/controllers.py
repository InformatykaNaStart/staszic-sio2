from staszic.new_base.controllers import StaszicContestController
from models import CConfiguration


class CConfMixin(object):
    def fill_evaluation_environ_post_problem(self, environ, submission):
        super(CConfMixin, self).fill_evaluation_environ_post_problem(environ, submission)
        environ['cconf'] = self.make_cconf(submission)

    def make_cconf(self, submission):
        model = CConfiguration.objects.filter(contest=submission.problem_instance.contest).first()
        if model is None:
            model = CConfiguration()

        cconf = {
            'compiler': model.compiler,
            'cflags': model.cflags,
            'cxxflags': model.cxxflags,
        }
        return cconf

StaszicContestController.mix_in(CConfMixin)
