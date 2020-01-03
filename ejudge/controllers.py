from staszic.new_base.controllers import StaszicContestController
from oioioi.contests.models import FailureReport
from django.template.loader import render_to_string
from django.template import RequestContext

class StaszicExternalContestController(StaszicContestController):
    description = 'Staszic closed with external judging'
    visible = False

    def judge(self, *args, **kwargs):
        return
    
    def render_report(self, request, report):
        if report.kind == 'FAILURE':
            failure_report = \
                    FailureReport.objects.get(submission_report=report)
            message = failure_report.message
            return render_to_string('contests/failure_report.html',
                    context_instance=RequestContext(request,
                        {'message': message, 'next_step': 'UNKNOWN',
                            'environ': 'No environ (submission judged externally)'}))
        else:
            return super(StaszicExternalContestController, self).render_report(request, report)
