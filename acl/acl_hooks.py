from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins
from oioioi.contests.models import Contest, ProblemInstance


class ACLHookBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['acl_hooks']
    abstract = True

    model = None
    actions = []

    @classmethod
    def get_dotted(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    def get_queryset(self, request):
        raise NotImplementedError

class ProblemInstanceHook(ACLHookBase):
    description = 'Problem instance'
    
    model = ProblemInstance
    actions = ['show', 'submit']

    def get_queryset(self, request):
        return self.model.objects.filter(contest=request.contest)

class ContestHook(ACLHookBase):
    description = 'Contest'
    
    model = Contest
    actions = ['access']

    def get_queryset(self, request):
        return self.model.objects.filter(pk=request.contest.pk)
