from models import PolygonImportRequest
from celery.task import task
import logging
from django.db import transaction
import traceback
from polygon_import import import_problem
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

@task
def importmgr_job(env):
    try:
        request = PolygonImportRequest.objects.get(pk = env['import_request_id'])
        def update_state(new_state):
            request.status = new_state
            logger.info('new state %s', new_state)
            request.save()
        try:
            with transaction.atomic():
                problem = import_problem(
                        problem_id=env['problem_id'],
                        contest_name=env['contest_name'],
                        statement_date=env['statement_date'],
                        state_reporter=update_state)
                env['problem_id'] = problem.pk

                request.status = 'OK'
                request.save()

                for handler in env['post_import_handlers']:
                    handler_f = import_string(handler)
                    env = handler_f(env)
        except Exception as e:
            logger.exception('Importing failed due to exception')

            request.status = 'KO'
            request.info = traceback.format_exc(100)
            request.save()
        return env

    except PolygonImportRequest.DoesNotExist:
        logger.warning('Shit happened: request %d erased from db before blah blah' % (env['import_request_id'], ))
        
