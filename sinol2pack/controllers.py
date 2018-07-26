from oioioi.sinolpack.controllers import SinolProblemController
from admin import HooksMixin
class Sinol2ProblemController(SinolProblemController):
    description = 'Sinol 1.1'

    def get_config(self, problem):
        obj = ExtraConfig.objects.filter(problem=self.problem).first()
        if obj is None: return {}
        return obj.parsed_config

    def mixins_for_admin(self):
        return super(Sinol2ProblemController, self).mixins_for_admin() + \
                (HooksMixin, )
