from oioioi.problems.problem_sources import ProblemSource
from django.template.loader import render_to_string
from forms import PolygonImportForm
from polygon_import import get_problem_info, check_import_problem
from django.contrib import messages
from models import PolygonImportRequest
from importmgr import importmgr_job

class PolygonProblemSource(ProblemSource):
    key = 'polygon'
    short_description = 'Import from Polygon system'

    def view(self, request, contest, existing_problem=None):
        if existing_problem is not None:
            return render_to_string('polygon/reupload.html', request=request)
        if request.method == 'POST':
            form = PolygonImportForm(contest, existing_problem, request.POST)
            if form.is_valid():
                data = form.cleaned_data

                problem_id = data['problem_id']
                problem_info = get_problem_info(problem_id)

                if not check_import_problem(problem_info):
                    messages.error(request, 'Problem %d is not accessible by user staszic-sio2' % (problem_id, ))
                else:
                    import_request = PolygonImportRequest.objects.create(
                        problem_id = problem_id,
                        problem_name = problem_info['name'],
                        contest = contest)
                    

                    env = dict(
                            import_request_id = import_request.pk,
                            problem_id = problem_id,
                            contest_name = data['statement_contest'],
                            statement_date = data['statement_date'],
                            post_import_handlers = ['oioioi.problems.handlers.update_problem_instance'],     
                            is_reupload = existing_problem is not None,
                        )
                    if contest:
                        env['contest_id'] = contest.id
                        env['round_id'] = data.get('round_id', None)

                    task = importmgr_job.s(env)
                    result = task.freeze()

                    import_request.celery_task_id = result.task_id
                    import_request.save()

                    task.delay()
                    messages.info(request, 'Importing will continue in background. I hope.')

        else:
            form = PolygonImportForm(contest, existing_problem)
        
        return render_to_string('polygon/form.html', dict(form=form), request=request)
            

